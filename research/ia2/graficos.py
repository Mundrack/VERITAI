# -*- coding: utf-8 -*-
"""Grafico comparativo de los cuatro modelos en las dos particiones (F1 macro).

Lee resultados/resultados.json (clasicos) y resultados/transformer.json y escribe
resultados/metricas.png. Sin red, sin modelos: solo dibuja lo ya medido.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> int:
    carpeta = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "resultados")
    r = json.loads((carpeta / "resultados.json").read_text(encoding="utf-8"))
    t_ruta = carpeta / "transformer.json"
    t = json.loads(t_ruta.read_text(encoding="utf-8")) if t_ruta.exists() else None

    nombres = ["Mayoría", "A · TF-IDF\npalabras + RL", "B · TF-IDF\ncaracteres + RL"]
    caso = [r["0_mayoria"]["f1_macro"], r["A_tfidf_palabras_lr"]["f1_macro"], r["B_tfidf_caracteres_lr"]["f1_macro"]]
    pp = r["particion_por_plantilla"]
    plantilla = [pp["0_mayoria"]["f1_macro"], pp["A_tfidf_palabras_lr"]["f1_macro"], pp["B_tfidf_caracteres_lr"]["f1_macro"]]
    if t and "por_caso" in t["particiones"] and "por_plantilla" in t["particiones"]:
        nombres.append("C · DistilBERT\nespañol")
        caso.append(t["particiones"]["por_caso"]["f1_macro"])
        plantilla.append(t["particiones"]["por_plantilla"]["f1_macro"])

    xs = np.arange(len(nombres))
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=150)
    b1 = ax.bar(xs - 0.19, caso, width=0.38, label="Partición por caso", color="#9aa3b0")
    b2 = ax.bar(xs + 0.19, plantilla, width=0.38, label="Partición por plantilla", color="#98242c")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.012, f"{b.get_height():.2f}".replace(".", ","),
                ha="center", fontsize=9)
    ax.set_xticks(xs, nombres, fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("F1 macro en prueba")
    ax.set_title("F1 macro por modelo y partición (semilla 42)", fontsize=10)
    ax.legend(frameon=False, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(carpeta / "metricas.png")
    print("escrito:", carpeta / "metricas.png", "| modelos:", len(nombres))
    return 0


if __name__ == "__main__":
    sys.exit(main())
