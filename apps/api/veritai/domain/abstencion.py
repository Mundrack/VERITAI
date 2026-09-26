"""Hard gates deterministas (R02 §11, nivel A).

Si faltan datos, VERITAI no adivina: devuelve el motivo. Cada motivo sale de
una condicion comprobable sobre el claim y el bundle, no de una probabilidad.
Los motivos BLOQUEANTES impiden cualquier veredicto; los demas dejan evaluar
`truth` con lo que hay y ponen `context` en undetermined.
"""

from __future__ import annotations

from veritai.domain.claim import ClaimEstructurado, TipoClaim
from veritai.domain.enums import AbstainReason
from veritai.domain.evidencia import EvidenceBundle

TIPOS_EVALUABLES = {TipoClaim.CAMBIO_ENTRE_PERIODOS, TipoClaim.NIVEL}


def hard_gates(
    claim: ClaimEstructurado, bundle: EvidenceBundle, series_coincidentes: int
) -> list[AbstainReason]:
    motivos: list[AbstainReason] = []

    if claim.tipo not in TIPOS_EVALUABLES:
        motivos.append(AbstainReason.UNSUPPORTED_CLAIM_TYPE)
    if claim.slots_faltantes():
        motivos.append(AbstainReason.REQUIRED_SLOT_MISSING)
    if series_coincidentes == 0:
        motivos.append(AbstainReason.PRIMARY_SOURCE_NOT_FOUND)
    elif series_coincidentes > 1:
        motivos.append(AbstainReason.SOURCE_VERSION_AMBIGUOUS)

    objetivo = bundle.buscar("objetivo")
    if series_coincidentes == 1 and objetivo is None:
        # La serie existe pero no tiene el periodo pedido: para el sistema es
        # una primaria sin la edicion que el claim cita.
        motivos.append(AbstainReason.PRIMARY_SOURCE_NOT_FOUND)
    if objetivo is not None and objetivo.valor is None:
        motivos.append(AbstainReason.EXTRACTION_FAILED)

    if claim.tipo is TipoClaim.CAMBIO_ENTRE_PERIODOS and claim.periodo_base is not None:
        if (
            claim.periodo_base.frecuencia != claim.periodo_objetivo.frecuencia
            or claim.periodo_base >= claim.periodo_objetivo
        ):
            motivos.append(AbstainReason.PERIOD_NOT_COMPARABLE)
        if (
            bundle.buscar("base_claim") is None
            and AbstainReason.PRIMARY_SOURCE_NOT_FOUND not in motivos
        ):
            motivos.append(AbstainReason.PREVIOUS_EDITION_NOT_FOUND)
        base = bundle.buscar("base_claim")
        if (
            objetivo is not None
            and base is not None
            and objetivo.version
            and base.version
            and objetivo.version != base.version
        ):
            motivos.append(AbstainReason.METHODOLOGY_NOT_COMPARABLE)

    # Dos valores distintos para el mismo periodo y serie: el emisor reviso, o
    # hay dos fuentes. No se elige una a ciegas (2b, PILOT-FAILURES 2.2).
    vistos: dict[tuple[str, str], float] = {}
    for item in bundle.items:
        if item.valor is None:
            continue
        clave = (item.serie_codigo, str(item.periodo))
        if clave in vistos and abs(vistos[clave] - float(item.valor)) > 1e-9:
            motivos.append(AbstainReason.CONFLICTING_PRIMARY_VALUES)
            break
        vistos[clave] = float(item.valor)

    # sin duplicados, en orden de aparicion
    return list(dict.fromkeys(motivos))
