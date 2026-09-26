"""Eje `truth`: la afirmacion literal es correcta?

Compara lo que el claim dice (valores, cambio, direccion) con lo que la
evidencia da, con una tolerancia de redondeo declarada. No mira el contexto:
un claim puede ser exacto y estar fuera de contexto (DEC-016).

Reglas:
    todas las comparaciones posibles cuadran      -> supported
    ninguna cuadra                                -> contradicted
    unas si y otras no                            -> mixed
    no hay nada comparable                        -> insufficient_evidence
"""

from __future__ import annotations

from dataclasses import dataclass, field

from veritai.domain.claim import ClaimEstructurado, TipoClaim, UnidadCambio
from veritai.domain.enums import Truth
from veritai.domain.evidencia import EvidenceBundle
from veritai.domain.tests.comparacion_base import cambio, direccion_de, tolerancia_para


@dataclass(frozen=True)
class Comparacion:
    que: str
    afirmado: float | str
    evidencia: float | str
    tolerancia: float | None
    cuadra: bool


@dataclass
class ResultadoVerdad:
    truth: Truth
    comparaciones: list[Comparacion] = field(default_factory=list)

    @property
    def resumen(self) -> str:
        return "; ".join(
            f"{c.que}: {'cuadra' if c.cuadra else 'NO cuadra'} "
            f"(claim {c.afirmado}, fuente {c.evidencia})"
            for c in self.comparaciones
        )


def _comparar_numero(que: str, afirmado: float, evidencia: float) -> Comparacion:
    tol = tolerancia_para(afirmado, evidencia)
    return Comparacion(que, afirmado, evidencia, tol, abs(afirmado - evidencia) <= tol)


def evaluar_verdad(claim: ClaimEstructurado, bundle: EvidenceBundle) -> ResultadoVerdad:
    comps: list[Comparacion] = []
    objetivo = bundle.buscar("objetivo")
    base = bundle.buscar("base_claim")
    v_obj = None if objetivo is None or objetivo.valor is None else float(objetivo.valor)
    v_base = None if base is None or base.valor is None else float(base.valor)

    if claim.valor_objetivo is not None and v_obj is not None:
        comps.append(
            _comparar_numero(
                f"valor en {claim.periodo_objetivo.etiqueta()}", claim.valor_objetivo, v_obj
            )
        )
    if claim.valor_base is not None and v_base is not None and claim.periodo_base is not None:
        comps.append(
            _comparar_numero(f"valor en {claim.periodo_base.etiqueta()}", claim.valor_base, v_base)
        )

    if claim.tipo is TipoClaim.CAMBIO_ENTRE_PERIODOS and v_obj is not None and v_base is not None:
        unidad = claim.unidad_cambio or UnidadCambio.PORCENTAJE
        recomputado = cambio(v_base, v_obj, unidad)
        if recomputado is not None:
            if claim.cambio_afirmado is not None:
                # La tolerancia del cambio es la de una cifra con los decimales del claim,
                # y nunca menor que 0,15 puntos: la prensa redondea a un decimal.
                tol = max(tolerancia_para(claim.cambio_afirmado, recomputado), 0.15)
                comps.append(
                    Comparacion(
                        f"cambio ({unidad.value})",
                        claim.cambio_afirmado,
                        round(recomputado, 3),
                        tol,
                        abs(claim.cambio_afirmado - recomputado) <= tol,
                    )
                )
            if claim.direccion_afirmada is not None:
                real = direccion_de(recomputado)
                comps.append(
                    Comparacion(
                        "direccion",
                        claim.direccion_afirmada.value,
                        real.value if real else "?",
                        None,
                        real == claim.direccion_afirmada,
                    )
                )

    if not comps:
        return ResultadoVerdad(Truth.INSUFFICIENT_EVIDENCE, comps)
    cuadran = sum(1 for c in comps if c.cuadra)
    if cuadran == len(comps):
        return ResultadoVerdad(Truth.SUPPORTED, comps)
    if cuadran == 0:
        return ResultadoVerdad(Truth.CONTRADICTED, comps)
    return ResultadoVerdad(Truth.MIXED, comps)
