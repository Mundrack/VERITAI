"""Eje truth y hard gates."""

from __future__ import annotations

from tests.dobles import ProveedorFalso, serie_trimestral
from veritai.application.analizar_claim import AnalizarClaim
from veritai.domain.abstencion import hard_gates
from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.enums import AbstainReason, Context, Truth
from veritai.domain.evidencia import EvidenceBundle
from veritai.domain.periodo import Periodo
from veritai.domain.verdad import evaluar_verdad

METRICA = MetricaEmisor(
    emisor="INE",
    tabla="65334",
    serie_nombre="Tasa de paro. Menores de 25.",
    unidad="pct",
    referencia_principal=Referencia.ANTERIOR,
)
SERIE = serie_trimestral({"2026-T2": 23.77, "2026-T1": 24.54, "2025-T4": 23.01, "2025-T2": 25.1})


def _claim(**kw) -> ClaimEstructurado:
    base = dict(
        claim_id="T",
        texto="t",
        fuente_url="https://x.test/",
        conjunto="desarrollo",
        tipo=TipoClaim.CAMBIO_ENTRE_PERIODOS,
        metrica=METRICA,
        periodo_objetivo=Periodo.parse("2026-T2"),
        periodo_base=Periodo.parse("2026-T1"),
        unidad_cambio=UnidadCambio.PUNTOS,
    )
    base.update(kw)
    return ClaimEstructurado(**base)


def _bundle(claim: ClaimEstructurado, serie=SERIE) -> EvidenceBundle:
    return AnalizarClaim(ProveedorFalso({METRICA.serie_nombre: serie})).bundle_de(claim)


def test_verdad_supported_con_redondeo_de_prensa() -> None:
    claim = _claim(valor_objetivo=23.8, cambio_afirmado=-0.8, direccion_afirmada=Direccion.BAJA)
    r = evaluar_verdad(claim, _bundle(claim))
    assert r.truth is Truth.SUPPORTED, r.resumen


def test_verdad_contradicted_en_numero_y_direccion() -> None:
    claim = _claim(valor_objetivo=24.5, direccion_afirmada=Direccion.SUBE)
    r = evaluar_verdad(claim, _bundle(claim))
    assert r.truth is Truth.CONTRADICTED, r.resumen


def test_verdad_mixed() -> None:
    claim = _claim(valor_objetivo=23.77, direccion_afirmada=Direccion.SUBE)
    assert evaluar_verdad(claim, _bundle(claim)).truth is Truth.MIXED


def test_verdad_insuficiente_sin_nada_comparable() -> None:
    claim = _claim(tipo=TipoClaim.NIVEL, periodo_base=None, unidad_cambio=None)
    assert evaluar_verdad(claim, _bundle(claim)).truth is Truth.INSUFFICIENT_EVIDENCE


def test_gates_tipo_no_soportado_y_slots() -> None:
    claim = _claim(tipo=TipoClaim.CRECIMIENTO_COMPUESTO)
    assert AbstainReason.UNSUPPORTED_CLAIM_TYPE in hard_gates(claim, _bundle(claim), 1)
    claim = _claim(periodo_base=None)
    assert AbstainReason.REQUIRED_SLOT_MISSING in hard_gates(claim, _bundle(claim), 1)


def test_gates_serie_no_encontrada_o_ambigua() -> None:
    claim = _claim(cambio_afirmado=-0.8)
    assert AbstainReason.PRIMARY_SOURCE_NOT_FOUND in hard_gates(claim, EvidenceBundle("T"), 0)
    assert AbstainReason.SOURCE_VERSION_AMBIGUOUS in hard_gates(claim, EvidenceBundle("T"), 2)


def test_gates_edicion_anterior_y_periodos() -> None:
    claim = _claim(cambio_afirmado=-0.8, periodo_base=Periodo.parse("2019-T1"))
    motivos = hard_gates(claim, _bundle(claim), 1)
    assert AbstainReason.PREVIOUS_EDITION_NOT_FOUND in motivos
    claim = _claim(cambio_afirmado=-0.8, periodo_base=Periodo.parse("2026-M03"))
    assert AbstainReason.PERIOD_NOT_COMPARABLE in hard_gates(claim, _bundle(claim), 1)


def test_caso_de_uso_control_negativo_y_abstencion() -> None:
    prov = ProveedorFalso({METRICA.serie_nombre: SERIE})
    caso = AnalizarClaim(prov)
    v = caso.ejecutar(
        _claim(valor_objetivo=23.8, cambio_afirmado=-0.8, direccion_afirmada=Direccion.BAJA)
    )
    assert (v.truth, v.context) == (Truth.SUPPORTED, Context.NO_DIVERGENCE_DETECTED)
    v = caso.ejecutar(
        _claim(tipo=TipoClaim.EXTREMO_HISTORICO, periodo_base=None, unidad_cambio=None)
    )
    assert v.abstiene and AbstainReason.UNSUPPORTED_CLAIM_TYPE in v.abstain_reasons
    v = caso.ejecutar(
        _claim(
            metrica=MetricaEmisor("INE", "65334", "Serie que no existe", "pct"),
            cambio_afirmado=-0.8,
        )
    )
    assert v.abstiene and AbstainReason.PRIMARY_SOURCE_NOT_FOUND in v.abstain_reasons
