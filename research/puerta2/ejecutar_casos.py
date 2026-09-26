#!/usr/bin/env python3
"""Puerta 2: ejecuta los casos de research/puerta2/casos/*.json contra la API y
guarda la trazabilidad completa.

POR QUE UN SCRIPT Y NO CURL A MANO
    Los 10 casos tienen que correr igual cada vez y dejar rastro: la respuesta
    completa de cada uno (veredicto + evidencia con spans) en resultados/, un
    CSV con una fila por caso y una tabla en Markdown que el informe pega tal
    cual. Ningun numero del informe se teclea.

USO
    docker compose up -d
    python research/puerta2/ejecutar_casos.py [--api http://127.0.0.1:8000] [--solo C16]

Los casos son de DESARROLLO (DEC-025): sirven para construir y depurar el
prototipo, nunca para evaluarlo.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CASOS = AQUI / "casos"
RESULTADOS = AQUI / "resultados"
CSV = AQUI / "resultados.csv"
MD = AQUI / "resultados.md"

COLUMNAS = [
    "case_id", "origen", "tipo", "truth", "context", "clase_primaria", "abstain_reasons",
    "test_aplicable", "test_disparo", "test_subtipo", "corpus_truth", "corpus_context",
    "corpus_clase", "acuerdo_truth", "acuerdo_context", "completeness", "missing_slots",
    "n_items", "bundle_hash", "duracion_ms", "http",
]


def analizar(api: str, caso: dict) -> tuple[int, dict]:
    cuerpo = {k: v for k, v in caso.items() if not k.startswith("_")}
    req = urllib.request.Request(
        f"{api}/analisis", data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.load(exc)
        except Exception:  # noqa: BLE001
            return exc.code, {"error": exc.reason}


def fila(caso: dict, estado: int, resp: dict) -> dict:
    v = resp.get("veredicto", {})
    e = resp.get("evidencia", {})
    t = (v.get("tests") or [{}])[0]
    corpus = caso.get("etiquetas_corpus", {})
    return {
        "case_id": caso["claim_id"], "origen": caso.get("origen_case_id", ""), "tipo": caso["tipo"],
        "truth": v.get("truth", ""), "context": v.get("context", ""),
        "clase_primaria": v.get("clase_primaria", ""),
        "abstain_reasons": "|".join(v.get("abstain_reasons", [])),
        "test_aplicable": t.get("aplicable", ""), "test_disparo": t.get("disparo", ""),
        "test_subtipo": t.get("subtipo", ""),
        "corpus_truth": corpus.get("truth", ""), "corpus_context": corpus.get("context", ""),
        "corpus_clase": corpus.get("clase_primaria", ""),
        "acuerdo_truth": "" if not corpus else str(v.get("truth") == corpus.get("truth")).lower(),
        "acuerdo_context": "" if not corpus else str(v.get("context") == corpus.get("context")).lower(),
        "completeness": e.get("completeness", ""), "missing_slots": "|".join(e.get("missing_slots", [])),
        "n_items": len(e.get("items", [])), "bundle_hash": (e.get("bundle_hash") or "")[:12],
        "duracion_ms": resp.get("duracion_ms", ""), "http": estado,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:8000")
    ap.add_argument("--solo", default="", help="case_id concreto")
    args = ap.parse_args()

    RESULTADOS.mkdir(exist_ok=True)
    filas: list[dict] = []
    for ruta in sorted(CASOS.glob("*.json")):
        caso = json.loads(ruta.read_text(encoding="utf-8"))
        if args.solo and caso["claim_id"] != args.solo:
            continue
        estado, resp = analizar(args.api, caso)
        (RESULTADOS / f"{caso['claim_id']}.json").write_text(
            json.dumps({"http": estado, "caso": caso, "respuesta": resp}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        f = fila(caso, estado, resp)
        filas.append(f)
        print(f"{f['case_id']:5} {estado} {f['truth']:22} {f['context']:24} {f['clase_primaria']:22} "
              f"{f['abstain_reasons'][:40]:40} {f['duracion_ms']} ms")

    if not filas:
        print("sin casos"); return 1
    with CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(filas)
    lineas = ["| caso | origen | tipo | truth | context | clase | abstención | test 2a | corpus (truth/context/clase) | acuerdo | ms |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for f in filas:
        test = "n/a" if f["test_aplicable"] in ("", False) else ("DISPARA " + f["test_subtipo"] if f["test_disparo"] else "no dispara")
        corpus = f"{f['corpus_truth']} / {f['corpus_context']} / {f['corpus_clase']}" if f["corpus_truth"] else "—"
        acuerdo = f"{f['acuerdo_truth']} / {f['acuerdo_context']}" if f["corpus_truth"] else "—"
        lineas.append(f"| {f['case_id']} | {f['origen']} | {f['tipo']} | {f['truth']} | {f['context']} | "
                      f"{f['clase_primaria']} | {f['abstain_reasons'] or '—'} | {test} | {corpus} | {acuerdo} | {f['duracion_ms']} |")
    MD.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    n = len(filas)
    print(f"\n{n} casos. truth: {dict((k, sum(1 for f in filas if f['truth']==k)) for k in sorted({f['truth'] for f in filas}))}")
    print(f"context: {dict((k, sum(1 for f in filas if f['context']==k)) for k in sorted({f['context'] for f in filas}))}")
    con_corpus = [f for f in filas if f["corpus_truth"]]
    if con_corpus:
        print(f"acuerdo con el corpus: truth {sum(1 for f in con_corpus if f['acuerdo_truth']=='true')}/{len(con_corpus)}, "
              f"context {sum(1 for f in con_corpus if f['acuerdo_context']=='true')}/{len(con_corpus)}")
    print(f"escritos: {CSV.name}, {MD.name}, resultados/*.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
