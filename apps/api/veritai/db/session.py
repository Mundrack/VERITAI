"""Acceso a PostgreSQL.

El motor se construye a partir de `DATABASE_URL` y de nada mas. La misma
funcion sirve para el contenedor local y para Supabase.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.pool import NullPool

from veritai.config import Settings

LOG = logging.getLogger(__name__)


def crear_engine(settings: Settings) -> Engine:
    """Construye el motor de SQLAlchemy segun el entorno.

    DB_USE_POOL=false desactiva el pool del lado del cliente y las sentencias
    preparadas. Es lo que hay que poner al conectar contra el pooler de
    Supabase en modo transaction (puerto 6543): ese pooler reparte la conexion
    entre transacciones, y una sentencia preparada del cliente se pierde entre
    una y otra. Detalle en:
    migracion-supabase-base-de-datos/02-DIFERENCIAS-LOCAL-VS-SUPABASE.md
    """
    opciones: dict[str, Any] = {
        "pool_pre_ping": True,
        "echo": False,
        "future": True,
    }

    if settings.db_use_pool:
        opciones["pool_size"] = settings.db_pool_size
        opciones["max_overflow"] = settings.db_pool_max_overflow
    else:
        opciones["poolclass"] = NullPool
        opciones["connect_args"] = {"prepare_threshold": None}

    LOG.info(
        "creando engine de base de datos (pool=%s)",
        "activado" if settings.db_use_pool else "desactivado",
    )
    return create_engine(settings.database_url.get_secret_value(), **opciones)


def comprobar_conexion(engine: Engine) -> tuple[bool, str | None]:
    """Devuelve (esta_viva, mensaje_de_error).

    Nunca propaga la excepcion original al cliente HTTP: el mensaje de un error
    de conexion puede contener el host y el usuario de la base de datos.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        return True, None
    except Exception as exc:  # noqa: BLE001 - se degrada, no se rompe
        LOG.warning("comprobacion de base de datos fallida: %s", type(exc).__name__)
        return False, type(exc).__name__
