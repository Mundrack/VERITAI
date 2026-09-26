"""ProveedorINE: implementa el puerto ProveedorEvidencia sobre Tempus.

Una tabla se descarga una vez por analisis (cache en memoria por instancia);
`nult` se calcula para cubrir el periodo mas antiguo que el claim necesita.
La serie se elige por su campo `Nombre` EXACTO: si casan cero o varias, el
dominio abstiene (PRIMARY_SOURCE_NOT_FOUND / SOURCE_VERSION_AMBIGUOUS) en vez
de elegir a ciegas. Lo aprendido en la TAREA 2 (C11): un filtro por codigo
devolvio otra comunidad autonoma; el nombre completo no engana.
"""

from __future__ import annotations

from datetime import UTC, datetime

from veritai.application.analizar_claim import ProveedorError
from veritai.domain.claim import MetricaEmisor, Referencia
from veritai.domain.enums import AbstainReason
from veritai.domain.evidencia import EvidenceItem, Rol
from veritai.domain.periodo import Periodo
from veritai.infrastructure.ine.extractor import ExtraccionError, SerieINE, extraer_series
from veritai.infrastructure.ine.tempus import ClienteTempus, RespuestaTempus, TempusError

PUBLISHER = "INE"
NULT_MINIMO = 24


def _norm(nombre: str) -> str:
    return " ".join(nombre.split()).strip().rstrip(".").lower()


class ProveedorINE:
    def __init__(self, cliente: ClienteTempus, hoy: Periodo | None = None) -> None:
        self.cliente = cliente
        self._cache: dict[str, tuple[RespuestaTempus, list[SerieINE]]] = {}
        self._hoy = hoy
        self._periodo_mas_antiguo: dict[str, Periodo] = {}

    # --- cobertura temporal -------------------------------------------------
    def preparar(self, metrica: MetricaEmisor, periodo_mas_antiguo: Periodo) -> None:
        """Dice al proveedor hasta donde atras hay que pedir antes de la primera llamada."""
        actual = self._periodo_mas_antiguo.get(metrica.tabla)
        if actual is None or periodo_mas_antiguo < actual:
            self._periodo_mas_antiguo[metrica.tabla] = periodo_mas_antiguo
            self._cache.pop(metrica.tabla, None)

    def _nult(self, tabla: str) -> int:
        antiguo = self._periodo_mas_antiguo.get(tabla)
        if antiguo is None:
            return NULT_MINIMO
        hoy = self._hoy or Periodo(
            datetime.now(UTC).year, antiguo.frecuencia, 1 if antiguo.frecuencia != "A" else 0
        )
        por_anio = {"M": 12, "T": 4, "A": 1}[antiguo.frecuencia]
        distancia = (hoy.anio - antiguo.anio) * por_anio + (hoy.indice - antiguo.indice)
        return max(NULT_MINIMO, distancia + por_anio + 2)

    # --- descarga -------------------------------------------------------------
    def _tabla(self, metrica: MetricaEmisor) -> tuple[RespuestaTempus, list[SerieINE]]:
        if metrica.emisor != PUBLISHER:
            raise ProveedorError(
                f"este proveedor solo sirve {PUBLISHER}, no {metrica.emisor}",
                AbstainReason.PRIMARY_SOURCE_NOT_FOUND,
            )
        if metrica.tabla not in self._cache:
            try:
                respuesta = self.cliente.datos_tabla(metrica.tabla, self._nult(metrica.tabla))
                series = extraer_series(respuesta.texto)
            except TempusError as exc:
                raise ProveedorError(str(exc), exc.motivo) from exc
            except ExtraccionError as exc:
                raise ProveedorError(str(exc), AbstainReason.EXTRACTION_FAILED) from exc
            self._cache[metrica.tabla] = (respuesta, series)
        return self._cache[metrica.tabla]

    def _serie(self, metrica: MetricaEmisor) -> SerieINE | None:
        _, series = self._tabla(metrica)
        objetivo = _norm(metrica.serie_nombre)
        coincidentes = [s for s in series if _norm(s.nombre) == objetivo]
        return coincidentes[0] if len(coincidentes) == 1 else None

    # --- puerto ---------------------------------------------------------------
    def series_coincidentes(self, metrica: MetricaEmisor) -> int:
        _, series = self._tabla(metrica)
        objetivo = _norm(metrica.serie_nombre)
        return sum(1 for s in series if _norm(s.nombre) == objetivo)

    def obtener_valor(
        self, metrica: MetricaEmisor, periodo: Periodo, etiqueta: str
    ) -> EvidenceItem | None:
        serie = self._serie(metrica)
        if serie is None:
            return None
        dato = serie.valor_en(periodo)
        if dato is None:
            return None
        respuesta, _ = self._tabla(metrica)
        return EvidenceItem(
            publisher=PUBLISHER,
            url=respuesta.url,
            source_tier=1,
            retrieved_at=respuesta.retrieved_at,
            format="api",
            extraction_method="json:DATOS_TABLA:Valor",
            raw_value_span=dato.span,
            serie_codigo=serie.codigo,
            serie_nombre=serie.nombre,
            periodo=periodo,
            valor=dato.valor,
            rol=Rol.PRIMARY if etiqueta == "objetivo" else Rol.HISTORICAL,
            version=f"tabla {metrica.tabla}",
            document_date=None,
            etiqueta=etiqueta,
        )

    def referencias_emisor(
        self, metrica: MetricaEmisor, periodo: Periodo
    ) -> list[tuple[Referencia, Periodo]]:
        if periodo.frecuencia == "A":
            return [(Referencia.ANTERIOR, periodo.anterior())]
        return [
            (Referencia.ANTERIOR, periodo.anterior()),
            (Referencia.INTERANUAL, periodo.interanual()),
        ]

    def ventana(self, metrica: MetricaEmisor, periodo: Periodo, n: int) -> list[EvidenceItem]:
        items: list[EvidenceItem] = []
        p = periodo
        for _ in range(n):
            p = p.anterior()
            item = self.obtener_valor(metrica, p, f"ventana:{p}")
            if item is not None:
                items.append(item)
        return items

    def metodologia(self, metrica: MetricaEmisor) -> EvidenceItem | None:
        serie = self._serie(metrica)
        if serie is None:
            return None
        respuesta, _ = self._tabla(metrica)
        return EvidenceItem(
            publisher=PUBLISHER,
            url=f"https://www.ine.es/jaxiT3/Tabla.htm?t={metrica.tabla}",
            source_tier=1,
            retrieved_at=respuesta.retrieved_at,
            format="api",
            extraction_method="json:DATOS_TABLA:Nombre",
            raw_value_span=f'"COD":"{serie.codigo}", "Nombre":"{serie.nombre}"',
            serie_codigo=serie.codigo,
            serie_nombre=serie.nombre,
            periodo=Periodo(1900),
            valor=None,
            rol=Rol.METHODOLOGY,
            version=f"tabla {metrica.tabla}",
            etiqueta="metodologia",
        )
