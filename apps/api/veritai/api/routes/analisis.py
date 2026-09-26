"""POST /analisis: analiza un claim estructurado y devuelve el veredicto.

Capa fina: valida con Pydantic (limites de tamano, enums cerrados, URL),
construye el claim de dominio y delega en el caso de uso. El contenido que
llega es DATO: se valida, no se interpreta. El unico emisor admitido es INE
(DEC-024); cualquier otro se rechaza con 422 antes de tocar la red.
"""

from __future__ import annotations

import logging
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, HttpUrl, field_validator

from veritai.application.analizar_claim import AnalizarClaim
from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.periodo import Periodo

LOG = logging.getLogger(__name__)
router = APIRouter(prefix="/analisis", tags=["analisis"])


class MetricaEntrada(BaseModel):
    emisor: Literal["INE"]
    tabla: str = Field(pattern=r"^\d{1,8}$")
    serie_nombre: str = Field(min_length=3, max_length=300)
    unidad: str = Field(min_length=1, max_length=20)
    referencia_principal: Literal["anterior", "interanual"] = "interanual"
    descripcion: str = Field(default="", max_length=300)


class ClaimEntrada(BaseModel):
    claim_id: str = Field(pattern=r"^[A-Za-z0-9_.-]{1,64}$")
    texto: str = Field(min_length=3, max_length=2000)
    fuente_url: HttpUrl
    conjunto: Literal["desarrollo", "evaluacion"] = "desarrollo"
    tipo: Literal[
        "cambio_entre_periodos",
        "nivel",
        "umbral",
        "extremo_historico",
        "crecimiento_compuesto",
        "otro",
    ]
    metrica: MetricaEntrada
    periodo_objetivo: str = Field(max_length=12)
    periodo_base: str | None = Field(default=None, max_length=12)
    valor_objetivo: float | None = None
    valor_base: float | None = None
    cambio_afirmado: float | None = None
    unidad_cambio: Literal["pct", "pp", "abs"] | None = None
    direccion_afirmada: Literal["sube", "baja", "igual"] | None = None
    origen_case_id: str = Field(default="", max_length=16)
    notas: str = Field(default="", max_length=2000)
    etiquetas_corpus: dict[str, str] = Field(default_factory=dict)

    @field_validator("periodo_objetivo", "periodo_base")
    @classmethod
    def _periodo_valido(cls, v: str | None) -> str | None:
        if v is not None:
            Periodo.parse(v)  # lanza ValueError -> 422
        return v

    @field_validator("etiquetas_corpus")
    @classmethod
    def _etiquetas_acotadas(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) > 10 or any(len(k) > 40 or len(x) > 80 for k, x in v.items()):
            raise ValueError("etiquetas_corpus: maximo 10 claves de 40 y valores de 80 caracteres")
        return v

    def a_dominio(self) -> ClaimEstructurado:
        m = self.metrica
        return ClaimEstructurado(
            claim_id=self.claim_id,
            texto=self.texto,
            fuente_url=str(self.fuente_url),
            conjunto=self.conjunto,
            tipo=TipoClaim(self.tipo),
            metrica=MetricaEmisor(
                emisor=m.emisor,
                tabla=m.tabla,
                serie_nombre=m.serie_nombre,
                unidad=m.unidad,
                referencia_principal=Referencia(m.referencia_principal),
                descripcion=m.descripcion,
            ),
            periodo_objetivo=Periodo.parse(self.periodo_objetivo),
            periodo_base=None if self.periodo_base is None else Periodo.parse(self.periodo_base),
            valor_objetivo=self.valor_objetivo,
            valor_base=self.valor_base,
            cambio_afirmado=self.cambio_afirmado,
            unidad_cambio=None if self.unidad_cambio is None else UnidadCambio(self.unidad_cambio),
            direccion_afirmada=None
            if self.direccion_afirmada is None
            else Direccion(self.direccion_afirmada),
            origen_case_id=self.origen_case_id,
            notas=self.notas,
            etiquetas_corpus=dict(self.etiquetas_corpus),
        )


class RespuestaAnalisis(BaseModel):
    veredicto: dict[str, Any]
    evidencia: dict[str, Any]
    persistido: bool
    duracion_ms: int


@router.post(
    "", response_model=RespuestaAnalisis, summary="Analiza un claim estructurado (INE, test 2a)"
)
def analizar(entrada: ClaimEntrada, request: Request) -> RespuestaAnalisis:
    proveedor = getattr(request.app.state, "proveedor_ine", None)
    if proveedor is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "proveedor de evidencia no inicializado"
        )
    repositorio = getattr(request.app.state, "repositorio", None)

    claim = entrada.a_dominio()
    caso = AnalizarClaim(proveedor, repositorio)
    if hasattr(proveedor, "preparar"):
        mas_antiguo = min(
            p
            for p in (
                claim.periodo_base,
                claim.periodo_objetivo.desplazado(-caso.ventana),
                claim.periodo_objetivo.interanual(),
            )
            if p is not None
        )
        proveedor.preparar(claim.metrica, mas_antiguo)

    from time import perf_counter

    t0 = perf_counter()
    try:
        veredicto = caso.ejecutar(claim)
    except Exception as exc:  # noqa: BLE001 - nunca se filtra la traza al cliente
        LOG.exception("fallo analizando %s", claim.claim_id)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"fallo interno ({type(exc).__name__})"
        ) from exc
    bundle = caso.bundle_de(claim)
    return RespuestaAnalisis(
        veredicto=veredicto.a_dict(),
        evidencia={
            "bundle_hash": bundle.bundle_hash,
            "completeness": bundle.completeness.value,
            "missing_slots": bundle.missing_slots,
            "items": [
                {
                    "etiqueta": i.etiqueta,
                    "rol": i.rol.value,
                    "serie": i.serie_codigo,
                    "periodo": str(i.periodo),
                    "valor": i.valor,
                    "raw_value_span": i.raw_value_span,
                    "url": i.url,
                    "version": i.version,
                }
                for i in bundle.items
            ],
        },
        persistido=repositorio is not None,
        duracion_ms=int((perf_counter() - t0) * 1000),
    )
