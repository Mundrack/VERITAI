"""Dobles de test: un proveedor en memoria que cumple el puerto ProveedorEvidencia."""

from __future__ import annotations

from datetime import UTC, datetime

from veritai.domain.claim import MetricaEmisor, Referencia
from veritai.domain.evidencia import EvidenceItem, Rol
from veritai.domain.periodo import Periodo


class ProveedorFalso:
    """series: {nombre_serie: {Periodo: valor}}. Los spans imitan el formato del INE."""

    def __init__(
        self, series: dict[str, dict[Periodo, float | None]], tabla: str = "65334"
    ) -> None:
        self.series = series
        self.tabla = tabla
        self.llamadas: list[str] = []

    def _nombre(self, metrica: MetricaEmisor) -> str | None:
        coincidentes = [
            n for n in self.series if n.strip().lower() == metrica.serie_nombre.strip().lower()
        ]
        return coincidentes[0] if len(coincidentes) == 1 else None

    def series_coincidentes(self, metrica: MetricaEmisor) -> int:
        return sum(
            1 for n in self.series if n.strip().lower() == metrica.serie_nombre.strip().lower()
        )

    def obtener_valor(
        self, metrica: MetricaEmisor, periodo: Periodo, etiqueta: str
    ) -> EvidenceItem | None:
        self.llamadas.append(f"{etiqueta}:{periodo}")
        nombre = self._nombre(metrica)
        if nombre is None or periodo not in self.series[nombre]:
            return None
        valor = self.series[nombre][periodo]
        return EvidenceItem(
            publisher="INE",
            url=f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{self.tabla}?nult=24&tip=A",
            source_tier=1,
            retrieved_at=datetime(2026, 9, 25, tzinfo=UTC),
            format="api",
            extraction_method="json:DATOS_TABLA:Valor",
            raw_value_span=(
                f'{{"T3_Periodo":"{periodo.codigo_ine()}", "Anyo":{periodo.anio}, "Valor":{valor}}}'
            ),
            serie_codigo="EPA000000",
            serie_nombre=nombre,
            periodo=periodo,
            valor=valor,
            rol=Rol.PRIMARY if etiqueta == "objetivo" else Rol.HISTORICAL,
            version=f"tabla {self.tabla}",
            etiqueta=etiqueta,
        )

    def referencias_emisor(
        self, metrica: MetricaEmisor, periodo: Periodo
    ) -> list[tuple[Referencia, Periodo]]:
        return [
            (Referencia.ANTERIOR, periodo.anterior()),
            (Referencia.INTERANUAL, periodo.interanual()),
        ]

    def ventana(self, metrica: MetricaEmisor, periodo: Periodo, n: int) -> list[EvidenceItem]:
        items = []
        p = periodo
        for _ in range(n):
            p = p.anterior()
            item = self.obtener_valor(metrica, p, f"ventana:{p}")
            if item is not None:
                items.append(item)
        return items

    def metodologia(self, metrica: MetricaEmisor) -> EvidenceItem | None:
        nombre = self._nombre(metrica)
        if nombre is None:
            return None
        return EvidenceItem(
            publisher="INE",
            url=f"https://www.ine.es/jaxiT3/Tabla.htm?t={self.tabla}",
            source_tier=1,
            retrieved_at=datetime(2026, 9, 25, tzinfo=UTC),
            format="api",
            extraction_method="json:DATOS_TABLA:Nombre",
            raw_value_span=f'"Nombre":"{nombre}"',
            serie_codigo="EPA000000",
            serie_nombre=nombre,
            periodo=Periodo(1900),
            valor=None,
            rol=Rol.METHODOLOGY,
            version=f"tabla {self.tabla}",
            etiqueta="metodologia",
        )


def serie_trimestral(valores: dict[str, float | None]) -> dict[Periodo, float | None]:
    return {Periodo.parse(k): v for k, v in valores.items()}
