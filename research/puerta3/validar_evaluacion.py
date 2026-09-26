#!/usr/bin/env python3
"""Valida el conjunto de evaluacion (lote_evaluacion.py) y emite sus salidas.

    research/puerta3/evaluacion-candidatos.csv   todos los candidatos, con criba
    research/puerta3/evaluacion-anotacion.csv    admitidos y trabajados (la ANOTACION)
    research/puerta3/casos/<E###>.json           la estructura que recibe POST /analisis,
                                                 sin etiquetas (la anotacion va aparte)

Imprime el llenado de cubetas contra el diseno (DEC-031), el n efectivo sin
hermanos, el reparto por emisor y por edicion primaria, y la proyeccion al
tope de cuatro jornadas con el ritmo real del cronometro. Sale 1 si hay una
violacion. Ningun numero del informe se teclea: sale de aqui.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / "research" / "scripts"))

from cronometro import leer as leer_cronometro, minutos  # noqa: E402
from lote_evaluacion import CANDIDATOS, OBJETIVO_CUBETA  # noqa: E402
from normalizar_a_enums import ABSTAIN, CLASE, CONTEXT, FORMATO, RECUPERABILIDAD, TRUTH  # noqa: E402
from validar_lote_crudo import (  # noqa: E402
    ALCANZABLE_HUMANO,
    BUCKET,
    CAMPOS_CRIBA,
    CAMPOS_TRABAJO,
    CRIBA_RESULTADO,
    EMISOR_NIVEL,
    POST_URL_TIPO,
    SI_NO,
    VIA_DE_ACCESO,
)

CSV_CANDIDATOS = AQUI / "evaluacion-candidatos.csv"
CSV_ANOTACION = AQUI / "evaluacion-anotacion.csv"
CASOS = AQUI / "casos"
PILOT40 = RAIZ / "research" / "PILOT-40.csv"
PUERTA2_CASOS = RAIZ / "research" / "puerta2" / "casos"

JORNADA_HORAS = 4.0
TOPE_JORNADAS = 4
MARCA_INICIO = "P3-J1"

CAMPOS_EXTRA = ["cubeta", "hermano_de", "mecanismo_candidato", "primaria_edicion", "conjunto"]
CAMPOS_ANOTACION = (
    ["case_id", "cid", "collected_at", "claim_date", "claim_text",
     "emisor", "emisor_tipo", "emisor_nivel", "pais", "tema",
     "post_url", "post_url_tipo", "sin_verificacion_confirmada",
     "criba_query_a", "criba_query_b", "descubrimiento_via", "descubrimiento_query"]
    + CAMPOS_TRABAJO
    + CAMPOS_EXTRA
    + ["minutes_to_locate", "minutes_to_extract", "cronometrado_por", "etiquetado_por"]
)
MECANISMOS = {"", "P17_agregacion_subgrupos", "C10_cambio_sin_edicion_anterior", "otro"}
# Vias de descubrimiento (DEC-020, DEC-032): las del lote crudo mas `titular_prensa`
# (via divergencia: titulares con cifra y comparacion propia, primaria despues).
VIAS = {
    "busqueda_a_organismo", "titular_prensa", "busqueda_de_rankings",
    "busqueda_de_encuestas", "busqueda_por_tema", "criba_negativa",
}
TIPOS = {"cambio_entre_periodos", "nivel", "umbral", "extremo_historico", "crecimiento_compuesto", "otro"}


def _err(errores: list[str], quien: str, msg: str) -> None:
    errores.append(f"{quien}: {msg}")


def _prohibidos() -> tuple[set[str], set[str]]:
    """URLs y textos del piloto y de la Puerta 2: no entran (DEC-025)."""
    urls, textos = set(), set()
    if PILOT40.exists():
        for f in csv.DictReader(PILOT40.open(encoding="utf-8")):
            urls.add(f["post_url"].strip()); textos.add(f["claim_text"].strip().lower())
    for ruta in PUERTA2_CASOS.glob("*.json"):
        c = json.loads(ruta.read_text(encoding="utf-8"))
        urls.add(c["fuente_url"].strip()); textos.add(c["texto"].strip().lower())
    return urls, textos


def validar(marcas: dict) -> list[str]:
    errores: list[str] = []
    urls_pro, textos_pro = _prohibidos()
    cids, case_ids, urls = Counter(), Counter(), Counter()
    for c in CANDIDATOS:
        q = c.get("cid", "?")
        cids[q] += 1
        for campo in CAMPOS_CRIBA:
            if campo != "case_id" and campo not in c:
                _err(errores, q, f"falta {campo}")
        if c.get("criba_resultado") not in CRIBA_RESULTADO:
            _err(errores, q, f"criba_resultado invalido: {c.get('criba_resultado')!r}")
        if c.get("post_url_tipo") not in POST_URL_TIPO:
            _err(errores, q, f"post_url_tipo invalido: {c.get('post_url_tipo')!r}")
        if c.get("emisor_nivel") not in EMISOR_NIVEL:
            _err(errores, q, f"emisor_nivel invalido: {c.get('emisor_nivel')!r}")
        if c.get("descubrimiento_via") not in VIAS:
            _err(errores, q, f"descubrimiento_via fuera de enum: {c.get('descubrimiento_via')!r}")
        urls[c.get("post_url", "")] += 1
        if c.get("post_url", "").strip() in urls_pro or c.get("claim_text", "").strip().lower() in textos_pro:
            _err(errores, q, "esta en el piloto o en la Puerta 2: no entra (DEC-025)")
        if c.get("criba_resultado") == "rechazado":
            if not c.get("criba_motivo"):
                _err(errores, q, "rechazado sin motivo")
            if "case_id" in c:
                _err(errores, q, "rechazado con case_id")
            continue
        if "case_id" not in c:
            continue  # admitido, aun sin trabajar
        e = c["case_id"]
        case_ids[e] += 1
        for campo in CAMPOS_TRABAJO + CAMPOS_EXTRA:
            if campo not in c:
                _err(errores, e, f"falta {campo}")
        if errores and errores[-1].startswith(e + ": falta "):
            continue
        # enums
        for campo, dominio in (("truth", TRUTH), ("context", CONTEXT), ("clase_primaria", CLASE),
                               ("recuperabilidad", RECUPERABILIDAD), ("formato", FORMATO),
                               ("via_de_acceso", VIA_DE_ACCESO), ("bucket_resultado", BUCKET),
                               ("alcanzable_por_humano", ALCANZABLE_HUMANO)):
            if c[campo] not in dominio:
                _err(errores, e, f"{campo} fuera de enum: {c[campo]!r}")
        for campo in ("access_requires_login", "current_edition_found", "previous_edition_found",
                      "historical_series_found", "methodology_found", "alcanzable_por_agente", "excedente"):
            if c[campo] not in SI_NO:
                _err(errores, e, f"{campo} debe ser si/no: {c[campo]!r}")
        for motivo in filter(None, c["abstain_reason"].split("|")):
            if motivo not in ABSTAIN:
                _err(errores, e, f"abstain_reason fuera de enum: {motivo!r}")
        if c["cubeta"] not in OBJETIVO_CUBETA:
            _err(errores, e, f"cubeta invalida: {c['cubeta']!r}")
        if c["mecanismo_candidato"] not in MECANISMOS:
            _err(errores, e, f"mecanismo_candidato invalido: {c['mecanismo_candidato']!r}")
        if c["conjunto"] != "evaluacion":
            _err(errores, e, "conjunto debe ser 'evaluacion'")
        # coherencia con la cubeta (DEC-031)
        cub, t, ctx, cl = c["cubeta"], c["truth"], c["context"], c["clase_primaria"]
        est = c.get("estructura")
        if cub == "A" and not (t == "supported" and ctx == "no_divergence_detected" and cl == "none"
                               and est and est.get("tipo") == "cambio_entre_periodos" and est.get("periodo_base")):
            _err(errores, e, "cubeta A exige supported + no_divergence + none + cambio_entre_periodos con base")
        if cub == "B" and not (ctx == "divergence_detected" and cl == "2_baseline_selection"):
            _err(errores, e, "cubeta B exige divergence_detected + 2_baseline_selection")
        if cub == "C" and not (ctx == "divergence_detected" and cl in
                               {"3_absolute_vs_relative", "4_denominator", "5_methodology_change",
                                "2b_base_revisada", "1_ranking_vs_value"}):
            _err(errores, e, "cubeta C exige divergence_detected con clase 3, 4, 2b, 2c o 1")
        if cub == "O" and not (ctx == "divergence_detected" and cl == "other_observed" and c["mecanismo_candidato"]):
            _err(errores, e, "cubeta O exige divergence_detected + other_observed + mecanismo_candidato")
        if cub == "D" and not (ctx == "undetermined" and est and est.get("tipo") != "cambio_entre_periodos"):
            _err(errores, e, "cubeta D exige undetermined y un tipo sin test aplicable")
        if cub == "E" and not (c["current_edition_found"] == "no" or c["previous_edition_found"] == "no"
                               or c["via_de_acceso"] == "bloqueado"):
            _err(errores, e, "cubeta E exige primaria o edicion anterior no localizada, o bloqueo")
        if cub == "F" and not (t == "contradicted" and ctx == "no_divergence_detected"):
            _err(errores, e, "cubeta F exige contradicted + no_divergence_detected")
        if ctx == "no_divergence_detected" and cl != "none":
            _err(errores, e, "no_divergence_detected con clase distinta de none")
        if ctx == "divergence_detected" and cl in ("none", ""):
            _err(errores, e, "divergence_detected sin clase")
        if c["via_de_acceso"] == "bloqueado" and c["alcanzable_por_agente"] != "no":
            _err(errores, e, "bloqueado implica alcanzable_por_agente=no (DEC-018)")
        if c["current_edition_found"] == "si" and not str(c["raw_value_span_actual"]).strip():
            _err(errores, e, "current_edition_found=si sin raw_value_span_actual")
        if est is not None:
            if est.get("tipo") not in TIPOS:
                _err(errores, e, f"estructura.tipo invalido: {est.get('tipo')!r}")
            for campo in ("metrica", "periodo_objetivo"):
                if not est.get(campo):
                    _err(errores, e, f"estructura sin {campo}")
        hitos = marcas.get(e, {})
        if not {"t0", "t1", "t2"} <= hitos.keys():
            _err(errores, e, f"faltan hitos en cronometro.log: tiene {sorted(hitos)}")
    for q, n in cids.items():
        if n > 1:
            _err(errores, q, "cid repetido")
    for e, n in case_ids.items():
        if n > 1:
            _err(errores, e, "case_id repetido")
    for u, n in urls.items():
        if n > 1:
            _err(errores, u, "post_url repetida")
    # tope: 3 controles por edicion primaria
    por_edicion = Counter(c["primaria_edicion"] for c in CANDIDATOS if c.get("cubeta") == "A")
    for ed, n in por_edicion.items():
        if n > 3:
            _err(errores, ed, f"{n} controles de la misma edicion primaria (tope 3)")
    return errores


def escribir(marcas: dict) -> tuple[list[dict], list[dict]]:
    candidatos, anotados = [], []
    for c in CANDIDATOS:
        fila = {k: c.get(k, "") for k in CAMPOS_CRIBA}
        fila["cubeta"] = c.get("cubeta", "")
        candidatos.append(fila)
        if c.get("criba_resultado") != "admitido" or "case_id" not in c or "bucket_resultado" not in c:
            continue
        loc, ext = minutos(c["case_id"])
        fila = {k: c.get(k, "") for k in CAMPOS_ANOTACION}
        fila["sin_verificacion_confirmada"] = "si"
        fila["minutes_to_locate"] = "" if loc is None else f"{loc:.1f}"
        fila["minutes_to_extract"] = "" if ext is None else f"{ext:.1f}"
        fila["cronometrado_por"] = "agente"
        fila["etiquetado_por"] = c.get("etiquetado_por", "agente")
        anotados.append(fila)
    with CSV_CANDIDATOS.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_CRIBA + ["cubeta"], quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(candidatos)
    with CSV_ANOTACION.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_ANOTACION, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(anotados)
    CASOS.mkdir(exist_ok=True)
    for c in CANDIDATOS:
        est = c.get("estructura")
        if "case_id" not in c or not est:
            continue
        caso = {"claim_id": c["case_id"], "texto": c["claim_text"], "fuente_url": c["post_url"],
                "conjunto": "evaluacion", "origen_case_id": "", **est}
        caso.setdefault("notas", "")
        (CASOS / f"{c['case_id']}.json").write_text(json.dumps(caso, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf-8")
    return candidatos, anotados


def resumen(anotados: list[dict], marcas: dict) -> None:
    n = len(anotados)
    admitidos = sum(1 for c in CANDIDATOS if c.get("criba_resultado") == "admitido")
    rechazados = [c for c in CANDIDATOS if c.get("criba_resultado") == "rechazado"]
    print(f"\n--- criba: {len(CANDIDATOS)} candidatos | admitidos {admitidos} | rechazados {len(rechazados)} ---")
    print("  motivos:", dict(Counter(str(c['criba_motivo']).split(':')[0] for c in rechazados)))
    print(f"\n--- cubetas (DEC-031), {n} anotados; entre parentesis sin hermanos ---")
    por = Counter(f["cubeta"] for f in anotados)
    indep = Counter(f["cubeta"] for f in anotados if not f["hermano_de"])
    for cub, (obj, mn) in OBJETIVO_CUBETA.items():
        if obj == 0:
            estado = "sin objetivo"
        else:
            estado = "OK" if indep[cub] >= obj else ("min" if indep[cub] >= mn else "FALTA")
        print(f"  {cub}  {por[cub]:3} ({indep[cub]:3})  objetivo {obj:3}  minimo {mn:3}   {estado}")
    print(f"  total {n} ({sum(indep.values())})  objetivo {sum(o for o, _ in OBJETIVO_CUBETA.values())}  "
          f"minimo {sum(m for _, m in OBJETIVO_CUBETA.values())}")
    if n:
        emisores = Counter(f["fuente_primaria"].split(" - ")[0].split(" (")[0] for f in anotados)
        print("\n--- emisor de la primaria ---")
        for em, k in emisores.most_common():
            print(f"  {em:40} {k:3}  {100 * k / n:5.1f} %")
        ine = sum(k for em, k in emisores.items() if em.upper().startswith("INE"))
        print(f"  INE {ine}/{n} = {100 * ine / n:.1f} % (tope 70 %)")
        print("  paises:", dict(Counter(f["pais"] for f in anotados)))
        print("  vias:", dict(Counter(f["descubrimiento_via"] for f in anotados)))
        # DEC-032: el sesgo de la via se mide, no se infiere
        print("\n--- cubeta x via de descubrimiento (DEC-032) ---")
        vias = sorted({f["descubrimiento_via"] for f in anotados})
        print("  cubeta " + "".join(f"{v[:22]:>24}" for v in vias))
        for cub in OBJETIVO_CUBETA:
            fila = [sum(1 for f in anotados if f["cubeta"] == cub and f["descubrimiento_via"] == v) for v in vias]
            if any(fila):
                print(f"  {cub:6} " + "".join(f"{k:>24}" for k in fila))
        div = [f for f in anotados if f["cubeta"] in ("B", "C", "F")]
        for v in vias:
            n_v = sum(1 for f in anotados if f["descubrimiento_via"] == v)
            b_v = sum(1 for f in div if f["descubrimiento_via"] == v)
            print(f"  {v:24} divergencias/claims falsos {b_v}/{n_v}")
        print("  truth x context:", dict(sorted(Counter((f["truth"], f["context"]) for f in anotados).items())))
        ed = Counter(f["primaria_edicion"] for f in anotados if f["cubeta"] == "A")
        print("  controles por edicion primaria (tope 3):", dict(ed.most_common(8)))
        mins = [float(f["minutes_to_locate"]) + float(f["minutes_to_extract"])
                for f in anotados if f["minutes_to_locate"] and f["minutes_to_extract"]]
        if mins:
            print(f"  cronometro por caso (localizar+extraer): media {sum(mins) / len(mins):.1f} min, max {max(mins):.1f}")
    ini = marcas.get(MARCA_INICIO, {}).get("t0")
    if ini:
        ahora = dt.datetime.now(dt.timezone.utc)
        # Pausas: marcas P3-PAUSA* con t0 (inicio) y t2 (fin); una pausa abierta llega hasta ahora.
        pausas = 0.0
        for cid, h in marcas.items():
            if cid.startswith("P3-PAUSA") and "t0" in h:
                pausas += (h.get("t2", ahora) - h["t0"]).total_seconds() / 3600
        horas = (ahora - ini).total_seconds() / 3600 - pausas
        print(f"\n  pausas descontadas: {pausas:.2f} h")
        ritmo = n / horas if horas > 0 else 0
        tope = TOPE_JORNADAS * JORNADA_HORAS
        print(f"\n--- reloj de recoleccion: {horas:.1f} h de {tope:.0f} h (jornada = {JORNADA_HORAS:.0f} h; "
              f"revision a la mitad = {tope / 2:.0f} h) ---")
        print(f"  ritmo {ritmo:.1f} casos/h -> proyeccion al tope: {ritmo * tope:.0f} casos"
              + (f"; cubeta A proyectada: {por['A'] / horas * tope:.0f}" if horas > 0 else ""))


def main() -> int:
    marcas = leer_cronometro()
    errores = validar(marcas)
    _, anotados = escribir(marcas)
    resumen(anotados, marcas)
    if errores:
        print(f"\nERRORES ({len(errores)}):")
        for e in errores:
            print("  -", e)
        return 1
    print(f"\nOK. Escritos: {CSV_CANDIDATOS.name}, {CSV_ANOTACION.name}, casos/*.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
