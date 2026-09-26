#!/usr/bin/env python3
"""Genera los 7 casos de DESARROLLO de la Puerta 2 que vienen del piloto (todos
con primaria INE), como JSON para POST /analisis.

El claim se estructura A MANO (START-HERE §18): aqui esta esa mano, escrita y
versionada. Texto, URL y etiquetas del corpus salen de research/PILOT-40.csv;
la estructura (tipo, metrica, periodos, valores afirmados) es la lectura del
titular que el sistema recibe. Ningun valor de la primaria entra aqui: los
recupera el conector.

Por que estos siete y no diez: son TODOS los casos del piloto cuya primaria es
el INE (DEC-024). Los otros tres se recolectan aparte (research/puerta2/casos/N01-N03).
Todos son conjunto=desarrollo (DEC-025): nunca evaluan.

Series y tablas, verificadas contra la API Tempus el 2026-09-25:
    65334  Tasa de paro por grupo de edad (EPA)        EPA452436 menores de 25, nacional
    25333  IPC, indices nacionales                     IPC290750 general, variacion anual
    13913  Sociedades mercantiles constituidas         SM21483  total nacional mercantiles
    28724  Personas condenadas por delitos sexuales    CON48031 total nacional (2017-2025)
    65217  EPA horas extra por ocupacion y sexo        EPA423404 mujeres, no pagadas, total
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CASOS = Path(__file__).resolve().parent / "casos"
PILOT40 = RAIZ / "research" / "PILOT-40.csv"

PARO_JUVENIL = {
    "emisor": "INE", "tabla": "65334",
    "serie_nombre": "Tasa de paro de la población. Ambos sexos. Total Nacional. Menores de 25 años. ",
    "unidad": "pct", "referencia_principal": "anterior",
    "descripcion": "EPA, tasa de paro de menores de 25 años, ambos sexos, total nacional",
}

ESTRUCTURA: dict[str, dict] = {
    "C11": {
        "tipo": "nivel",
        "metrica": {"emisor": "INE", "tabla": "25333",
                    "serie_nombre": "Nacional. Índice general. Variación anual. ", "unidad": "pct",
                    "referencia_principal": "anterior",
                    "descripcion": "IPC general, variacion anual, nacional (base 2025)"},
        "periodo_objetivo": "2026-M08", "valor_objetivo": 4.3,
        "notas": ("Claim de NIVEL: el 4,3% es la variacion anual publicada. 'La mas alta en mas de tres "
                  "anos' es un extremo historico que este prototipo no evalua; el test 2a no aplica."),
    },
    "C16": {
        "tipo": "cambio_entre_periodos", "metrica": PARO_JUVENIL,
        "periodo_objetivo": "2026-T2", "periodo_base": "2026-T1",
        "valor_objetivo": 23.77, "cambio_afirmado": -0.77, "unidad_cambio": "pp",
        "direccion_afirmada": "baja",
        "notas": "Control negativo del piloto: cae 0,77 pp del 1T al 2T; la base es la referencia del emisor.",
    },
    "C17": {
        "tipo": "cambio_entre_periodos", "metrica": PARO_JUVENIL,
        "periodo_objetivo": "2026-T2", "periodo_base": "2026-T1",
        "valor_objetivo": 24.5, "direccion_afirmada": "sube",
        "notas": ("Claim falso del piloto: 24,5% es el valor del 1T; en el 2T la serie da 23,77 y baja. "
                  "El corpus lo etiqueta contradicted / no_divergence (claim_falso); el test 2a puede "
                  "disparar por 'valor atribuido a otro periodo': se compara y se reporta."),
    },
    "P11": {
        "tipo": "cambio_entre_periodos",
        "metrica": {"emisor": "INE", "tabla": "13913",
                    "serie_nombre": "Sociedades Constituídas. Número de Sociedades. Total Nacional. Mercantiles. ",
                    "unidad": "unidades", "referencia_principal": "interanual",
                    "descripcion": "Sociedades mercantiles constituidas, total nacional, mensual"},
        "periodo_objetivo": "2018-M12", "periodo_base": "2018-M05",
        "cambio_afirmado": -23, "unidad_cambio": "pct", "direccion_afirmada": "baja",
        "notas": ("El unico 2a del piloto con primaria INE. El claim (marzo 2019) compara mayo con diciembre "
                  "de 2018; diciembre es un mes bajo y la referencia del INE es interanual. La API de hoy "
                  "da mayo 2018 = 8.830 y diciembre 2018 = 6.809; el PDF de febrero de 2019 daba 8.908 "
                  "(total) / 8.830 (S.L.) y 6.811: la serie fue REVISADA. Se registra tal cual."),
    },
    "P04": {
        "tipo": "crecimiento_compuesto",
        "metrica": {"emisor": "INE", "tabla": "28724",
                    "serie_nombre": "Total Nacional. Dato base. Por delitos sexuales. ", "unidad": "unidades",
                    "referencia_principal": "anterior",
                    "descripcion": "Personas condenadas por delitos sexuales, total nacional, anual"},
        "periodo_objetivo": "2018", "periodo_base": "1998",
        "cambio_afirmado": 10, "unidad_cambio": "pct", "direccion_afirmada": "sube",
        "notas": ("'Un 10% al ano desde 1998' es crecimiento compuesto: fuera de lo que este prototipo evalua "
                  "(UNSUPPORTED_CLAIM_TYPE). Ademas la tabla Tempus empieza en 2017: 1998 no esta."),
    },
    "P16": {
        "tipo": "umbral",
        "metrica": {"emisor": "INE", "tabla": "65217",
                    "serie_nombre": "Asalariados : Total. Total Nacional. Mujeres. Total. Horas extra no pagadas. Horas totales. ",
                    "unidad": "miles_horas", "referencia_principal": "anterior",
                    "descripcion": "EPA, horas extra no pagadas de mujeres asalariadas, total"},
        "periodo_objetivo": "2025-T4",
        "notas": ("'Mas de la mitad' exige dividir dos series (no pagadas / totales): umbral con "
                  "denominador. Fuera de lo que este prototipo evalua (UNSUPPORTED_CLAIM_TYPE)."),
    },
    "P19": {
        "tipo": "extremo_historico", "metrica": PARO_JUVENIL,
        "periodo_objetivo": "2026-T1",
        "notas": ("'El menor paro juvenil de la historia' es un extremo historico y ademas ambiguo entre "
                  "tasa y numero absoluto (METRIC_AMBIGUOUS en el corpus). Fuera del prototipo."),
    },
}


def main() -> int:
    filas = {r["case_id"]: r for r in csv.DictReader(PILOT40.open(encoding="utf-8"))}
    CASOS.mkdir(parents=True, exist_ok=True)
    for case_id, estructura in ESTRUCTURA.items():
        r = filas[case_id]
        caso = {
            "claim_id": case_id, "texto": r["claim_text"], "fuente_url": r["post_url"],
            "conjunto": "desarrollo", "origen_case_id": case_id,
            "etiquetas_corpus": {"truth": r["truth"], "context": r["context"],
                                 "clase_primaria": r["clase_primaria"], "lote": r["lote"]},
            **estructura,
        }
        (CASOS / f"{case_id}.json").write_text(json.dumps(caso, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
        print(f"{case_id}: {caso['tipo']:24} {caso['metrica']['tabla']:6} {r['claim_text'][:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
