"""DEC-034: el veredicto de 2b lleva las dos evidencias separadas, cada una con su fecha.

La evidencia al publicar (edicion con la que se calculo el claim, fecha de
publicacion) y la vigente (edicion que sirve hoy el emisor, fecha de consulta)
son dos campos distintos de la salida, no una nota en el diseno.
"""

from __future__ import annotations

from veritai.domain.enums import Clase, Context, Truth
from veritai.domain.plantilla import lineas_ediciones
from veritai.domain.veredicto import EvidenciaEdicion, Veredicto

AL_PUBLICAR = EvidenciaEdicion(
    valor=740149,
    raw_value_span="[CTH0725.xlsx, hoja EOH_Hoja3, fila 23] 'Balears, Illes', ..., 740149, ...",
    edicion="INE CTH0725 (julio 2025, datos provisionales)",
    fecha="2025-08-22",
    url="https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx",
)
VIGENTE = EvidenciaEdicion(
    valor=786273,
    raw_value_span="[INE API tabla 2074] EOT22193 2025-M07: 786273",
    edicion="API Tempus, tabla 2074, edicion vigente",
    fecha="2026-09-26",
)


def test_a_dict_lleva_las_dos_evidencias_con_su_fecha() -> None:
    v = Veredicto(
        claim_id="E043",
        truth=Truth.MIXED,
        context=Context.DIVERGENCE_DETECTED,
        clase_primaria=Clase.BASE_REVISADA,
        evidencia_al_publicar=AL_PUBLICAR,
        evidencia_vigente=VIGENTE,
    )
    d = v.a_dict()
    assert d["evidencia_al_publicar"]["valor"] == 740149
    assert d["evidencia_al_publicar"]["fecha"] == "2025-08-22"
    assert d["evidencia_vigente"]["valor"] == 786273
    assert d["evidencia_vigente"]["fecha"] == "2026-09-26"
    assert d["evidencia_al_publicar"]["fecha"] != d["evidencia_vigente"]["fecha"]


def test_sin_2b_los_dos_campos_van_a_null() -> None:
    v = Veredicto(
        claim_id="X",
        truth=Truth.SUPPORTED,
        context=Context.NO_DIVERGENCE_DETECTED,
        clase_primaria=Clase.NONE,
    )
    d = v.a_dict()
    assert d["evidencia_al_publicar"] is None
    assert d["evidencia_vigente"] is None


def test_la_plantilla_imprime_cada_evidencia_con_su_fecha_y_su_span() -> None:
    lineas, usados = lineas_ediciones(AL_PUBLICAR, VIGENTE)
    assert "publicada el 2025-08-22" in lineas[0] and "740149" in lineas[0]
    assert "consultada el 2026-09-26" in lineas[1] and "786273" in lineas[1]
    assert [u.etiqueta for u in usados] == ["evidencia_al_publicar", "evidencia_vigente"]
    assert all(str(int(u.valor)) in u.raw_value_span for u in usados)
