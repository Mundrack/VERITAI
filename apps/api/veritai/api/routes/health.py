"""Endpoints de salud.

Tres niveles, cada uno con un proposito distinto:

    /health/live   el proceso responde. Sin dependencias externas.
                   Es el que usa el HEALTHCHECK de Docker: si dependiera de la
                   base de datos, una caida de Postgres reiniciaria la API en
                   bucle sin arreglar nada.

    /health/ready  la API puede atender trabajo real, es decir, hay base de
                   datos. Devuelve 503 si no la hay.

    /health        resumen legible para una persona.
"""

from __future__ import annotations

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

from veritai import __version__
from veritai.db.session import comprobar_conexion

router = APIRouter(prefix="/health", tags=["salud"])


class RespuestaVivo(BaseModel):
    estado: str
    version: str


class RespuestaListo(BaseModel):
    estado: str
    base_de_datos: str
    detalle: str | None = None


class RespuestaSalud(BaseModel):
    servicio: str
    version: str
    entorno: str
    base_de_datos: str


@router.get("/live", response_model=RespuestaVivo, summary="El proceso responde")
def vivo() -> RespuestaVivo:
    return RespuestaVivo(estado="vivo", version=__version__)


@router.get("/ready", response_model=RespuestaListo, summary="Hay base de datos")
def listo(request: Request, response: Response) -> RespuestaListo:
    engine = getattr(request.app.state, "engine", None)
    if engine is None:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return RespuestaListo(estado="no_listo", base_de_datos="sin_inicializar", detalle=None)

    viva, error = comprobar_conexion(engine)
    if not viva:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return RespuestaListo(estado="no_listo", base_de_datos="caida", detalle=error)

    return RespuestaListo(estado="listo", base_de_datos="conectada")


@router.get("", response_model=RespuestaSalud, summary="Resumen del servicio")
def salud(request: Request) -> RespuestaSalud:
    engine = getattr(request.app.state, "engine", None)
    viva = engine is not None and comprobar_conexion(engine)[0]
    settings = request.app.state.settings
    return RespuestaSalud(
        servicio="veritai-api",
        version=__version__,
        entorno=settings.veritai_env,
        base_de_datos="conectada" if viva else "no_disponible",
    )
