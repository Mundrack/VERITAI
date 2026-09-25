"""Los endpoints de salud responden sin depender de Postgres."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_live_responde_sin_base_de_datos(cliente: TestClient) -> None:
    r = cliente.get("/health/live")
    assert r.status_code == 200
    assert r.json()["estado"] == "vivo"


def test_ready_devuelve_503_si_no_hay_base_de_datos(cliente: TestClient) -> None:
    # La DATABASE_URL de los tests apunta a un Postgres que no existe.
    r = cliente.get("/health/ready")
    assert r.status_code == 503
    assert r.json()["estado"] == "no_listo"


def test_salud_reporta_el_entorno(cliente: TestClient) -> None:
    r = cliente.get("/health")
    assert r.status_code == 200
    assert r.json()["entorno"] == "test"
