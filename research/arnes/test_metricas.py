"""Tests del arnes: intervalos, las cinco de R02 §7, FPR/H3, acuerdo y guardia."""

from __future__ import annotations

import pytest
from metricas import (
    acuerdo,
    cinco_metricas,
    fpr,
    regla_de_tres,
    semaforo,
    verificar_conjunto,
    wilson,
)


def test_wilson_valores_conocidos() -> None:
    p, lo, hi = wilson(0, 40)
    assert p == 0 and lo == 0 and hi == pytest.approx(0.0876, abs=0.0005)
    p, lo, hi = wilson(18, 20)
    assert (p, lo, hi) == (pytest.approx(0.9), pytest.approx(0.699, abs=0.001), pytest.approx(0.972, abs=0.001))
    p, lo, hi = wilson(2, 50)
    assert hi == pytest.approx(0.135, abs=0.001)
    with pytest.raises(ValueError):
        wilson(0, 0)
    with pytest.raises(ValueError):
        wilson(5, 4)


def test_regla_de_tres_y_semaforo() -> None:
    assert regla_de_tres(40) == pytest.approx(0.075)
    assert semaforo(74.2, 60, 30) == "verde"
    assert semaforo(45, 60, 30) == "ambar"
    assert semaforo(10, 60, 30) == "rojo"
    assert semaforo(15.0, 20, 45, mayor_es_mejor=False) == "verde"
    assert semaforo(None, 60, 30) == "n/d"


def _fila(case_id: str, truth="supported", context="no_divergence_detected", clase="none", **kw) -> dict:
    base = {
        "case_id": case_id, "truth": truth, "context": context, "clase_primaria": clase,
        "current_edition_found": "si", "previous_edition_found": "si", "alcanzable_por_agente": "si",
        "recuperabilidad": "A", "minutes_to_locate": "5", "minutes_to_extract": "3",
        "cronometrado_por": "agente", "abstain_reason": "",
    }
    base.update(kw)
    return base


def _resultado(context="no_divergence_detected", truth="supported", clase="none", aplicable=True,
               senales=(), abstain=()) -> dict:
    return {"veredicto": {"truth": truth, "context": context, "clase_primaria": clase,
                          "abstain_reasons": list(abstain),
                          "tests": [{"aplicable": aplicable, "disparo": context == "divergence_detected",
                                     "senales": list(senales)}]}}


def test_cinco_metricas_sintetico_y_columna_ausente() -> None:
    filas = [
        _fila("A1"),
        _fila("A2", previous_edition_found="no"),
        _fila("A3", alcanzable_por_agente="no", recuperabilidad="D"),
        _fila("A4", context="divergence_detected", clase="2_baseline_selection"),
        _fila("A5", context="divergence_detected", clase="4_denominator", cronometrado_por="humano",
              minutes_to_locate="25", minutes_to_extract="15"),  # 40 min: ambar (20-45)
    ]
    m = cinco_metricas(filas)
    assert m["edicion_anterior_localizada"]["conservadora"]["k"] == 3  # A2 no, A3 bloqueado
    assert m["edicion_anterior_localizada"]["leniente"]["k"] == 4
    assert m["fuente_primaria_localizada"]["conservadora"]["k"] == 4
    assert m["extraccion_sin_intervencion_extrema"]["conservadora"]["k"] == 4
    assert m["clases_de_divergencia_observadas"] == {
        "n_clases": 2, "clases": ["2_baseline_selection", "4_denominator"], "semaforo": "ambar",
        "umbral": {"verde": ">=3", "ambar": "2"},
    }
    assert m["tiempo_medio_por_caso"]["agente"]["media_min"] == 8.0
    assert m["tiempo_medio_por_caso"]["humano"]["semaforo"] == "ambar"
    sin_col = [{k: v for k, v in f.items() if k != "current_edition_found"} for f in filas]
    assert cinco_metricas(sin_col)["fuente_primaria_localizada"] is None


def test_fpr_y_h3_con_los_umbrales_del_diseno() -> None:
    filas = [_fila(f"C{i:02d}") for i in range(40)]
    resultados = {f["case_id"]: _resultado() for f in filas}
    resultados["C00"] = _resultado(context="divergence_detected", clase="2_baseline_selection")
    resultados["C01"] = _resultado(senales=("horizonte_largo",))
    r = fpr(filas, resultados)
    assert r["fpr"]["k"] == 1 and r["fpr"]["n"] == 40 and r["falsos_positivos"] == ["C00"]
    assert r["fpr"]["ic95"][1] == 12.9 and r["h3"]["veredicto"] == "sostenida"
    assert r["controles_con_senal"] == ["C01"]  # la senal no es falso positivo (DEC-029)

    # 30 controles: por debajo del minimo, no evaluable aunque no haya errores
    assert fpr(filas[:30], {k: _resultado() for k in resultados})["h3"]["veredicto"] == "no_evaluable"

    # 3 falsos positivos en 40: limite superior 19,9 > 15 -> no sostenida
    for cid in ("C02", "C03"):
        resultados[cid] = _resultado(context="divergence_detected", clase="2_baseline_selection")
    assert fpr(filas, resultados)["h3"]["veredicto"] == "no_sostenida"

    # un control de nivel sin test aplicable no entra en el denominador
    filas.append(_fila("N1"))
    resultados["N1"] = _resultado(context="undetermined", aplicable=False)
    r = fpr(filas, resultados)
    assert r["fpr"]["n"] == 40 and r["controles_sin_test_aplicable"] == ["N1"]

    # claim falso anotado sin divergencia y el sistema dispara: cuenta en la secundaria, no en el FPR
    filas.append(_fila("F1", truth="contradicted"))
    resultados["F1"] = _resultado(truth="contradicted", context="divergence_detected", clase="2_baseline_selection")
    r = fpr(filas, resultados)
    assert r["fpr"]["n"] == 40 and r["disparos_sobre_no_divergencia_anotada"]["n"] == 41
    assert "F1" in r["disparos_ids"]


def test_acuerdo_y_recall_2a() -> None:
    filas = [
        _fila("P1", context="divergence_detected", clase="2_baseline_selection"),
        _fila("P2", context="divergence_detected", clase="2_baseline_selection"),
        _fila("C1"),
        _fila("X1", truth="insufficient_evidence", context="undetermined", abstain_reason="UNSUPPORTED_CLAIM_TYPE"),
    ]
    resultados = {
        "P1": _resultado(context="divergence_detected", clase="2_baseline_selection"),
        "P2": _resultado(),
        "C1": _resultado(),
        "X1": _resultado(truth="insufficient_evidence", context="undetermined", aplicable=False,
                         abstain=("UNSUPPORTED_CLAIM_TYPE",)),
    }
    a = acuerdo(filas, resultados)
    assert a["n_pares"] == 4
    assert a["acuerdo_truth"]["k"] == 4 and a["acuerdo_context"]["k"] == 3
    assert a["recall_2a"]["k"] == 1 and a["recall_2a"]["n"] == 2 and a["recall_2a"]["detectados"] == ["P1"]
    assert a["abstencion_cuando_anotada"]["k"] == 1
    assert a["matriz_context_anotado_x_sistema"]["divergence_detected -> no_divergence_detected"] == 1


def test_guardia_de_conjunto() -> None:
    casos = {"A": {"conjunto": "desarrollo"}, "B": {"conjunto": "evaluacion"}, "C": {}}
    errores = verificar_conjunto(casos, permitir_desarrollo=False)
    assert [e.split(":")[0] for e in errores] == ["A", "C"]
    assert verificar_conjunto(casos, permitir_desarrollo=True) == []
