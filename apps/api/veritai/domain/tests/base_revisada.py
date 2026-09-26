"""Test 2b — base revisada (familia "comparacion de base", DEC-034).

QUE DETECTA
    Un claim afirma una tasa de cambio entre dos periodos. El emisor ha revisado
    el valor del periodo base desde que lo publico: la edicion VIGENTE (la que
    sirve hoy la API) no es la edicion AL PUBLICAR (la nota y el anexo de
    entonces). El test dispara cuando la tasa afirmada:

        NO se reproduce con la base vigente, y
        SI se reproduce con la base tal como se publico en su edicion.

    El claim no esta mal calculado: esta calculado contra una base que el emisor
    ya no sostiene. Subtipos: `cambio_de_signo` si la revision invierte el signo
    de la tasa (E043, E053), `magnitud` si solo cambia la magnitud (E031, E042,
    E047, E055, E056).

QUE NO DECIDE
    Intencion; si la revision es "grande"; niveles, extremos o rankings (tipos
    sin test). Si la tasa cuadra con la vigente, no hay nada que explicar y el
    test no dispara. Si no cuadra con ninguna de las dos ediciones, tampoco: el
    numero es incorrecto, no el marco (E050, cubeta F).

ORDEN Y ABSTENCION (aplicacion, no aqui)
    verdad -> 2a -> 2b. Si hace falta la edicion al publicar y no esta en la
    evidencia, el caso de uso abstiene con PREVIOUS_EDITION_NOT_FOUND o, si la
    operacion no esta en el mapa del conector, PREVIOUS_EDITION_OUT_OF_MAP
    (fallo de cobertura declarado, no maquillado). `context` queda undetermined.

TOLERANCIA
    La misma que usa el eje `truth` para el cambio: media unidad del ultimo
    decimal del claim, con minimo de 0,15 puntos (la prensa redondea a un
    decimal). Fijada antes de ver los casos de la jornada 3.

Funcion pura: sin red, sin LLM, sin estado.
"""

from __future__ import annotations

from veritai.domain.claim import ClaimEstructurado, TipoClaim, UnidadCambio
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem
from veritai.domain.tests.comparacion_base import cambio, tolerancia_para
from veritai.domain.tests.resultado import ResultadoTest

NOMBRE = "2b_base_revisada"
SUBTIPO_SIGNO = "cambio_de_signo"
SUBTIPO_MAGNITUD = "magnitud"
ETIQUETA_AL_PUBLICAR = "base_al_publicar"
TOLERANCIA_MINIMA = 0.15


def _valor(item: EvidenceItem | None) -> float | None:
    return None if item is None or item.valor is None else float(item.valor)


def _signo(x: float) -> int:
    return 0 if abs(x) < 1e-9 else (1 if x > 0 else -1)


def tasa_cuadra_con_vigente(claim: ClaimEstructurado, bundle: EvidenceBundle) -> bool | None:
    """True/False si se puede comparar la tasa afirmada con la base vigente; None si no."""
    if claim.tipo is not TipoClaim.CAMBIO_ENTRE_PERIODOS or claim.cambio_afirmado is None:
        return None
    objetivo = _valor(bundle.buscar("objetivo"))
    base = _valor(bundle.buscar("base_claim"))
    if objetivo is None or base is None:
        return None
    unidad = claim.unidad_cambio or UnidadCambio.PORCENTAJE
    tasa = cambio(base, objetivo, unidad)
    if tasa is None:
        return None
    tol = max(tolerancia_para(claim.cambio_afirmado, tasa), TOLERANCIA_MINIMA)
    return abs(claim.cambio_afirmado - tasa) <= tol


def aplicar_2b(claim: ClaimEstructurado, bundle: EvidenceBundle) -> ResultadoTest:
    if claim.tipo is not TipoClaim.CAMBIO_ENTRE_PERIODOS:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo=f"no aplicable a claims de tipo {claim.tipo.value}",
        )
    if claim.cambio_afirmado is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="el claim no afirma una tasa de cambio: no hay base que revisar",
        )

    objetivo = _valor(bundle.buscar("objetivo"))
    base_vigente = _valor(bundle.buscar("base_claim"))
    if objetivo is None or base_vigente is None or claim.periodo_base is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="faltan el valor objetivo o el de la base vigente en la evidencia",
        )

    unidad = claim.unidad_cambio or UnidadCambio.PORCENTAJE
    tasa_vigente = cambio(base_vigente, objetivo, unidad)
    if tasa_vigente is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="no se puede recomputar la tasa (base vigente cero)",
        )
    tol = max(tolerancia_para(claim.cambio_afirmado, tasa_vigente), TOLERANCIA_MINIMA)
    calculos: dict[str, float | str | None] = {
        "unidad": unidad.value,
        "periodo_objetivo": str(claim.periodo_objetivo),
        "valor_objetivo": objetivo,
        "periodo_base": str(claim.periodo_base),
        "valor_base_vigente": base_vigente,
        "tasa_con_base_vigente": round(tasa_vigente, 3),
        "cambio_afirmado": claim.cambio_afirmado,
        "tolerancia": round(tol, 4),
    }

    if abs(claim.cambio_afirmado - tasa_vigente) <= tol:
        return ResultadoTest(
            NOMBRE,
            aplicable=True,
            disparo=False,
            motivo=(
                f"la tasa afirmada ({claim.cambio_afirmado:+.2f} {unidad.value}) se reproduce "
                f"con la edicion vigente ({tasa_vigente:+.2f}): no hay base revisada que explicar"
            ),
            calculos=calculos,
        )

    al_publicar = bundle.buscar(ETIQUETA_AL_PUBLICAR)
    base_al_publicar = _valor(al_publicar)
    if al_publicar is None or base_al_publicar is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo=(
                f"la tasa afirmada ({claim.cambio_afirmado:+.2f} {unidad.value}) no se reproduce "
                f"con la edicion vigente ({tasa_vigente:+.2f}) y no hay edicion al publicar en la "
                "evidencia"
            ),
            calculos=calculos,
        )

    tasa_al_publicar = cambio(base_al_publicar, objetivo, unidad)
    edicion = al_publicar.version or "edicion al publicar"
    fecha = al_publicar.document_date or "fecha no leida"
    calculos["edicion_al_publicar"] = edicion
    calculos["fecha_publicacion"] = fecha
    calculos["valor_base_al_publicar"] = base_al_publicar
    calculos["tasa_con_base_al_publicar"] = (
        None if tasa_al_publicar is None else round(tasa_al_publicar, 3)
    )
    calculos["revision_absoluta"] = round(base_vigente - base_al_publicar, 3)
    calculos["revision_relativa_pct"] = (
        None
        if base_al_publicar == 0
        else round((base_vigente - base_al_publicar) / abs(base_al_publicar) * 100.0, 3)
    )
    if tasa_al_publicar is None:
        return ResultadoTest(
            NOMBRE,
            aplicable=False,
            disparo=False,
            motivo="no se puede recomputar la tasa con la edicion al publicar (base cero)",
            calculos=calculos,
        )

    if abs(claim.cambio_afirmado - tasa_al_publicar) <= tol:
        cambia_signo = _signo(tasa_vigente) != _signo(tasa_al_publicar)
        subtipo = SUBTIPO_SIGNO if cambia_signo else SUBTIPO_MAGNITUD
        calculos["subtipo"] = subtipo
        return ResultadoTest(
            NOMBRE,
            aplicable=True,
            disparo=True,
            subtipo=subtipo,
            motivo=(
                f"la tasa afirmada ({claim.cambio_afirmado:+.2f} {unidad.value}) se reproduce con "
                f"la base tal como se publico en {edicion} (publicada el {fecha}: "
                f"{base_al_publicar:g} -> {tasa_al_publicar:+.2f}) y no con la edicion vigente "
                f"({base_vigente:g} -> {tasa_vigente:+.2f})"
                + ("; la revision cambia el signo" if cambia_signo else "")
            ),
            calculos=calculos,
        )
    return ResultadoTest(
        NOMBRE,
        aplicable=True,
        disparo=False,
        motivo=(
            f"la tasa afirmada ({claim.cambio_afirmado:+.2f} {unidad.value}) no se reproduce ni "
            f"con la edicion vigente ({tasa_vigente:+.2f}) ni con la edicion al publicar "
            f"({tasa_al_publicar:+.2f}, {edicion}): el numero es incorrecto, no el marco"
        ),
        calculos=calculos,
    )


__all__ = [
    "ETIQUETA_AL_PUBLICAR",
    "NOMBRE",
    "SUBTIPO_MAGNITUD",
    "SUBTIPO_SIGNO",
    "TOLERANCIA_MINIMA",
    "aplicar_2b",
    "tasa_cuadra_con_vigente",
]
