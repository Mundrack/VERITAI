"""Enums cerrados del dominio.

Son los mismos valores que usa la investigacion (research/scripts/normalizar_a_enums.py
y docs/GLOSARIO.md): el sistema y el corpus hablan el mismo vocabulario, sin traducir.
Los valores son cadenas para que viajen tal cual a la base de datos y al JSON.

POR QUE dos ejes (DEC-016)
    `truth` responde "la afirmacion literal es correcta?" y `context` responde
    "los datos muestran una divergencia?". Son maquinas de estado independientes:
    un dato puede ser exacto y estar fuera de contexto (supported + divergence).
    Y "ningun test disparo" produce no_divergence_detected, nunca supported.
"""

from __future__ import annotations

from enum import StrEnum


class Truth(StrEnum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    MIXED = "mixed"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NOT_APPLICABLE = "not_applicable"


class Context(StrEnum):
    DIVERGENCE_DETECTED = "divergence_detected"
    NO_DIVERGENCE_DETECTED = "no_divergence_detected"
    UNDETERMINED = "undetermined"
    NOT_APPLICABLE = "not_applicable"


class Clase(StrEnum):
    """Taxonomia vigente (DEC-026). La Puerta 2 solo implementa 2a."""

    RANKING_VS_VALOR = "1_ranking_vs_value"
    BASE_ELEGIDA = "2_baseline_selection"  # familia 2 · 2a periodo o base elegida
    BASE_REVISADA = "2b_base_revisada"  # familia 2 · 2b
    ABSOLUTO_VS_RELATIVO = "3_absolute_vs_relative"
    DENOMINADOR = "4_denominator"
    CAMBIO_DE_METODO = "5_methodology_change"  # familia 2 · 2c
    NONE = "none"
    OTHER_OBSERVED = "other_observed"


class AbstainReason(StrEnum):
    """Hard gates deterministas (R02 §11) mas METRIC_AMBIGUOUS (DEC-015)."""

    UNSUPPORTED_CLAIM_TYPE = "UNSUPPORTED_CLAIM_TYPE"
    REQUIRED_SLOT_MISSING = "REQUIRED_SLOT_MISSING"
    PRIMARY_SOURCE_NOT_FOUND = "PRIMARY_SOURCE_NOT_FOUND"
    PREVIOUS_EDITION_NOT_FOUND = "PREVIOUS_EDITION_NOT_FOUND"
    PERIOD_NOT_COMPARABLE = "PERIOD_NOT_COMPARABLE"
    METHODOLOGY_NOT_COMPARABLE = "METHODOLOGY_NOT_COMPARABLE"
    SOURCE_VERSION_AMBIGUOUS = "SOURCE_VERSION_AMBIGUOUS"
    CONFLICTING_PRIMARY_VALUES = "CONFLICTING_PRIMARY_VALUES"
    EXTRACTION_FAILED = "EXTRACTION_FAILED"
    METRIC_AMBIGUOUS = "METRIC_AMBIGUOUS"


# Motivos que impiden cualquier veredicto: sin evidencia utilizable no hay truth
# ni context, solo abstencion. Los demas motivos (PREVIOUS_EDITION_NOT_FOUND,
# PERIOD/METHODOLOGY_NOT_COMPARABLE, CONFLICTING_PRIMARY_VALUES) dejan evaluar
# truth con lo que hay y ponen context en undetermined.
BLOQUEANTES: frozenset[AbstainReason] = frozenset(
    {
        AbstainReason.UNSUPPORTED_CLAIM_TYPE,
        AbstainReason.REQUIRED_SLOT_MISSING,
        AbstainReason.PRIMARY_SOURCE_NOT_FOUND,
        AbstainReason.SOURCE_VERSION_AMBIGUOUS,
        AbstainReason.EXTRACTION_FAILED,
        AbstainReason.METRIC_AMBIGUOUS,
    }
)
