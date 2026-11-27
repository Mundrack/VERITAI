# -*- coding: utf-8 -*-
"""Analisis de los resultados del modulo IA2: semillas, sesgo por grupo objetivo y graficos.

Lee de resultados/:
    resultados.json                  modelos clasicos (dos particiones)
    transformer_s<semilla>_e<ep>.json  cada ajuste del transformer
    pred_<modelo>_<particion>.csv    predicciones por ejemplo (texto, real, predicho, functionality, target_ident)
Escribe en resultados/:
    analisis.json                    medias y desviaciones por semilla; sesgo por grupo; errores por funcionalidad
    fig_semillas.png                 F1 macro por modelo y particion, con la dispersion entre semillas
    fig_sesgo_grupos.png             tasa de falsos positivos sobre frases NO hostiles, por grupo objetivo
    fig_curvas.png                   perdida de entrenamiento por epoca del transformer
    fig_conjuntos.png                F1 macro de los cuatro modelos en los tres escenarios (si hay HaterNet)
    fig_matrices_haternet.png        matrices de confusion en HaterNet, A frente a C
No usa red ni modelos: solo lee lo ya medido.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CARPETA = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "resultados")
GRUPOS_ES = {
    "women": "mujeres", "trans people": "personas trans", "gay people": "personas gais",
    "black people": "personas negras", "disabled people": "personas con discapacidad",
    "Muslims": "musulmanes", "immigrants": "inmigrantes", "indigenous people": "pueblos indígenas",
    "jews": "personas judías", "nan": "sin grupo",
}


def media_sd(xs):
    xs = np.array(xs, dtype=float)
    return {"media": round(float(xs.mean()), 4), "sd": round(float(xs.std(ddof=1)) if len(xs) > 1 else 0.0, 4),
            "n": int(len(xs)), "valores": [round(float(x), 4) for x in xs]}


def main() -> int:
    r = json.loads((CARPETA / "resultados.json").read_text(encoding="utf-8"))
    corridas = sorted(CARPETA.glob("transformer_s*_e*.json"))
    tr = [json.loads(p.read_text(encoding="utf-8")) for p in corridas]
    tr = [t for t in tr if "por_caso" in t["particiones"] and "por_plantilla" in t["particiones"]]
    salida = {"transformer_corridas": [p.name for p in corridas], "transformer_completas": len(tr)}

    # ---- 1. semillas ----
    clasicos = {
        "0_mayoria": ("Mayoría", r["0_mayoria"]["f1_macro"], r["particion_por_plantilla"]["0_mayoria"]["f1_macro"]),
        "A_tfidf_palabras_lr": ("A · TF-IDF palabras", r["A_tfidf_palabras_lr"]["f1_macro"], r["particion_por_plantilla"]["A_tfidf_palabras_lr"]["f1_macro"]),
        "B_tfidf_caracteres_lr": ("B · TF-IDF caracteres", r["B_tfidf_caracteres_lr"]["f1_macro"], r["particion_por_plantilla"]["B_tfidf_caracteres_lr"]["f1_macro"]),
    }
    salida["f1_macro"] = {k: {"por_caso": v[1], "por_plantilla": v[2]} for k, v in clasicos.items()}
    if tr:
        for part in ("por_caso", "por_plantilla"):
            salida["f1_macro"].setdefault("C_transformer", {})[part] = media_sd([t["particiones"][part]["f1_macro"] for t in tr])
            for m in ("accuracy", "precision_hateful", "recall_hateful"):
                salida.setdefault("transformer_" + m, {})[part] = media_sd([t["particiones"][part][m] for t in tr])
        salida["transformer_config"] = {k: tr[0][k] for k in ("modelo", "epocas", "lote", "lr", "max_len")}
        salida["transformer_semillas"] = [t.get("semilla_modelo") for t in tr]
        salida["transformer_segundos"] = {part: media_sd([t["particiones"][part]["segundos"] for t in tr]) for part in ("por_caso", "por_plantilla")}

    # figura semillas
    etiquetas = [v[0] for v in clasicos.values()] + (["C · DistilBERT es"] if tr else [])
    caso = [v[1] for v in clasicos.values()]
    plan = [v[2] for v in clasicos.values()]
    err_c = [0, 0, 0]
    err_p = [0, 0, 0]
    if tr:
        caso.append(salida["f1_macro"]["C_transformer"]["por_caso"]["media"])
        plan.append(salida["f1_macro"]["C_transformer"]["por_plantilla"]["media"])
        err_c.append(salida["f1_macro"]["C_transformer"]["por_caso"]["sd"])
        err_p.append(salida["f1_macro"]["C_transformer"]["por_plantilla"]["sd"])
    xs = np.arange(len(etiquetas))
    fig, ax = plt.subplots(figsize=(8.4, 4.4), dpi=150)
    b1 = ax.bar(xs - 0.19, caso, 0.38, yerr=err_c, capsize=4, label="Por caso", color="#9aa3b0")
    b2 = ax.bar(xs + 0.19, plan, 0.38, yerr=err_p, capsize=4, label="Por plantilla", color="#98242c")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.025, f"{b.get_height():.2f}".replace(".", ","), ha="center", fontsize=9)
    ax.set_xticks(xs, etiquetas, fontsize=9)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("F1 macro en prueba")
    titulo = "F1 macro por modelo y partición"
    if tr:
        titulo += f" (transformer: media de {len(tr)} semillas, barras = desviación)"
    ax.set_title(titulo, fontsize=10)
    ax.legend(frameon=False, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(CARPETA / "fig_semillas.png")

    # ---- 1b. HaterNet (tuits reales): clasicos + transformer, y figura de los tres escenarios ----
    rh = CARPETA / "resultados_haternet.json"
    trh = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CARPETA.glob("transformer_haternet_s*_e*.json"))]
    trh = [t for t in trh if "por_caso" in t["particiones"]]
    if rh.exists():
        r2 = json.loads(rh.read_text(encoding="utf-8"))
        hn = {"transformer_completas": len(trh),
              "f1_macro": {k: r2[k]["f1_macro"] for k in ("0_mayoria", "A_tfidf_palabras_lr", "B_tfidf_caracteres_lr")}}
        if trh:
            for m in ("f1_macro", "accuracy", "precision_hateful", "recall_hateful"):
                hn["transformer_" + m] = media_sd([t["particiones"]["por_caso"][m] for t in trh])
            hn["transformer_semillas"] = [t.get("semilla_modelo") for t in trh]
            hn["transformer_segundos"] = media_sd([t["particiones"]["por_caso"]["segundos"] for t in trh])
        salida["haternet"] = hn

        # figura: F1 macro de los cuatro modelos en los tres escenarios
        escenarios = ["HateCheck\npor caso", "HateCheck\npor plantilla", "HaterNet\ntuits reales"]
        series = {
            "Mayoría": ([clasicos["0_mayoria"][1], clasicos["0_mayoria"][2], hn["f1_macro"]["0_mayoria"]], "#c9ced6"),
            "A · TF-IDF palabras": ([clasicos["A_tfidf_palabras_lr"][1], clasicos["A_tfidf_palabras_lr"][2], hn["f1_macro"]["A_tfidf_palabras_lr"]], "#9aa3b0"),
            "B · TF-IDF caracteres": ([clasicos["B_tfidf_caracteres_lr"][1], clasicos["B_tfidf_caracteres_lr"][2], hn["f1_macro"]["B_tfidf_caracteres_lr"]], "#6b7480"),
        }
        errores = {k: [0, 0, 0] for k in series}
        if tr and trh:
            series["C · DistilBERT es"] = ([salida["f1_macro"]["C_transformer"]["por_caso"]["media"], salida["f1_macro"]["C_transformer"]["por_plantilla"]["media"], hn["transformer_f1_macro"]["media"]], "#98242c")
            errores["C · DistilBERT es"] = [salida["f1_macro"]["C_transformer"]["por_caso"]["sd"], salida["f1_macro"]["C_transformer"]["por_plantilla"]["sd"], hn["transformer_f1_macro"]["sd"]]
        fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=150)
        nser = len(series)
        ancho = 0.8 / nser
        for i, (nombre, (vals, color)) in enumerate(series.items()):
            pos = np.arange(3) + (i - (nser - 1) / 2) * ancho
            bb = ax.bar(pos, vals, ancho * 0.95, yerr=errores[nombre], capsize=3, label=nombre, color=color)
            for b in bb:
                ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.03, f"{b.get_height():.2f}".replace(".", ","), ha="center", fontsize=8)
        ax.set_xticks(np.arange(3), escenarios, fontsize=9.5)
        ax.set_ylim(0, 1.12)
        ax.set_ylabel("F1 macro en prueba")
        ax.set_title("F1 macro de los cuatro modelos en los tres escenarios" + (f" (transformer: media de {len(tr)} semillas)" if tr and trh else ""), fontsize=10)
        ax.legend(frameon=False, ncol=2, loc="upper right", fontsize=8.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        fig.tight_layout()
        fig.savefig(CARPETA / "fig_conjuntos.png")

        # figura: matrices de confusion en HaterNet, A frente a C (semilla 42 si existe)
        mats = [("A · TF-IDF palabras + RL", r2["A_tfidf_palabras_lr"]["matriz_confusion"]["valores"])]
        c42 = [t for t in trh if t.get("semilla_modelo") == 42] or trh
        if c42:
            mats.append((f"C · DistilBERT es (semilla {c42[0].get('semilla_modelo')})", c42[0]["particiones"]["por_caso"]["matriz_confusion"]["valores"]))
        fig, axs = plt.subplots(1, len(mats), figsize=(4.6 * len(mats), 4.2), dpi=150)
        axs = np.atleast_1d(axs)
        for ax, (titulo, m) in zip(axs, mats):
            m = np.array(m)
            ax.imshow(m, cmap="Reds", vmin=0, vmax=m.max())
            for (i, j), v in np.ndenumerate(m):
                ax.text(j, i, f"{v:,}".replace(",", " "), ha="center", va="center", fontsize=13, color="white" if v > m.max() * 0.6 else "#222")
            ax.set_xticks([0, 1], ["odio", "no odio"])
            ax.set_yticks([0, 1], ["odio", "no odio"])
            ax.set_xlabel("Predicho")
            ax.set_ylabel("Real")
            ax.set_title(titulo, fontsize=10)
        fig.suptitle("HaterNet, 1 200 tuits de prueba", fontsize=10)
        fig.tight_layout()
        fig.savefig(CARPETA / "fig_matrices_haternet.png")

    # ---- 2. sesgo por grupo objetivo: tasa de falsos positivos sobre frases no hostiles ----
    def fpr_por_grupo(ruta):
        d = pd.read_csv(ruta)
        d["target_ident"] = d["target_ident"].fillna("nan").astype(str)
        nh = d[d["real"] == "non-hateful"]
        g = nh.groupby("target_ident").apply(lambda x: pd.Series({"n": len(x), "fp": int((x["predicho"] == "hateful").sum())}))
        g["fpr"] = (g["fp"] / g["n"]).round(4)
        h = d[d["real"] == "hateful"]
        rec = h.groupby("target_ident").apply(lambda x: pd.Series({"n_h": len(x), "acierto": int((x["predicho"] == "hateful").sum())}))
        rec["recall"] = (rec["acierto"] / rec["n_h"]).round(4)
        return g, rec, d

    sesgo = {}
    archivos = {"A_tfidf_palabras_lr": CARPETA / "pred_A_tfidf_palabras_lr_por_plantilla.csv",
                "B_tfidf_caracteres_lr": CARPETA / "pred_B_tfidf_caracteres_lr_por_plantilla.csv"}
    pred_tr = sorted(CARPETA.glob("pred_transformer_s*_e*_por_plantilla.csv"))
    if pred_tr:
        archivos["C_transformer"] = pred_tr[0]  # la primera semilla (42) para el detalle por ejemplo
    errores_func = {}
    for nombre, ruta in archivos.items():
        if not ruta.exists():
            continue
        g, rec, d = fpr_por_grupo(ruta)
        sesgo[nombre] = {
            "fpr_no_hostiles_por_grupo": {GRUPOS_ES.get(k, k): {"n": int(v["n"]), "fp": int(v["fp"]), "fpr": float(v["fpr"])} for k, v in g.iterrows()},
            "recall_hostiles_por_grupo": {GRUPOS_ES.get(k, k): {"n": int(v["n_h"]), "recall": float(v["recall"])} for k, v in rec.iterrows()},
        }
        err = d[d["real"] != d["predicho"]]
        errores_func[nombre] = {"total": int(len(err)), "por_funcionalidad": {str(k): int(v) for k, v in err["functionality"].value_counts().head(10).items()}}
    salida["sesgo_por_grupo_particion_por_plantilla"] = sesgo
    salida["errores_por_funcionalidad_particion_por_plantilla"] = errores_func

    # figura sesgo (A frente a transformer si existe)
    if sesgo:
        modelos = [m for m in ("A_tfidf_palabras_lr", "C_transformer") if m in sesgo]
        grupos = sorted({g for m in modelos for g in sesgo[m]["fpr_no_hostiles_por_grupo"]}, key=lambda s: (s == "sin grupo", s))
        fig, ax = plt.subplots(figsize=(8.4, 4.4), dpi=150)
        ancho = 0.8 / len(modelos)
        colores = {"A_tfidf_palabras_lr": "#9aa3b0", "C_transformer": "#98242c"}
        nombres = {"A_tfidf_palabras_lr": "A · TF-IDF palabras", "C_transformer": "C · DistilBERT es"}
        for i, m in enumerate(modelos):
            vals = [sesgo[m]["fpr_no_hostiles_por_grupo"].get(g, {"fpr": 0})["fpr"] for g in grupos]
            ax.bar(np.arange(len(grupos)) + (i - (len(modelos) - 1) / 2) * ancho, vals, ancho, label=nombres[m], color=colores[m])
        ax.set_xticks(np.arange(len(grupos)), grupos, rotation=20, ha="right", fontsize=9)
        ax.set_ylabel("Falsos positivos / frases no hostiles")
        ax.set_ylim(0, 1.0)
        ax.set_title("Sesgo por grupo objetivo: tasa de falsas alarmas sobre frases NO hostiles (partición por plantilla)", fontsize=9.5)
        ax.legend(frameon=False)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.tight_layout()
        fig.savefig(CARPETA / "fig_sesgo_grupos.png")

    # ---- 3. curvas de entrenamiento ----
    if tr:
        fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=150)
        for t in tr:
            for part, estilo in (("por_caso", "-"), ("por_plantilla", "--")):
                c = t["particiones"][part]["curva"]
                ax.plot([e["epoca"] for e in c], [e["perdida_media"] for e in c], estilo, marker="o",
                        label=f"{part.replace('_', ' ')} · semilla {t.get('semilla_modelo')}")
        ax.set_xticks(sorted({e["epoca"] for t in tr for part in ("por_caso", "por_plantilla") for e in t["particiones"][part]["curva"]}))
        ax.set_xlabel("Época")
        ax.set_ylabel("Pérdida media de entrenamiento")
        ax.set_title("Curvas de entrenamiento del transformer", fontsize=10)
        ax.legend(frameon=False, fontsize=7)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.tight_layout()
        fig.savefig(CARPETA / "fig_curvas.png")

    (CARPETA / "analisis.json").write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: salida[k] for k in salida if k in ("transformer_completas", "f1_macro", "transformer_semillas")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
