"""Reglas de configuracion que no se pueden relajar."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from veritai.config import Settings


def test_cors_rechaza_comodin() -> None:
    with pytest.raises(ValidationError):
        Settings(
            database_url="postgresql+psycopg://u:p@h:5432/d",
            cors_allowed_origins="*",
        )


def test_la_url_de_base_de_datos_no_se_filtra_en_repr() -> None:
    s = Settings(
        database_url="postgresql+psycopg://usuario:secretisimo@host:5432/db",
        cors_allowed_origins="http://localhost:5173",
    )
    assert "secretisimo" not in repr(s)
    assert "secretisimo" not in str(s.database_url)
