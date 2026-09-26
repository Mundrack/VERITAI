"""Punto de entrada de la API de VERITAI.

Estado del proyecto: Puerta 2 (DEC-023). Ademas de la salud, la API expone
`POST /analisis`: analiza un claim estructurado contra el INE con el test 2a
(comparacion de base) y guarda la trazabilidad completa.

Desde que existe un endpoint que recibe contenido externo aplican sin
excepcion las secciones 23, 24 y 25 del START-HERE: limites de tamano, limites
de tiempo, validacion estricta con Pydantic, y la regla de que el contenido
recuperado es DATA y nunca INSTRUCCION.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from veritai import __version__
from veritai.api.routes import analisis, health
from veritai.config import obtener_settings
from veritai.db.session import crear_engine
from veritai.infrastructure.ine.edicion_anterior import EdicionAnteriorINE
from veritai.infrastructure.ine.proveedor import ProveedorINE
from veritai.infrastructure.ine.tempus import ClienteTempus
from veritai.infrastructure.repositorio import RepositorioPostgres

LOG = logging.getLogger("veritai")


def configurar_logging(nivel: str) -> None:
    logging.basicConfig(
        level=nivel.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    settings = obtener_settings()
    configurar_logging(settings.log_level)

    app.state.settings = settings
    app.state.engine = crear_engine(settings)

    # Unico emisor de la Puerta 2 (DEC-024). El cliente HTTP vive lo que vive la app.
    cliente_ine = ClienteTempus(
        timeout_s=settings.http_timeout_s,
        max_bytes=settings.http_max_bytes,
        cache_dir=Path(settings.evidencia_cache_dir) if settings.evidencia_cache_dir else None,
    )
    app.state.cliente_ine = cliente_ine
    app.state.proveedor_ine = ProveedorINE(cliente_ine)
    # Edicion anterior fuera de Tempus (2b, DEC-034): mapa cerrado de 8 operaciones.
    app.state.proveedor_edicion = EdicionAnteriorINE(
        timeout_s=settings.http_timeout_s, max_bytes=settings.http_max_bytes
    )
    app.state.repositorio = RepositorioPostgres(app.state.engine)
    LOG.info("veritai-api %s lista | entorno=%s", __version__, settings.veritai_env)

    try:
        yield
    finally:
        cliente_ine.cerrar()
        app.state.engine.dispose()
        LOG.info("veritai-api detenida")


def crear_app() -> FastAPI:
    settings = obtener_settings()

    app = FastAPI(
        title="VERITAI API",
        version=__version__,
        summary="Deteccion de divergencia contextual en afirmaciones estadisticas",
        # La documentacion interactiva solo se sirve en local.
        docs_url="/docs" if settings.es_local else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.es_local else None,
        lifespan=ciclo_de_vida,
    )

    # Lista blanca explicita de origenes. El validador de config rechaza "*".
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origenes_cors,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    app.include_router(health.router)
    app.include_router(analisis.router)
    return app


app = crear_app()
