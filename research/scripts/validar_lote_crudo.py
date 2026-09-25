#!/usr/bin/env python3
"""Valida el lote crudo y emite los tres CSV de la TAREA 2.

    research/pilot-crudo-screening.csv    todos los candidatos, con motivo
    research/pilot-crudo-20.csv           el lote: admitidos trabajados con excedente=no
    research/pilot-crudo-trabajados.csv   todos los admitidos trabajados, excedentes incluidos
                                          (sobre este se calcula la tasa natural, P-16)

Los enums compartidos con la TAREA 1 se IMPORTAN de normalizar_a_enums.py: una
sola definicion, para que PILOT-40 se pueda fusionar sin traducir nada.

Codigo de salida 1 si hay cualquier violacion. Los conteos que imprime son los
que van al informe; el informe no inventa numeros.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from cronometro import leer as leer_cronometro, minutos  # noqa: E402
from lote_crudo import CANDIDATOS  # noqa: E402
from normalizar_a_enums import (  # noqa: E402
    ABSTAIN, CLASE, CONTEXT, FORMATO, RECUPERABILIDAD, TRUTH,
)

RAIZ = AQUI.parents[1]
CSV_SCREENING = RAIZ / "research" / "pilot-crudo-screening.csv"
CSV_LOTE = RAIZ / "research" / "pilot-crudo-20.csv"
CSV_TRABAJADOS = RAIZ / "research" / "pilot-crudo-trabajados.csv"

# ---------------------------------------------------------------------------
# Enums propios de la TAREA 2
# ---------------------------------------------------------------------------

CRIBA_RESULTADO = {"admitido", "rechazado"}
POST_URL_TIPO = {"prensa", "nota_oficial", "declaracion"}
EMISOR_NIVEL = {1, 2, 3, 4, 5}
VIA_DE_ACCESO = {"api", "dataset", "html", "pdf", "scan", "bloqueado", "none"}
SI_NO = {"si", "no"}
ALCANZABLE_HUMANO = {"si", "probable", "no"}
BUCKET = {
    "control_negativo",
    "divergencia_real",
    "primaria_no_localizable",
    "edicion_anterior_no_localizable",
    "formato_hostil",
    # Anadida el 2026-09-25 al aparecer el primer caso (C09): la primaria existe
    # y se sabe donde esta, pero el publicador bloquea al agente (403, desafio
    # JS). DEC-018 prohibe rodearlo. No es "no localizable" ni cabe en ninguna
    # de las cinco cubetas de composicion; se cuenta aparte y sin objetivo. Es
    # justo lo que separa recuperable-por-humano de recuperable-por-agente.
    "bloqueado_por_publicador",
    # Anadida el 2026-09-25 al aparecer el primer caso (C17): un claim FALSO sin
    # divergencia contextual (truth=contradicted, context=no_divergence_detected).
    # No es control negativo (no esta bien enmarcado) ni divergencia (el numero
    # es incorrecto, no el marco). Es la celda que DEC-016 dijo que hace medible
    # el FPR por el eje truth. Sin objetivo de composicion; se cuenta aparte.
    "claim_falso",
}
OBJETIVO_BUCKET = {
    "control_negativo": 7,
    "divergencia_real": 6,
    "primaria_no_localizable": 3,
    "edicion_anterior_no_localizable": 2,
    "formato_hostil": 2,
}
ABANDONO = {"", "localizar", "extraer"}

CAMPOS_CRIBA = [
    "cid", "claim_text", "claim_date", "post_url", "post_url_tipo",
    "emisor", "emisor_tipo", "emisor_nivel", "pais", "tema",
    "criba_query_a", "criba_query_b", "criba_resultado", "criba_motivo",
    "criba_url_verificacion", "case_id",
]

CAMPOS_TRABAJO = [
    "fuente_primaria", "primaria_url", "primaria_url_tipo", "via_de_acceso",
    "access_requires_login",
    "current_edition_found", "previous_edition_found",
    "historical_series_found", "methodology_found",
    "alcanzable_por_agente", "alcanzable_por_humano",
    "recuperabilidad", "formato",
    "dato_actual", "dato_anterior", "raw_value_span_actual", "raw_value_span_anterior",
    "truth", "context", "clase_primaria", "clases_secundarias", "abstain_reason",
    "abandonado_por_tiempo", "bucket_resultado", "excedente", "notas",
]

CAMPOS_LOTE = (
    ["case_id", "cid", "collected_at", "claim_date", "claim_text",
     "emisor", "emisor_tipo", "emisor_nivel", "pais", "tema",
     "post_url", "post_url_tipo", "sin_verificacion_confirmada",
     "criba_query_a", "criba_query_b"]
    + CAMPOS_TRABAJO
    + ["minutes_to_locate", "minutes_to_extract", "cronometrado_por", "etiquetado_por"]
)


def _err(errores: list[str], cid: str, msg: str) -> None:
    errores.append(f"{cid}: {msg}")


def validar() -> list[str]:
    errores: list[str] = []
    vistos_cid: set[str] = set()
    vistos_case: set[str] = set()
    marcas = leer_cronometro()

    for c in CANDIDATOS:
        cid = c.get("cid", "?")
        if cid in vistos_cid:
            _err(errores, cid, "cid repetido")
        vistos_cid.add(cid)

        for campo in CAMPOS_CRIBA[:-1]:
            if campo not in c:
                _err(errores, cid, f"falta '{campo}'")
        if c.get("criba_resultado") not in CRIBA_RESULTADO:
            _err(errores, cid, f"criba_resultado '{c.get('criba_resultado')}' fuera de enum")
        if c.get("post_url_tipo") not in POST_URL_TIPO:
            _err(errores, cid, f"post_url_tipo '{c.get('post_url_tipo')}' fuera de enum")
        if c.get("emisor_nivel") not in EMISOR_NIVEL:
            _err(errores, cid, f"emisor_nivel '{c.get('emisor_nivel')}' fuera de 1-5")
        if not str(c.get("criba_query_a", "")).strip() or not str(c.get("criba_query_b", "")).strip():
            _err(errores, cid, "las dos consultas de criba son obligatorias")

        if c.get("criba_resultado") == "rechazado":
            if not str(c.get("criba_motivo", "")).strip():
                _err(errores, cid, "rechazado sin motivo")
            if "case_id" in c:
                _err(errores, cid, "un rechazado no lleva case_id")
            continue

        # --- admitido: campos de trabajo -------------------------------------
        case_id = c.get("case_id")
        if not case_id:
            _err(errores, cid, "admitido sin case_id")
            continue
        if case_id in vistos_case:
            _err(errores, cid, f"case_id {case_id} repetido")
        vistos_case.add(case_id)

        # Un admitido sin NINGUN campo de trabajo esta pendiente: se cuenta, no
        # se penaliza. Un admitido con algunos campos y otros no, es un error.
        presentes = [campo for campo in CAMPOS_TRABAJO if campo in c]
        if not presentes:
            continue
        if len(presentes) < len(CAMPOS_TRABAJO):
            faltan = [campo for campo in CAMPOS_TRABAJO if campo not in c]
            _err(errores, case_id, f"trabajo incompleto, faltan: {', '.join(faltan)}")
            continue

        if c["via_de_acceso"] not in VIA_DE_ACCESO:
            _err(errores, case_id, f"via_de_acceso '{c['via_de_acceso']}' fuera de enum")
        for campo in ("current_edition_found", "previous_edition_found",
                      "historical_series_found", "methodology_found",
                      "alcanzable_por_agente", "excedente"):
            if c[campo] not in SI_NO:
                _err(errores, case_id, f"{campo} '{c[campo]}' debe ser si/no")
        if c["alcanzable_por_humano"] not in ALCANZABLE_HUMANO:
            _err(errores, case_id, f"alcanzable_por_humano '{c['alcanzable_por_humano']}' fuera de enum")
        if c["recuperabilidad"] not in RECUPERABILIDAD:
            _err(errores, case_id, f"recuperabilidad '{c['recuperabilidad']}' fuera de enum")
        if c["formato"] not in FORMATO:
            _err(errores, case_id, f"formato '{c['formato']}' fuera de enum")
        if c["truth"] not in TRUTH or not c["truth"]:
            _err(errores, case_id, f"truth '{c['truth']}' fuera de enum o vacio")
        if c["context"] not in CONTEXT or not c["context"]:
            _err(errores, case_id, f"context '{c['context']}' fuera de enum o vacio")
        if c["clase_primaria"] not in CLASE:
            _err(errores, case_id, f"clase_primaria '{c['clase_primaria']}' fuera de enum")
        for sec in filter(None, str(c["clases_secundarias"]).split("|")):
            if sec not in CLASE:
                _err(errores, case_id, f"clase secundaria '{sec}' fuera de enum")
        if c["abstain_reason"] not in ABSTAIN:
            _err(errores, case_id, f"abstain_reason '{c['abstain_reason']}' fuera de enum")
        if c["abandonado_por_tiempo"] not in ABANDONO:
            _err(errores, case_id, f"abandonado_por_tiempo '{c['abandonado_por_tiempo']}' fuera de enum")
        if c["bucket_resultado"] not in BUCKET:
            _err(errores, case_id, f"bucket_resultado '{c['bucket_resultado']}' fuera de enum")

        # --- reglas de trazabilidad --------------------------------------------
        if c["previous_edition_found"] == "si" and not str(c["raw_value_span_anterior"]).strip():
            _err(errores, case_id, "previous_edition_found=si sin raw_value_span_anterior")
        if c["current_edition_found"] == "si" and not str(c["raw_value_span_actual"]).strip():
            _err(errores, case_id, "current_edition_found=si sin raw_value_span_actual")
        if c["via_de_acceso"] == "bloqueado" and c["alcanzable_por_agente"] != "no":
            _err(errores, case_id, "bloqueado implica alcanzable_por_agente=no (DEC-018)")
        if c["via_de_acceso"] == "bloqueado" and c["bucket_resultado"] == "primaria_no_localizable":
            _err(errores, case_id, "bloqueado NO es primaria_no_localizable: son columnas distintas")
        if c["previous_edition_found"] == "no" and c["bucket_resultado"] == "divergencia_real":
            _err(errores, case_id, "divergencia_real exige edicion anterior localizada")
        if c["bucket_resultado"] == "control_negativo" and not (
            c["truth"] == "supported" and c["context"] == "no_divergence_detected"
        ):
            _err(errores, case_id, "control_negativo exige supported + no_divergence_detected")
        if c["abandonado_por_tiempo"] and not str(c["notas"]).strip():
            _err(errores, case_id, "abandonado sin motivo en notas")

        # --- cronometro ---------------------------------------------------------
        hitos = marcas.get(case_id, {})
        if not {"t0", "t1", "t2"} <= hitos.keys():
            _err(errores, case_id, f"faltan hitos en cronometro.log: tiene {sorted(hitos)}")

    # --- cubetas: objetivo, sin contar excedentes ---------------------------------
    admitidos = [c for c in CANDIDATOS if c.get("criba_resultado") == "admitido"
                 and "bucket_resultado" in c]
    en_lote = [c for c in admitidos if c.get("excedente") == "no"]
    por_bucket = Counter(c["bucket_resultado"] for c in en_lote)
    for b, objetivo in OBJETIVO_BUCKET.items():
        if por_bucket.get(b, 0) > objetivo:
            _err(errores, b, f"{por_bucket[b]} en lote supera el objetivo {objetivo}; sobrantes deben ir a excedente")

    return errores


def fila_screening(c: dict) -> dict:
    return {k: c.get(k, "") for k in CAMPOS_CRIBA}


def fila_lote(c: dict) -> dict:
    loc, ext = minutos(c["case_id"])
    f = {k: c.get(k, "") for k in CAMPOS_LOTE}
    f["sin_verificacion_confirmada"] = "si"
    f["minutes_to_locate"] = f"{loc:.1f}" if loc is not None else ""
    f["minutes_to_extract"] = f"{ext:.1f}" if ext is not None else ""
    f["cronometrado_por"] = "agente"
    f["etiquetado_por"] = "agente_provisional"
    return f


def escribir() -> None:
    with CSV_SCREENING.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_CRIBA, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for c in CANDIDATOS:
            w.writerow(fila_screening(c))
    admitidos = [c for c in CANDIDATOS if c.get("criba_resultado") == "admitido" and "case_id" in c]
    trabajados = [c for c in admitidos if c.get("bucket_resultado")]
    # El lote son los que NO son excedente; los excedentes van al CSV de trabajados,
    # que es el denominador de la tasa natural (P-16). Un admitido sin trabajar no
    # entra en ninguno de los dos.
    for ruta, filas in ((CSV_LOTE, [c for c in trabajados if c.get("excedente") == "no"]),
                        (CSV_TRABAJADOS, trabajados)):
        with ruta.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=CAMPOS_LOTE, quoting=csv.QUOTE_ALL)
            w.writeheader()
            for c in filas:
                w.writerow(fila_lote(c))


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:5.1f}%" if d else "   -- "


def resumen() -> None:
    total = len(CANDIDATOS)
    rech = [c for c in CANDIDATOS if c.get("criba_resultado") == "rechazado"]
    adm = [c for c in CANDIDATOS if c.get("criba_resultado") == "admitido"]
    trabajados = [c for c in adm if "bucket_resultado" in c]
    lote = [c for c in trabajados if c.get("excedente") == "no"]

    print("\n--- criba ---")
    pendientes = len(adm) - len(trabajados)
    print(f"  candidatos {total} | rechazados {len(rech)} ({pct(len(rech), total)}) | "
          f"admitidos {len(adm)} | trabajados {len(trabajados)} | pendientes {pendientes}")
    for motivo, n in Counter(c["criba_motivo"].split(":")[0] for c in rech).most_common():
        print(f"    rechazo: {motivo:40} {n}")

    print("\n--- cubetas (en lote, sin excedentes) ---")
    por_bucket = Counter(c["bucket_resultado"] for c in lote)
    for b, obj in OBJETIVO_BUCKET.items():
        print(f"  {b:34} {por_bucket.get(b, 0):2} / {obj}")
    for b, n in por_bucket.items():
        if b not in OBJETIVO_BUCKET:
            print(f"  {b:34} {n:2}   (sin objetivo, se cuenta aparte)")
    exc = Counter(c["bucket_resultado"] for c in trabajados if c.get("excedente") == "si")
    if exc:
        print("  excedentes:", dict(exc))

    if lote:
        n = len(lote)
        print(f"\n--- LAS DOS METRICAS (sobre {n} en lote) ---")
        prev = sum(1 for c in lote if c["previous_edition_found"] == "si")
        print(f"  edicion anterior localizada           {prev:2}/{n}  {pct(prev, n)}")
        ag = sum(1 for c in lote if c["alcanzable_por_agente"] == "si")
        hu = sum(1 for c in lote if c["alcanzable_por_humano"] in ("si", "probable"))
        prev_ag = sum(1 for c in lote if c["previous_edition_found"] == "si" and c["alcanzable_por_agente"] == "si")
        print(f"  recuperable-por-agente (anterior+alc.) {prev_ag:2}/{n}  {pct(prev_ag, n)}   <- DECIDE")
        print(f"  alcanzable_por_agente                  {ag:2}/{n}  {pct(ag, n)}")
        print(f"  alcanzable_por_humano (si|probable)    {hu:2}/{n}  {pct(hu, n)}")

        print("\n--- por nivel de emisor ---")
        for nivel in sorted({c["emisor_nivel"] for c in lote}):
            sub = [c for c in lote if c["emisor_nivel"] == nivel]
            p = sum(1 for c in sub if c["previous_edition_found"] == "si")
            locs = [minutos(c["case_id"])[0] for c in sub]
            locs = [x for x in locs if x is not None]
            media = f"{sum(locs)/len(locs):5.1f} min" if locs else "  -- "
            print(f"  nivel {nivel}: {len(sub):2} casos | anterior {p}/{len(sub)} | localizar medio {media}")

        print("\n--- clases en divergencia_real (P-15) ---")
        div = [c for c in lote if c["bucket_resultado"] == "divergencia_real"]
        for k, v in Counter(c["clase_primaria"] for c in div).most_common():
            print(f"  {k:28} {v}")

        print("\n--- truth x context ---")
        for (t, x), v in sorted(Counter((c["truth"], c["context"]) for c in lote).items()):
            print(f"  {t:13} x {x:24} {v}")

        print("\n--- via de acceso / abandono ---")
        print("  via:", dict(Counter(c["via_de_acceso"] for c in lote)))
        print("  abandonados por tiempo:", dict(Counter(c["abandonado_por_tiempo"] for c in lote if c["abandonado_por_tiempo"])) or "ninguno")


def main() -> int:
    print("=" * 84)
    print("  VERITAI - TAREA 2: validacion del lote crudo")
    print("=" * 84)
    errores = validar()
    if errores:
        print("\n  VIOLACIONES:")
        for e in errores:
            print(f"    - {e}")
        return 1
    print(f"\n  {len(CANDIDATOS)} candidatos validados. Cero valores fuera de enum.")
    resumen()
    escribir()
    print(f"\n  Escritos: {CSV_SCREENING.name}, {CSV_LOTE.name}, {CSV_TRABAJADOS.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
