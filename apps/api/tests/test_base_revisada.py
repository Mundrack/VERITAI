"""Test 2b (base revisada) con bundles sinteticos: signo, magnitud, vigente que cuadra, sin edicion.

Los numeros son los de los casos B de la Puerta 3 (research/puerta3/casos), con
la edicion al publicar tal como la sirve el anexo del INE.
"""

from __future__ import annotations

from datetime import UTC, datetime

from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem, Rol
from veritai.domain.periodo import Periodo
from veritai.domain.tests.base_revisada import (
    ETIQUETA_AL_PUBLICAR,
    SUBTIPO_MAGNITUD,
    SUBTIPO_SIGNO,
    aplicar_2b,
    tasa_cuadra_con_vigente,
)

METRICA = MetricaEmisor(
    emisor="INE",
    tabla="2074",
    serie_nombre="Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato.",
    unidad="pernoctaciones",
    referencia_principal=Referencia.INTERANUAL,
)


def _item(
    etiqueta: str, periodo: str, valor: float, version: str = "tabla 2074", fecha: str | None = None
) -> EvidenceItem:
    return EvidenceItem(
        publisher="INE",
        url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074?nult=24&tip=A",
        source_tier=1,
        retrieved_at=datetime(2026, 9, 26, tzinfo=UTC),
        format="api" if fecha is None else "dataset",
        extraction_method="json:DATOS_TABLA:Valor" if fecha is None else "xlsx:EOH_Hoja3:x:5",
        raw_value_span=f'"Valor":{valor}' if fecha is None else f"[anexo] {valor}",
        serie_codigo="EOT22193" if fecha is None else "CTH0725:EOH_Hoja3",
        serie_nombre=METRICA.serie_nombre,
        periodo=Periodo.parse(periodo),
        valor=valor,
        rol=Rol.PRIMARY if etiqueta == "objetivo" else Rol.HISTORICAL,
        version=version,
        document_date=fecha,
        etiqueta=etiqueta,
    )


def _bundle(objetivo: float, base_vigente: float, base_al_publicar: float | None) -> EvidenceBundle:
    b = EvidenceBundle(claim_id="T")
    b.primary_items.append(_item("objetivo", "2026-M07", objetivo))
    b.historical_items.append(_item("base_claim", "2025-M07", base_vigente))
    if base_al_publicar is not None:
        b.historical_items.append(
            _item(ETIQUETA_AL_PUBLICAR, "2025-M07", base_al_publicar, "nota CTH0725", "2025-08-22")
        )
    return b


def _claim(cambio: float | None, direccion: Direccion = Direccion.SUBE) -> ClaimEstructurado:
    return ClaimEstructurado(
        claim_id="T",
        texto="t",
        fuente_url="https://x.test/",
        conjunto="desarrollo",
        tipo=TipoClaim.CAMBIO_ENTRE_PERIODOS,
        metrica=METRICA,
        periodo_objetivo=Periodo.parse("2026-M07"),
        periodo_base=Periodo.parse("2025-M07"),
        valor_objetivo=None,
        cambio_afirmado=cambio,
        unidad_cambio=UnidadCambio.PORCENTAJE,
        direccion_afirmada=direccion,
    )


def test_dispara_con_cambio_de_signo_baleares_residentes() -> None:
    # E043: +3,8% publicado (base provisional 740.149) frente a -2,3% vigente (786.273)
    r = aplicar_2b(_claim(3.8), _bundle(768195, 786273, 740149))
    assert r.aplicable and r.disparo
    assert r.subtipo == SUBTIPO_SIGNO
    assert r.calculos["edicion_al_publicar"] == "nota CTH0725"
    assert r.calculos["fecha_publicacion"] == "2025-08-22"
    assert r.calculos["tasa_con_base_vigente"] == -2.299
    assert r.calculos["tasa_con_base_al_publicar"] == 3.789
    assert "cambia el signo" in r.motivo


def test_dispara_por_magnitud_murcia() -> None:
    # E056: +4,09% publicado (394.572) frente a +3,32% vigente (397.508)
    r = aplicar_2b(_claim(4.09), _bundle(410706, 397508, 394572))
    assert r.disparo and r.subtipo == SUBTIPO_MAGNITUD
    assert r.calculos["revision_absoluta"] == 2936.0


def test_no_dispara_si_la_vigente_reproduce_la_tasa() -> None:
    # E035: Canarias +2,39% con la base vigente 6.622.855
    r = aplicar_2b(_claim(2.39), _bundle(6781369, 6622855, 6552626))
    assert r.aplicable and not r.disparo
    assert "edicion vigente" in r.motivo
    assert tasa_cuadra_con_vigente(_claim(2.39), _bundle(6781369, 6622855, None)) is True


def test_no_aplicable_sin_edicion_al_publicar() -> None:
    r = aplicar_2b(_claim(3.8), _bundle(768195, 786273, None))
    assert not r.aplicable and not r.disparo
    assert "no hay edicion al publicar" in r.motivo
    assert tasa_cuadra_con_vigente(_claim(3.8), _bundle(768195, 786273, None)) is False


def test_no_dispara_si_ninguna_edicion_reproduce_la_tasa() -> None:
    # E050: +15,9% afirmado; vigente -0,55%, provisional -0,75% -> el numero es el error
    r = aplicar_2b(_claim(15.9), _bundle(533954, 536919, 538001))
    assert r.aplicable and not r.disparo
    assert "ni con la edicion vigente" in r.motivo and "ni con la edicion al publicar" in r.motivo


def test_no_aplicable_sin_tasa_afirmada_ni_fuera_de_tipo() -> None:
    assert not aplicar_2b(_claim(None), _bundle(1, 1, 1)).aplicable
    nivel = ClaimEstructurado(
        claim_id="N",
        texto="n",
        fuente_url="https://x.test/",
        conjunto="desarrollo",
        tipo=TipoClaim.NIVEL,
        metrica=METRICA,
        periodo_objetivo=Periodo.parse("2026-M07"),
        valor_objetivo=1.0,
    )
    assert not aplicar_2b(nivel, _bundle(1, 1, 1)).aplicable
    assert tasa_cuadra_con_vigente(nivel, _bundle(1, 1, 1)) is None
