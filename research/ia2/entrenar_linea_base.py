# -*- coding: utf-8 -*-
"""Linea base del modulo IA2 de VERITAI: clasificacion de lenguaje hostil en espanol.

Entrega 2 del proyecto semestral de Inteligencia Artificial 2 (UDLA, 2026).
Reproducible: datos publicos, particion con semilla fija, sin modelos de lenguaje.

Datos: HateCheck en espanol (Rottger et al., 2022), conjunto funcional de casos
de prueba etiquetados como hateful / non-hateful. Se descarga de Hugging Face
(`Paul/hatecheck-spanish`). Licencia CC BY 4.0.

Modelos comparados:
    0. Mayoria: predice siempre la clase mayoritaria (suelo).
    A. TF-IDF de palabras (1-2 gramas) + regresion logistica  <- linea base de la propuesta.
    B. TF-IDF de caracteres (2-5 gramas) + regresion logistica (variante robusta a morfologia).
El modelo propuesto (transformer multilingue ajustado) queda pendiente: se entrena en Colab.

Uso:
    python entrenar_linea_base.py --salida resultados
Salidas (en --salida): resultados.json, metricas.png, matriz_confusion.png, errores.csv, datos_resumen.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

SEMILLA = 42
REPO_DATOS = "Paul/hatecheck-spanish"
URL_DATOS = "https://huggingface.co/datasets/Paul/hatecheck-spanish/resolve/main/test.csv"


def cargar_datos() -> tuple[pd.DataFrame, str, str, dict]:
    # El CSV publico se descarga una vez a datos/ (curl o navegador) desde
    # https://huggingface.co/datasets/Paul/hatecheck-spanish/resolve/main/test.csv
    # y se lee con pandas. (Las librerias `datasets` y `huggingface_hub` fallaban
    # en esta maquina con Python 3.13; la descarga directa evita la dependencia.)
    ruta = Path(__file__).resolve().parent / "datos" / "hatecheck_es_test.csv"
    if not ruta.exists():
        import urllib.request
        ruta.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL_DATOS, ruta)
    particion = "test.csv"
    df = pd.read_csv(ruta)
    col_texto = next(c for c in ("test_case", "text", "texto") if c in df.columns)
    col_etiqueta = next(c for c in ("label_gold", "label", "etiqueta") if c in df.columns)
    info = {
        "repo": REPO_DATOS,
        "particion_original": particion,
        "filas": int(len(df)),
        "columnas": list(df.columns),
        "col_texto": col_texto,
        "col_etiqueta": col_etiqueta,
        "distribucion": {str(k): int(v) for k, v in df[col_etiqueta].value_counts().items()},
    }
    if "functionality" in df.columns:
        info["funcionalidades"] = int(df["functionality"].nunique())
    if "target_ident" in df.columns:
        info["grupos_objetivo"] = {str(k): int(v) for k, v in df["target_ident"].value_counts(dropna=False).items()}
    return df, col_texto, col_etiqueta, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--test", type=float, default=0.2)
    args = ap.parse_args()
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    df, col_texto, col_etiqueta, info = cargar_datos()
    X = np.array(df[col_texto].astype(str).tolist(), dtype=object)
    y = np.array(df[col_etiqueta].astype(str).tolist(), dtype=object)
    clases = sorted(set(y))
    positiva = "hateful" if "hateful" in clases else clases[0]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=args.test, random_state=SEMILLA, stratify=y
    )
    info["entrenamiento"] = int(len(X_tr))
    info["prueba"] = int(len(X_te))
    (salida / "datos_resumen.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    modelos = {
        "0_mayoria": DummyClassifier(strategy="most_frequent"),
        "A_tfidf_palabras_lr": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, lowercase=True, sublinear_tf=True)),
            ("lr", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced", random_state=SEMILLA)),
        ]),
        "B_tfidf_caracteres_lr": Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, lowercase=True, sublinear_tf=True)),
            ("lr", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced", random_state=SEMILLA)),
        ]),
    }
    resultados = {}
    predicciones = {}
    for nombre, modelo in modelos.items():
        modelo.fit(X_tr, y_tr)
        pred = modelo.predict(X_te)
        predicciones[nombre] = pred
        resultados[nombre] = {
            "accuracy": round(float(accuracy_score(y_te, pred)), 4),
            "f1_macro": round(float(f1_score(y_te, pred, average="macro")), 4),
            "precision_hateful": round(float(precision_score(y_te, pred, pos_label=positiva, zero_division=0)), 4),
            "recall_hateful": round(float(recall_score(y_te, pred, pos_label=positiva, zero_division=0)), 4),
            "f1_hateful": round(float(f1_score(y_te, pred, pos_label=positiva, zero_division=0)), 4),
            "matriz_confusion": {"clases": clases, "valores": confusion_matrix(y_te, pred, labels=clases).tolist()},
            "informe": classification_report(y_te, pred, zero_division=0),
        }

    # rasgos mas influyentes del modelo A (palabras)
    mA = modelos["A_tfidf_palabras_lr"]
    vocab = np.array(mA.named_steps["tfidf"].get_feature_names_out())
    coef = mA.named_steps["lr"].coef_[0]
    idx_pos = np.argsort(coef)[-15:][::-1]
    idx_neg = np.argsort(coef)[:15]
    clase_coef_positiva = mA.named_steps["lr"].classes_[1]
    resultados["rasgos_modelo_A"] = {
        "clase_del_coeficiente_positivo": str(clase_coef_positiva),
        "hacia_esa_clase": [(str(vocab[i]), round(float(coef[i]), 3)) for i in idx_pos],
        "hacia_la_otra": [(str(vocab[i]), round(float(coef[i]), 3)) for i in idx_neg],
    }

    # errores del modelo A para analisis cualitativo
    pred_A = predicciones["A_tfidf_palabras_lr"]
    err = pd.DataFrame({"texto": X_te, "real": y_te, "predicho": pred_A})
    extra = [c for c in ("functionality", "target_ident") if c in df.columns]
    # predicciones por ejemplo de los modelos clasicos (particion por caso), para el analisis por grupo
    _extra = df[[col_texto] + extra].drop_duplicates(col_texto).set_index(col_texto)
    for _n in ("A_tfidf_palabras_lr", "B_tfidf_caracteres_lr"):
        pd.DataFrame({"texto": X_te, "real": y_te, "predicho": predicciones[_n]}).join(_extra, on="texto").to_csv(
            salida / f"pred_{_n}_por_caso.csv", index=False, encoding="utf-8")
    if extra:
        df_te = df.loc[df[col_texto].astype(str).isin(set(X_te)), [col_texto] + extra].drop_duplicates(col_texto)
        err = err.merge(df_te, left_on="texto", right_on=col_texto, how="left").drop(columns=[col_texto])
    err = err[err["real"] != err["predicho"]]
    err.to_csv(salida / "errores.csv", index=False, encoding="utf-8")
    resultados["errores_modelo_A"] = int(len(err))
    if "functionality" in err.columns:
        resultados["errores_por_funcionalidad_A"] = {str(k): int(v) for k, v in err["functionality"].value_counts().head(12).items()}

    # Particion mas exigente: por PLANTILLA (templ_id), para que ninguna plantilla
    # vista en entrenamiento aparezca en prueba. Mide generalizacion real, no memoria.
    if "templ_id" in df.columns:
        from sklearn.model_selection import GroupShuffleSplit

        grupos = df["templ_id"].fillna(-1).astype(int).to_numpy()
        gss = GroupShuffleSplit(n_splits=1, test_size=args.test, random_state=SEMILLA)
        i_tr, i_te = next(gss.split(X, y, groups=grupos))
        por_plantilla = {"entrenamiento": int(len(i_tr)), "prueba": int(len(i_te)),
                         "plantillas_prueba": int(len(set(grupos[i_te])))}
        for nombre in ("0_mayoria", "A_tfidf_palabras_lr", "B_tfidf_caracteres_lr"):
            from sklearn.base import clone
            m = clone(modelos[nombre]).fit(X[i_tr], y[i_tr])
            pr = m.predict(X[i_te])
            if nombre != "0_mayoria":
                pd.DataFrame({"texto": X[i_te], "real": y[i_te], "predicho": pr}).join(_extra, on="texto").to_csv(
                    salida / f"pred_{nombre}_por_plantilla.csv", index=False, encoding="utf-8")
            por_plantilla[nombre] = {
                "accuracy": round(float(accuracy_score(y[i_te], pr)), 4),
                "f1_macro": round(float(f1_score(y[i_te], pr, average="macro")), 4),
                "precision_hateful": round(float(precision_score(y[i_te], pr, pos_label=positiva, zero_division=0)), 4),
                "recall_hateful": round(float(recall_score(y[i_te], pr, pos_label=positiva, zero_division=0)), 4),
                "matriz_confusion": confusion_matrix(y[i_te], pr, labels=clases).tolist(),
            }
        resultados["particion_por_plantilla"] = por_plantilla

    (salida / "resultados.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")

    # graficos
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nombres = ["0_mayoria", "A_tfidf_palabras_lr", "B_tfidf_caracteres_lr"]
    etiquetas = ["Mayoría", "A · TF-IDF palabras + RL", "B · TF-IDF caracteres + RL"]
    f1 = [resultados[n]["f1_macro"] for n in nombres]
    acc = [resultados[n]["accuracy"] for n in nombres]
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
    xs = np.arange(len(nombres))
    b1 = ax.bar(xs - 0.18, f1, width=0.36, label="F1 macro", color="#98242c")
    b2 = ax.bar(xs + 0.18, acc, width=0.36, label="Exactitud", color="#5c6470")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.01, f"{b.get_height():.2f}", ha="center", fontsize=9)
    ax.set_xticks(xs, etiquetas, fontsize=9)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Valor en el conjunto de prueba")
    ax.set_title("Resultados preliminares (prueba = {} casos, semilla {})".format(info["prueba"], SEMILLA), fontsize=10)
    ax.legend(frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(salida / "metricas.png")

    mc = np.array(resultados["A_tfidf_palabras_lr"]["matriz_confusion"]["valores"])
    fig, ax = plt.subplots(figsize=(4.4, 4.0), dpi=150)
    ax.imshow(mc, cmap="Reds")
    for i in range(mc.shape[0]):
        for j in range(mc.shape[1]):
            ax.text(j, i, str(mc[i, j]), ha="center", va="center", fontsize=14, color="black" if mc[i, j] < mc.max() * 0.6 else "white")
    ax.set_xticks(range(len(clases)), clases)
    ax.set_yticks(range(len(clases)), clases)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de confusión · modelo A", fontsize=10)
    fig.tight_layout()
    fig.savefig(salida / "matriz_confusion.png")

    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "informe"} if isinstance(v, dict) and "informe" in v else v
                      for k, v in resultados.items()}, ensure_ascii=False, indent=1))
    print("DATOS:", json.dumps(info, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
