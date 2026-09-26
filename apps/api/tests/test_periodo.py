"""Aritmetica de periodos."""

from __future__ import annotations

import pytest

from veritai.domain.periodo import Periodo


def test_parse_y_codigo() -> None:
    assert str(Periodo.parse("2026-M08")) == "2026-M08"
    assert str(Periodo.parse("2026-T2")) == "2026-T2"
    assert str(Periodo.parse("2025")) == "2025"
    assert Periodo.parse("2026-M8").codigo_ine() == "M08"
    assert Periodo.parse("2026-T2").codigo_ine() == "T2"
    assert Periodo.parse("2025").codigo_ine() is None


def test_anterior_e_interanual_cruzan_el_anio() -> None:
    assert Periodo.parse("2026-M01").anterior() == Periodo.parse("2025-M12")
    assert Periodo.parse("2026-T1").anterior() == Periodo.parse("2025-T4")
    assert Periodo.parse("2026-T2").interanual() == Periodo.parse("2025-T2")
    assert Periodo.parse("2026-M03").desplazado(-3) == Periodo.parse("2025-M12")


def test_desde_ine() -> None:
    assert Periodo.desde_ine(2026, "T2") == Periodo.parse("2026-T2")
    assert Periodo.desde_ine(2025, "M12") == Periodo.parse("2025-M12")
    assert Periodo.desde_ine(2024, None) == Periodo(2024)
    # tablas anuales del INE: 'A', vacio o ausente (tabla 28724, condenados)
    assert Periodo.desde_ine(2018, "A") == Periodo(2018)
    assert Periodo.desde_ine(2018, "") == Periodo(2018)


def test_etiqueta_en_espanol() -> None:
    assert Periodo.parse("2018-M12").etiqueta() == "diciembre de 2018"
    assert Periodo.parse("2026-T2").etiqueta() == "2T 2026"


@pytest.mark.parametrize("malo", ["2026-M13", "2026-T5", "26-M01", "agosto 2026", "2026-Q2"])
def test_rechaza_periodos_invalidos(malo: str) -> None:
    with pytest.raises(ValueError):
        Periodo.parse(malo)


def test_orden_cronologico() -> None:
    assert Periodo.parse("2018-M05") < Periodo.parse("2018-M12")
    assert Periodo.parse("2025-T4") < Periodo.parse("2026-T1")
