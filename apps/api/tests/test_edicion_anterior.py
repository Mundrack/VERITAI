"""Conector de edicion anterior: codigo de nota, mapa cerrado, extraccion y seguridad. Sin red.

Las filas completas de los anexos vienen de las descargas de la Puerta 3
(tests/fixtures/d2b/filas_absolutas.json; sha256 de cada anexo en
research/evidencia/D2B_*.json): el test comprueba que el mapa apunta a la
columna absoluta que da el valor publicado.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import openpyxl
import pytest

from veritai.domain.claim import MetricaEmisor
from veritai.domain.periodo import Periodo
from veritai.infrastructure.ine.edicion_anterior import (
    DescargaError,
    EdicionAnteriorINE,
    PublicadorRechazaError,
    codigo_nota,
    extraer_celda,
    fecha_publicacion,
)
from veritai.infrastructure.ine.mapa_anexos import (
    OPERACIONES,
    Celda,
    localizar,
    normalizar_etiqueta,
    operacion_de,
)

FIXTURE = Path(__file__).parent / "fixtures" / "d2b" / "filas_absolutas.json"
FILAS = json.loads(FIXTURE.read_text(encoding="utf-8"))["filas"]


def _fila(codigo: str, hoja: str, etiqueta: str) -> list:
    return FILAS[codigo][hoja][etiqueta]


def _xlsx(hojas: dict[str, list[list]]) -> bytes:
    libro = openpyxl.Workbook()
    libro.remove(libro.active)
    for nombre, filas in hojas.items():
        ws = libro.create_sheet(nombre)
        for fila in filas:
            ws.append(fila)
    buf = io.BytesIO()
    libro.save(buf)
    return buf.getvalue()


# --- codigo de nota y fecha ---------------------------------------------------------


def test_codigo_nota_mensual_y_trimestral() -> None:
    assert codigo_nota("CTH", Periodo.parse("2025-M07")) == "CTH0725"
    assert codigo_nota("ETDP", Periodo.parse("2025-M07")) == "ETDP0725"
    assert codigo_nota("IPV", Periodo.parse("2026-T2")) == "IPV2T26"
    with pytest.raises(ValueError):
        codigo_nota("CTH", Periodo.parse("2025"))


def test_fecha_publicacion_se_lee_de_la_nota() -> None:
    html = b"<p>Notas de prensa y comunicados publicados 22 de agosto de 2025</p>"
    assert fecha_publicacion(html) == "2025-08-22"
    assert fecha_publicacion(b"<p>sin fecha</p>") is None


# --- mapa cerrado -------------------------------------------------------------------


def test_el_mapa_cubre_ocho_operaciones_y_se_cierra_ahi() -> None:
    assert len(OPERACIONES) == 8
    assert {op.codigo for op in OPERACIONES} == {
        "CTH",
        "EOAT",
        "ETDP",
        "H",
        "SM",
        "IPI",
        "FRONTUR",
        "EGATUR",
    }
    assert operacion_de("99999") is None  # fuera del mapa: fallo de cobertura, no se maquilla
    assert localizar("99999", "Lo que sea. Pernoctaciones. Total.") is None
    sin_tasa = {op.codigo for op in OPERACIONES if not op.tasa_por_ccaa}
    assert sin_tasa == {"CTH", "EOAT"}  # donde el redactor tiene que calcular la tasa


def test_normalizar_etiqueta() -> None:
    assert normalizar_etiqueta("Madrid (Comunidad de)") == "Madrid, Comunidad de"
    assert normalizar_etiqueta("Balears (Illes)") == "Balears, Illes"
    assert normalizar_etiqueta("Balears, Illes") == "Balears, Illes"
    assert normalizar_etiqueta("Castilla - La Mancha") == "Castilla-La Mancha"
    assert normalizar_etiqueta("Total Nacional") == "TOTAL"
    assert normalizar_etiqueta("Nacional", nacional="Nacional") == "Nacional"


BAL_RES = "Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato. "
BAL_TOT = "Balears, Illes. Pernoctaciones. Total categorías. Total. Dato. "
SM_NAC = "Sociedades Constituídas. Número de Sociedades. Total Nacional. Mercantiles."


@pytest.mark.parametrize(
    ("tabla", "serie", "esperado"),
    [
        (
            "2074",
            "Madrid (Comunidad de). Pernoctaciones. Total.",
            Celda("EOH_Hoja3", "Madrid, Comunidad de", 9),
        ),
        ("2074", BAL_RES, Celda("EOH_Hoja3", "Balears, Illes", 11)),
        (
            "2074",
            "Galicia. Viajeros. Residentes en el extranjero.",
            Celda("EOH_Hoja3", "Galicia", 7),
        ),
        (
            "36570",
            "Nacional. Pernoctaciones. Total categorías. Total.",
            Celda("EOH_Hoja3", "TOTAL", 9),
        ),
        ("1993", "Andalucía. Pernoctaciones. Total.", Celda("EOAP_Hoja1", "Andalucía", 8)),
        (
            "2016",
            "Madrid (Comunidad de). Viajeros. Total.",
            Celda("EOAC_Hoja1", "Madrid, Comunidad de", 2),
        ),
        ("6150", "Total Nacional. General. Compraventa. Número. ", Celda("Hoja9", "TOTAL", 8)),
        ("6150", "País Vasco. General. Compraventa. Número. ", Celda("Hoja9", "País Vasco", 8)),
        (
            "6150",
            "Total Nacional. Vivienda segunda mano. Compraventa. Número. ",
            Celda("Hoja3", "TOTAL", 10),
        ),
        (
            "76316",
            "Viviendas. Número de hipotecas. Total Nacional. Base nueva. Mensual. ",
            Celda("Hoja6", "TOTAL", 6),
        ),
        (
            "76316",
            "Total fincas. Andalucía. Número de hipotecas. Base nueva. Mensual. ",
            Celda("Hoja1", "Andalucía", 2),
        ),
        ("13913", SM_NAC, Celda("Hoja 1", "TOTAL", 2)),
        (
            "13913",
            "Galicia. Sociedades Constituídas. Mercantiles. Número de Sociedades. ",
            Celda("Hoja 1", "Galicia", 2),
        ),
        ("60272", "Total Nacional. Total industria. Índice. ", Celda("Tabla 5", "Nacional", 3)),
        ("60272", "Andalucía. Total industria. Índice. ", Celda("Tabla 5", "Andalucía", 3)),
        ("75722", "Total. Total Nacional. Dato base. ", Celda("Hoja1", "TOTAL", 2)),
        (
            "75715",
            "Total. Turista. Gasto total. Total Nacional. Dato base. ",
            Celda("Gasto partidas", "TOTAL", 2),
        ),
    ],
)
def test_localizar_serie_en_el_anexo(tabla: str, serie: str, esperado: Celda) -> None:
    assert localizar(tabla, serie) == esperado


def test_series_que_no_son_el_dato_quedan_fuera() -> None:
    assert localizar("60272", "Total Nacional. Total industria. Variación anual. ") is None
    assert localizar("75722", "Total. Total Nacional. Tasa de variación anual. ") is None
    assert (
        localizar("76316", "Total fincas. Andalucía. Importe de hipotecas. Base nueva. Mensual. ")
        is None
    )
    assert localizar("13913", "Andalucía. Sociedades Constituídas. Mercantiles. Capital. ") is None


# --- el mapa apunta a la columna del valor publicado (filas reales de la Puerta 3) --------


@pytest.mark.parametrize(
    ("codigo", "tabla", "serie", "esperado"),
    [
        ("CTH0725", "2074", BAL_TOT, 10987630),
        ("CTH0725", "2074", BAL_RES, 740149),
        ("CTH0725", "2074", "Galicia. Pernoctaciones. Total.", 1325548),
        ("CTH0825", "2074", "Madrid (Comunidad de). Pernoctaciones. Total.", 2115059),
        (
            "CTH0825",
            "2074",
            "Madrid (Comunidad de). Viajeros. Residentes en el extranjero.",
            589025,
        ),
        ("CTH0825", "2074", "Castilla y León. Pernoctaciones. Total.", 1051890),
        ("EOAT0725", "1993", "Andalucía. Pernoctaciones. Total.", 1382026),
        ("EOAT0725", "2016", "Andalucía. Pernoctaciones. Total.", 915262),
        ("ETDP0725", "6150", "Total Nacional. General. Compraventa. Número. ", 64730),
        ("ETDP0725", "6150", "Navarra (Comunidad Foral de). General. Compraventa. Número. ", 516),
        ("ETDP0725", "6150", "Total Nacional. Vivienda segunda mano. Compraventa. Número. ", 51090),
        (
            "H0625",
            "76316",
            "Viviendas. Número de hipotecas. Total Nacional. Base nueva. Mensual. ",
            41834,
        ),
        (
            "H0625",
            "76316",
            "Total fincas. Andalucía. Número de hipotecas. Base nueva. Mensual. ",
            10199,
        ),
        ("SM0725", "13913", SM_NAC, 10902),
        (
            "SM0725",
            "13913",
            "Andalucía. Sociedades Constituídas. Mercantiles. Número de Sociedades. ",
            1769,
        ),
        ("IPI0725", "60272", "Total Nacional. Total industria. Índice. ", 110.1),
        ("IPI0725", "60272", "Andalucía. Total industria. Índice. ", 118.8),
        ("FRONTUR0725", "75722", "Total. Total Nacional. Dato base. ", 16250218),
        ("EGATUR0725", "75715", "Total. Turista. Gasto total. Total Nacional. Dato base. ", 16452),
    ],
)
def test_columna_del_mapa_da_el_valor_publicado(
    codigo: str, tabla: str, serie: str, esperado: float
) -> None:
    celda = localizar(tabla, serie)
    assert celda is not None
    fila = _fila(codigo, celda.hoja, celda.etiqueta_fila)
    assert fila[celda.columna] == esperado


# --- extraccion y seguridad -----------------------------------------------------------

FILA_BALEARS = _fila("CTH0725", "EOH_Hoja3", "Balears, Illes")
FILA_TOTAL = _fila("CTH0725", "EOH_Hoja3", "TOTAL")
HOJAS = {"EOH_Hoja3": [["4. Viajeros, pernoctaciones y estancia media"], FILA_TOTAL, FILA_BALEARS]}


def test_extraer_celda_valida_los_bytes_magicos() -> None:
    with pytest.raises(DescargaError):
        extraer_celda(b"<html>no soy un xlsx</html>", Celda("EOH_Hoja3", "Balears, Illes", 9))


def test_extraer_celda_devuelve_valor_y_fila() -> None:
    valor, fila = extraer_celda(_xlsx(HOJAS), Celda("EOH_Hoja3", "Balears, Illes", 11))
    assert valor == 740149
    assert fila[0] == "Balears, Illes"
    assert extraer_celda(_xlsx(HOJAS), Celda("EOH_Hoja3", "Canarias", 9)) is None
    assert extraer_celda(_xlsx(HOJAS), Celda("Otra", "Balears, Illes", 9)) is None
    # la hoja se encuentra aunque el INE le deje un espacio al final ('Hoja1 ' en H0625)
    fila_h = _fila("H0625", "Hoja1", "TOTAL")
    valor_h, _ = extraer_celda(_xlsx({"Hoja1 ": [fila_h]}), Celda("Hoja1", "TOTAL", 2))
    assert valor_h == 53438


def _conector(respuestas: dict[str, tuple[int, bytes]]) -> EdicionAnteriorINE:
    llamadas: list[str] = []

    def descargar(url: str) -> tuple[int, bytes]:
        llamadas.append(url)
        return respuestas.get(url, (404, b""))

    conector = EdicionAnteriorINE(descargar=descargar)
    conector.llamadas = llamadas  # type: ignore[attr-defined]
    return conector


METRICA = MetricaEmisor(emisor="INE", tabla="2074", serie_nombre=BAL_RES, unidad="pernoctaciones")
URL_XLSX = "https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx"
URL_HTML = "https://www.ine.es/dyngs/Prensa/CTH0725.htm"


def test_obtener_devuelve_el_item_con_fecha_y_span() -> None:
    conector = _conector(
        {
            URL_XLSX: (200, _xlsx(HOJAS)),
            URL_HTML: (200, b"comunicados publicados 22 de agosto de 2025"),
        }
    )
    assert conector.disponible(METRICA)
    item = conector.obtener(METRICA, Periodo.parse("2025-M07"))
    assert item is not None
    assert item.valor == 740149
    assert item.document_date == "2025-08-22"
    assert item.version == "nota CTH0725"
    assert item.etiqueta == "base_al_publicar"
    assert item.serie_codigo == "CTH0725:EOH_Hoja3"
    assert "740149" in item.raw_value_span and "CTH0725.xlsx" in item.raw_value_span
    assert item.url == URL_XLSX
    # segunda llamada: cache, sin nueva descarga
    conector.obtener(METRICA, Periodo.parse("2025-M07"))
    assert conector.llamadas.count(URL_XLSX) == 1  # type: ignore[attr-defined]


def test_sin_anexo_o_sin_fila_devuelve_none_nunca_inventa() -> None:
    assert _conector({}).obtener(METRICA, Periodo.parse("2025-M07")) is None
    sin_fila = _conector({URL_XLSX: (200, _xlsx({"EOH_Hoja3": [FILA_TOTAL]}))})
    assert sin_fila.obtener(METRICA, Periodo.parse("2025-M07")) is None


def test_rechazo_del_publicador_cierra_el_caso() -> None:
    with pytest.raises(PublicadorRechazaError):
        _conector({URL_XLSX: (403, b"")}).obtener(METRICA, Periodo.parse("2025-M07"))


def test_fuera_del_mapa_no_esta_disponible() -> None:
    conector = _conector({})
    fuera = MetricaEmisor("INE", "99999", "Algo. Pernoctaciones. Total.", "u")
    assert not conector.disponible(fuera)
    assert not conector.disponible(
        MetricaEmisor("SEPE", "2074", "Algo. Pernoctaciones. Total.", "u")
    )
    assert conector.obtener(fuera, Periodo.parse("2025-M07")) is None
