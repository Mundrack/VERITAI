"""Caso de uso con 2b: los siete B de la Puerta 3 disparan con sus fechas; abstencion y cobertura.

Sin red: Tempus es `ProveedorFalso` y la edicion anterior es un doble con el
valor del anexo. Los numeros son los de research/puerta3/casos/E031, E042,
E043, E047, E053, E055, E056 (edicion vigente y edicion al publicar).
"""

from __future__ import annotations

import re
from datetime import UTC, datetime

import pytest

from tests.dobles import ProveedorFalso
from veritai.application.analizar_claim import AnalizarClaim
from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.enums import AbstainReason, Clase, Context, Truth
from veritai.domain.evidencia import EvidenceItem, Rol
from veritai.domain.periodo import Periodo
from veritai.domain.tests.base_revisada import ETIQUETA_AL_PUBLICAR, SUBTIPO_MAGNITUD, SUBTIPO_SIGNO


class EdicionFalsa:
    """Doble del puerto ProveedorEdicionAnterior: {serie: {periodo: (valor, codigo, fecha)}}."""

    def __init__(self, ediciones: dict[str, dict[str, tuple[float, str, str]]], tablas=("2074",)):
        self.ediciones = ediciones
        self.tablas = set(tablas)

    def disponible(self, metrica: MetricaEmisor) -> bool:
        return metrica.emisor == "INE" and metrica.tabla in self.tablas

    def obtener(self, metrica: MetricaEmisor, periodo: Periodo) -> EvidenceItem | None:
        dato = self.ediciones.get(metrica.serie_nombre, {}).get(str(periodo))
        if dato is None:
            return None
        valor, codigo, fecha = dato
        return EvidenceItem(
            publisher="INE",
            url=f"https://www.ine.es/prensa/anexo_tablas/es/{codigo}.xlsx",
            source_tier=1,
            retrieved_at=datetime(2026, 9, 26, tzinfo=UTC),
            format="dataset",
            extraction_method="xlsx:EOH_Hoja3:fila:col",
            raw_value_span=f"[{codigo}.xlsx, hoja EOH_Hoja3] ['x', {valor}]",
            serie_codigo=f"{codigo}:EOH_Hoja3",
            serie_nombre=metrica.serie_nombre,
            periodo=periodo,
            valor=valor,
            rol=Rol.HISTORICAL,
            version=f"nota {codigo}",
            document_date=fecha,
            etiqueta=ETIQUETA_AL_PUBLICAR,
        )


def _mensual(valores: dict[str, float]) -> dict[Periodo, float]:
    return {Periodo.parse(k): v for k, v in valores.items()}


def _claim(
    serie: str,
    objetivo: str,
    base: str,
    cambio: float,
    valor_objetivo: float | None = None,
    tabla: str = "2074",
) -> ClaimEstructurado:
    return ClaimEstructurado(
        claim_id="B",
        texto="t",
        fuente_url="https://x.test/",
        conjunto="evaluacion",
        tipo=TipoClaim.CAMBIO_ENTRE_PERIODOS,
        metrica=MetricaEmisor("INE", tabla, serie, "pernoctaciones", Referencia.INTERANUAL),
        periodo_objetivo=Periodo.parse(objetivo),
        periodo_base=Periodo.parse(base),
        valor_objetivo=valor_objetivo,
        cambio_afirmado=cambio,
        unidad_cambio=UnidadCambio.PORCENTAJE,
        direccion_afirmada=Direccion.SUBE if cambio > 0 else Direccion.BAJA,
    )


# (caso, serie, periodo objetivo, valor objetivo, valor base vigente, cambio afirmado,
#  valor base al publicar, codigo de la nota, fecha de publicacion, subtipo esperado)
CASOS_B = [
    (
        "E031",
        "Madrid (Comunidad de). Pernoctaciones. Total.",
        "2026-M08",
        2165029,
        2090878,
        2.36,
        2115059,
        "CTH0825",
        "2025-09-23",
        SUBTIPO_MAGNITUD,
    ),
    (
        "E042",
        "Madrid (Comunidad de). Pernoctaciones. Total.",
        "2026-M07",
        2297978,
        2322289,
        -1.43,
        2330843,
        "CTH0725",
        "2025-08-22",
        SUBTIPO_MAGNITUD,
    ),
    (
        "E043",
        "Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato. ",
        "2026-M07",
        768195,
        786273,
        3.8,
        740149,
        "CTH0725",
        "2025-08-22",
        SUBTIPO_SIGNO,
    ),
    (
        "E047",
        "Balears, Illes. Pernoctaciones. Total categorías. Total. Dato. ",
        "2026-M08",
        11367443,
        11418035,
        -0.2,
        11388816,
        "CTH0825",
        "2025-09-23",
        SUBTIPO_MAGNITUD,
    ),
    (
        "E053",
        "Galicia. Pernoctaciones. Total.",
        "2026-M07",
        1334577,
        1339309,
        0.68,
        1325548,
        "CTH0725",
        "2025-08-22",
        SUBTIPO_SIGNO,
    ),
    (
        "E055",
        "Castilla y León. Pernoctaciones. Total.",
        "2026-M08",
        1005272,
        1038403,
        -4.5,
        1051890,
        "CTH0825",
        "2025-09-23",
        SUBTIPO_MAGNITUD,
    ),
    (
        "E056",
        "Murcia (Región de). Pernoctaciones. Total.",
        "2026-M07",
        410706,
        397508,
        4.09,
        394572,
        "CTH0725",
        "2025-08-22",
        SUBTIPO_MAGNITUD,
    ),
]


def _numeros(texto: str) -> set[str]:
    return {m.replace(",", ".") for m in re.findall(r"\d+(?:[.,]\d+)?", texto)}


@pytest.mark.parametrize(
    (
        "caso",
        "serie",
        "objetivo",
        "v_obj",
        "v_base",
        "cambio",
        "v_pub",
        "codigo",
        "fecha",
        "subtipo",
    ),
    CASOS_B,
    ids=[c[0] for c in CASOS_B],
)
def test_los_siete_b_de_la_puerta_3_disparan_2b_con_sus_fechas(
    caso, serie, objetivo, v_obj, v_base, cambio, v_pub, codigo, fecha, subtipo
) -> None:
    p_obj = Periodo.parse(objetivo)
    base = p_obj.interanual()
    tempus = ProveedorFalso(
        {
            serie: _mensual(
                {str(p_obj): v_obj, str(base): v_base, str(p_obj.anterior()): v_obj * 0.9}
            )
        },
        tabla="2074",
    )
    edicion = EdicionFalsa({serie: {str(base): (v_pub, codigo, fecha)}})
    v = AnalizarClaim(tempus, proveedor_edicion=edicion).ejecutar(
        _claim(serie, objetivo, str(base), cambio, valor_objetivo=v_obj)
    )
    assert v.context is Context.DIVERGENCE_DETECTED, caso
    assert v.clase_primaria is Clase.BASE_REVISADA
    assert v.truth is Truth.MIXED
    r2b = next(t for t in v.tests if t.nombre == "2b_base_revisada")
    assert r2b.disparo and r2b.subtipo == subtipo
    assert v.evidencia_al_publicar is not None and v.evidencia_vigente is not None
    assert v.evidencia_al_publicar.valor == v_pub
    assert v.evidencia_al_publicar.fecha == fecha
    assert v.evidencia_al_publicar.edicion == f"nota {codigo}"
    assert v.evidencia_vigente.valor == v_base
    assert v.evidencia_vigente.fecha == "2026-09-25"  # fecha de consulta del doble de Tempus
    assert "Evidencia al publicar" in v.explicacion and "Evidencia vigente" in v.explicacion
    # trazabilidad: cada numero de la explicacion que viene de la evidencia lleva span
    spans = {n.raw_value_span for n in v.numeros_usados}
    for numero in (str(int(v_pub)), str(int(v_base))):
        assert any(numero in s for s in spans), numero
    d = v.a_dict()
    assert d["evidencia_al_publicar"]["fecha"] != d["evidencia_vigente"]["fecha"]


def _tempus_baleares() -> ProveedorFalso:
    serie = "Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato. "
    return ProveedorFalso(
        {serie: _mensual({"2026-M07": 768195, "2025-M07": 786273, "2026-M06": 700000})},
        tabla="2074",
    )


SERIE_BAL = "Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato. "


def test_fuera_del_mapa_es_fallo_de_cobertura_declarado() -> None:
    edicion = EdicionFalsa({}, tablas=("36570",))  # 2074 no esta en su mapa
    v = AnalizarClaim(_tempus_baleares(), proveedor_edicion=edicion).ejecutar(
        _claim(SERIE_BAL, "2026-M07", "2025-M07", 3.8)
    )
    assert v.context is Context.UNDETERMINED
    assert AbstainReason.PREVIOUS_EDITION_OUT_OF_MAP in v.abstain_reasons
    assert v.clase_primaria is Clase.NONE
    assert v.truth is Truth.CONTRADICTED
    assert "fallo de cobertura" in v.explicacion


def test_edicion_no_localizada_abstiene_sin_inventar() -> None:
    edicion = EdicionFalsa({})  # en el mapa, pero el anexo no da la fila
    v = AnalizarClaim(_tempus_baleares(), proveedor_edicion=edicion).ejecutar(
        _claim(SERIE_BAL, "2026-M07", "2025-M07", 3.8)
    )
    assert v.context is Context.UNDETERMINED
    assert AbstainReason.PREVIOUS_EDITION_NOT_FOUND in v.abstain_reasons
    assert v.evidencia_al_publicar is None


def test_sin_conector_el_prototipo_se_comporta_como_antes() -> None:
    v = AnalizarClaim(_tempus_baleares()).ejecutar(_claim(SERIE_BAL, "2026-M07", "2025-M07", 3.8))
    assert v.context is Context.NO_DIVERGENCE_DETECTED  # 2a aplicable y no dispara; 2b no aplicable
    assert v.truth is Truth.CONTRADICTED
    assert not any(t.nombre == "2b_base_revisada" and t.aplicable for t in v.tests)


def test_la_vigente_que_cuadra_no_pide_la_edicion_anterior() -> None:
    serie = "Canarias. Pernoctaciones. Total."
    tempus = ProveedorFalso(
        {serie: _mensual({"2026-M07": 6781369, "2025-M07": 6622855})}, tabla="2074"
    )
    llamadas: list[str] = []

    class Espia(EdicionFalsa):
        def obtener(self, metrica, periodo):  # noqa: ANN001
            llamadas.append(str(periodo))
            return super().obtener(metrica, periodo)

    v = AnalizarClaim(tempus, proveedor_edicion=Espia({})).ejecutar(
        _claim(serie, "2026-M07", "2025-M07", 2.39)
    )
    assert llamadas == []
    assert v.context is Context.NO_DIVERGENCE_DETECTED and v.truth is Truth.SUPPORTED


def test_claim_falso_bajo_las_dos_ediciones_no_dispara() -> None:
    # E050: 533.954 frente a "460.550": ni la vigente (536.919) ni la provisional (538.001)
    serie = "Madrid (Comunidad de). Pernoctaciones. Total."
    tempus = ProveedorFalso(
        {serie: _mensual({"2026-M06": 533954, "2025-M06": 536919})}, tabla="1993"
    )
    edicion = EdicionFalsa(
        {serie: {"2025-M06": (538001, "EOAT0625", "2025-07-31")}}, tablas=("1993",)
    )
    v = AnalizarClaim(tempus, proveedor_edicion=edicion).ejecutar(
        _claim(serie, "2026-M06", "2025-M06", 15.9, tabla="1993")
    )
    assert v.context is Context.NO_DIVERGENCE_DETECTED
    assert v.truth is Truth.CONTRADICTED
    assert v.clase_primaria is Clase.NONE
    assert v.evidencia_al_publicar is None
