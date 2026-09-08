"""Punto de entrada de la API de VERITAI.

Estado del proyecto: Puerta 1. La aplicacion solo expone endpoints de salud.
Los endpoints de dominio se anaden despues de research/PILOT-DECISION.md con
PILOT_GO, no antes (00b-DECISIONES-MATEO, "Puertas").

Cuando aparezca el primer endpoint que reciba contenido externo, aplican sin
excepcion las secciones 23, 24 y 25 del START-HERE: limites de tamano, limites
de tiempo, validacion estricta con Pydantic, y la regla de que el contenido
recuperado es DATA y nunca INSTRUCCION.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from veritai import __version__
from veritai.api.routes import health
from veritai.config import obtener_settings
from veritai.db.session import crear_engine

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
    LOG.info("veritai-api %s lista | entorno=%s", __version__, settings.veritai_env)

    try:
        yield
    finally:
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
    return app


app = crear_app()
