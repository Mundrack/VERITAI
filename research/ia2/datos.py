# -*- coding: utf-8 -*-
"""Carga de los conjuntos de datos del modulo IA2, con un formato comun.

Cada cargador devuelve un DataFrame con las columnas:
    texto      la frase o tuit
    etiqueta   "hateful" / "non-hateful" (mismo vocabulario en los dos conjuntos)
    grupo      identificador para particionar sin fuga (plantilla en HateCheck); None si no hay
    functionality, target_ident   solo HateCheck; NaN en los demas

Conjuntos:
    hatecheck  Multilingual HateCheck, espanol (Rottger et al., 2022). CC BY 4.0. 3 745 casos de plantilla.
    haternet   HaterNet (Pereira-Kohatsu et al., 2019), 6 000 tuits en espanol etiquetados odio / no odio.
               CC BY 4.0, Zenodo 10.5281/zenodo.2592149. Formato: id=<id>;||;<texto>;||;<0|1>.
Los archivos se descargan una vez a datos/ (no se versionan). Sin modelos, sin huggingface_hub.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"

FUENTES = {
    "hatecheck": ("hatecheck_es_test.csv", "https://huggingface.co/datasets/Paul/hatecheck-spanish/resolve/main/test.csv"),
    "haternet": ("haternet_labeled_corpus_6K.txt", "https://zenodo.org/records/2592149/files/labeled_corpus_6K.txt?download=1"),
}
CITAS = {
    "hatecheck": "Röttger et al. (2022), Multilingual HateCheck, WOAH 2022, DOI 10.18653/v1/2022.woah-1.15",
    "haternet": "Quijano-Sánchez, Pereira-Kohatsu, Liberatore y Camacho-Collados (2019), HaterNet, Zenodo DOI 10.5281/zenodo.2592149",
}


def _ruta(nombre: str) -> Path:
    archivo, url = FUENTES[nombre]
    ruta = DATOS / archivo
    if not ruta.exists():
        DATOS.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, ruta)
    return ruta


def cargar(nombre: str) -> pd.DataFrame:
    if nombre == "hatecheck":
        df = pd.read_csv(_ruta(nombre))
        return pd.DataFrame({
            "texto": df["test_case"].astype(str),
            "etiqueta": df["label_gold"].astype(str),
            "grupo": df["templ_id"].fillna(-1).astype(int),
            "functionality": df["functionality"],
            "target_ident": df["target_ident"],
        })
    if nombre == "haternet":
        filas = []
        with io.open(_ruta(nombre), encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                if not linea:
                    continue
                partes = linea.split(";||;")
                if len(partes) != 3:
                    raise ValueError(f"linea inesperada en HaterNet: {linea[:80]!r}")
                ident, texto, et = partes
                filas.append((ident.replace("id=", ""), texto, "hateful" if et.strip() == "1" else "non-hateful"))
        df = pd.DataFrame(filas, columns=["id", "texto", "etiqueta"])
        return pd.DataFrame({
            "texto": df["texto"].astype(str),
            "etiqueta": df["etiqueta"],
            "grupo": None,
            "functionality": float("nan"),
            "target_ident": float("nan"),
        })
    raise KeyError(nombre)


def resumen(nombre: str, df: pd.DataFrame) -> dict:
    r = {"conjunto": nombre, "cita": CITAS[nombre], "filas": int(len(df)),
         "distribucion": {str(k): int(v) for k, v in df["etiqueta"].value_counts().items()},
         "longitud_media_caracteres": round(float(df["texto"].str.len().mean()), 1)}
    if nombre == "hatecheck":
        r["funcionalidades"] = int(df["functionality"].nunique())
        r["plantillas"] = int(df["grupo"].nunique())
    return r
