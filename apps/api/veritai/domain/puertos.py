"""Puertos del dominio: lo que la infraestructura tiene que implementar.

Direccion de las dependencias (CLAUDE.md §4): api -> application -> domain.
El dominio define estas interfaces; `infrastructure/` las implementa (conector
INE, repositorio PostgreSQL) y los tests las sustituyen por dobles en memoria.
"""

from __future__ import annotations

from typing import Protocol

from veritai.domain.claim import ClaimEstructurado, MetricaEmisor, Referencia
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem
from veritai.domain.periodo import Periodo


class ProveedorEvidencia(Protocol):
    """Recupera evidencia primaria de UN emisor. En la Puerta 2, el INE."""

    def obtener_valor(
        self, metrica: MetricaEmisor, periodo: Periodo, etiqueta: str
    ) -> EvidenceItem | None:
        """El valor de la serie en ese periodo, con su span literal; None si no existe."""

    def referencias_emisor(
        self, metrica: MetricaEmisor, periodo: Periodo
    ) -> list[tuple[Referencia, Periodo]]:
        """Los periodos contra los que el emisor compara ese periodo (anterior, interanual)."""

    def ventana(self, metrica: MetricaEmisor, periodo: Periodo, n: int) -> list[EvidenceItem]:
        """Los n periodos anteriores al dado, para detectar valores atribuidos a otro periodo."""

    def series_coincidentes(self, metrica: MetricaEmisor) -> int:
        """Cuantas series de la tabla casan con el nombre: 0 = no encontrada, >1 = ambigua."""


class Repositorio(Protocol):
    """Persistencia con trazabilidad completa: claim, bundle, items, veredicto, audit."""

    def guardar_analisis(
        self, claim: ClaimEstructurado, bundle: EvidenceBundle, veredicto: object, duracion_ms: int
    ) -> int:
        """Guarda todo en una transaccion y devuelve el id del veredicto."""
