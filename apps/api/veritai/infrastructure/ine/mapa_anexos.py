"""Mapa cerrado de anexos del INE para el conector de edicion anterior (DEC-034).

El alcance del conector son estas OCHO operaciones y se cierra aqui
(docs/PROPUESTA-2B.md §4.4). No se anade ninguna durante la evaluacion: un 2b
fuera del mapa cuenta como fallo de cobertura (PREVIOUS_EDITION_OUT_OF_MAP) y
no se maquilla.

Una entrada por operacion: el prefijo del codigo de la nota (<PREFIJO><MM><YY>),
las tablas Tempus que cubre y un localizador que, dado el nombre EXACTO de la
serie Tempus, dice en que hoja del anexo, en que fila (etiqueta) y en que
columna esta el mismo dato. La columna es el indice ABSOLUTO en la hoja
(0 = columna A): las filas de los anexos traen celdas vacias intercaladas y,
en alguna, ceros sueltos (ETDP0725, fila TOTAL), asi que contar solo las
celdas no vacias no es estable; la posicion absoluta si lo fue en todas las
ediciones comparadas (2025 y 2026). Las filas completas de referencia estan en
tests/fixtures/d2b/filas_absolutas.json, sacadas de los anexos descargados en
la Puerta 3 (sha256 en research/evidencia/D2B_*.json).

`tasa_por_ccaa`: si el anexo (o la nota) ya publica la tasa de variacion por
comunidad. Donde la trae hecha, el redactor no tiene que calcularla y 2b no
aparecio; donde no, la calcula cada redaccion contra su propia base
(diseno de la Puerta 3 §4d). Es el limite declarado del fenomeno.

Verificacion, por operacion, contra los anexos descargados:
    CTH      CTH0725/0825/0826: EOH_Hoja3, CCAA y provincias         verificada (7 casos B)
    EOAT     EOAT0625/0626/0725: EOAP_Hoja1, EOAC_Hoja1                 verificada (E049, E054)
    ETDP     ETDP0725/0726: Hoja9 (ETDP.11) y Hoja3 (ETDP.5)             verificada (TOTAL y CCAA)
    H        H0625: Hoja6 (H.9) viviendas, Hoja1 (H.1) total fincas      verificada (TOTAL y CCAA)
    SM       SM0725: 'Hoja 1' (SM.1)                                     verificada (TOTAL y CCAA)
    IPI      IPI0725: 'Tabla 5' indices originales                       verificada (Nacional, CCAA)
    FRONTUR  FRONTUR0725: Hoja1, TOTAL (mensual y acumulado)             verificada (TOTAL)
    EGATUR   EGATUR0725: 'Gasto partidas' y 'Datos acumulados', TOTAL    verificada (TOTAL)
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

NACIONAL = "TOTAL"

_PARENTESIS = re.compile(r"^(?P<a>.+?) \((?P<b>.+)\)$")


def normalizar_etiqueta(entidad: str, nacional: str = NACIONAL) -> str:
    """Del nombre de entidad en Tempus a la etiqueta de fila del anexo.

    'Madrid (Comunidad de)' -> 'Madrid, Comunidad de'; 'Castilla - La Mancha' ->
    'Castilla-La Mancha'; 'Total Nacional' / 'Nacional' / 'Total' -> nacional.
    """
    e = " ".join(entidad.split()).strip().rstrip(".")
    if e.lower() in {"total nacional", "nacional", "total", "españa"}:
        return nacional
    m = _PARENTESIS.match(e)
    if m:
        e = f"{m.group('a')}, {m.group('b')}"
    return e.replace(" - ", "-")


def _segmentos(nombre: str) -> list[str]:
    return [s.strip() for s in nombre.split(".") if s.strip()]


@dataclass(frozen=True)
class Celda:
    hoja: str  # nombre de la hoja (se compara sin espacios sobrantes)
    etiqueta_fila: str
    columna: int  # indice absoluto de columna en la hoja (0 = A)
    ocurrencia: int = 1  # si la etiqueta se repite en la hoja, cual (1 = la primera)


Localizador = Callable[[str], "Celda | None"]


@dataclass(frozen=True)
class Operacion:
    codigo: str  # prefijo del codigo de la nota
    nombre: str
    tablas: frozenset[str]
    localizar: Localizador
    tasa_por_ccaa: bool
    periodicidad: str = "M"


# --- localizadores, uno por operacion -------------------------------------------


def _residencia(segs: list[str]) -> int:
    texto = " ".join(segs).lower()
    if "residentes en españa" in texto or "residentes en espana" in texto:
        return 1
    if "extranjero" in texto:
        return 2
    return 0


def _viajeros_pernoctaciones(hoja: str, col_viajeros: int, col_pernoctaciones: int) -> Localizador:
    """Layout comun de EOH y EOAT: viajeros y pernoctaciones, cada uno total/res/ext en columnas
    alternas (una vacia entre medias)."""

    def localizar(nombre: str) -> Celda | None:
        segs = _segmentos(nombre)
        if len(segs) < 2:
            return None
        variable = segs[1].lower()
        if variable.startswith("viajero"):
            base = col_viajeros
        elif variable.startswith("pernoctaciones"):
            base = col_pernoctaciones
        else:
            return None
        return Celda(hoja, normalizar_etiqueta(segs[0]), base + 2 * _residencia(segs[2:]))

    return localizar


def _etdp(nombre: str) -> Celda | None:
    segs = _segmentos(nombre)
    if len(segs) < 4 or segs[2].lower() != "compraventa" or segs[3].lower() != "número":
        return None
    entidad = normalizar_etiqueta(segs[0])
    regimen = segs[1].lower()
    if regimen == "general":
        return Celda("Hoja9", entidad, 8)  # ETDP.11: compraventas de viviendas, numero
    columnas = {
        "vivienda libre": 4,
        "vivienda protegida": 6,
        "vivienda nueva": 8,
        "vivienda segunda mano": 10,
    }
    if regimen in columnas:
        return Celda("Hoja3", entidad, columnas[regimen])  # ETDP.5
    return None


_H_FINCAS = {
    "viviendas": ("Hoja6", 6),  # H.9 fincas urbanas segun naturaleza: viviendas, numero
    "total fincas": ("Hoja1", 2),  # H.1: total fincas, numero
    "fincas rústicas": ("Hoja1", 6),
    "fincas urbanas": ("Hoja1", 10),
}
_H_RESERVADAS = {
    "número de hipotecas",
    "importe de hipotecas",
    "base nueva",
    "mensual",
    *_H_FINCAS,
}


def _h(nombre: str) -> Celda | None:
    segs = _segmentos(nombre)
    bajos = [s.lower() for s in segs]
    if "número de hipotecas" not in bajos:
        return None
    finca = next((f for f in _H_FINCAS if f in bajos), None)
    entidad = next((s for s in segs if s.lower() not in _H_RESERVADAS), None)
    if finca is None or entidad is None:
        return None
    hoja, col = _H_FINCAS[finca]
    return Celda(hoja, normalizar_etiqueta(entidad), col)


_SM_RESERVADAS = {
    "sociedades constituídas",
    "sociedades constituidas",
    "mercantiles",
    "número de sociedades",
    "capital",
}


def _sm(nombre: str) -> Celda | None:
    segs = _segmentos(nombre)
    bajos = [s.lower() for s in segs]
    if "número de sociedades" not in bajos or "mercantiles" not in bajos:
        return None
    entidad = next((s for s in segs if s.lower() not in _SM_RESERVADAS), None)
    if entidad is None:
        return None
    return Celda("Hoja 1", normalizar_etiqueta(entidad), 2)  # SM.1: sociedades creadas, numero


def _ipi(nombre: str) -> Celda | None:
    segs = _segmentos(nombre)
    if len(segs) < 3 or segs[1].lower() != "total industria" or segs[2].lower() != "índice":
        return None
    return Celda("Tabla 5", normalizar_etiqueta(segs[0], nacional="Nacional"), 3)


def _frontur(nombre: str) -> Celda | None:
    segs = [s.lower() for s in _segmentos(nombre)]
    if segs[:2] != ["total", "total nacional"] or len(segs) < 3:
        return None
    if segs[2] == "dato base":
        return Celda("Hoja1", NACIONAL, 2)
    if segs[2].startswith("acumulado"):
        return Celda("Hoja1", NACIONAL, 6)
    return None


def _egatur(nombre: str) -> Celda | None:
    segs = [s.lower() for s in _segmentos(nombre)]
    if segs[:4] != ["total", "turista", "gasto total", "total nacional"] or len(segs) < 5:
        return None
    if segs[4] == "dato base":
        return Celda("Gasto partidas", NACIONAL, 2)
    if segs[4].startswith("acumulado"):
        return Celda("Datos acumulados", NACIONAL, 2)
    return None


# --- el mapa, cerrado en ocho operaciones ------------------------------------------

OPERACIONES: tuple[Operacion, ...] = (
    Operacion(
        "CTH",
        "Coyuntura Turistica Hotelera (EOH)",
        frozenset({"2074", "36570"}),
        _viajeros_pernoctaciones("EOH_Hoja3", 3, 9),
        tasa_por_ccaa=False,
    ),
    Operacion(
        "EOAT",
        "Alojamientos turisticos extrahoteleros: apartamentos (EOAP) y campings (EOAC)",
        frozenset({"1993", "2016"}),
        lambda nombre: None,  # se resuelve por tabla, abajo
        tasa_por_ccaa=False,
    ),
    Operacion(
        "ETDP",
        "Transmisiones de derechos de la propiedad",
        frozenset({"6150"}),
        _etdp,
        tasa_por_ccaa=True,
    ),
    Operacion("H", "Hipotecas", frozenset({"76316"}), _h, tasa_por_ccaa=True),
    Operacion("SM", "Sociedades mercantiles", frozenset({"13913"}), _sm, tasa_por_ccaa=True),
    Operacion(
        "IPI", "Indice de produccion industrial", frozenset({"60272"}), _ipi, tasa_por_ccaa=True
    ),
    Operacion(
        "FRONTUR", "Llegadas de turistas", frozenset({"75722"}), _frontur, tasa_por_ccaa=True
    ),
    Operacion("EGATUR", "Gasto turistico", frozenset({"75715"}), _egatur, tasa_por_ccaa=True),
)

_LOCALIZADOR_POR_TABLA: dict[str, Localizador] = {
    "1993": _viajeros_pernoctaciones("EOAP_Hoja1", 2, 8),
    "2016": _viajeros_pernoctaciones("EOAC_Hoja1", 2, 8),
}

POR_TABLA: dict[str, Operacion] = {t: op for op in OPERACIONES for t in op.tablas}


def operacion_de(tabla: str) -> Operacion | None:
    return POR_TABLA.get(tabla)


def localizar(tabla: str, serie_nombre: str) -> Celda | None:
    """Donde vive en el anexo la serie de la tabla Tempus `tabla`; None si esta fuera del mapa."""
    op = operacion_de(tabla)
    if op is None:
        return None
    loc = _LOCALIZADOR_POR_TABLA.get(tabla, op.localizar)
    return loc(serie_nombre)


__all__ = [
    "NACIONAL",
    "OPERACIONES",
    "POR_TABLA",
    "Celda",
    "Operacion",
    "localizar",
    "normalizar_etiqueta",
    "operacion_de",
]
