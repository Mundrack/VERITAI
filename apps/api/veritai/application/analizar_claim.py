"""Caso de uso: analizar un claim estructurado de principio a fin.

    claim -> EvidenceBundle -> hard gates -> truth -> tests (2a, 2b) -> context
          -> plantilla -> persistencia

Orquesta dominio e infraestructura a traves de los puertos; no sabe si el
proveedor es el INE real o un doble de test. Toda la logica de decision vive
en el dominio; aqui solo se encadena.

Reglas de `context` (DEC-016, R02 §10):
    algun test aplicable disparo                          -> divergence_detected
    hubo tests aplicables, ninguno disparo, sin motivos   -> no_divergence_detected
    ningun test aplicable, o motivo no bloqueante         -> undetermined

Orden de los tests (DEC-034): verdad -> 2a -> 2b. 2b solo pide la edicion al
publicar cuando la tasa afirmada NO cuadra con la edicion vigente. Si hace
falta y no se puede recuperar, se abstiene (PREVIOUS_EDITION_NOT_FOUND) o, si
la operacion esta fuera del mapa cerrado del conector, se declara el fallo de
cobertura (PREVIOUS_EDITION_OUT_OF_MAP); en ambos casos `context` queda
undetermined. Si 2b dispara, la clase primaria es 2b, `truth` pasa a mixed (el
numero es rastreable a una edicion del emisor, el marco no) y el veredicto
lleva las dos evidencias con su fecha.
"""

from __future__ import annotations

import logging
from time import perf_counter

from veritai.domain.abstencion import hard_gates
from veritai.domain.claim import ClaimEstructurado, TipoClaim
from veritai.domain.enums import BLOQUEANTES, AbstainReason, Clase, Context, Truth
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem
from veritai.domain.plantilla import explicar
from veritai.domain.puertos import ProveedorEdicionAnterior, ProveedorEvidencia, Repositorio
from veritai.domain.tests.base_revisada import aplicar_2b, tasa_cuadra_con_vigente
from veritai.domain.tests.comparacion_base import aplicar_2a
from veritai.domain.tests.resultado import ResultadoTest
from veritai.domain.verdad import ResultadoVerdad, evaluar_verdad
from veritai.domain.veredicto import EvidenciaEdicion, Veredicto

LOG = logging.getLogger(__name__)

VENTANA_POR_DEFECTO = 8


class ProveedorError(Exception):
    """El proveedor no pudo recuperar evidencia. `motivo` es el AbstainReason que corresponde."""

    def __init__(
        self, mensaje: str, motivo: AbstainReason = AbstainReason.PRIMARY_SOURCE_NOT_FOUND
    ) -> None:
        super().__init__(mensaje)
        self.motivo = motivo


class AnalizarClaim:
    def __init__(
        self,
        proveedor: ProveedorEvidencia,
        repositorio: Repositorio | None = None,
        ventana: int = VENTANA_POR_DEFECTO,
        proveedor_edicion: ProveedorEdicionAnterior | None = None,
    ) -> None:
        self.proveedor = proveedor
        self.repositorio = repositorio
        self.ventana = ventana
        self.proveedor_edicion = proveedor_edicion

    # --- recuperacion -------------------------------------------------------
    def _recuperar(self, claim: ClaimEstructurado) -> tuple[EvidenceBundle, int, str]:
        """Devuelve (bundle, series coincidentes, detalle de error si lo hubo)."""
        bundle = EvidenceBundle(claim_id=claim.claim_id)
        m = claim.metrica
        try:
            coincidentes = self.proveedor.series_coincidentes(m)
            if coincidentes != 1:
                bundle.missing_slots.append("objetivo")
                return bundle, coincidentes, ""

            objetivo = self.proveedor.obtener_valor(m, claim.periodo_objetivo, "objetivo")
            if objetivo is None:
                bundle.missing_slots.append("objetivo")
            else:
                bundle.primary_items.append(objetivo)

            if claim.periodo_base is not None:
                base = self.proveedor.obtener_valor(m, claim.periodo_base, "base_claim")
                if base is None:
                    bundle.missing_slots.append("base_claim")
                else:
                    bundle.historical_items.append(base)

            if claim.tipo is TipoClaim.CAMBIO_ENTRE_PERIODOS:
                for ref, periodo in self.proveedor.referencias_emisor(m, claim.periodo_objetivo):
                    item = self.proveedor.obtener_valor(m, periodo, f"ref:{ref.value}")
                    if item is None:
                        bundle.missing_slots.append(f"ref:{ref.value}")
                    else:
                        bundle.historical_items.append(item)

            for item in self.proveedor.ventana(m, claim.periodo_objetivo, self.ventana):
                bundle.historical_items.append(item)

            metodologia = self.proveedor.metodologia(m)
            if metodologia is not None:
                bundle.methodology_items.append(metodologia)
            else:
                bundle.missing_slots.append("metodologia")
            return bundle, coincidentes, ""
        except ProveedorError as exc:
            LOG.warning("proveedor fallo para %s: %s", claim.claim_id, exc)
            bundle.missing_slots.append("objetivo")
            return bundle, 0, f"{exc.motivo.value}: {exc}"

    # --- 2b: la edicion al publicar solo cuando hace falta ---------------------
    def _recuperar_edicion_anterior(
        self, claim: ClaimEstructurado, bundle: EvidenceBundle
    ) -> AbstainReason | None:
        """Anade la base tal como se publico al bundle; si no pudo, devuelve el motivo."""
        cuadra = tasa_cuadra_con_vigente(claim, bundle)
        if cuadra is None or cuadra:
            return None  # 2b no necesita nada mas: no aplica, o la vigente ya explica la tasa
        if self.proveedor_edicion is None:
            return None  # sin conector: el prototipo se queda como estaba (2b no aplicable)
        if not self.proveedor_edicion.disponible(claim.metrica):
            bundle.missing_slots.append("base_al_publicar")
            return AbstainReason.PREVIOUS_EDITION_OUT_OF_MAP
        try:
            base = claim.periodo_base
            conector = self.proveedor_edicion
            item = conector.obtener(claim.metrica, base)  # type: ignore[arg-type]
        except Exception as exc:  # noqa: BLE001 - un rechazo o un fallo de red cierran el caso
            LOG.warning("edicion anterior no recuperable para %s: %s", claim.claim_id, exc)
            item = None
        if item is None:
            bundle.missing_slots.append("base_al_publicar")
            return AbstainReason.PREVIOUS_EDITION_NOT_FOUND
        bundle.historical_items.append(item)
        return None

    @staticmethod
    def _evidencias_2b(
        bundle: EvidenceBundle,
    ) -> tuple[EvidenciaEdicion | None, EvidenciaEdicion | None]:
        al_publicar = bundle.buscar("base_al_publicar")
        vigente = bundle.buscar("base_claim")
        if al_publicar is None or vigente is None:
            return None, None
        return (
            EvidenciaEdicion(
                valor=float(al_publicar.valor),  # type: ignore[arg-type]
                raw_value_span=al_publicar.raw_value_span,
                edicion=al_publicar.version,
                fecha=al_publicar.document_date or "",
                url=al_publicar.url,
                item_id=al_publicar.id,
            ),
            EvidenciaEdicion(
                valor=float(vigente.valor),  # type: ignore[arg-type]
                raw_value_span=vigente.raw_value_span,
                edicion=f"{vigente.version} (edicion vigente)",
                fecha=vigente.retrieved_at.date().isoformat(),
                url=vigente.url,
                item_id=vigente.id,
            ),
        )

    # --- decision -----------------------------------------------------------
    def ejecutar(self, claim: ClaimEstructurado) -> Veredicto:
        t0 = perf_counter()
        bundle, coincidentes, detalle_error = self._recuperar(claim)
        motivos = hard_gates(claim, bundle, coincidentes)
        bloqueantes = [m for m in motivos if m in BLOQUEANTES]

        tests: list[ResultadoTest] = []
        al_publicar = vigente = None
        if bloqueantes:
            verdad = ResultadoVerdad(Truth.INSUFFICIENT_EVIDENCE)
            truth, context = Truth.INSUFFICIENT_EVIDENCE, Context.UNDETERMINED
        else:
            verdad = evaluar_verdad(claim, bundle)
            truth = verdad.truth
            motivo_2b = self._recuperar_edicion_anterior(claim, bundle)
            if motivo_2b is not None and motivo_2b not in motivos:
                motivos.append(motivo_2b)
            r2a = aplicar_2a(claim, bundle)
            r2b = aplicar_2b(claim, bundle)
            tests = [r2a, r2b]
            aplicables = [t for t in tests if t.aplicable]
            if any(t.disparo for t in aplicables):
                context = Context.DIVERGENCE_DETECTED
            elif aplicables and not motivos:
                context = Context.NO_DIVERGENCE_DETECTED
            else:
                context = Context.UNDETERMINED
            if r2b.disparo:
                # El numero es rastreable a una edicion del emisor; el marco no (DEC-034).
                truth = Truth.MIXED
                al_publicar, vigente = self._evidencias_2b(bundle)

        clase = Clase.NONE
        if tests and tests[1].disparo:
            clase = Clase.BASE_REVISADA
        elif tests and tests[0].disparo:
            clase = Clase.BASE_ELEGIDA
        explicacion, usados = explicar(
            claim, bundle, verdad, tests, truth, context, motivos, al_publicar, vigente
        )
        if detalle_error:
            explicacion += f"\nProveedor: {detalle_error}."

        veredicto = Veredicto(
            claim_id=claim.claim_id,
            truth=truth,
            context=context,
            clase_primaria=clase,
            abstain_reasons=motivos,
            tests=tests,
            comparaciones=verdad.comparaciones,
            numeros_usados=usados,
            explicacion=explicacion,
            evidencia_al_publicar=al_publicar,
            evidencia_vigente=vigente,
            bundle_hash=bundle.bundle_hash,
        )
        duracion_ms = int((perf_counter() - t0) * 1000)
        if self.repositorio is not None:
            self.repositorio.guardar_analisis(claim, bundle, veredicto, duracion_ms)
        LOG.info(
            "analisis %s: truth=%s context=%s clase=%s motivos=%s (%d ms)",
            claim.claim_id,
            truth.value,
            context.value,
            clase.value,
            [m.value for m in motivos],
            duracion_ms,
        )
        return veredicto

    def bundle_de(self, claim: ClaimEstructurado) -> EvidenceBundle:
        """Solo la recuperacion, para inspeccion y para el informe de casos."""
        return self._recuperar(claim)[0]


def items_usados(bundle: EvidenceBundle) -> list[EvidenceItem]:
    return [i for i in bundle.items if i.valor is not None]
