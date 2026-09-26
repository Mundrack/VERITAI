"""EvidenceBundle y EvidenceItem (START-HERE §5, R02 §9).

La regla que define la arquitectura: ningun numero del veredicto puede tener
como unico origen el LLM. Cada `EvidenceItem` lleva `raw_value_span`, el texto
literal de la fuente de donde salio el numero, y `bundle_hash` hace el paquete
reproducible: mismo hash, misma evidencia.

`base_version` es la adicion de la Puerta 2 (PILOT-FAILURES 2.2): los emisores
revisan ediciones anteriores, y hay que saber contra que version se compara.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from veritai.domain.periodo import Periodo


class Completitud(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient"


class Rol(StrEnum):
    PRIMARY = "primary"  # edicion actual
    HISTORICAL = "historical"  # ediciones anteriores
    METHODOLOGY = "methodology"


@dataclass(frozen=True)
class EvidenceItem:
    publisher: str
    url: str
    source_tier: int  # 1 = organismo estadistico oficial
    retrieved_at: datetime
    format: str  # api | dataset | html | pdf
    extraction_method: str  # p. ej. "json:DATOS_TABLA:Valor"
    raw_value_span: str  # texto literal de la fuente
    serie_codigo: str
    serie_nombre: str
    periodo: Periodo
    valor: float | None
    rol: Rol
    version: str = ""  # base_version: tabla/base del emisor
    document_date: str | None = None
    etiqueta: str = ""  # "objetivo" | "base_claim" | "ref:anterior" | "ref:interanual" | "ventana"

    @property
    def id(self) -> str:
        return f"{self.publisher}:{self.serie_codigo}:{self.periodo}"


@dataclass
class EvidenceBundle:
    claim_id: str
    primary_items: list[EvidenceItem] = field(default_factory=list)
    historical_items: list[EvidenceItem] = field(default_factory=list)
    methodology_items: list[EvidenceItem] = field(default_factory=list)
    missing_slots: list[str] = field(default_factory=list)

    @property
    def items(self) -> list[EvidenceItem]:
        return [*self.primary_items, *self.historical_items, *self.methodology_items]

    @property
    def completeness(self) -> Completitud:
        if not self.primary_items:
            return Completitud.INSUFFICIENT
        return Completitud.PARTIAL if self.missing_slots else Completitud.COMPLETE

    def buscar(self, etiqueta: str) -> EvidenceItem | None:
        return next((i for i in self.items if i.etiqueta == etiqueta), None)

    def por_periodo(self, periodo: Periodo) -> list[EvidenceItem]:
        return [i for i in self.items if i.periodo == periodo]

    @property
    def bundle_hash(self) -> str:
        """sha256 sobre lo que decide el veredicto: fuente, serie, periodo, span, version.

        No entra `retrieved_at`: dos recuperaciones de la misma evidencia deben
        dar el mismo hash, y una revision del emisor (span distinto) uno nuevo.
        """
        base = sorted(
            (i.publisher, i.url, i.serie_codigo, str(i.periodo), i.raw_value_span, i.version)
            for i in self.items
        )
        return hashlib.sha256(json.dumps(base, ensure_ascii=False).encode("utf-8")).hexdigest()
