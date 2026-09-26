"""Test 2a — periodo o base elegida (familia "comparacion de base", DEC-026).

QUE DETECTA
    Un claim compara el periodo objetivo con una base que el eligio. El emisor
    publica su propia comparacion de referencia (el periodo anterior, o el
    mismo periodo del anio anterior). El test dispara cuando:

    (A) la base del claim NO es ninguna referencia del emisor, y recomputar el
        cambio contra la referencia principal del emisor cambia el signo o la
        magnitud por encima de un umbral fijado a priori (P11: mayo -> diciembre
        da -22,9%; diciembre contra diciembre da +1,1%); o

    (B) el valor que el claim atribuye al periodo objetivo no es el de ese
        periodo, pero SI es el de otro periodo de la ventana (P05, C17: el
        numero existe, en otra fecha).

    No dispara cuando la base del claim coincide con una referencia del emisor:
    ahi el claim compara lo mismo que compara el emisor.

UMBRALES, fijados antes de ver los casos de la Puerta 2
    umbral_ratio = 2.0   la magnitud recomputada difiere >= 2x (o el signo cambia)
    tolerancia     = ver `tolerancia_para`: media unidad del ultimo decimal, con
                     un minimo relativo del 0,5%, para absorber redondeos de prensa.

Funcion pura: sin red, sin LLM, sin estado.
"""

from __future__ import annotations

import math

from veritai.domain.claim import ClaimEstructurado, Direccion, Referencia, TipoClaim, UnidadCambio
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem
from veritai.domain.tests.resultado import ResultadoTest

NOMBRE = "2a_periodo_o_base_elegida"
UMBRAL_RATIO = 2.0


def tolerancia_para(valor_claim: float, valor_evidencia: float) -> float:
    """Media unidad del ultimo decimal que muestra el claim, con minimo relativo del 0,5%."""
    texto = f"{valor_claim}"
    decimales = len(texto.split(".")[1]) if "." in texto and not texto.endswith(".0") else 0
    media_unidad = 0.5 * 10 ** (-decimales)
    return max(media_unidad, 0.005 * abs(valor_evidencia))


def cambio(base: float, objetivo: float, unidad: UnidadCambio) -> float | None:
    if unidad is UnidadCambio.PORCENTAJE:
        if base == 0:
            return None
        return (objetivo - base) / abs(base) * 100.0
    return objetivo - base


def _signo(x: float) -> int:
    return 0 if abs(x) < 1e-9 else (1 if x > 0 else -1)


def _valor(item: EvidenceItem | None) -> float | None:
    return None if item is None or item.valor is None else float(item.valor)


def aplicar_2a(
    claim: ClaimEstructurado, bundle: EvidenceBundle, umbral_ratio: float = UMBRAL_RATIO
) -> ResultadoTest:
    if claim.tipo is not TipoClaim.CAMBIO_ENTRE_PERIODOS:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo=f"no aplicable a claims de tipo {claim.tipo.value}",
        )

    objetivo = _valor(bundle.buscar("objetivo"))
    base = _valor(bundle.buscar("base_claim"))
    if objetivo is None or base is None or claim.periodo_base is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="faltan el valor objetivo o el de la base del claim en la evidencia",
        )

    unidad = claim.unidad_cambio or UnidadCambio.PORCENTAJE
    cambio_claim = cambio(base, objetivo, unidad)
    calculos: dict[str, float | str | None] = {
        "unidad": unidad.value,
        "periodo_base_claim": str(claim.periodo_base),
        "valor_base_claim": base,
        "periodo_objetivo": str(claim.periodo_objetivo),
        "valor_objetivo": objetivo,
        "cambio_recomputado_con_base_del_claim": None
        if cambio_claim is None
        else round(cambio_claim, 3),
        "cambio_afirmado": claim.cambio_afirmado,
    }

    # (B) el valor afirmado para el objetivo es el de otro periodo de la ventana
    if claim.valor_objetivo is not None:
        tol = tolerancia_para(claim.valor_objetivo, objetivo)
        if abs(claim.valor_objetivo - objetivo) > tol:
            for item in bundle.historical_items:
                if (
                    item.etiqueta.startswith("ventana")
                    and item.valor is not None
                    and abs(claim.valor_objetivo - float(item.valor)) <= tol
                ):
                    calculos["valor_afirmado"] = claim.valor_objetivo
                    calculos["periodo_donde_si_aparece"] = str(item.periodo)
                    return ResultadoTest(
                        NOMBRE,
                        aplicable=True,
                        disparo=True,
                        subtipo="valor_atribuido_a_otro_periodo",
                        motivo=(
                            f"el claim atribuye {claim.valor_objetivo} a "
                            f"{claim.periodo_objetivo.etiqueta()}, "
                            f"pero ese es el valor de {item.periodo.etiqueta()}; en "
                            f"{claim.periodo_objetivo.etiqueta()} la serie da {objetivo}"
                        ),
                        calculos=calculos,
                    )

    # (A) la base del claim contra la referencia del emisor
    referencias = [i for i in bundle.historical_items if i.etiqueta.startswith("ref:")]
    if not referencias:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="no hay valor de la referencia del emisor en la evidencia",
            calculos=calculos,
        )

    periodos_ref = {i.periodo for i in referencias}
    if claim.periodo_base in periodos_ref:
        cual = next(i.etiqueta for i in referencias if i.periodo == claim.periodo_base)
        return ResultadoTest(
            NOMBRE,
            aplicable=True,
            disparo=False,
            motivo=f"la base del claim ({claim.periodo_base.etiqueta()}) es la referencia "
            f"del emisor ({cual.removeprefix('ref:')})",
            calculos=calculos,
        )

    principal = claim.metrica.referencia_principal
    ref = next((i for i in referencias if i.etiqueta == f"ref:{principal.value}"), referencias[0])
    valor_ref = _valor(ref)
    if valor_ref is None or cambio_claim is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="la referencia del emisor no tiene valor numerico",
            calculos=calculos,
        )

    cambio_ref = cambio(valor_ref, objetivo, unidad)
    calculos["referencia_emisor"] = f"{ref.etiqueta.removeprefix('ref:')} ({ref.periodo})"
    calculos["valor_referencia_emisor"] = valor_ref
    calculos["cambio_recomputado_con_referencia_emisor"] = (
        None if cambio_ref is None else round(cambio_ref, 3)
    )

    if cambio_ref is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="no se puede recomputar contra la referencia (base cero)",
            calculos=calculos,
        )

    cambia_signo = _signo(cambio_claim) != _signo(cambio_ref)
    ratio = math.inf if abs(cambio_ref) < 1e-9 else abs(cambio_claim) / abs(cambio_ref)
    calculos["ratio_magnitudes"] = None if math.isinf(ratio) else round(ratio, 3)
    calculos["umbral_ratio"] = umbral_ratio

    if cambia_signo or ratio >= umbral_ratio or ratio <= 1.0 / umbral_ratio:
        que = "cambia de signo" if cambia_signo else f"difiere {ratio:.1f}x en magnitud"
        return ResultadoTest(
            NOMBRE,
            aplicable=True,
            disparo=True,
            subtipo="base_no_es_referencia",
            motivo=(
                f"el claim compara contra {claim.periodo_base.etiqueta()} "
                f"({cambio_claim:+.2f} {unidad.value}); contra la referencia del emisor, "
                f"{principal.value} ({ref.periodo.etiqueta()}), el cambio es "
                f"{cambio_ref:+.2f} {unidad.value}: {que}"
            ),
            calculos=calculos,
        )
    return ResultadoTest(
        NOMBRE,
        aplicable=True,
        disparo=False,
        motivo=(
            f"la base del claim no es la del emisor, pero el cambio recomputado contra "
            f"{principal.value} ({cambio_ref:+.2f}) es comparable al del claim "
            f"({cambio_claim:+.2f})"
        ),
        calculos=calculos,
    )


def direccion_de(cambio_valor: float | None) -> Direccion | None:
    if cambio_valor is None:
        return None
    s = _signo(cambio_valor)
    return Direccion.IGUAL if s == 0 else (Direccion.SUBE if s > 0 else Direccion.BAJA)


__all__ = [
    "NOMBRE",
    "UMBRAL_RATIO",
    "Referencia",
    "cambio",
    "direccion_de",
    "aplicar_2a",
    "tolerancia_para",
]
