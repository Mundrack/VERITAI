"""Conector INE: extractor con spans literales, cliente con allowlist y rechazos, proveedor."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from veritai.application.analizar_claim import ProveedorError
from veritai.domain.claim import MetricaEmisor, Referencia
from veritai.domain.enums import AbstainReason
from veritai.domain.periodo import Periodo
from veritai.infrastructure.ine.extractor import ExtraccionError, extraer_series
from veritai.infrastructure.ine.proveedor import ProveedorINE
from veritai.infrastructure.ine.tempus import ClienteTempus, PublicadorRechazaError, RespuestaTempus

FIXTURE = Path(__file__).parent / "fixtures" / "ine_65334_min.json"
NOMBRE = "Tasa de paro de la población. Ambos sexos. Total Nacional. Menores de 25 años. "
METRICA = MetricaEmisor(
    emisor="INE",
    tabla="65334",
    serie_nombre=NOMBRE,
    unidad="pct",
    referencia_principal=Referencia.ANTERIOR,
)


def test_extractor_conserva_el_span_literal() -> None:
    series = extraer_series(FIXTURE.read_text(encoding="utf-8"))
    assert [s.codigo for s in series] == ["EPA452434", "EPA452436"]
    juvenil = series[1]
    dato = juvenil.valor_en(Periodo.parse("2026-T2"))
    assert dato is not None and dato.valor == 23.77
    assert '"Valor":23.77' in dato.span and dato.span.startswith('{"Fecha"')
    assert juvenil.valor_en(Periodo.parse("2019-T1")) is None


def test_extractor_falla_ante_json_roto_o_spans_que_no_cuadran() -> None:
    with pytest.raises(ExtraccionError):
        extraer_series("[{no es json")
    with pytest.raises(ExtraccionError):
        extraer_series(
            (
                '[{"COD":"X", "Nombre":"n", "Data":[{"Anyo":2026, "Valor":1}, '
                '{"Anyo":2025, "Valor":2}]}]'
            ).replace('{"Anyo":2025', '{"Fecha":"f", "Anyo":2025')
        )


class _ClienteFijo:
    """Doble de ClienteTempus que devuelve el fixture sin tocar la red."""

    def __init__(self, texto: str) -> None:
        self.texto = texto
        self.peticiones: list[tuple[str, int]] = []

    def datos_tabla(self, tabla: str, nult: int) -> RespuestaTempus:
        self.peticiones.append((tabla, nult))
        return RespuestaTempus(
            url=f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla}?nult={nult}&tip=A",
            texto=self.texto,
            retrieved_at=datetime(2026, 9, 25, tzinfo=UTC),
            estado=200,
        )


def test_proveedor_selecciona_por_nombre_exacto() -> None:
    cliente = _ClienteFijo(FIXTURE.read_text(encoding="utf-8"))
    prov = ProveedorINE(cliente, hoy=Periodo.parse("2026-T3"))  # type: ignore[arg-type]
    assert prov.series_coincidentes(METRICA) == 1
    assert prov.series_coincidentes(MetricaEmisor("INE", "65334", "Tasa de paro", "pct")) == 0
    item = prov.obtener_valor(METRICA, Periodo.parse("2026-T2"), "objetivo")
    assert item is not None and item.valor == 23.77 and item.serie_codigo == "EPA452436"
    assert item.version == "tabla 65334" and item.source_tier == 1 and item.format == "api"
    assert prov.obtener_valor(METRICA, Periodo.parse("2020-T1"), "x") is None
    refs = dict(prov.referencias_emisor(METRICA, Periodo.parse("2026-T2")))
    assert refs[Referencia.ANTERIOR] == Periodo.parse("2026-T1")
    assert refs[Referencia.INTERANUAL] == Periodo.parse("2025-T2")
    assert [str(i.periodo) for i in prov.ventana(METRICA, Periodo.parse("2026-T2"), 4)] == [
        "2026-T1",
        "2025-T4",
    ]
    assert prov.metodologia(METRICA) is not None
    # una sola descarga por tabla
    assert len(cliente.peticiones) == 1


def test_proveedor_calcula_nult_para_cubrir_la_base() -> None:
    cliente = _ClienteFijo(FIXTURE.read_text(encoding="utf-8"))
    prov = ProveedorINE(cliente, hoy=Periodo.parse("2026-M09"))  # type: ignore[arg-type]
    m = MetricaEmisor("INE", "25333", NOMBRE, "pct")
    prov.preparar(m, Periodo.parse("2018-M05"))
    prov.series_coincidentes(m)
    assert cliente.peticiones[-1][1] >= 100  # mayo 2018 -> septiembre 2026 son 100 meses


def test_proveedor_rechaza_otro_emisor() -> None:
    prov = ProveedorINE(_ClienteFijo("[]"))  # type: ignore[arg-type]
    with pytest.raises(ProveedorError):
        prov.series_coincidentes(MetricaEmisor("Eurostat", "1", "x", "pct"))


def test_cliente_valida_tabla_y_allowlist() -> None:
    with pytest.raises(ValueError):
        ClienteTempus(base_url="https://evil.example/wstempus/js/ES")
    cliente = ClienteTempus(
        cliente=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200)))
    )
    with pytest.raises(ValueError):
        cliente.url_datos_tabla("65334; drop", 3)
    assert cliente.url_datos_tabla("65334", 3).startswith(
        "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65334?"
    )


@pytest.mark.parametrize("codigo", [403, 406, 418])
def test_cliente_respeta_el_rechazo_del_publicador(codigo: int) -> None:
    transporte = httpx.MockTransport(lambda r: httpx.Response(codigo, text="no"))
    cliente = ClienteTempus(cliente=httpx.Client(transport=transporte))
    with pytest.raises(PublicadorRechazaError) as exc:
        cliente.datos_tabla("65334", 3)
    assert exc.value.motivo is AbstainReason.PRIMARY_SOURCE_NOT_FOUND


def test_cliente_corta_respuestas_demasiado_grandes() -> None:
    transporte = httpx.MockTransport(
        lambda r: httpx.Response(200, content=b"[" + b"x" * 20_000 + b"]")
    )
    cliente = ClienteTempus(max_bytes=10_000, cliente=httpx.Client(transport=transporte))
    with pytest.raises(Exception) as exc:
        cliente.datos_tabla("65334", 3)
    assert getattr(exc.value, "motivo", None) is AbstainReason.EXTRACTION_FAILED


def test_cliente_devuelve_texto_crudo_e_identifica_al_agente() -> None:
    visto: dict[str, str] = {}

    def handler(r: httpx.Request) -> httpx.Response:
        visto["ua"] = r.headers.get("user-agent", "")
        return httpx.Response(200, text=FIXTURE.read_text(encoding="utf-8"))

    cliente = ClienteTempus(cliente=httpx.Client(transport=httpx.MockTransport(handler)))
    resp = cliente.datos_tabla("65334", 3)
    assert resp.texto.startswith("[") and "EPA452436" in resp.texto
    assert visto["ua"].startswith("VERITAI-prototipo/")
