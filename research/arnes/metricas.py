"""Metricas del arnes de evaluacion (Puerta 3): las cinco de R02 §7 y el FPR con intervalos.

Funciones puras sobre listas de diccionarios: sin red, sin base de datos, sin LLM.
La aritmetica de los intervalos es la misma que justifica el tamano del conjunto
en research/PUERTA-3-DISENO.md: Wilson al 95 % y regla de tres cuando k = 0.

Entradas
    anotaciones  filas del CSV de anotacion (esquema de pilot-crudo-trabajados.csv o
                 PILOT-40.csv). Columnas usadas, todas opcionales salvo las cuatro
                 primeras: case_id, truth, context, clase_primaria,
                 current_edition_found, previous_edition_found, alcanzable_por_agente,
                 recuperabilidad, minutes_to_locate, minutes_to_extract,
                 cronometrado_por, abstain_reason
    resultados   {case_id: respuesta de POST /analisis} (lo que escribe
                 research/puerta2/ejecutar_casos.py en resultados/<id>.json, clave
                 "respuesta")

Definiciones fijadas antes de ver el conjunto de evaluacion
    conservadora  = el agente lo localizo SIN evadir nada (alcanzable_por_agente = si)
    leniente      = alguien lo localizo (DEC-019, DEC-021)
    control       = truth supported y context no_divergence_detected en la anotacion
    test aplicable= veredicto.tests[0].aplicable del sistema
    falso positivo= control con test aplicable y context divergence_detected del sistema
    senal         = no cuenta como falso positivo (DEC-029); se cuenta aparte
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from statistics import mean

Z95 = 1.959964

# Umbrales de R02 §7 (verde, ambar). "Edicion anterior" es la fila que manda.
UMBRALES_R02 = {
    "fuente_primaria_localizada": (70, 40),
    "edicion_anterior_localizada": (60, 30),
    "extraccion_sin_intervencion_extrema": (60, 30),
}
CLASES_NO_CONTABLES = {"", "none", "other_observed"}
CLASE_2A = "2_baseline_selection"


# --- intervalos ---------------------------------------------------------------
def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float, float]:
    """(proporcion, limite inferior, limite superior) de Wilson. n debe ser > 0."""
    if n <= 0 or k < 0 or k > n:
        raise ValueError(f"wilson: k={k}, n={n} fuera de rango")
    p = k / n
    d = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / d
    medio = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, centro - medio), min(1.0, centro + medio)


def regla_de_tres(n: int) -> float:
    """Limite superior aproximado al 95 % cuando k = 0: 3/n."""
    if n <= 0:
        raise ValueError("regla de tres: n debe ser > 0")
    return 3.0 / n


def semaforo(valor: float | None, verde: float, ambar: float, mayor_es_mejor: bool = True) -> str:
    if valor is None:
        return "n/d"
    if mayor_es_mejor:
        return "verde" if valor > verde else ("ambar" if valor >= ambar else "rojo")
    return "verde" if valor < verde else ("ambar" if valor <= ambar else "rojo")


@dataclass(frozen=True)
class Tasa:
    nombre: str
    k: int
    n: int

    @property
    def p(self) -> float | None:
        return None if self.n == 0 else self.k / self.n

    @property
    def ic95(self) -> tuple[float, float] | None:
        if self.n == 0:
            return None
        _, lo, hi = wilson(self.k, self.n)
        return lo, hi

    def a_dict(self) -> dict:
        ic = self.ic95
        return {
            "nombre": self.nombre,
            "k": self.k,
            "n": self.n,
            "p": None if self.p is None else round(100 * self.p, 1),
            "ic95": None if ic is None else [round(100 * ic[0], 1), round(100 * ic[1], 1)],
            "regla_de_tres": (
                round(min(100.0, 100 * regla_de_tres(self.n)), 1)
                if self.n and self.k == 0
                else None
            ),
        }


# --- utilidades sobre filas ---------------------------------------------------
def _si(fila: dict, columna: str) -> bool:
    return str(fila.get(columna) or "").strip().lower() == "si"


def _hay(anotaciones: list[dict], columna: str) -> bool:
    return bool(anotaciones) and all(columna in fila for fila in anotaciones)


def _minutos(fila: dict) -> float | None:
    try:
        a = float(fila.get("minutes_to_locate") or 0)
        b = float(fila.get("minutes_to_extract") or 0)
    except ValueError:
        return None
    if not (fila.get("minutes_to_locate") or fila.get("minutes_to_extract")):
        return None
    return a + b


# --- 1. las cinco de R02 §7 ----------------------------------------------------
def cinco_metricas(anotaciones: list[dict]) -> dict:
    """Las cinco metricas de R02 §7 sobre la anotacion, cada tasa en version
    conservadora y leniente con su IC 95 %. Una metrica cuya columna falta sale None."""
    n = len(anotaciones)
    salida: dict = {"n": n}

    def tasa(nombre: str, cond_cons, cond_len, col_necesaria: str) -> dict | None:
        if not _hay(anotaciones, col_necesaria):
            return None
        kc = sum(1 for f in anotaciones if cond_cons(f))
        kl = sum(1 for f in anotaciones if cond_len(f))
        verde, ambar = UMBRALES_R02[nombre]
        cons, len_ = Tasa(nombre + "_conservadora", kc, n), Tasa(nombre + "_leniente", kl, n)
        return {
            "conservadora": cons.a_dict(),
            "leniente": len_.a_dict(),
            "semaforo": semaforo(None if cons.p is None else 100 * cons.p, verde, ambar),
            "umbral": {"verde": verde, "ambar": ambar},
        }

    salida["fuente_primaria_localizada"] = tasa(
        "fuente_primaria_localizada",
        lambda f: _si(f, "current_edition_found") and _si(f, "alcanzable_por_agente"),
        lambda f: _si(f, "current_edition_found"),
        "current_edition_found",
    )
    salida["edicion_anterior_localizada"] = tasa(
        "edicion_anterior_localizada",
        lambda f: _si(f, "previous_edition_found") and _si(f, "alcanzable_por_agente"),
        lambda f: _si(f, "previous_edition_found"),
        "previous_edition_found",
    )
    salida["extraccion_sin_intervencion_extrema"] = tasa(
        "extraccion_sin_intervencion_extrema",
        lambda f: str(f.get("recuperabilidad") or "").strip() in ("A", "B"),
        lambda f: str(f.get("recuperabilidad") or "").strip() in ("A", "B"),
        "recuperabilidad",
    )

    clases = sorted(
        {
            str(f.get("clase_primaria") or "").strip()
            for f in anotaciones
            if str(f.get("context") or "").strip() == "divergence_detected"
        }
        - CLASES_NO_CONTABLES
    )
    salida["clases_de_divergencia_observadas"] = {
        "n_clases": len(clases),
        "clases": clases,
        "semaforo": "verde" if len(clases) >= 3 else ("ambar" if len(clases) == 2 else "rojo"),
        "umbral": {"verde": ">=3", "ambar": "2"},
    }

    por_quien: dict[str, list[float]] = {}
    for f in anotaciones:
        m = _minutos(f)
        if m is None:
            continue
        quien = str(f.get("cronometrado_por") or "sin_indicar").strip() or "sin_indicar"
        por_quien.setdefault(quien, []).append(m)
    tiempos = {
        quien: {
            "n": len(ms),
            "media_min": round(mean(ms), 1),
            "max_min": round(max(ms), 1),
            "semaforo": semaforo(mean(ms), 20, 45, mayor_es_mejor=False),
        }
        for quien, ms in por_quien.items()
    }
    salida["tiempo_medio_por_caso"] = tiempos or None
    return salida


# --- 2. FPR y H3 ---------------------------------------------------------------
def _veredicto(resultado: dict) -> dict:
    return resultado.get("veredicto") or {}


def test_aplicable(resultado: dict) -> bool:
    tests = _veredicto(resultado).get("tests") or []
    return bool(tests) and bool(tests[0].get("aplicable"))


def senales_de(resultado: dict) -> list[str]:
    tests = _veredicto(resultado).get("tests") or []
    return list(tests[0].get("senales") or []) if tests else []


def es_control(fila: dict) -> bool:
    return (
        str(fila.get("truth") or "").strip() == "supported"
        and str(fila.get("context") or "").strip() == "no_divergence_detected"
    )


def fpr(
    anotaciones: list[dict],
    resultados: dict[str, dict],
    min_n: int = 40,
    tasa_h3: float = 10.0,
    limite_h3: float = 15.0,
) -> dict:
    """Falsos positivos sobre controles con test aplicable, con IC 95 %, y el
    veredicto sobre H3 con la tasa y el limite fijados ANTES de evaluar."""
    controles = [
        (f, resultados[f["case_id"]])
        for f in anotaciones
        if f["case_id"] in resultados and es_control(f) and test_aplicable(resultados[f["case_id"]])
    ]
    fps = [f["case_id"] for f, r in controles if _veredicto(r).get("context") == "divergence_detected"]
    con_senal = [f["case_id"] for f, r in controles if senales_de(r)]
    t = Tasa("fpr_controles_con_test_aplicable", len(fps), len(controles))

    if t.n < min_n:
        h3 = "no_evaluable"
    else:
        _, _, hi = wilson(t.k, t.n)
        h3 = "sostenida" if 100 * t.p <= tasa_h3 and 100 * hi <= limite_h3 else "no_sostenida"

    # secundaria: todo lo anotado sin divergencia (incluye claims falsos) con test aplicable
    no_div = [
        (f, resultados[f["case_id"]])
        for f in anotaciones
        if f["case_id"] in resultados
        and str(f.get("context") or "").strip() == "no_divergence_detected"
        and test_aplicable(resultados[f["case_id"]])
    ]
    disparos = [f["case_id"] for f, r in no_div if _veredicto(r).get("context") == "divergence_detected"]
    controles_sin_test = [
        f["case_id"]
        for f in anotaciones
        if f["case_id"] in resultados and es_control(f) and not test_aplicable(resultados[f["case_id"]])
    ]
    return {
        "fpr": t.a_dict(),
        "falsos_positivos": fps,
        "controles_con_senal": con_senal,
        "controles_sin_test_aplicable": controles_sin_test,
        "h3": {
            "veredicto": h3,
            "tasa_fijada_pct": tasa_h3,
            "limite_superior_pct": limite_h3,
            "min_n": min_n,
        },
        "disparos_sobre_no_divergencia_anotada": Tasa(
            "disparos_sobre_no_divergencia_anotada", len(disparos), len(no_div)
        ).a_dict(),
        "disparos_ids": disparos,
    }


# --- 3. acuerdo sistema / anotacion (adicional, no es de R02 §7) --------------
def acuerdo(anotaciones: list[dict], resultados: dict[str, dict]) -> dict:
    pares = [(f, resultados[f["case_id"]]) for f in anotaciones if f["case_id"] in resultados]
    n = len(pares)

    def cuenta(cond) -> Tasa:
        return Tasa("", sum(1 for f, r in pares if cond(f, r)), n)

    truth = cuenta(lambda f, r: _veredicto(r).get("truth") == str(f.get("truth") or "").strip())
    context = cuenta(lambda f, r: _veredicto(r).get("context") == str(f.get("context") or "").strip())
    matriz = Counter(
        (str(f.get("context") or "").strip(), str(_veredicto(r).get("context") or "")) for f, r in pares
    )

    pos_2a = [
        (f, r)
        for f, r in pares
        if str(f.get("context") or "").strip() == "divergence_detected"
        and str(f.get("clase_primaria") or "").strip() == CLASE_2A
    ]
    det_2a = [
        f["case_id"]
        for f, r in pos_2a
        if _veredicto(r).get("context") == "divergence_detected"
        and _veredicto(r).get("clase_primaria") == CLASE_2A
    ]
    abst_anot = [(f, r) for f, r in pares if str(f.get("abstain_reason") or "").strip()]
    abst_ok = [f["case_id"] for f, r in abst_anot if _veredicto(r).get("abstain_reasons")]
    return {
        "n_pares": n,
        "acuerdo_truth": {**truth.a_dict(), "nombre": "acuerdo_truth"},
        "acuerdo_context": {**context.a_dict(), "nombre": "acuerdo_context"},
        "matriz_context_anotado_x_sistema": {f"{a} -> {s}": c for (a, s), c in sorted(matriz.items())},
        "recall_2a": {**Tasa("recall_2a", len(det_2a), len(pos_2a)).a_dict(), "detectados": det_2a},
        "abstencion_cuando_anotada": {
            **Tasa("abstencion_cuando_anotada", len(abst_ok), len(abst_anot)).a_dict(),
            "ids": abst_ok,
        },
    }


# --- guardia de conjunto (DEC-025) -------------------------------------------
def verificar_conjunto(casos: dict[str, dict], permitir_desarrollo: bool) -> list[str]:
    """Devuelve los errores que impiden evaluar: casos que no son de evaluacion."""
    errores = []
    for case_id, caso in sorted(casos.items()):
        conjunto = str(caso.get("conjunto") or "").strip()
        if conjunto != "evaluacion" and not permitir_desarrollo:
            errores.append(
                f"{case_id}: conjunto={conjunto or 'ausente'}; solo 'evaluacion' evalua (DEC-025). "
                "Para humo sobre desarrollo, --desarrollo"
            )
    return errores
