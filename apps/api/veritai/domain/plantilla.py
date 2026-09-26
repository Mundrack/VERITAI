"""Explicacion numerica por plantilla. Sin LLM.

Cada numero que aparece aqui sale de un EvidenceItem o del propio claim; la
funcion devuelve tambien la lista de numeros usados con su span, que es lo que
la trazabilidad comprueba.
"""

from __future__ import annotations

from veritai.domain.claim import ClaimEstructurado
from veritai.domain.enums import AbstainReason, Context, Truth
from veritai.domain.evidencia import EvidenceBundle, EvidenceItem
from veritai.domain.tests.resultado import ResultadoTest
from veritai.domain.verdad import ResultadoVerdad
from veritai.domain.veredicto import NumeroUsado

SALIDA = {
    (Truth.SUPPORTED, Context.DIVERGENCE_DETECTED): "Verdadero pero descontextualizado",
    (Truth.SUPPORTED, Context.NO_DIVERGENCE_DETECTED): "Respaldado, sin divergencia detectada",
    (Truth.SUPPORTED, Context.UNDETERMINED): "Respaldado; contexto no evaluable",
    (Truth.MIXED, Context.DIVERGENCE_DETECTED): "Parcialmente respaldado y descontextualizado",
    (
        Truth.MIXED,
        Context.NO_DIVERGENCE_DETECTED,
    ): "Parcialmente respaldado, sin divergencia detectada",
    (Truth.MIXED, Context.UNDETERMINED): "Parcialmente respaldado; contexto no evaluable",
    (Truth.INSUFFICIENT_EVIDENCE, Context.UNDETERMINED): "Sin veredicto: evidencia insuficiente",
}

MOTIVOS = {
    AbstainReason.UNSUPPORTED_CLAIM_TYPE: (
        "el tipo de afirmacion no esta soportado por el prototipo"
    ),
    AbstainReason.REQUIRED_SLOT_MISSING: "al claim le falta un dato imprescindible para evaluarlo",
    AbstainReason.PRIMARY_SOURCE_NOT_FOUND: (
        "no se localizo la serie o el periodo en la fuente primaria"
    ),
    AbstainReason.PREVIOUS_EDITION_NOT_FOUND: "no se localizo el valor del periodo base",
    AbstainReason.PERIOD_NOT_COMPARABLE: "los periodos comparados no son comparables",
    AbstainReason.METHODOLOGY_NOT_COMPARABLE: (
        "los dos periodos vienen de bases o metodologias distintas"
    ),
    AbstainReason.SOURCE_VERSION_AMBIGUOUS: "mas de una serie de la fuente casa con la metrica",
    AbstainReason.CONFLICTING_PRIMARY_VALUES: (
        "la fuente da dos valores distintos para el mismo periodo"
    ),
    AbstainReason.EXTRACTION_FAILED: "no se pudo extraer un numero de la fuente",
    AbstainReason.METRIC_AMBIGUOUS: "el claim no dice que metrica usa",
}


def _num(item: EvidenceItem, etiqueta: str) -> NumeroUsado:
    return NumeroUsado(float(item.valor), item.raw_value_span, item.id, etiqueta)  # type: ignore[arg-type]


def explicar(
    claim: ClaimEstructurado,
    bundle: EvidenceBundle,
    verdad: ResultadoVerdad,
    tests: list[ResultadoTest],
    truth: Truth,
    context: Context,
    motivos: list[AbstainReason],
) -> tuple[str, list[NumeroUsado]]:
    usados: list[NumeroUsado] = []
    lineas: list[str] = []

    if truth is Truth.CONTRADICTED and context is Context.DIVERGENCE_DETECTED:
        titulo = "Contradicho y descontextualizado"
    elif truth is Truth.CONTRADICTED:
        titulo = "Contradicho"
    else:
        titulo = SALIDA.get((truth, context), f"{truth.value} / {context.value}")
    lineas.append(f"{titulo}.")
    lineas.append(f'Afirmacion: "{claim.texto}"')

    objetivo = bundle.buscar("objetivo")
    if objetivo is not None and objetivo.valor is not None:
        usados.append(_num(objetivo, "objetivo"))
        lineas.append(
            f"Fuente ({objetivo.publisher}, serie {objetivo.serie_codigo}, "
            f'"{objetivo.serie_nombre.strip()}"): '
            f"{claim.periodo_objetivo.etiqueta()} = {objetivo.valor}."
        )
    base = bundle.buscar("base_claim")
    if base is not None and base.valor is not None and claim.periodo_base is not None:
        usados.append(_num(base, "base_claim"))
        lineas.append(f"Base que usa el claim: {claim.periodo_base.etiqueta()} = {base.valor}.")
    for item in bundle.historical_items:
        if item.etiqueta.startswith("ref:") and item.valor is not None:
            usados.append(_num(item, item.etiqueta))
            lineas.append(
                f"Referencia del emisor ({item.etiqueta.removeprefix('ref:')}): "
                f"{item.periodo.etiqueta()} = {item.valor}."
            )

    if verdad.comparaciones:
        lineas.append("Verdad: " + verdad.resumen + ".")
    for t in tests:
        estado = "no aplicable" if not t.aplicable else ("DISPARA" if t.disparo else "no dispara")
        lineas.append(f"Test {t.nombre}: {estado}. {t.motivo}.")
        if t.senales:
            lineas.append(
                "Senales registradas: "
                + ", ".join(t.senales)
                + " (se anotan, no cuentan como divergencia; DEC-029)."
            )
        for it in bundle.historical_items:
            if (
                it.etiqueta.startswith("ventana")
                and it.valor is not None
                and t.calculos.get("periodo_donde_si_aparece") == str(it.periodo)
            ):
                usados.append(_num(it, it.etiqueta))
    if motivos:
        lineas.append(
            "Abstencion: " + "; ".join(f"{m.value} ({MOTIVOS[m]})" for m in motivos) + "."
        )
    if bundle.missing_slots:
        lineas.append("Evidencia incompleta: faltan " + ", ".join(bundle.missing_slots) + ".")
    lineas.append(f"Evidencia: {len(bundle.items)} items, bundle {bundle.bundle_hash[:12]}.")
    return "\n".join(lineas), usados
