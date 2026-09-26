"""Del JSON crudo de Tempus a series con el span literal de cada valor.

El INE devuelve una lista de series:
    {"COD":"EPA452436", "Nombre":"Tasa de paro ... Menores de 25 anos.", ...,
     "Data":[{"Fecha":"2026-04-01T00:00:00.000+02:00", "T3_TipoDato":"Definitivo",
              "T3_Periodo":"T2", "Anyo":2026, "Valor":23.77}, ...]}

`raw_value_span` es el objeto literal de cada dato tal como viene en el texto
(`{"Fecha":..., "Valor":23.77}`), no una reconstruccion: si el INE cambia el
numero, cambia el span y cambia el bundle_hash.

Se parsea con `json` (nunca eval) y se cruza el conteo de datos del parseo con
el de los fragmentos literales: si no cuadran, la extraccion falla en vez de
devolver numeros sin span.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from veritai.domain.periodo import Periodo

_COD = re.compile(r'"COD"\s*:\s*"([^"]+)"')
_DATO = re.compile(r'\{\s*"Fecha"[^{}]*\}')


class ExtraccionError(Exception):
    pass


@dataclass(frozen=True)
class DatoINE:
    periodo: Periodo
    valor: float | None
    span: str
    tipo_dato: str = ""


@dataclass
class SerieINE:
    codigo: str
    nombre: str
    unidad: str = ""
    datos: list[DatoINE] = field(default_factory=list)

    def valor_en(self, periodo: Periodo) -> DatoINE | None:
        return next((d for d in self.datos if d.periodo == periodo), None)


def _a_float(v: object) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, int | float):
        return float(v)
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def extraer_series(texto: str) -> list[SerieINE]:
    try:
        parseado = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ExtraccionError(f"JSON invalido: {exc.msg}") from exc
    if not isinstance(parseado, list):
        raise ExtraccionError("se esperaba una lista de series")

    # Segmentos literales por serie: de cada "COD" hasta el siguiente.
    posiciones = [(m.start(), m.group(1)) for m in _COD.finditer(texto)]
    segmentos: dict[str, str] = {}
    for k, (inicio, cod) in enumerate(posiciones):
        fin = posiciones[k + 1][0] if k + 1 < len(posiciones) else len(texto)
        segmentos[cod] = texto[inicio:fin]
    if len(segmentos) != len(parseado):
        raise ExtraccionError(
            f"{len(parseado)} series parseadas, {len(segmentos)} segmentos literales"
        )

    series: list[SerieINE] = []
    for s in parseado:
        cod = str(s.get("COD", ""))
        fragmentos = _DATO.findall(segmentos.get(cod, ""))
        datos_json = s.get("Data") or []
        if len(fragmentos) != len(datos_json):
            raise ExtraccionError(
                f"serie {cod}: {len(datos_json)} datos parseados, {len(fragmentos)} spans"
            )
        serie = SerieINE(
            codigo=cod, nombre=str(s.get("Nombre", "")), unidad=str(s.get("T3_Unidad", "") or "")
        )
        for d, frag in zip(datos_json, fragmentos, strict=True):
            try:
                periodo = Periodo.desde_ine(int(d["Anyo"]), d.get("T3_Periodo"))
            except (KeyError, ValueError, TypeError) as exc:
                raise ExtraccionError(f"serie {cod}: periodo ilegible en {frag[:80]}") from exc
            serie.datos.append(
                DatoINE(
                    periodo=periodo,
                    valor=_a_float(d.get("Valor")),
                    span=frag,
                    tipo_dato=str(d.get("T3_TipoDato", "")),
                )
            )
        series.append(serie)
    return series
