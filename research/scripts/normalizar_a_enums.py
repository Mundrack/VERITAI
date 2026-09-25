#!/usr/bin/env python3
"""Fases A2, A3 y A4 de la auditoria: normaliza los 20 casos a enums cerrados.

QUE HACE
    Convierte las etiquetas libres del Excel en valores de los enums cerrados
    definidos en docs/GLOSARIO.md, y emite research/pilot-20-normalizado.csv.

POR QUE
    Defecto D4 de la adenda: "Truth preliminar" tiene 12 valores distintos en 20
    filas, con etiquetas como "supported (si se refiere a valor)". Una etiqueta
    con parentesis explicativos no es una etiqueta: es texto libre y no se puede
    contar. Los matices van a un campo de notas, no a la etiqueta.

REGLA DE ESTE ARCHIVO
    Cada resolucion lleva su justificacion en una linea. Colapsar
    "supported (si se refiere a valor)" a "supported" pierde informacion si no
    se anota por que se colapso asi.

USO
    python research/scripts/normalizar_a_enums.py
    Codigo de salida 1 si alguna fila contiene un valor fuera de enum.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "research" / "pilot-20-normalizado.csv"

# ---------------------------------------------------------------------------
# Enums cerrados. Fuente: docs/GLOSARIO.md
# ---------------------------------------------------------------------------

TRUTH = {"supported", "contradicted", "mixed", "insufficient_evidence", "not_applicable"}

CONTEXT = {"divergence_detected", "no_divergence_detected", "undetermined", "not_applicable"}

CLASE = {
    "1_ranking_vs_value",
    "2_baseline_selection",
    "3_absolute_vs_relative",
    "4_denominator",
    "5_methodology_change",
    "none",
    "other_observed",
}

ABSTAIN = {
    "UNSUPPORTED_CLAIM_TYPE",
    "REQUIRED_SLOT_MISSING",
    "PRIMARY_SOURCE_NOT_FOUND",
    "PREVIOUS_EDITION_NOT_FOUND",
    "PERIOD_NOT_COMPARABLE",
    "METHODOLOGY_NOT_COMPARABLE",
    "SOURCE_VERSION_AMBIGUOUS",
    "CONFLICTING_PRIMARY_VALUES",
    "EXTRACTION_FAILED",
    "METRIC_AMBIGUOUS",   # DEC-015 (2026-09-25): el claim no dice que metrica usa.
                          # 4 de 20 en el piloto. El enum describe la realidad
                          # observada, no al reves.
    "",          # null explicito: no hay motivo de abstencion
}

RECUPERABILIDAD = {"A", "B", "C", "D"}

FORMATO = {"api", "dataset", "html", "pdf", "scan", "none"}

# verificado          cifras confirmadas contra la fuente PRIMARIA, con raw_value_span
# parcial             primaria viva y aritmetica correcta, pero las cifras exigen
#                     navegacion interactiva o descarga: sin raw_value_span
# NEEDS_REVIEW        error encontrado, o primaria no alcanzable, o URL que no
#                     identifica ningun dato (portada)
# fuera_de_alcance    DEC-013
AUDIT_STATUS = {"verificado", "parcial", "NEEDS_REVIEW", "fuera_de_alcance"}

POST_URL_ESTADO = {
    "200_verificado", "200_contenido_parcial", "403_bloqueo_bot", "no_alcanzable",
}
PRIMARIA_URL_ESTADO = {
    "200_cifras_verificadas",        # el numero del Excel aparece en la primaria
    "200_cifras_no_coinciden",       # la primaria da OTRO numero
    "200_soporte_parcial",           # respalda parte del Dato A/B, no todo
    "200_portal_sin_cifras",         # portal o buscador: exige navegar
    "200_tablas_con_descarga",       # pagina de tablas con CSV/XLSX: exige descargar
    "200_homepage",                  # portada institucional: no identifica nada
    "200_js_verificado_por_api",     # HTML vacio, pero la API del mismo publicador si
    "403_cloudflare_challenge",
    "403_bloqueo_bot",
    "no_alcanzable",
    "no_alcanzable_por_herramienta",
}


@dataclass
class Caso:
    case_id: str
    en_alcance_tesis: bool

    # --- normalizado ---
    truth: str
    context: str
    clase_primaria: str
    clases_secundarias: str
    recuperabilidad: str
    formato: str
    abstain_reason: str

    # --- original, para que la traduccion sea auditable ---
    truth_original: str
    context_original: str
    clase_original: str
    recuperabilidad_original: str
    abstain_reason_original: str

    # --- justificaciones de la normalizacion ---
    justificacion: str

    # --- resultado de la auditoria ---
    audit_status: str
    audit_notas: str

    # --- se rellenan en la Fase B (verificacion de URLs) ---
    primaria_url_tipo: str = "pendiente_fase_b"
    aritmetica_verificada: str = ""
    raw_value_span: str = "pendiente_fase_b"
    access_requires_login: str = "pendiente_fase_b"

    # --- candidatos a extender el enum de abstencion ---
    abstain_candidato: str = ""

    # --- resultado de la Fase B, ver FASE_B ---
    post_url_estado: str = "pendiente_fase_b"
    primaria_url_estado: str = "pendiente_fase_b"
    cronometrado_por: str = "agente"


# ---------------------------------------------------------------------------
# Los 20 casos. Una entrada por caso, con la decision y su porque.
# ---------------------------------------------------------------------------

CASOS: list[Caso] = [
    Caso(
        "P01", True,
        truth="mixed", context="divergence_detected",
        clase_primaria="1_ranking_vs_value", clases_secundarias="",
        recuperabilidad="B", formato="pdf", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted / mixed",
        context_original="divergence_detected",
        clase_original="1 - ranking_vs_value",
        recuperabilidad_original="A/B",
        abstain_reason_original="Si el indice concreto no puede identificarse o falta edicion comparable",
        justificacion=(
            "truth: el claim afirma mejora en CUATRO indices y el corpus solo documenta uno "
            "(EIU). No se puede sostener 'contradicted' con la evidencia registrada, ni "
            "'supported' porque la posicion empeora. mixed. | "
            "recuperabilidad: A/B resuelto a B, el informe del EIU es PDF y no dataset."
        ),
        audit_status="NEEDS_REVIEW",
        audit_notas=(
            "El claim cubre cuatro indices; el Excel documenta solo el Democracy Index del EIU. "
            "Los otros tres no estan en el corpus, asi que la afirmacion del Contraste "
            "('otros indices citados no mejoran') esta asertada pero no documentada."
        ),
    ),
    Caso(
        "P02", True,
        truth="supported", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="3_absolute_vs_relative",
        recuperabilidad="A", formato="dataset", abstain_reason="METRIC_AMBIGUOUS",
        truth_original="supported (si se refiere a valor)",
        context_original="divergence_detected",
        clase_original="2 + 3 - baseline_selection / absolute_vs_relative",
        recuperabilidad_original="A",
        abstain_reason_original="Si no se puede determinar si 'compra' significa valor o volumen",
        justificacion=(
            "truth: el parentesis '(si se refiere a valor)' sale de la etiqueta y va a notas. "
            "El valor monetario sube 8.948%, compatible con el 9.000% del claim. supported. | "
            "clase: primaria baseline (2025 fue base anormalmente baja), secundaria "
            "absoluto/relativo. | abstain: METRIC_AMBIGUOUS, valor-vs-volumen. Entro en el "
            "enum por DEC-015 tras verse en 4 de 20 casos."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: valor +8.948% (~8.945% en el Excel, entradas aproximadas). "
            "Volumen +6.711%, no 9.000%: el claim solo se sostiene si 'compra' significa "
            "euros. El Excel no da cifra para el volumen."
        ),    ),
    Caso(
        "P03", True,
        truth="supported", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="",
        recuperabilidad="A", formato="html", abstain_reason="PERIOD_NOT_COMPARABLE",
        truth_original="supported (el +25,7% existe)",
        context_original="divergence_detected",
        clase_original="2 - baseline_selection",
        recuperabilidad_original="A",
        abstain_reason_original="Si no hay un baseline comparable por un shock estructural",
        justificacion=(
            "truth: el parentesis sale de la etiqueta. El +25,7% es correcto. supported. | "
            "abstain: 'shock estructural impide baseline comparable' mapea limpio a "
            "PERIOD_NOT_COMPARABLE, que ya existe en el enum."
        ),
        audit_status="NEEDS_REVIEW",
        audit_notas=(
            "ERROR ARITMETICO en el corpus. El Excel dice que 2022 vs 2019 es +5,03%; "
            "1.127.147 sobre 1.070.421 da +5,30%. Transposicion de digitos. "
            "El +25,7% de 2022 vs 2021 si es correcto (+25,65%)."
        ),
    ),
    Caso(
        "P04", True,
        truth="contradicted", context="divergence_detected",
        clase_primaria="3_absolute_vs_relative", clases_secundarias="",
        recuperabilidad="C", formato="html", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted",
        context_original="divergence_detected",
        clase_original="3 - absolute_vs_relative / calculo de tasa",
        recuperabilidad_original="B/C",
        abstain_reason_original="Si la serie necesaria no esta publicamente completa",
        justificacion=(
            "clase: 'calculo de tasa' no es un valor; confundir crecimiento acumulado con "
            "tasa anual es confundir magnitudes, que es lo que cubre la clase 3. | "
            "recuperabilidad: B/C resuelto a C, porque el Excel dice que parte de la serie "
            "no era publica y la URL primaria es la portada del INE. | "
            "abstain: falta el slot historical_items del bundle."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado y correcto: total +192,5%, division ingenua 9,63%, CAGR real 5,51%. "
            "El Excel reproduce bien tanto el error del emisor como el calculo correcto."
        ),
    ),
    Caso(
        "P05", True,
        truth="contradicted", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="",
        recuperabilidad="B", formato="pdf", abstain_reason="METHODOLOGY_NOT_COMPARABLE",
        truth_original="contradicted in temporal attribution",
        context_original="divergence_detected",
        clase_original="7 - true_number_false_frame / temporal",
        recuperabilidad_original="B",
        abstain_reason_original="Si la pregunta o categorias no son comparables entre barometros",
        justificacion=(
            "truth: 'in temporal attribution' es un matiz, no una etiqueta. Va a notas. | "
            "clase: la 7 quedo fuera de la tesis, asi que se registra como other_observed "
            "con el detalle en notas, para no perder la frecuencia observada."
        ),
        audit_status="verificado",
        audit_notas=(
            "Atribucion temporal desplazada: el ~66,7% existe, pero en 2019-2023, no en 2018. "
            "Recomputado: la caida real abril2018 -> abril2026 es de 1 pp (56,9% a 55,9%), "
            "mientras el claim afirmaba 16,7 pp (dos tercios a la mitad)."
        ),
    ),
    Caso(
        "P06", True,
        truth="contradicted", context="divergence_detected",
        clase_primaria="5_methodology_change", clases_secundarias="",
        recuperabilidad="B", formato="html", abstain_reason="METHODOLOGY_NOT_COMPARABLE",
        truth_original="contradicted",
        context_original="divergence_detected",
        clase_original="5 - methodology_change",
        recuperabilidad_original="A/B",
        abstain_reason_original="METHODOLOGY_NOT_COMPARABLE si no puede reconstruirse la equivalencia",
        justificacion=(
            "recuperabilidad: A/B resuelto a B, porque hay que homologar categorias entre "
            "el sistema antiguo y el nuevo, lo que es trabajo manual. | "
            "abstain: ya venia con un valor del enum; solo se le quita la condicional."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: con categoria homogenea 2018->2025 es +86,1%. El 374% del claim "
            "sale de comparar 147 con una categoria antigua de 31 que excluia abusos. "
            "Ambas cifras reproducibles. Caso canonico de cambio metodologico real."
        ),
    ),
    Caso(
        "P07", True,
        truth="contradicted", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="4_denominator",
        recuperabilidad="B", formato="pdf", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted",
        context_original="divergence_detected",
        clase_original="7 - scope/geography mismatch",
        recuperabilidad_original="B",
        abstain_reason_original="Si no se puede resolver el ambito geografico exacto del claim",
        justificacion=(
            "clase: 'scope/geography mismatch' no es una de las cinco candidatas. Se registra "
            "como other_observed, con 4_denominator como secundaria porque el fallo es que "
            "numerador y denominador pertenecen a ambitos distintos."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: Espania 32,7% (19.939/60.938), Cataluna 53,0% (4.554/8.594). "
            "El 50% del claim se parece al dato catalan y se traslada indebidamente al "
            "conjunto de Espania."
        ),
        abstain_candidato="SCOPE_NOT_RESOLVABLE",
    ),
    Caso(
        "P08", False,
        truth="contradicted", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="4_denominator",
        recuperabilidad="B", formato="html", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted",
        context_original="divergence_detected",
        clase_original="4 - missing_or_wrong_denominator",
        recuperabilidad_original="A/B",
        abstain_reason_original="REQUIRED_EVIDENCE_INCOMPLETE si el seguimiento no permite formar el denominador",
        justificacion=(
            "FUERA DE ALCANCE por DEC-013: es un bulo sobre un articulo del NEJM en ingles, "
            "necesita otra familia de conectores y 'edicion anterior' no significa lo mismo "
            "para un paper. Se registra como other_observed con 4_denominator en secundarias "
            "para conservar la clase real. | abstain: REQUIRED_EVIDENCE_INCOMPLETE no existe "
            "en el enum; mapea a REQUIRED_SLOT_MISSING."
        ),
        audit_status="fuera_de_alcance",
        audit_notas=(
            "El 82% es aritmeticamente correcto (104/127): el defecto esta en el denominador, "
            "no en la division. Informativo: con los 905 embarazos pendientes de seguimiento "
            "incluidos, la proporcion baja a 10,1%. El propio NEJM publico una correccion "
            "diciendo que no habia denominador disponible."
        ),
    ),
    Caso(
        "P09", False,
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="3_absolute_vs_relative",
        recuperabilidad="B", formato="html", abstain_reason="UNSUPPORTED_CLAIM_TYPE",
        truth_original="mixed / overclaimed",
        context_original="divergence_detected",
        clase_original="3 + 6 - absolute_vs_relative / correlation_causation",
        recuperabilidad_original="A/B",
        abstain_reason_original="Si el estudio no permite inferir causalidad o falta tasa absoluta",
        justificacion=(
            "FUERA DE ALCANCE por DEC-013, igual que P08. | truth: 'overclaimed' es un matiz; "
            "mixed. | clase: la 6 (correlacion/causalidad) esta fuera de la tesis; "
            "other_observed con 3 en secundarias. | abstain: la inferencia causal no es un "
            "tipo de claim que el sistema soporte, de ahi UNSUPPORTED_CLAIM_TYPE."
        ),
        audit_status="fuera_de_alcance",
        audit_notas=(
            "No recomputable: el Excel no da valores absolutos, porque el caso trata "
            "precisamente de que un +610% relativo no comunica el riesgo absoluto "
            "(del orden de 1 caso por 10.000 dosis) y convierte una senial "
            "observado/esperado en causalidad."
        ),
    ),
    Caso(
        "P10", True,
        truth="supported", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="",
        recuperabilidad="A", formato="dataset", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="supported",
        context_original="divergence_detected",
        clase_original="2 - baseline_selection / outlier",
        recuperabilidad_original="A",
        abstain_reason_original="Si no se recupera serie suficiente para detectar outliers",
        justificacion=(
            "clase: 'outlier' es el mecanismo dentro de baseline_selection, no otra clase. "
            "Va a notas. | abstain: sin serie historica falta el slot historical_items."
        ),
        audit_status="NEEDS_REVIEW",
        audit_notas=(
            "NUMEROS NO VERIFICABLES. Dato A es '>20.000 M EUR' y Dato B '~7.500 M EUR': "
            "no son valores, son aproximaciones. No se puede comprobar ni 'un tercio' ni "
            "'13.000 millones menos'. Hay que registrar las cifras exactas de DataInvex."
        ),
    ),
    Caso(
        "P11", True,
        truth="supported", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="",
        recuperabilidad="B", formato="pdf", abstain_reason="PERIOD_NOT_COMPARABLE",
        truth_original="supported (numeros puntuales)",
        context_original="divergence_detected",
        clase_original="2 - baseline_selection / seasonality",
        recuperabilidad_original="A/B",
        abstain_reason_original="BASELINE_NOT_COMPARABLE si se comparan meses con patron estacional",
        justificacion=(
            "truth: el parentesis sale de la etiqueta. | clase: 'seasonality' es el mecanismo, "
            "va a notas. | recuperabilidad: A/B resuelto a B, la fuente es un PDF mensual. | "
            "abstain: BASELINE_NOT_COMPARABLE no existe en el enum; comparar meses con patron "
            "estacional es exactamente PERIOD_NOT_COMPARABLE."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: mayo -> diciembre 2018 es -22,87%, exacto. Pero diciembre es "
            "sistematicamente un mes bajo: el calculo es correcto y la comparacion mal elegida. "
            "Es la distincion que el caso sirve para ensenar."
        ),
    ),
    Caso(
        "P12", True,
        truth="supported", context="divergence_detected",
        clase_primaria="4_denominator", clases_secundarias="other_observed",
        recuperabilidad="B", formato="pdf", abstain_reason="PERIOD_NOT_COMPARABLE",
        truth_original="supported values / invalid comparison",
        context_original="divergence_detected",
        clase_original="4/7 - incompatible denominator/time basis",
        recuperabilidad_original="B",
        abstain_reason_original="PERIOD_NOT_COMPARABLE",
        justificacion=(
            "truth: los valores son correctos; lo invalido es la comparacion, que es "
            "precisamente lo que captura context. supported + divergence_detected es la "
            "combinacion canonica de este proyecto. | clase: 4 primaria, la 7 (marco falso) "
            "a secundarias como other_observed."
        ),
        audit_status="verificado",
        audit_notas=(
            "Informativo: 23.663 altas acumuladas sobre 11.894 hospitalizados da 1,99, un "
            "grafico que parece mostrar el doble de altas. La razon no significa nada: una "
            "serie es acumulada y la otra es stock del dia. La desinformacion esta en la "
            "visualizacion, no en los numeros."
        ),
    ),
    Caso(
        "P13", True,
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="5_methodology_change", clases_secundarias="",
        recuperabilidad="A", formato="dataset", abstain_reason="",
        truth_original="contradicted",
        context_original="divergence_detected",
        clase_original="5 - methodology_change (control de comparabilidad)",
        recuperabilidad_original="A/B",
        abstain_reason_original="METHODOLOGY_NOT_COMPARABLE solo si no puede verificarse la homogeneizacion",
        justificacion=(
            "CORRECCION DE ETIQUETA. context pasa de divergence_detected a "
            "no_divergence_detected: el proposito declarado del caso, en su propia columna de "
            "notas, es 'evitar que VERITAI genere falsos positivos simplemente porque detecto "
            "cambio de metodologia'. AEMET recalculo la serie desde 1961, asi que la "
            "comparabilidad se mantiene y NO hay divergencia real. Etiquetarlo "
            "divergence_detected convierte el control en un falso positivo. | "
            "abstain: la condicional se resuelve, la homogeneizacion si esta documentada, "
            "asi que no hay motivo de abstencion."
        ),
        audit_status="verificado",
        audit_notas=(
            "Control de comparabilidad, no caso positivo. Serie de 64 anios (1961-2025) "
            "recalculada con metodologia de rejillas en 2020. El claim de que los registros "
            "empiezan en 2020 es falso; el cambio metodologico no rompio la serie."
        ),
    ),
    Caso(
        "P14", True,
        truth="mixed", context="divergence_detected",
        clase_primaria="3_absolute_vs_relative", clases_secundarias="1_ranking_vs_value",
        recuperabilidad="A", formato="dataset", abstain_reason="METRIC_AMBIGUOUS",
        truth_original="supported approximately",
        context_original="divergence_detected",
        clase_original="1 + 3 - ranking_vs_value / absolute_vs_relative",
        recuperabilidad_original="A",
        abstain_reason_original="Si no se especifica si 'deuda' significa euros o % PIB, mostrar ambos",
        justificacion=(
            "truth: 'supported approximately' no es un valor del enum. x2,76 en euros y x2,37 "
            "en % PIB; ninguno es x3. El orden de magnitud se sostiene y la palabra "
            "'triplicar' no. mixed. | clase: primaria la 3, porque la eleccion euros-vs-%PIB "
            "es la que mueve el multiplicador; la 1 a secundarias por el cambio de posicion."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: euros x2,76 (4.282 -> 11.823 M EUR), % PIB x2,37 (7,5% -> 17,8%). "
            "Ambos coinciden con el Excel."
        ),    ),
    Caso(
        "P15", True,
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="1_ranking_vs_value",
        recuperabilidad="A", formato="dataset", abstain_reason="METRIC_AMBIGUOUS",
        truth_original="contradicted",
        context_original="not_applicable / simple ranking contradiction",
        clase_original="1/3 - ranking/metric ambiguity",
        recuperabilidad_original="A",
        abstain_reason_original="METRIC_AMBIGUOUS si 'lider' no especifica porcentaje o volumen",
        justificacion=(
            "context: no_divergence_detected, corregido por DEC-016. La primera version de "
            "esta auditoria puso not_applicable; Mateo lo revoco: los tests corren y no "
            "encuentran divergencia contextual, el claim es simplemente falso. truth y "
            "context son ejes independientes (R02 10): P15 = contradicted + no_divergence, "
            "P20 = supported + no_divergence. Misma context, distinta truth, y con eso el "
            "FPR es medible. | clase: 'none' porque no hay clase de divergencia; "
            "1_ranking_vs_value en secundarias como la que se habria aplicado."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: Espania 2,6% frente a 4,1% de la UE, 1,5 pp por debajo. Coherencia "
            "interna verificada: 565.400 personas al 2,6% implican 21,7 M de ocupados, que es "
            "el orden correcto para Espania. No lidera ni por tasa ni por volumen."
        ),    ),
    Caso(
        "P16", True,
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="4_denominator",
        recuperabilidad="A", formato="html", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted",
        context_original="no_divergence_detected / calculo literal basta",
        clase_original="3/4 - share / denominator arithmetic",
        recuperabilidad_original="A/B",
        abstain_reason_original="Si no estan disponibles por separado total/pagadas/no pagadas",
        justificacion=(
            "context: el valor doble se resuelve a no_divergence_detected. | clase: 'none' por "
            "la misma razon que P15: el claim es falso por aritmetica, sin divergencia "
            "contextual. | recuperabilidad: A/B resuelto a A, la URL primaria es una tabla "
            "concreta del INE (t=65217), no un portal."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: no pagadas 45,09% del total, pagadas 54,91%. Y las tres cifras del "
            "Excel son mutuamente consistentes: 1.192,7 + 1.452,5 = 2.645,2 exacto. "
            "El claim 'mas de la mitad' es falso por aritmetica: no hace falta LLM."
        ),
    ),
    Caso(
        "P17", True,
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="",
        recuperabilidad="B", formato="dataset", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted / mixed",
        context_original="divergence_detected",
        clase_original="7 + aggregation - subgroup masking",
        recuperabilidad_original="A/B",
        abstain_reason_original="GROUPS_NOT_HOMOGENEOUS si se mezclan rutas con tendencias opuestas",
        justificacion=(
            "truth: mixed y no contradicted. El techo del claim ('hasta el 60%') si se cumple "
            "en una ruta (-67,4% en Canarias), pero el universal ('todas las rutas') es falso "
            "porque el Mediterraneo Occidental sube. | clase: subgroup masking no es una de "
            "las cinco; other_observed. | recuperabilidad: A/B resuelto a B."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: Mediterraneo Occidental +17,0%, Canarias -67,4%, agregado -36,1%. "
            "El claim decia caida de hasta 60% en todas las rutas. Una ruta sube. "
            "Los tres calculos del Excel coinciden."
        ),
        abstain_candidato="GROUPS_NOT_HOMOGENEOUS",
    ),
    Caso(
        "P18", True,
        truth="contradicted", context="divergence_detected",
        clase_primaria="4_denominator", clases_secundarias="other_observed",
        recuperabilidad="B", formato="pdf", abstain_reason="REQUIRED_SLOT_MISSING",
        truth_original="contradicted by scope",
        context_original="divergence_detected",
        clase_original="4/7 - wrong denominator / sample generalization",
        recuperabilidad_original="B",
        abstain_reason_original="SAMPLE_NOT_REPRESENTATIVE",
        justificacion=(
            "truth: 'by scope' es el motivo, no la etiqueta. Va a notas. | clase: 4 primaria; "
            "'sample generalization' a secundarias como other_observed. | "
            "abstain: SAMPLE_NOT_REPRESENTATIVE no existe en el enum; el slot que falta es el "
            "universo de referencia, de ahi REQUIRED_SLOT_MISSING."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: 31% espanioles implica 69% extranjeros, asi que el 69% del claim es "
            "correcto DENTRO de la submuestra. El defecto es el universo: 95 agresores en "
            "grupo desconocidos para la victima, de 2010, presentados como 'todos los varones "
            "imputados en violaciones grupales'."
        ),
        abstain_candidato="SAMPLE_NOT_REPRESENTATIVE",
    ),
    Caso(
        "P19", True,
        truth="mixed", context="divergence_detected",
        clase_primaria="3_absolute_vs_relative", clases_secundarias="",
        recuperabilidad="B", formato="html", abstain_reason="METRIC_AMBIGUOUS",
        truth_original="supported under one metric",
        context_original="divergence_detected",
        clase_original="3 - absolute_vs_relative",
        recuperabilidad_original="A/B",
        abstain_reason_original="METRIC_AMBIGUOUS si no se puede inferir numero vs tasa",
        justificacion=(
            "truth: 'supported under one metric' es la definicion de mixed. | "
            "recuperabilidad: A/B resuelto a B, la URL primaria es la portada del INE y hay "
            "que localizar la tabla de la EPA."
        ),
        audit_status="verificado",
        audit_notas=(
            "Recomputado: la tasa actual (24,5%) esta 7,6 pp por encima del minimo historico "
            "(16,9% en 3T2006). Por numero absoluto el claim puede ser cierto (407.900 "
            "jovenes parados, minimo en absoluto). Cierto o falso segun la metrica."
        ),    ),
    Caso(
        "P20", True,
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="",
        recuperabilidad="A", formato="html", abstain_reason="",
        truth_original="supported",
        context_original="no_divergence_detected",
        clase_original="CONTROL NEGATIVO - correctamente enmarcado",
        recuperabilidad_original="A",
        abstain_reason_original="",
        justificacion=(
            "clase: 'CONTROL NEGATIVO' es una descripcion, no una etiqueta. El valor del enum "
            "para un control negativo es 'none'."
        ),
        audit_status="verificado",
        audit_notas=(
            "UNICO CONTROL NEGATIVO del lote (1 de 20). Recomputado: -0,4 pp interanuales "
            "homogeneos (3,8% a 3,4%). Sin divergencia. Es el unico caso que permite medir "
            "algo de tasa de falsos positivos, y con n=1 no se puede medir."
        ),
    ),
]


# ---------------------------------------------------------------------------
# FASE B - verificacion de las 40 URLs (2026-09-24, 20:59 a 21:06, agente)
#
# Se mantiene en una tabla aparte para que las decisiones de la Fase A sigan
# siendo legibles por si solas. Lo que hay aqui es lo que devolvieron las
# fuentes, no una interpretacion. raw_value_span es texto LITERAL.
#
# Sobre los tiempos: las 36 URLs se consultaron en paralelo, asi que el
# cronometro por caso no tiene sentido. Se registra el reloj de la fase entera
# (~7 minutos, 36 URLs + 8 seguimientos) y cronometrado_por = agente (DEC-014).
# ---------------------------------------------------------------------------

FASE_B: dict[str, dict[str, str]] = {
    "P01": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="no_alcanzable_por_herramienta",
        primaria_url_tipo="informe_pdf_del_emisor",
        access_requires_login="no_verificable",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "Newtral responde 200 a un navegador (curl con User-Agent de Chrome) y 403 al "
            "fetcher: bloqueo de bots, no enlace muerto. EIU no alcanzable con la "
            "herramienta, asi que no se pudo comprobar si exige registro (prediccion 3 "
            "sin resolver)."
        ),
    ),
    "P02": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="200_portal_sin_cifras",
        primaria_url_tipo="portal_interactivo_con_csv",
        access_requires_login="no",
        raw_value_span=(
            "[SECUNDARIA okdiario 21/08/2026] 'Espana se ha pasado de importar 641.072 euros "
            "de este liquido desde el pais del norte de Africa en los primeros seis meses "
            "del 2025 a casi 58 millones de euros en el mismo periodo de este ano' | "
            "'Esto supone un incremento del 8945% en terminos interanuales'"
        ),
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "Euros y 8.945% confirmados en okdiario, que cita DataComex. Pero DataComex "
            "exige consulta interactiva: las cifras del Excel quedan SIN raw_value_span de "
            "la primaria. Y hay un hallazgo: okdiario dice 'casi 19 toneladas' y 'apenas "
            "los 300 kg'; el Excel dice 18.798 t y 276 t. Plausibilidad: 58 M EUR / 19 t = "
            "3.052 EUR/kg, absurdo para aceite a granel; 58 M EUR / 18.798 t = 3,1 EUR/kg, "
            "plausible. Las cifras del Excel son las coherentes: la prosa de okdiario tiene "
            "un error de unidad de x1000. La fuente secundaria se equivoca y la primaria no."
        ),
    ),
    "P03": dict(
        post_url_estado="200_contenido_parcial",
        primaria_url_estado="200_portal_sin_cifras",
        primaria_url_tipo="portal_estadistico",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="DISCREPA",
        status="NEEDS_REVIEW",
        notas_b=(
            "Maldita no cita ninguna publicacion viral concreta: el 'claim' del Excel es el "
            "encuadre del propio verificador ('la delincuencia vuelve a niveles de 2019'). "
            "No hay entrada reproducible del sistema. Portal del Interior vivo; las cifras "
            "exigen navegar hasta la serie."
        ),
    ),
    "P04": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="200_homepage",
        primaria_url_tipo="portada_institucional",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "La URL primaria es la portada del INE (muestra IPC, PIB, tasa de paro "
            "generales): no identifica la tabla de condenados. Maldita confirma el claim de "
            "Sanchez y las cifras 831 / 2.431, pero sin cita literal en la respuesta del "
            "fetcher. Sin raw_value_span."
        ),
    ),
    "P05": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_homepage",
        primaria_url_tipo="portada_institucional",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "URL primaria es la portada del CIS: no identifica ningun barometro. Newtral "
            "bloqueada al fetcher (403), viva para navegador. Sin raw_value_span."
        ),
    ),
    "P06": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_portal_sin_cifras",
        primaria_url_tipo="portal_estadistico",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="parcial",
        notas_b=(
            "Portal del Interior vivo, ofrece 'series anuales desglosadas por comunidades "
            "autonomas y provincias'. Las cifras exigen navegar. Newtral 403 al fetcher."
        ),
    ),
    "P07": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="no_alcanzable",
        primaria_url_tipo="portada_institucional",
        access_requires_login="no_verificable",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "institucionpenitenciaria.es: ECONNREFUSED desde el fetcher y timeout de 15 s "
            "con curl. No alcanzable desde esta red. Ademas la URL es una portada, no la "
            "estadistica mensual. Newtral 403."
        ),
    ),
    "P08": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="403_bloqueo_bot",
        primaria_url_tipo="articulo_cientifico",
        access_requires_login="no_verificable",
        raw_value_span="",
        aritmetica_verificada="si",
        status="fuera_de_alcance",
        notas_b="NEJM devuelve 403 al fetcher. Fuera de alcance por DEC-013; no se insiste.",
    ),
    "P09": dict(
        post_url_estado="200_contenido_parcial",
        primaria_url_estado="403_bloqueo_bot",
        primaria_url_tipo="articulo_cientifico",
        access_requires_login="no_verificable",
        raw_value_span="",
        aritmetica_verificada="no_aplicable",
        status="fuera_de_alcance",
        notas_b="ScienceDirect devuelve 403 al fetcher. Fuera de alcance por DEC-013.",
    ),
    "P10": dict(
        post_url_estado="200_contenido_parcial",
        primaria_url_estado="200_portal_sin_cifras",
        primaria_url_tipo="pagina_indice",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="no_verificable",
        status="NEEDS_REVIEW",
        notas_b=(
            "La URL primaria es la pagina de presentacion con dos botones 'Entrar' hacia "
            "DataComex y DataInvex: no contiene datos. Maldita confirma los claims de "
            "Casado y menciona 20.000 / 7.500 / 14.000 millones, pero como aproximaciones. "
            "Sigue sin haber cifras exactas."
        ),
    ),
    "P11": dict(
        post_url_estado="200_contenido_parcial",
        primaria_url_estado="200_cifras_verificadas",
        primaria_url_tipo="pdf_nota_de_prensa",
        access_requires_login="no",
        raw_value_span=(
            "[INE sm1218.pdf, 8 feb 2019, p.1] 'En diciembre se crean 6.811 sociedades, un "
            "1,1% mas que en el mismo mes de 2017' | [p.11, tabla SM.4 Sociedades creadas "
            "segun clase de sociedad] 'Mayo 8.908 395.469 8.830 393.831 0 0 78 1.638'"
        ),
        aritmetica_verificada="si_pero_dato_a_mal_transcrito",
        status="NEEDS_REVIEW",
        notas_b=(
            "PDF vivo (prediccion 2 de link rot: FALLIDA). Y revela un error del corpus: "
            "8.830 es la columna de sociedades limitadas de mayo; el TOTAL de mayo es 8.908 "
            "(8.830 + 78 anonimas). El 6.811 de diciembre si es el total. El Excel compara "
            "una subcategoria de mayo contra el total de diciembre. Total contra total: "
            "8.908 -> 6.811 = -23,5%, no -22,87%. Curiosamente mas cerca del -23% del "
            "claim. La divergencia (estacionalidad) sigue siendo valida; el Dato A no."
        ),
    ),
    "P12": dict(
        post_url_estado="200_contenido_parcial",
        primaria_url_estado="200_cifras_no_coinciden",
        primaria_url_tipo="pdf_informe_oficial",
        access_requires_login="no",
        raw_value_span=(
            "[Sanidad, Actualizacion n 71, 10.04.2020, datos a 09.04.2020, p.1] "
            "'Madrid 44.783 383,29 12.432(Y) 1.399(Y) 5.972 22.414 906' | nota al pie: "
            "'(Y) Los datos de estas comunidades son datos de prevalencia (personas "
            "ingresadas a fecha de hoy). No reflejan el total'"
        ),
        aritmetica_verificada="no_aplicable",
        status="NEEDS_REVIEW",
        notas_b=(
            "PDF vivo (prediccion 2: FALLIDA). Las cifras del Excel (23.663 curados, 11.894 "
            "hospitalizados) NO estan en la primaria citada, que da 22.414 curados y 12.432 "
            "hospitalizados para Madrid. El propio Excel decia 'p.ej. 23.663 en el grafico': "
            "los numeros vienen del grafico de Ayuso/Aguado, no de la fuente citada. "
            "HALLAZGO POSITIVO: la primaria contiene la advertencia metodologica que explica "
            "el caso, en una nota al pie: los hospitalizados de Madrid son prevalencia, no "
            "acumulado. Un slot methodology_items del EvidenceBundle lo capturaria."
        ),
    ),
    "P13": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="200_soporte_parcial",
        primaria_url_tipo="pagina_de_publicacion_con_pdf",
        access_requires_login="no",
        raw_value_span=(
            "[AEMET, Nota Tecnica 31 'Analisis de las temperaturas en Espana en el periodo "
            "1961-2018'] 'rejillas mensuales de temperatura de alta resolucion para el "
            "periodo 1961-2018'"
        ),
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "NT31 respalda el Dato A (serie desde 1961, rejillas) y con eso basta para "
            "contradecir el claim de '2020'. Pero NO respalda el Dato B: la NT31 cubre "
            "1961-2018 y no menciona 2020 ni recalculo. La afirmacion 'en 2020 cambia el "
            "metodo y recalcula la serie' esta asertada en el Excel sin fuente citada. "
            "Maldita confirma 1961."
        ),
    ),
    "P14": dict(
        post_url_estado="no_alcanzable",
        primaria_url_estado="200_tablas_con_descarga",
        primaria_url_tipo="pagina_de_tablas_csv_xlsx",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="parcial",
        notas_b=(
            "Boletin Estadistico cap. 13 del BdE vivo, con descarga CSV/XLSX. Las cifras de "
            "Galicia estan en las tablas descargables, no en la pagina. Maldita cargo pero "
            "el contenido llego como WebP/base64 ilegible: no se pudo confirmar el claim."
        ),
    ),
    "P15": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_js_verificado_por_api",
        primaria_url_tipo="dataset_con_api_json_stat",
        access_requires_login="no",
        raw_value_span=(
            "[Eurostat API, dataset tqoe3a5, unit=PC sex=T age=15-64 geo=[EU27_2020,ES] "
            "time=[2024,2025]] '\"0\":4.0,\"1\":4.1,\"2\":2.7,\"3\":2.6' -> EU27 2025 = 4,1 ; "
            "ES 2025 = 2,6"
        ),
        aritmetica_verificada="si",
        status="verificado",
        notas_b=(
            "El databrowser HTML es solo JS y no devuelve nada al fetcher. La API de "
            "diseminacion del MISMO publicador y MISMO dataset devuelve JSON-stat con los "
            "dos valores del Excel. El formato real es 'api', no 'dataset'. Newtral 403."
        ),
    ),
    "P16": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_js_verificado_por_api",
        primaria_url_tipo="tabla_concreta_con_api_json",
        access_requires_login="no",
        raw_value_span=(
            "[INE API wstempus, tabla 65217, serie EPA423402 'Asalariados: Total. Total "
            "Nacional. Mujeres. Total. Total. Horas totales', periodo 22 (4T) 2025] "
            "'\"Valor\":2645.2' | [serie EPA423404 no pagadas, 4T 2025] '1192.7'"
        ),
        aritmetica_verificada="si",
        status="verificado",
        notas_b=(
            "La tabla HTML (t=65217) tiene el titulo correcto pero muestra '0 series y 0 "
            "datos' sin JS. La API JSON del INE para la misma tabla devuelve los valores "
            "exactos del Excel. Formato real: 'api'. Newtral 403."
        ),
    ),
    "P17": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_tablas_con_descarga",
        primaria_url_tipo="mapa_con_dataset_mensual",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="parcial",
        notas_b=(
            "Frontex vivo, ofrece 'Detections of illegal border-crossings statistics "
            "download (updated monthly)'. Las cifras por ruta estan en el fichero, no en la "
            "pagina. Con el fichero seria recuperabilidad A. Newtral 403."
        ),
    ),
    "P18": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="403_cloudflare_challenge",
        primaria_url_tipo="pdf_informe_oficial",
        access_requires_login="no_verificable",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b=(
            "interior.gob.es devuelve 403 con cabecera 'Cf-Mitigated: challenge': "
            "Cloudflare exige superar un desafio JS. La pagina existe para un navegador y "
            "no para un fetcher. Maldita confirma el claim de Abascal con 69% y 10%."
        ),
    ),
    "P19": dict(
        post_url_estado="403_bloqueo_bot",
        primaria_url_estado="200_homepage",
        primaria_url_tipo="portada_institucional",
        access_requires_login="no",
        raw_value_span="",
        aritmetica_verificada="si",
        status="NEEDS_REVIEW",
        notas_b="URL primaria es la portada del INE, igual que P04. Newtral 403.",
    ),
    "P20": dict(
        post_url_estado="200_verificado",
        primaria_url_estado="200_cifras_verificadas",
        primaria_url_tipo="nota_oficial_html_con_enlace_a_encuesta",
        access_requires_login="no",
        raw_value_span=(
            "[INEC, 27 abr 2026] 'la tasa de desempleo se ubico en 3,4%, mientras que en el "
            "primer trimestre de 2025 fue de 3,8%'"
        ),
        aritmetica_verificada="si",
        status="verificado",
        notas_b=(
            "Unico caso donde la URL de contenido ES la primaria y ambas cifras aparecen "
            "literalmente. Enlaza a la ENEMDU trimestral. Fecha de publicacion confirmada: "
            "27 de abril de 2026, coincide con el Excel."
        ),
    ),
}

FASE_B_RELOJ = "2026-09-24 20:59-21:06, ~7 min, 36 URLs + 8 seguimientos en paralelo"


def aplicar_fase_b() -> None:
    """Vuelca los resultados de la Fase B sobre los casos de la Fase A."""
    for c in CASOS:
        b = FASE_B[c.case_id]
        c.primaria_url_tipo = b["primaria_url_tipo"]
        c.raw_value_span = b["raw_value_span"]
        c.access_requires_login = b["access_requires_login"]
        c.aritmetica_verificada = b["aritmetica_verificada"]
        c.audit_status = b["status"]
        c.audit_notas = f"{c.audit_notas} || FASE B: {b['notas_b']}"
        c.post_url_estado = b["post_url_estado"]            # type: ignore[attr-defined]
        c.primaria_url_estado = b["primaria_url_estado"]    # type: ignore[attr-defined]
        c.cronometrado_por = "agente"                        # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Validacion de enums
# ---------------------------------------------------------------------------

def validar() -> list[str]:
    """Devuelve la lista de violaciones de enum. Vacia = todo correcto."""
    errores: list[str] = []
    for c in CASOS:
        if c.truth not in TRUTH:
            errores.append(f"{c.case_id}: truth '{c.truth}' fuera de enum")
        if c.context not in CONTEXT:
            errores.append(f"{c.case_id}: context '{c.context}' fuera de enum")
        if c.clase_primaria not in CLASE:
            errores.append(f"{c.case_id}: clase_primaria '{c.clase_primaria}' fuera de enum")
        for sec in filter(None, c.clases_secundarias.split("|")):
            if sec not in CLASE:
                errores.append(f"{c.case_id}: clase secundaria '{sec}' fuera de enum")
        if c.recuperabilidad not in RECUPERABILIDAD:
            errores.append(f"{c.case_id}: recuperabilidad '{c.recuperabilidad}' fuera de enum")
        if c.formato not in FORMATO:
            errores.append(f"{c.case_id}: formato '{c.formato}' fuera de enum")
        if c.abstain_reason not in ABSTAIN:
            errores.append(f"{c.case_id}: abstain_reason '{c.abstain_reason}' fuera de enum")
        if c.audit_status not in AUDIT_STATUS:
            errores.append(f"{c.case_id}: audit_status '{c.audit_status}' fuera de enum")
        # DEC-016: truth y context son ejes independientes y AMBOS van poblados en
        # todas las filas. Sin los dos, la tasa de falsos positivos no se puede medir.
        if not c.truth.strip() or not c.context.strip():
            errores.append(f"{c.case_id}: truth o context vacio; son dos ejes obligatorios")
        if c.post_url_estado not in POST_URL_ESTADO:
            errores.append(f"{c.case_id}: post_url_estado '{c.post_url_estado}' fuera de enum")
        if c.primaria_url_estado not in PRIMARIA_URL_ESTADO:
            errores.append(
                f"{c.case_id}: primaria_url_estado '{c.primaria_url_estado}' fuera de enum"
            )
        if not c.justificacion.strip():
            errores.append(f"{c.case_id}: normalizacion sin justificacion")
        # Regla de trazabilidad del plan: 'verificado' exige raw_value_span de la
        # primaria, y todo NEEDS_REVIEW exige un motivo escrito.
        if c.audit_status == "verificado" and not c.raw_value_span.strip():
            errores.append(f"{c.case_id}: 'verificado' sin raw_value_span")
        if c.audit_status == "verificado" and c.raw_value_span.startswith("[SECUNDARIA"):
            errores.append(f"{c.case_id}: 'verificado' con raw_value_span de fuente secundaria")
        if c.audit_status == "NEEDS_REVIEW" and "FASE B:" not in c.audit_notas:
            errores.append(f"{c.case_id}: NEEDS_REVIEW sin motivo de Fase B")
    return errores


def escribir_csv() -> None:
    campos = [
        "case_id", "en_alcance_tesis",
        "truth", "context", "clase_primaria", "clases_secundarias",
        "recuperabilidad", "formato", "abstain_reason",
        "truth_original", "context_original", "clase_original",
        "recuperabilidad_original", "abstain_reason_original",
        "abstain_candidato",
        "post_url_estado", "primaria_url_estado", "primaria_url_tipo",
        "access_requires_login", "aritmetica_verificada", "raw_value_span",
        "cronometrado_por",
        "audit_status", "audit_notas", "justificacion",
    ]
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for c in CASOS:
            fila = {k: getattr(c, k) for k in campos}
            fila["en_alcance_tesis"] = "si" if c.en_alcance_tesis else "no"
            w.writerow(fila)


def resumen() -> None:
    def cuenta(attr: str) -> dict[str, int]:
        d: dict[str, int] = {}
        for c in CASOS:
            d[getattr(c, attr)] = d.get(getattr(c, attr), 0) + 1
        return dict(sorted(d.items(), key=lambda kv: -kv[1]))

    print("\n--- distribucion despues de normalizar ---")
    for attr in ("truth", "context", "clase_primaria", "recuperabilidad",
                 "formato", "abstain_reason", "audit_status"):
        pares = ", ".join(f"{k or '(null)'}={v}" for k, v in cuenta(attr).items())
        print(f"  {attr:16} {pares}")

    originales_truth = {c.truth_original for c in CASOS}
    print(f"\n  valores distintos de truth: {len(originales_truth)} antes -> "
          f"{len(cuenta('truth'))} despues")

    # DEC-016: la tabla cruzada de los dos ejes. Es lo que hace medible el FPR:
    # la fila context = no_divergence_detected contiene los casos donde el
    # sistema NO debe alertar, y truth dice por que (claim correcto o claim falso).
    print("\n--- truth x context (DEC-016) ---")
    cruce: dict[tuple[str, str], list[str]] = {}
    for c in CASOS:
        cruce.setdefault((c.truth, c.context), []).append(c.case_id)
    for (t, x), ids in sorted(cruce.items()):
        print(f"  {t:13} x {x:24} {len(ids):2}   {' '.join(ids)}")

    candidatos: dict[str, list[str]] = {}
    for c in CASOS:
        if c.abstain_candidato:
            candidatos.setdefault(c.abstain_candidato, []).append(c.case_id)
    print("\n--- candidatos a extender el enum de abstencion ---")
    for nombre, casos in sorted(candidatos.items(), key=lambda kv: -len(kv[1])):
        print(f"  {nombre:28} {len(casos)} caso(s): {', '.join(casos)}")

    en_alcance = sum(1 for c in CASOS if c.en_alcance_tesis)
    print(f"\n  en alcance de tesis: {en_alcance} | fuera: {len(CASOS) - en_alcance}")

    print(f"\n--- Fase B: URLs ({FASE_B_RELOJ}) ---")
    for attr in ("post_url_estado", "primaria_url_estado", "aritmetica_verificada"):
        pares = ", ".join(f"{k}={v}" for k, v in cuenta(attr).items())
        print(f"  {attr:22} {pares}")
    con_span = [c.case_id for c in CASOS
                if c.raw_value_span and not c.raw_value_span.startswith("[SECUNDARIA")]
    print(f"\n  raw_value_span de la PRIMARIA capturado en {len(con_span)} de {len(CASOS)}: "
          f"{', '.join(con_span)}")
    print(f"  post_url ES el verificador en "
          f"{sum(1 for c in CASOS if c.case_id not in ('P02', 'P20'))} de {len(CASOS)}")


def main() -> int:
    print("=" * 88)
    print("  VERITAI - Fases A2/A3/A4 + B: normalizacion a enums cerrados y URLs")
    print("=" * 88)

    aplicar_fase_b()
    errores = validar()
    if errores:
        print("\n  VALORES FUERA DE ENUM:")
        for e in errores:
            print(f"    - {e}")
        return 1

    print(f"\n  {len(CASOS)} casos validados contra los enums de docs/GLOSARIO.md. "
          "Cero valores libres.")
    resumen()
    escribir_csv()
    print(f"\n  Escrito: {SALIDA.relative_to(RAIZ).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
