"""POST /analisis de punta a punta con un proveedor en memoria y repositorio en memoria."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.dobles import ProveedorFalso, serie_trimestral
from veritai.infrastructure.repositorio import RepositorioMemoria

NOMBRE = "Tasa de paro de la población. Ambos sexos. Total Nacional. Menores de 25 años."
SERIE = serie_trimestral(
    {"2026-T2": 23.77, "2026-T1": 24.54, "2025-T4": 23.01, "2025-T3": 24.9, "2025-T2": 25.1}
)


@pytest.fixture
def api(cliente: TestClient):
    app = cliente.app
    original = (getattr(app.state, "proveedor_ine", None), getattr(app.state, "repositorio", None))
    app.state.proveedor_ine = ProveedorFalso({NOMBRE: SERIE})
    app.state.repositorio = RepositorioMemoria()
    yield cliente
    app.state.proveedor_ine, app.state.repositorio = original


def _cuerpo(**kw) -> dict:
    base = {
        "claim_id": "C16",
        "texto": "La tasa de paro juvenil cae al 23,77% pese a sumar 19.600 desempleados",
        "fuente_url": "https://www.infobae.com/x",
        "conjunto": "desarrollo",
        "tipo": "cambio_entre_periodos",
        "metrica": {
            "emisor": "INE",
            "tabla": "65334",
            "serie_nombre": NOMBRE,
            "unidad": "pct",
            "referencia_principal": "anterior",
        },
        "periodo_objetivo": "2026-T2",
        "periodo_base": "2026-T1",
        "valor_objetivo": 23.77,
        "cambio_afirmado": -0.77,
        "unidad_cambio": "pp",
        "direccion_afirmada": "baja",
        "origen_case_id": "C16",
    }
    base.update(kw)
    return base


def test_control_negativo_de_punta_a_punta(api: TestClient) -> None:
    r = api.post("/analisis", json=_cuerpo())
    assert r.status_code == 200, r.text
    cuerpo = r.json()
    v = cuerpo["veredicto"]
    assert (v["truth"], v["context"], v["clase_primaria"]) == (
        "supported",
        "no_divergence_detected",
        "none",
    )
    assert v["abstain_reasons"] == []
    assert cuerpo["evidencia"]["completeness"] == "complete"
    assert all(i["raw_value_span"] for i in cuerpo["evidencia"]["items"])
    assert cuerpo["persistido"] is True
    assert api.app.state.repositorio.analisis[-1]["veredicto"]["claim_id"] == "C16"


def test_valor_de_otro_periodo_da_contradicho_y_divergencia(api: TestClient) -> None:
    r = api.post(
        "/analisis",
        json=_cuerpo(
            claim_id="C17", valor_objetivo=24.5, cambio_afirmado=None, direccion_afirmada="sube"
        ),
    )
    assert r.status_code == 200, r.text
    v = r.json()["veredicto"]
    assert v["truth"] == "contradicted"
    assert v["context"] == "divergence_detected" and v["clase_primaria"] == "2_baseline_selection"
    assert v["tests"][0]["subtipo"] == "valor_atribuido_a_otro_periodo"


def test_rechaza_emisores_fuera_de_alcance_y_periodos_malos(api: TestClient) -> None:
    malo = _cuerpo()
    malo["metrica"]["emisor"] = "Eurostat"
    assert api.post("/analisis", json=malo).status_code == 422
    assert api.post("/analisis", json=_cuerpo(periodo_objetivo="2T 2026")).status_code == 422
    assert api.post("/analisis", json=_cuerpo(texto="x" * 2001)).status_code == 422
    malo = _cuerpo()
    malo["metrica"]["tabla"] = "65334; drop table"
    assert api.post("/analisis", json=malo).status_code == 422


def test_abstiene_si_la_serie_no_existe(api: TestClient) -> None:
    cuerpo = _cuerpo()
    cuerpo["metrica"]["serie_nombre"] = "Una serie que el INE no publica"
    r = api.post("/analisis", json=cuerpo)
    assert r.status_code == 200
    v = r.json()["veredicto"]
    assert (
        v["truth"] == "insufficient_evidence" and "PRIMARY_SOURCE_NOT_FOUND" in v["abstain_reasons"]
    )
