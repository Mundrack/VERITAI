# -*- coding: utf-8 -*-
"""Modelo propuesto del modulo IA2: transformer en espanol ajustado para hostil / no hostil.

Mismo conjunto de datos y las MISMAS particiones que la linea base
(`entrenar_linea_base.py`): por caso (estratificada, semilla 42) y por plantilla
(GroupShuffleSplit por templ_id, semilla 42). Asi la comparacion es justa.

Modelo: DistilBERT en espanol (dccuchile/distilbert-base-spanish-uncased), con los
pesos descargados a research/ia2/modelos/ (sin huggingface_hub). Corre en CPU.

Uso:
    python ajustar_transformer.py --salida resultados --epocas 2
Salida: resultados/transformer.json
"""
from __future__ import annotations

import logging

# En esta maquina (Python 3.13, Windows) crear un registro de `logging` desde las
# librerias de Hugging Face provoca una violacion de acceso. Se desactiva el
# logging por completo antes de importarlas; no afecta a los resultados.
logging.disable(logging.CRITICAL)

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer

SEMILLA = 42
AQUI = Path(__file__).resolve().parent
MODELO = AQUI / "modelos" / "distilbert-base-spanish-uncased"
DATOS = AQUI / "datos" / "hatecheck_es_test.csv"


def metricas(y_real, y_pred, clases, positiva):
    return {
        "accuracy": round(float(accuracy_score(y_real, y_pred)), 4),
        "f1_macro": round(float(f1_score(y_real, y_pred, average="macro")), 4),
        "precision_hateful": round(float(precision_score(y_real, y_pred, pos_label=positiva, zero_division=0)), 4),
        "recall_hateful": round(float(recall_score(y_real, y_pred, pos_label=positiva, zero_division=0)), 4),
        "matriz_confusion": {"clases": clases, "valores": confusion_matrix(y_real, y_pred, labels=clases).tolist()},
    }


def entrenar_y_evaluar(X_tr, y_tr, X_te, y_te, clases, epocas, lote, lr, max_len, registro, semilla=SEMILLA):
    torch.manual_seed(semilla)
    np.random.seed(semilla)
    idx = {c: i for i, c in enumerate(clases)}
    tok = AutoTokenizer.from_pretrained(str(MODELO))
    modelo = AutoModelForSequenceClassification.from_pretrained(str(MODELO), num_labels=len(clases))
    modelo.train()
    opt = torch.optim.AdamW(modelo.parameters(), lr=lr, weight_decay=0.01)
    y_tr_i = torch.tensor([idx[c] for c in y_tr])
    n = len(X_tr)
    pasos_total = epocas * ((n + lote - 1) // lote)
    paso = 0
    t0 = time.time()
    for ep in range(epocas):
        orden = np.random.permutation(n)
        perdida_ep = 0.0
        for i in range(0, n, lote):
            b = orden[i:i + lote]
            enc = tok([str(X_tr[j]) for j in b], padding=True, truncation=True, max_length=max_len, return_tensors="pt")
            out = modelo(**enc, labels=y_tr_i[b])
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
            # calentamiento lineal corto y decaimiento lineal
            paso += 1
            factor = min(1.0, paso / max(1, int(0.1 * pasos_total))) * max(0.0, 1 - paso / pasos_total)
            for g in opt.param_groups:
                g["lr"] = lr * max(factor, 0.05)
            opt.step()
            opt.zero_grad()
            perdida_ep += float(out.loss)
        registro.append({"epoca": ep + 1, "perdida_media": round(perdida_ep / ((n + lote - 1) // lote), 4),
                         "segundos": round(time.time() - t0, 1)})
        print("epoca", ep + 1, registro[-1], flush=True)
    modelo.eval()
    pred = []
    with torch.no_grad():
        for i in range(0, len(X_te), 64):
            enc = tok([str(x) for x in X_te[i:i + 64]], padding=True, truncation=True, max_length=max_len, return_tensors="pt")
            logits = modelo(**enc).logits
            pred.extend(logits.argmax(-1).tolist())
    inv = {i: c for c, i in idx.items()}
    return np.array([inv[p] for p in pred], dtype=object), round(time.time() - t0, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--epocas", type=int, default=2)
    ap.add_argument("--lote", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--max-len", type=int, default=48)
    ap.add_argument("--solo", choices=["caso", "plantilla", "ambas"], default="ambas")
    ap.add_argument("--semilla", type=int, default=SEMILLA, help="semilla del modelo; las particiones usan siempre 42")
    ap.add_argument("--nombre", default="transformer", help="nombre base de los archivos de salida")
    ap.add_argument("--datos", choices=["hatecheck", "haternet"], default="hatecheck")
    args = ap.parse_args()
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    import datos as _datos
    df = _datos.cargar(args.datos)
    df = df.rename(columns={"texto": "test_case", "etiqueta": "label_gold", "grupo": "templ_id"})
    X = np.array(df["test_case"].astype(str).tolist(), dtype=object)
    y = np.array(df["label_gold"].astype(str).tolist(), dtype=object)
    if args.datos != "hatecheck" and args.solo == "ambas":
        args.solo = "caso"  # sin plantillas no hay particion por plantilla
    clases = sorted(set(y))
    positiva = "hateful"
    resultado = {"modelo": MODELO.name, "datos": args.datos, "epocas": args.epocas, "lote": args.lote, "lr": args.lr, "max_len": args.max_len,
                 "semilla_modelo": args.semilla, "hilos_cpu": torch.get_num_threads(), "particiones": {}}
    extra = df[["test_case", "functionality", "target_ident"]].drop_duplicates("test_case").set_index("test_case")

    def guardar_pred(nombre_part, X_te, y_te, pred):
        d = pd.DataFrame({"texto": X_te, "real": y_te, "predicho": pred})
        d = d.join(extra, on="texto")
        d.to_csv(salida / f"pred_{args.nombre}_{nombre_part}.csv", index=False, encoding="utf-8")

    if args.solo in ("caso", "ambas"):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEMILLA, stratify=y)
        registro = []
        pred, seg = entrenar_y_evaluar(X_tr, y_tr, X_te, y_te, clases, args.epocas, args.lote, args.lr, args.max_len, registro, args.semilla)
        guardar_pred("por_caso", X_te, y_te, pred)
        resultado["particiones"]["por_caso"] = {"entrenamiento": int(len(X_tr)), "prueba": int(len(X_te)),
                                                 "segundos": seg, "curva": registro, **metricas(y_te, pred, clases, positiva)}
        print("por_caso", json.dumps(resultado["particiones"]["por_caso"], ensure_ascii=False), flush=True)
        (salida / f"{args.nombre}.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.solo in ("plantilla", "ambas"):
        grupos = df["templ_id"].fillna(-1).astype(int).to_numpy()
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEMILLA)
        i_tr, i_te = next(gss.split(X, y, groups=grupos))
        registro = []
        pred, seg = entrenar_y_evaluar(X[i_tr], y[i_tr], X[i_te], y[i_te], clases, args.epocas, args.lote, args.lr, args.max_len, registro, args.semilla)
        guardar_pred("por_plantilla", X[i_te], y[i_te], pred)
        resultado["particiones"]["por_plantilla"] = {"entrenamiento": int(len(i_tr)), "prueba": int(len(i_te)),
                                                      "plantillas_prueba": int(len(set(grupos[i_te]))),
                                                      "segundos": seg, "curva": registro, **metricas(y[i_te], pred, clases, positiva)}
        print("por_plantilla", json.dumps(resultado["particiones"]["por_plantilla"], ensure_ascii=False), flush=True)

    (salida / f"{args.nombre}.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
