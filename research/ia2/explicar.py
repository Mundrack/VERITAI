# -*- coding: utf-8 -*-
"""Explicacion por fragmentos: que parte del texto sostiene el veredicto de cada modelo.

Para un punado de ejemplos de la particion de prueba:
  - Modelo A (TF-IDF palabras + regresion logistica): contribucion de cada n-grama
    presente en el texto (valor TF-IDF x coeficiente). Es exacta: la suma de las
    contribuciones mas el sesgo es el logit del modelo.
  - Modelo C (DistilBERT ajustado): ocultacion. Se quita una palabra a la vez y se
    mide cuanto cambia la probabilidad de "hostil". Las palabras cuya ausencia mas
    baja esa probabilidad son las que sostienen el veredicto.

Particiones identicas a las de los otros scripts (semilla 42): HateCheck por
plantilla (frases de plantillas no vistas), HaterNet por caso. El transformer se
reentrena con la semilla 42 y se guarda en modelos/ (no versionado) la primera vez.

Los ejemplos se eligen de forma determinista a partir de las predicciones ya
guardadas (pred_*.csv): aciertos de ambos, errores de A que C corrige, errores de C
que A acierta y errores de ambos; dentro de cada grupo, los textos mas cortos.

Uso:
    python explicar.py --parte a                       # solo la linea base (segundos)
    python explicar.py --parte ambas --conjunto ambos  # con el transformer (minutos en CPU)
Salida: resultados/explicaciones.json
"""
from __future__ import annotations

import logging

logging.disable(logging.CRITICAL)  # ver ajustar_transformer.py

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline

import datos as _datos

SEMILLA = 42
AQUI = Path(__file__).resolve().parent
POSITIVA = "hateful"


def particion(conjunto: str):
    df = _datos.cargar(conjunto)
    X = np.array(df["texto"].astype(str).tolist(), dtype=object)
    y = np.array(df["etiqueta"].astype(str).tolist(), dtype=object)
    if conjunto == "hatecheck":
        grupos = df["grupo"].fillna(-1).astype(int).to_numpy()
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEMILLA)
        i_tr, i_te = next(gss.split(X, y, groups=grupos))
        return X[i_tr], y[i_tr], X[i_te], y[i_te], "por_plantilla"
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEMILLA, stratify=y)
    return X_tr, y_tr, X_te, y_te, "por_caso"


def modelo_a(X_tr, y_tr) -> Pipeline:
    m = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, lowercase=True, sublinear_tf=True)),
        ("lr", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced", random_state=SEMILLA)),
    ])
    m.fit(X_tr, y_tr)
    return m


def fragmentos_a(m: Pipeline, texto: str, k: int = 3) -> dict:
    vec, clf = m.named_steps["tfidf"], m.named_steps["lr"]
    x = vec.transform([texto])
    # clases ordenadas: ['hateful', 'non-hateful']; coef positivo empuja hacia la segunda
    signo = -1.0 if clf.classes_[1] != POSITIVA else 1.0
    contrib = signo * x.toarray()[0] * clf.coef_[0]
    nombres = vec.get_feature_names_out()
    nz = np.nonzero(contrib)[0]
    orden = nz[np.argsort(-contrib[nz])]
    hacia_hostil = [[str(nombres[i]), round(float(contrib[i]), 3)] for i in orden if contrib[i] > 0][:k]
    hacia_no = [[str(nombres[i]), round(float(contrib[i]), 3)] for i in orden[::-1] if contrib[i] < 0][:k]
    p = m.predict_proba([texto])[0][list(clf.classes_).index(POSITIVA)]
    return {"p_hostil": round(float(p), 3), "hacia_hostil": hacia_hostil, "hacia_no_hostil": hacia_no,
            "sesgo": round(float(signo * clf.intercept_[0]), 3), "n_rasgos_activos": int(len(nz))}


def seleccionar(conjunto: str, resultados: Path, X_te, y_te, n_por_grupo: int) -> list[dict]:
    """Elige ejemplos con las predicciones guardadas por los otros scripts."""
    if conjunto == "hatecheck":
        pa = resultados / "pred_A_tfidf_palabras_lr_por_plantilla.csv"
        pc = sorted(resultados.glob("pred_transformer_s42_e*_por_plantilla.csv"))
    else:
        pa = resultados / "pred_A_tfidf_palabras_lr_haternet_por_caso.csv"
        pc = sorted(resultados.glob("pred_transformer_haternet_s42_e*_por_caso.csv"))
    d = pd.DataFrame({"texto": X_te, "real": y_te})
    a = pd.read_csv(pa)[["texto", "predicho"]].drop_duplicates("texto").rename(columns={"predicho": "pred_A"})
    d = d.merge(a, on="texto", how="left")
    if pc:
        c = pd.read_csv(pc[-1])[["texto", "predicho"]].drop_duplicates("texto").rename(columns={"predicho": "pred_C"})
        d = d.merge(c, on="texto", how="left")
    else:
        d["pred_C"] = None
    d["largo"] = d["texto"].str.len()
    d = d.sort_values(["largo", "texto"])  # determinista: los mas cortos primero
    ok_a = d["pred_A"] == d["real"]
    ok_c = (d["pred_C"] == d["real"]) if pc else pd.Series(False, index=d.index)
    grupos = {
        "acierto_ambos_hostil": d[ok_a & ok_c & (d["real"] == POSITIVA)] if pc else d[ok_a & (d["real"] == POSITIVA)],
        "A_falla_C_acierta": d[~ok_a & ok_c] if pc else d[~ok_a],
        "C_falla_A_acierta": d[ok_a & ~ok_c] if pc else d.iloc[0:0],
        "fallan_ambos": d[~ok_a & ~ok_c] if pc else d.iloc[0:0],
    }
    ejemplos = []
    for nombre, g in grupos.items():
        # textos de longitud media: ni los mas cortos (poco informativos) ni los mas largos (no caben en una lamina)
        g = g[(g["largo"] >= 25) & (g["largo"] <= 110)] if len(g) > n_por_grupo else g
        for _, fila in g.head(n_por_grupo).iterrows():
            ejemplos.append({"grupo": nombre, "texto": fila["texto"], "real": fila["real"],
                             "pred_A": fila["pred_A"], "pred_C": (fila["pred_C"] if pc else None)})
    return ejemplos


def cargar_o_entrenar_transformer(conjunto: str, X_tr, y_tr, X_te, y_te, epocas: int, max_len: int):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    import ajustar_transformer as at
    carpeta = AQUI / "modelos" / f"ajustado_{conjunto}_e{epocas}_s{SEMILLA}"
    if not (carpeta / "config.json").exists():
        registro = []
        clases = sorted(set(y_tr))
        torch.set_num_threads(max(1, (__import__("os").cpu_count() or 1)))
        at.entrenar_y_evaluar(X_tr, y_tr, X_te[:8], y_te[:8], clases, epocas, 16, 3e-5, max_len, registro, SEMILLA, guardar=carpeta)
    tok = AutoTokenizer.from_pretrained(str(carpeta))
    modelo = AutoModelForSequenceClassification.from_pretrained(str(carpeta))
    modelo.eval()
    return tok, modelo, carpeta


def fragmentos_c(tok, modelo, texto: str, max_len: int, k: int = 3) -> dict:
    import torch
    palabras = texto.split()
    variantes = [texto] + [" ".join(palabras[:i] + palabras[i + 1:]) for i in range(len(palabras))]
    probs = []
    with torch.no_grad():
        for i in range(0, len(variantes), 64):
            enc = tok(variantes[i:i + 64], padding=True, truncation=True, max_length=max_len, return_tensors="pt")
            probs.extend(torch.softmax(modelo(**enc).logits, -1)[:, 0].tolist())  # indice 0 = 'hateful' (clases ordenadas)
    p0 = probs[0]
    efectos = [(palabras[i], p0 - probs[i + 1]) for i in range(len(palabras))]  # >0: la palabra sostiene "hostil"
    orden = sorted(efectos, key=lambda e: -abs(e[1]))
    return {"p_hostil": round(float(p0), 3),
            "sostienen_hostil": [[w, round(float(d), 3)] for w, d in orden if d > 0][:k],
            "sostienen_no_hostil": [[w, round(float(-d), 3)] for w, d in orden if d < 0][:k],
            "efecto_por_palabra": [[w, round(float(d), 3)] for w, d in efectos]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--parte", choices=["a", "transformer", "ambas"], default="a")
    ap.add_argument("--conjunto", choices=["hatecheck", "haternet", "ambos"], default="ambos")
    ap.add_argument("--epocas", type=int, default=3)
    ap.add_argument("--n", type=int, default=2, help="ejemplos por grupo de seleccion")
    ap.add_argument("--reseleccionar", action="store_true", help="volver a elegir los ejemplos aunque ya existan (descarta explicaciones previas)")
    args = ap.parse_args()
    salida = Path(args.salida)
    ruta = salida / "explicaciones.json"
    previo = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    conjuntos = ["hatecheck", "haternet"] if args.conjunto == "ambos" else [args.conjunto]
    out = dict(previo)
    for conjunto in conjuntos:
        X_tr, y_tr, X_te, y_te, nombre_part = particion(conjunto)
        max_len = 48 if conjunto == "hatecheck" else 64
        bloque = out.get(conjunto, {})
        bloque.update({"particion": nombre_part, "entrenamiento": int(len(X_tr)), "prueba": int(len(X_te)),
                       "metodo_A": "contribucion exacta: tfidf x coeficiente por n-grama presente",
                       "metodo_C": "ocultacion: cambio de P(hostil) al quitar cada palabra; modelo reentrenado con semilla 42"})
        if "ejemplos" not in bloque or args.reseleccionar:
            bloque["ejemplos"] = seleccionar(conjunto, salida, X_te, y_te, args.n)
        if args.parte in ("a", "ambas"):
            m = modelo_a(X_tr, y_tr)
            for e in bloque["ejemplos"]:
                e["A"] = fragmentos_a(m, e["texto"])
        if args.parte in ("transformer", "ambas"):
            tok, modelo, carpeta = cargar_o_entrenar_transformer(conjunto, X_tr, y_tr, X_te, y_te, args.epocas, max_len)
            bloque["modelo_C_guardado_en"] = str(carpeta.relative_to(AQUI))
            for e in bloque["ejemplos"]:
                e["C"] = fragmentos_c(tok, modelo, e["texto"], max_len)
        out[conjunto] = bloque
        print(conjunto, nombre_part, len(bloque["ejemplos"]), "ejemplos", flush=True)
        for e in bloque["ejemplos"]:
            print(" ", e["grupo"], "|", e["texto"][:70], "| real", e["real"], "| A", e["pred_A"], "| C", e["pred_C"])
            if "A" in e:
                print("    A:", e["A"]["p_hostil"], e["A"]["hacia_hostil"], "||", e["A"]["hacia_no_hostil"])
            if "C" in e:
                print("    C:", e["C"]["p_hostil"], e["C"]["sostienen_hostil"], "||", e["C"]["sostienen_no_hostil"])
    ruta.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
