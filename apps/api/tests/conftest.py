"""Configuracion comun de los tests.

Se fija una DATABASE_URL ficticia antes de importar la aplicacion: el motor de
SQLAlchemy se construye de forma perezosa y no abre ninguna conexion al
crearse, asi que los tests unitarios corren sin necesidad de Postgres.
"""

from __future__ import annotations

import os

os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://tester:tester@localhost:5432/veritai_test"
)
os.environ.setdefault("VERITAI_ENV", "test")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "http://localhost:5173")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def cliente() -> TestClient:
    from veritai.main import app

    with TestClient(app) as c:
        yield c
