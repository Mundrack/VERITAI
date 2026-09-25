#!/usr/bin/env python3
"""Reconstruye la via de descubrimiento de cada candidato del lote crudo.

POR QUE EXISTE
    DEC-020: la TAREA 3 tiene que cuantificar el sesgo del buscador. Para eso
    hace falta saber QUE consulta saco cada candidato, y eso no se registro
    por candidato durante la TAREA 2. Se reconstruye del transcript de la
    sesion (el .jsonl de Claude Code), que guarda cada busqueda web con su
    consulta y sus resultados.

QUE HACE
    1. Lee el transcript y ordena todas las llamadas web (WebSearch, WebFetch)
       con su resultado.
    2. Para cada candidato de lote_crudo.CANDIDATOS busca la PRIMERA llamada
       cuyo resultado contiene su post_url (normalizada). Si no aparece
       entera, prueba con dominio + primer segmento de ruta (match 'laxo').
    3. Clasifica la consulta en una via de descubrimiento (enum VIA, abajo).
    4. Escribe research/pilot-crudo-descubrimiento.csv e imprime la tabla
       via x recuperabilidad sobre los trabajados.
    5. Con --aplicar, inserta descubrimiento_via y descubrimiento_query en
       cada candidato de lote_crudo.py (idempotente), para que el CSV de
       screening los lleve.

LIMITE
    El transcript vive fuera del repo (contiene la sesion entera) y no se
    versiona. La reconstruccion es reproducible mientras exista ese archivo;
    el CSV que produce SI se versiona, y es lo que la TAREA 3 usa.

USO
    python research/scripts/reconstruir_descubrimiento.py [--transcript RUTA] [--aplicar]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lote_crudo import CANDIDATOS  # noqa: E402

TRANSCRIPT_DEFECTO = Path.home() / ".claude" / "projects" / "C--Users-mateo-WORK-SPACE-VERITAI" / \
    "0ab7628b-d5c1-41fd-a522-c3be90344cd4.jsonl"
CSV_SALIDA = RAIZ / "research" / "pilot-crudo-descubrimiento.csv"
LOTE_PY = RAIZ / "research" / "scripts" / "lote_crudo.py"

# Enum cerrado de vias. El orden importa: la primera regla que casa gana.
#   criba_negativa           el candidato aparecio en una busqueda negativa de la
#                            criba de OTRO candidato ("... verificacion OR bulo OR fact-check")
#   busqueda_de_rankings     consulta dirigida a titulares de ranking ("cae puestos", "ocupa el puesto")
#   busqueda_de_encuestas    consulta dirigida a encuestas y estudios ("segun un estudio", "encuesta ... revela")
#   busqueda_a_organismo     consulta que nombra un emisor oficial (INE, INEC, INEGI, DANE, INEI, SEPE,
#                            Eurostat, AEMET, Interior, Ministerio, INDEC, Moncloa)
#   busqueda_por_tema        consulta por tema sin nombrar emisor ("abandono escolar temprano 2026 dato")
VIA = ("criba_negativa", "busqueda_de_rankings", "busqueda_de_encuestas",
       "busqueda_a_organismo", "busqueda_por_tema")
REGLAS = (
    ("criba_negativa", re.compile(r"verificaci|bulo|fact-check", re.I)),
    ("busqueda_de_rankings", re.compile(r"cae puestos|ocupa el puesto|ranking", re.I)),
    ("busqueda_de_encuestas", re.compile(r"seg[uú]n un estudio|encuesta|bar[oó]metro|por ciento", re.I)),
    ("busqueda_a_organismo", re.compile(
        r"\b(INE|INEC|INEGI|DANE|INEI|SEPE|Eurostat|AEMET|INDEC|Moncloa|Ministerio|Interior|"
        r"Banco de Espa[nñ]a|BCE|FMI|OCDE)\b", re.I)),
    ("busqueda_por_tema", re.compile(r".", re.S)),
)


def normalizar(u: str) -> str:
    u = u.strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u.rstrip("/")


def clasificar(query: str) -> str:
    for via, rx in REGLAS:
        if rx.search(query):
            return via
    return "busqueda_por_tema"


def leer_eventos(transcript: Path) -> list[dict]:
    """Llamadas web en orden, cada una con su consulta/URL, timestamp y texto del resultado."""
    usos: dict[str, dict] = {}
    eventos: list[dict] = []
    n = 0
    with transcript.open(encoding="utf-8") as fh:
        for linea in fh:
            try:
                d = json.loads(linea)
            except json.JSONDecodeError:
                continue
            msg = d.get("message") or {}
            contenido = msg.get("content") if isinstance(msg.get("content"), list) else []
            for b in contenido:
                if b.get("type") == "tool_use" and b.get("name") in ("WebSearch", "WebFetch"):
                    n += 1
                    entrada = b.get("input") or {}
                    usos[b["id"]] = {"n": n, "ts": d.get("timestamp"), "herramienta": b["name"],
                                     "consulta": entrada.get("query") or entrada.get("url") or ""}
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in usos:
                    c = b.get("content")
                    texto = c if isinstance(c, str) else " ".join(
                        x.get("text", "") for x in c if isinstance(x, dict))
                    ev = dict(usos[b["tool_use_id"]])
                    ev["resultado"] = texto.lower()
                    eventos.append(ev)
    return eventos


def sin_acentos(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn").lower()


def localizar(eventos: list[dict], post_url: str) -> tuple[dict | None, str]:
    u = normalizar(post_url)
    for ev in eventos:
        if u in ev["resultado"]:
            return ev, "estricto"
    partes = u.split("/")
    laxo = "/".join(partes[:2]) if len(partes) > 1 else u
    for ev in eventos:
        if laxo in ev["resultado"]:
            return ev, "laxo"
    return None, "no_reconstruible"


def cribas_de(c: dict) -> set[str]:
    return {sin_acentos(c[k]).strip() for k in ("criba_query_a", "criba_query_b") if c.get(k)}


# Candidatos CREADOS durante la criba: aparecieron en la busqueda negativa de otro
# candidato y se anadieron al pool en ese momento (cids posteriores a K34). Para
# ellos la criba negativa ES la via de descubrimiento, aunque compartan la consulta
# de criba con su hermano. K40 (C20) tambien es tardio pero salio del barrido a
# Interior (#52), no de una criba: el match estricto lo resuelve solo.
HERMANOS_DE_CRIBA = {"K35", "K36", "K37", "K38", "K39", "K41"}

# Palabras demasiado genericas para servir de pista de descubrimiento.
PISTAS_VETADAS = {"espana", "ecuador", "mexico", "colombia", "peru", "gobierno", "desempleo",
                  "empleo", "inflacion", "criminalidad", "ministerio", "primer", "trimestre",
                  "presidente", "daniel", "encuesta", "segun", "sube", "espanoles"}


def pistas(c: dict) -> list[str]:
    """Tokens con los que se reconoce al candidato en un resultado sin su URL:
    primero las cifras del claim, despues nombres propios no genericos."""
    cifras = re.findall(r"\d+(?:[,.]\d+)+%?|\d{2,}(?:\.\d{3})+", c["claim_text"])
    palabras = [w for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{5,}", c["claim_text"])
                if w[0].isupper() and sin_acentos(w) not in PISTAS_VETADAS]
    return [sin_acentos(t) for t in cifras + palabras[:3]]


def reconstruir(transcript: Path) -> list[dict]:
    eventos = leer_eventos(transcript)
    # que criba pertenece a que caso, para nombrar al "hermano" del que salio cada uno
    duenos: dict[str, list[str]] = {}
    for c in CANDIDATOS:
        for q in cribas_de(c):
            duenos.setdefault(q, []).append(c.get("case_id") or c["cid"])
    filas = []
    for c in CANDIDATOS:
        ev, tipo = localizar(eventos, c["post_url"])
        origen = ""
        if ev and c["cid"] not in HERMANOS_DE_CRIBA and sin_acentos(ev["consulta"]).strip() in cribas_de(c):
            # La URL exacta aparece por primera vez en la PROPIA criba del candidato:
            # el candidato ya existia antes, asi que se descubrio en un evento anterior
            # que lo menciono sin esa URL (otro medio, o el buscador en texto).
            # Se busca el primer evento anterior con alguna pista del claim.
            for ant in eventos:
                if ant["n"] >= ev["n"]:
                    break
                r = sin_acentos(ant["resultado"])
                hit = next((p for p in pistas(c) if p in r), None)
                if hit:
                    ev, tipo = ant, f"propia_criba->pista:{hit}"
                    break
            else:
                tipo = "propia_criba"
        if ev and clasificar(ev["consulta"]) == "criba_negativa":
            yo = c.get("case_id") or c["cid"]
            origen = ",".join(d for d in duenos.get(sin_acentos(ev["consulta"]).strip(), []) if d != yo) or "?"
        filas.append({
            "cid": c["cid"], "case_id": c.get("case_id", ""), "post_url": c["post_url"],
            "descubrimiento_via": clasificar(ev["consulta"]) if ev else "no_reconstruible",
            "descubrimiento_query": ev["consulta"] if ev else "",
            "descubrimiento_origen": origen,  # criba_negativa: de que caso era la criba
            "descubrimiento_herramienta": ev["herramienta"] if ev else "",
            "descubrimiento_ts": ev["ts"] if ev else "",
            "descubrimiento_orden": ev["n"] if ev else "",
            "match": tipo,
        })
    return filas


def aplicar(filas: list[dict]) -> int:
    """Inserta descubrimiento_via/query en lote_crudo.py tras criba_url_verificacion. Idempotente."""
    src = LOTE_PY.read_text(encoding="utf-8")
    hechos = 0
    for f in filas:
        i = src.index(f'cid="{f["cid"]}"')
        j = src.index("    dict(", i) if "    dict(" in src[i:] else len(src)
        bloque = src[i:j]
        q = f["descubrimiento_query"].replace("\\", "\\\\").replace('"', '\\"')
        linea = (f'descubrimiento_via="{f["descubrimiento_via"]}", '
                 f'descubrimiento_query="{q}",  # reconstruido del transcript (DEC-020)')
        if "descubrimiento_via=" in bloque:
            # ya insertado: se actualiza en sitio si cambio
            nuevo = re.sub(r'descubrimiento_via="[^"\n]*", descubrimiento_query="[^"\n]*",[^\n]*', linea, bloque)
            if nuevo == bloque:
                continue
            bloque = nuevo
        else:
            # criba_url_verificacion puede ir sola en su linea o detras de otros campos;
            # se inserta una linea nueva justo despues, con la misma indentacion.
            m = re.search(r'criba_url_verificacion="[^"\n]*",', bloque)
            if not m:
                raise SystemExit(f"{f['cid']}: no encuentro criba_url_verificacion")
            inicio_linea = bloque.rfind("\n", 0, m.start()) + 1
            indent = re.match(r"\s*", bloque[inicio_linea:]).group(0)
            bloque = bloque[:m.end()] + f"\n{indent}{linea}" + bloque[m.end():]
        src = src[:i] + bloque + src[j:]
        hechos += 1
    LOTE_PY.write_text(src, encoding="utf-8", newline="\n")
    return hechos


def resumen(filas: list[dict]) -> None:
    por_cid = {f["cid"]: f for f in filas}
    print(f"candidatos {len(filas)} | match: {dict(Counter(f['match'] for f in filas))}")
    print("\n--- via de descubrimiento (38 candidatos) ---")
    for via, k in Counter(f["descubrimiento_via"] for f in filas).most_common():
        print(f"  {via:26} {k:2}")
    trabajados = [c for c in CANDIDATOS if c.get("case_id") and c.get("bucket_resultado")]
    if not trabajados:
        return
    print(f"\n--- via x recuperabilidad, sobre los {len(trabajados)} trabajados (DEC-020) ---")
    print(f"  {'via':26} {'n':>3}  {'conservadora':>12}  {'leniente':>9}  {'nivel 1':>8}")
    for via in VIA:
        g = [c for c in trabajados if por_cid[c["cid"]]["descubrimiento_via"] == via]
        if not g:
            continue
        con = sum(1 for c in g if c["previous_edition_found"] == "si" and c["alcanzable_por_agente"] == "si")
        lin = sum(1 for c in g if c["previous_edition_found"] == "si")
        n1 = sum(1 for c in g if c["emisor_nivel"] == 1)
        print(f"  {via:26} {len(g):3}  {con:5}/{len(g):<6}  {lin:4}/{len(g):<4}  {n1:4}/{len(g)}")
    print("\n  consultas distintas que aportaron candidatos:",
          len({f['descubrimiento_query'] for f in filas if f['descubrimiento_query']}))
    hermanos = [f for f in filas if f["descubrimiento_via"] == "criba_negativa"]
    if hermanos:
        print("  hermanos (salieron de la criba de otro caso):",
              ", ".join(f"{f['case_id'] or f['cid']}<-{f['descubrimiento_origen']}" for f in hermanos))
    raros = [f for f in filas if f["match"] not in ("estricto", "laxo")]
    if raros:
        print("  match no trivial:", ", ".join(f"{f['case_id'] or f['cid']}:{f['match']}" for f in raros))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", type=Path, default=TRANSCRIPT_DEFECTO)
    ap.add_argument("--aplicar", action="store_true", help="inserta los campos en lote_crudo.py")
    args = ap.parse_args()
    if not args.transcript.exists():
        print(f"no existe el transcript: {args.transcript}")
        return 2
    filas = reconstruir(args.transcript)
    with CSV_SALIDA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(filas)
    print(f"escrito {CSV_SALIDA.name}")
    resumen(filas)
    if args.aplicar:
        print(f"\nlote_crudo.py: {aplicar(filas)} candidatos actualizados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
