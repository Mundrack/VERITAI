"""Test 2a con bundles sinteticos: signo, umbral, base coincidente, valor en otro periodo."""

from __future__ import annotations

import pytest

from tests.dobles import ProveedorFalso, serie_trimestral
from veritai.application.analizar_claim import AnalizarClaim
from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.periodo import Periodo
from veritai.domain.tests.comparacion_base import aplicar_2a, cambio, tolerancia_para

METRICA_MENSUAL = MetricaEmisor(
    emisor="INE",
    tabla="99999",
    serie_nombre="Sociedades creadas. Total.",
    unidad="unidades",
    referencia_principal=Referencia.INTERANUAL,
)
METRICA_TRIM = MetricaEmisor(
    emisor="INE",
    tabla="65334",
    serie_nombre="Tasa de paro. Menores de 25.",
    unidad="pct",
    referencia_principal=Referencia.ANTERIOR,
)


def _claim(**kw) -> ClaimEstructurado:
    base = dict(
        claim_id="T",
        texto="t",
        fuente_url="https://x.test/",
        conjunto="desarrollo",
        tipo=TipoClaim.CAMBIO_ENTRE_PERIODOS,
        metrica=METRICA_MENSUAL,
        periodo_objetivo=Periodo.parse("2018-M12"),
        periodo_base=Periodo.parse("2018-M05"),
        unidad_cambio=UnidadCambio.PORCENTAJE,
    )
    base.update(kw)
    return ClaimEstructurado(**base)


def _bundle(proveedor: ProveedorFalso, claim: ClaimEstructurado):
    return AnalizarClaim(proveedor).bundle_de(claim)


def test_cambio_y_tolerancia() -> None:
    assert round(cambio(8908, 6811, UnidadCambio.PORCENTAJE), 2) == -23.54
    assert cambio(24.54, 23.77, UnidadCambio.PUNTOS) == pytest.approx(-0.77)
    assert cambio(0, 5, UnidadCambio.PORCENTAJE) is None
    assert tolerancia_para(23.8, 23.77) >= 0.05
    assert tolerancia_para(6811.0, 6811.0) >= 34.0  # 0,5% de 6.811


def test_dispara_cuando_la_base_elegida_cambia_el_signo() -> None:
    # P11: mayo -> diciembre da -23,5%; diciembre contra diciembre del anio anterior da +1,1%.
    serie = {
        Periodo.parse("2018-M05"): 8908.0,
        Periodo.parse("2018-M12"): 6811.0,
        Periodo.parse("2018-M11"): 8000.0,
        Periodo.parse("2017-M12"): 6737.0,
    }
    prov = ProveedorFalso({METRICA_MENSUAL.serie_nombre: serie}, tabla="99999")
    claim = _claim(cambio_afirmado=-23.0, direccion_afirmada=Direccion.BAJA)
    r = aplicar_2a(claim, _bundle(prov, claim))
    assert r.aplicable and r.disparo
    assert r.subtipo == "base_no_es_referencia"
    assert (
        r.calculos["cambio_recomputado_con_base_del_claim"]
        < 0
        < r.calculos["cambio_recomputado_con_referencia_emisor"]
    )


def test_no_dispara_si_la_base_es_la_referencia_del_emisor() -> None:
    serie = serie_trimestral(
        {"2026-T2": 23.77, "2026-T1": 24.54, "2025-T2": 25.1, "2025-T4": 23.01}
    )
    prov = ProveedorFalso({METRICA_TRIM.serie_nombre: serie})
    claim = _claim(
        metrica=METRICA_TRIM,
        periodo_objetivo=Periodo.parse("2026-T2"),
        periodo_base=Periodo.parse("2026-T1"),
        unidad_cambio=UnidadCambio.PUNTOS,
        cambio_afirmado=-0.77,
        direccion_afirmada=Direccion.BAJA,
    )
    r = aplicar_2a(claim, _bundle(prov, claim))
    assert r.aplicable and not r.disparo
    assert "referencia del emisor" in r.motivo


def test_no_dispara_si_magnitudes_comparables() -> None:
    # base distinta a la referencia pero el recomputo es parecido: no hay base elegida a
    # conveniencia que detectar
    serie = {
        Periodo.parse("2018-M05"): 7000.0,
        Periodo.parse("2018-M12"): 6811.0,
        Periodo.parse("2018-M11"): 6900.0,
        Periodo.parse("2017-M12"): 7010.0,
    }
    prov = ProveedorFalso({METRICA_MENSUAL.serie_nombre: serie}, tabla="99999")
    claim = _claim(cambio_afirmado=-2.7)
    r = aplicar_2a(claim, _bundle(prov, claim))
    assert r.aplicable and not r.disparo


def test_dispara_cuando_el_valor_es_de_otro_periodo() -> None:
    # C17: el titular atribuye 24,5% al 2T; ese es el valor del 1T. En el 2T la serie da 23,77.
    serie = serie_trimestral(
        {"2026-T2": 23.77, "2026-T1": 24.54, "2025-T4": 23.01, "2025-T2": 25.1}
    )
    prov = ProveedorFalso({METRICA_TRIM.serie_nombre: serie})
    claim = _claim(
        metrica=METRICA_TRIM,
        periodo_objetivo=Periodo.parse("2026-T2"),
        periodo_base=Periodo.parse("2026-T1"),
        unidad_cambio=UnidadCambio.PUNTOS,
        valor_objetivo=24.5,
        direccion_afirmada=Direccion.SUBE,
    )
    r = aplicar_2a(claim, _bundle(prov, claim))
    assert r.disparo and r.subtipo == "valor_atribuido_a_otro_periodo"
    assert r.calculos["periodo_donde_si_aparece"] == "2026-T1"


def test_no_aplicable_a_claims_de_nivel() -> None:
    serie = serie_trimestral({"2026-T2": 23.77})
    prov = ProveedorFalso({METRICA_TRIM.serie_nombre: serie})
    claim = _claim(
        metrica=METRICA_TRIM,
        tipo=TipoClaim.NIVEL,
        periodo_objetivo=Periodo.parse("2026-T2"),
        periodo_base=None,
        unidad_cambio=None,
        valor_objetivo=23.8,
    )
    r = aplicar_2a(claim, _bundle(prov, claim))
    assert not r.aplicable and not r.disparo
