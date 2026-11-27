# -*- coding: utf-8 -*-
"""Pruebas del modulo IA2. Ejecutar desde research/ia2:  python -m pytest -q test_modulo.py

Necesitan los dos archivos de datos en datos/ (se descargan solos la primera vez).
No cargan el transformer: prueban la carga de datos, las particiones y que la
explicacion por fragmentos de la linea base es exacta.
"""
from __future__ import annotations

import numpy as np
import pytest

import datos
import explicar


@pytest.fixture(scope="module")
def hatecheck():
    return datos.cargar("hatecheck")


@pytest.fixture(scope="module")
def haternet():
    return datos.cargar("haternet")


def test_hatecheck_tiene_la_forma_declarada(hatecheck):
    assert len(hatecheck) == 3745
    assert set(hatecheck["etiqueta"]) == {"hateful", "non-hateful"}
    assert int((hatecheck["etiqueta"] == "hateful").sum()) == 2632
    assert hatecheck["functionality"].nunique() == 27
    assert hatecheck["grupo"].dtype.kind == "i"


def test_haternet_se_parsea_entero(haternet):
    assert len(haternet) == 6000
    d = haternet["etiqueta"].value_counts().to_dict()
    assert d == {"non-hateful": 4433, "hateful": 1567}
    assert haternet["texto"].str.len().min() > 0
    assert not haternet["texto"].str.contains(";||;", regex=False).any()


def test_particiones_coinciden_con_los_scripts():
    X_tr, y_tr, X_te, y_te, nombre = explicar.particion("hatecheck")
    assert nombre == "por_plantilla" and (len(X_tr), len(X_te)) == (3026, 719)
    X_tr, y_tr, X_te, y_te, nombre = explicar.particion("haternet")
    assert nombre == "por_caso" and (len(X_tr), len(X_te)) == (4800, 1200)
    # estratificada: misma proporcion de odio en entrenamiento y prueba (±1 punto)
    p_tr = np.mean(y_tr == "hateful"); p_te = np.mean(y_te == "hateful")
    assert abs(p_tr - p_te) < 0.01


def test_contribuciones_de_A_suman_el_logit(hatecheck):
    # una de cada seis filas: el archivo va ordenado por funcionalidad y las primeras son todas hostiles
    X = np.array(hatecheck["texto"].tolist()[::6], dtype=object)
    y = np.array(hatecheck["etiqueta"].tolist()[::6], dtype=object)
    assert len(set(y)) == 2
    m = explicar.modelo_a(X, y)
    vec, clf = m.named_steps["tfidf"], m.named_steps["lr"]
    for texto in ("Las mujeres son fantásticas.", "Odio a los inmigrantes.", "No conozco a muchos trans."):
        e = explicar.fragmentos_a(m, texto, k=1000)
        suma = sum(v for _, v in e["hacia_hostil"]) + sum(v for _, v in e["hacia_no_hostil"]) + e["sesgo"]
        # logit hacia 'hateful' = -decision_function (la clase positiva de sklearn es 'non-hateful')
        logit = -float(clf.decision_function(vec.transform([texto]))[0])
        assert suma == pytest.approx(logit, abs=0.01)
        assert 0.0 <= e["p_hostil"] <= 1.0
