#!/usr/bin/env python3
"""Arnes de evaluacion (Puerta 3): cruza la anotacion con los veredictos del sistema y
calcula las cinco metricas de R02 §7 mas el FPR con intervalos.

QUE HACE Y QUE NO
    Lee (1) el CSV de anotacion y (2) los resultados que escribio
    research/puerta2/ejecutar_casos.py (resultados/<case_id>.json). No llama a la
    API: correr los casos es trabajo del ejecutor; medir es trabajo de esto. No
    recolecta, no anota, no cambia etiquetas.

GUARDIA DE CONJUNTO (DEC-025)
    Solo evalua casos con conjunto = "evaluacion". Con casos de desarrollo se
    niega, salvo --desarrollo, y entonces marca la salida como HUMO en la
    primera linea. Nada que salga con --desarrollo es una evaluacion.

USO
    python research/arnes/arnes.py --anotacion research/puerta3/anotacion.csv \
        --resultados research/puerta3/resultados --salida research/puerta3/evaluacion
    python research/arnes/arnes.py --anotacion research/PILOT-40.csv \
        --resultados research/puerta2/resultados --desarrollo --salida research/arnes/humo-puerta2

Escribe <salida>.md (para pegar en el informe) y <salida>.json (los numeros).
Los umbrales de H3 (--h3-tasa, --h3-limite, --h3-min-n) son los del diseno
(research/PUERTA-3-DISENO.md); se pasan explicitos para que queden en el JSON.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metricas import acuerdo, cinco_metricas, fpr, verificar_conjunto

RAIZ = Path(__file__).resolve().parents[2]


def leer_anotacion(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh))
    faltan = {"case_id", "truth", "context", "clase_primaria"} - set(filas[0].keys() if filas else [])
    if faltan:
        raise SystemExit(f"anotacion sin columnas obligatorias: {sorted(faltan)}")
    return filas


def leer_resultados(carpeta: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    respuestas: dict[str, dict] = {}
    casos: dict[str, dict] = {}
    for ruta in sorted(carpeta.glob("*.json")):
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        caso = datos.get("caso") or {}
        cid = caso.get("claim_id") or ruta.stem
        if datos.get("http") != 200:
            print(f"AVISO {cid}: http {datos.get('http')}, sin veredicto; se cuenta como no corrido")
            continue
        respuestas[cid] = datos.get("respuesta") or {}
        casos[cid] = caso
    return respuestas, casos


def _pct(d: dict | None) -> str:
    if not d or d.get("p") is None:
        return "n/d"
    ic = d.get("ic95")
    texto = f"{d['k']}/{d['n']} = {d['p']:.1f} % [{ic[0]:.1f}; {ic[1]:.1f}]"
    if d.get("regla_de_tres") is not None:
        texto += f" (regla de tres: {d['regla_de_tres']:.1f})"
    return texto


def a_markdown(informe: dict) -> str:
    cab = informe["cabecera"]
    lineas = []
    if cab["humo"]:
        lineas.append("> **HUMO SOBRE CONJUNTO DE DESARROLLO — NO ES UNA EVALUACIÓN (DEC-025).**")
        lineas.append("")
    lineas += [
        f"# Arnés de evaluación — {cab['conjunto']}",
        "",
        (
            f"Generado {cab['generado_en']} · anotación `{cab['anotacion']}` "
            f"({cab['n_anotados']} filas) · resultados `{cab['resultados']}` "
            f"({cab['n_resultados']} veredictos) · pares evaluables **{cab['n_pares']}**"
        ),
        "",
    ]
    if cab["sin_resultado"]:
        lineas.append(f"Anotados sin veredicto ({len(cab['sin_resultado'])}): {', '.join(cab['sin_resultado'])}")
    if cab["sin_anotacion"]:
        lineas.append(f"Veredictos sin anotación ({len(cab['sin_anotacion'])}): {', '.join(cab['sin_anotacion'])}")
    lineas += ["", "## 1. Las cinco métricas de R02 §7 (sobre la anotación de los pares)", "",
               "| métrica | conservadora | leniente | semáforo |", "|---|---|---|---|"]
    m = informe["cinco_metricas_r02"]
    for clave, nombre in (("fuente_primaria_localizada", "Fuente primaria localizada"),
                          ("edicion_anterior_localizada", "Edición anterior localizada **(manda)**"),
                          ("extraccion_sin_intervencion_extrema", "Extracción sin intervención extrema (A|B)")):
        d = m.get(clave)
        if d is None:
            lineas.append(f"| {nombre} | n/d (columna ausente) | n/d | n/d |")
        else:
            lineas.append(f"| {nombre} | {_pct(d['conservadora'])} | {_pct(d['leniente'])} | {d['semaforo']} |")
    c = m["clases_de_divergencia_observadas"]
    lineas.append(f"| Clases de divergencia observadas (≥ 3) | {c['n_clases']}: {', '.join(c['clases']) or '—'} | — | {c['semaforo']} |")
    t = m.get("tiempo_medio_por_caso") or {}
    if t:
        for quien, d in t.items():
            lineas.append(f"| Tiempo medio por caso, {quien} (< 20 min) | {d['media_min']} min (n = {d['n']}, máx {d['max_min']}) | — | {d['semaforo']} |")
    else:
        lineas.append("| Tiempo medio por caso | n/d | — | n/d |")

    f = informe["fpr"]
    h3 = f["h3"]
    lineas += ["", "## 2. Falsos positivos (H3)", "",
               f"- **FPR sobre controles con test aplicable:** {_pct(f['fpr'])}",
               f"- Falsos positivos: {', '.join(f['falsos_positivos']) or 'ninguno'}",
               f"- Controles con señal registrada (no cuentan, DEC-029): {', '.join(f['controles_con_senal']) or 'ninguno'}",
               f"- Controles sin test aplicable (fuera del denominador): {', '.join(f['controles_sin_test_aplicable']) or 'ninguno'}",
               f"- Secundaria, disparos sobre todo lo anotado sin divergencia (incluye claims falsos): {_pct(f['disparos_sobre_no_divergencia_anotada'])}"
               + (f" → {', '.join(f['disparos_ids'])}" if f["disparos_ids"] else ""),
               f"- **H3: {h3['veredicto']}** (tasa fijada {h3['tasa_fijada_pct']:.0f} %, límite superior IC95 ≤ {h3['limite_superior_pct']:.0f} %, mínimo n = {h3['min_n']})"]

    a = informe["acuerdo"]
    lineas += ["", "## 3. Acuerdo sistema / anotación (adicional; no es de R02 §7)", "",
               f"- Verdad: {_pct(a['acuerdo_truth'])} · Contexto: {_pct(a['acuerdo_context'])}",
               f"- 2a anotada detectada como 2a (recall): {_pct(a['recall_2a'])}" + (f" → {', '.join(a['recall_2a']['detectados'])}" if a["recall_2a"]["detectados"] else ""),
               f"- Abstención cuando la anotación abstiene: {_pct(a['abstencion_cuando_anotada'])}",
               "", "| contexto anotado → sistema | casos |", "|---|---|"]
    lineas += [f"| {k} | {v} |" for k, v in a["matriz_context_anotado_x_sistema"].items()]

    lineas += ["", "## 4. Casos", "", "| caso | anotado (truth / context / clase) | sistema (truth / context / clase) | test | señales | acuerdo |", "|---|---|---|---|---|---|"]
    for fila in informe["casos"]:
        lineas.append(f"| {fila['case_id']} | {fila['anotado']} | {fila['sistema']} | {fila['test']} | {fila['senales'] or '—'} | {fila['acuerdo']} |")
    return "\n".join(lineas) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--anotacion", required=True, type=Path)
    ap.add_argument("--resultados", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path, help="prefijo: se escriben .md y .json")
    ap.add_argument("--desarrollo", action="store_true", help="permite casos de desarrollo (HUMO)")
    ap.add_argument("--h3-tasa", type=float, default=10.0)
    ap.add_argument("--h3-limite", type=float, default=15.0)
    ap.add_argument("--h3-min-n", type=int, default=40)
    args = ap.parse_args()

    anotaciones = leer_anotacion(args.anotacion)
    respuestas, casos = leer_resultados(args.resultados)
    errores = verificar_conjunto(casos, args.desarrollo)
    if errores:
        print("NO SE EVALUA:\n  " + "\n  ".join(errores))
        return 2

    ids_anot = {f["case_id"] for f in anotaciones}
    pares = [f for f in anotaciones if f["case_id"] in respuestas]
    sin_resultado = sorted(ids_anot - set(respuestas))
    sin_anotacion = sorted(set(respuestas) - ids_anot)
    humo = any(str(c.get("conjunto") or "") != "evaluacion" for c in casos.values())

    filas_casos = []
    for f in pares:
        v = respuestas[f["case_id"]].get("veredicto") or {}
        tests = v.get("tests") or []
        t = tests[0] if tests else {}
        if not t.get("aplicable"):
            test = "n/a"
        elif t.get("disparo"):
            test = "DISPARA " + str(t.get("subtipo") or "")
        else:
            test = "no dispara"
        filas_casos.append({
            "case_id": f["case_id"],
            "anotado": f"{f['truth']} / {f['context']} / {f['clase_primaria']}",
            "sistema": f"{v.get('truth')} / {v.get('context')} / {v.get('clase_primaria')}",
            "test": test,
            "senales": "|".join(t.get("senales") or []),
            "acuerdo": f"{str(v.get('truth') == f['truth']).lower()} / {str(v.get('context') == f['context']).lower()}",
        })

    informe = {
        "cabecera": {
            "conjunto": "DESARROLLO (humo)" if humo else "evaluacion",
            "humo": humo,
            "generado_en": datetime.now(UTC).isoformat(timespec="seconds"),
            "anotacion": str(args.anotacion).replace("\\", "/"),
            "resultados": str(args.resultados).replace("\\", "/"),
            "n_anotados": len(anotaciones),
            "n_resultados": len(respuestas),
            "n_pares": len(pares),
            "sin_resultado": sin_resultado,
            "sin_anotacion": sin_anotacion,
        },
        "cinco_metricas_r02": cinco_metricas(pares),
        "fpr": fpr(pares, respuestas, min_n=args.h3_min_n, tasa_h3=args.h3_tasa, limite_h3=args.h3_limite),
        "acuerdo": acuerdo(pares, respuestas),
        "casos": filas_casos,
    }
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.with_suffix(".json").write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.salida.with_suffix(".md").write_text(a_markdown(informe), encoding="utf-8")
    f = informe["fpr"]
    print(("HUMO (desarrollo) | " if humo else "") + f"pares {len(pares)} | FPR {_pct(f['fpr'])} | H3 {f['h3']['veredicto']} | "
          f"escritos {args.salida.with_suffix('.md').name}, {args.salida.with_suffix('.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
