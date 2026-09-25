#!/usr/bin/env python3
"""Fase A1 de la auditoria del piloto: recomputa la aritmetica de los 20 casos.

QUE HACE
    Cada caso del Excel tiene una columna "Contraste / calculo clave" con
    porcentajes y razones ya calculados a mano. Este script los recalcula desde
    los valores de "Dato A" y "Dato B" y compara.

POR QUE EXISTE
    START-HERE 9, paso 5: "confirma que los numeros del Excel esten respaldados".
    Un numero mal calculado en el corpus se propaga a cada test de regresion que
    se escriba despues. Y es lo unico de la auditoria que se puede comprobar sin
    depender de que ningun servidor siga vivo.

POR QUE LAS EXPRESIONES ESTAN ESCRITAS A MANO Y NO PARSEADAS DEL EXCEL
    Parsear "2018: score 8,08; puesto 19" con una expresion regular seria
    adivinar. Cada comprobacion se transcribe explicitamente, con su origen
    citado, para que un tercero pueda verificar la transcripcion contra el Excel.
    Es mas trabajo y es auditable; un parser generico no lo seria.

USO
    python research/scripts/auditar_aritmetica.py
    Codigo de salida 1 si hay alguna discrepancia real (no de redondeo).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable

# ---------------------------------------------------------------------------
# Politica de tolerancia
# ---------------------------------------------------------------------------
# Una diferencia no es un error si cae dentro de lo que explica el redondeo de
# las entradas. Sin esta politica el script reportaria como fallo cada "~" del
# Excel, que es ruido y esconde los errores de verdad.
#
#   exacta      ambas entradas son cifras exactas -> margen estrecho
#   aproximada  alguna entrada lleva "~", ">" o "del orden de" -> margen amplio
#   citada      el valor del Excel es la cifra que dijo el emisor, no un calculo
#               propio -> se comprueba que sea plausible, no que cuadre al decimal


def tolerancia(valor_excel: float, entrada: str) -> float:
    """Margen absoluto admisible, en puntos porcentuales."""
    magnitud = abs(valor_excel)
    if entrada == "aproximada":
        return max(0.5, magnitud * 0.002)      # 0,2% relativo
    if entrada == "citada":
        return max(1.0, magnitud * 0.005)      # 0,5% relativo
    if magnitud < 100:
        return 0.1
    if magnitud < 1000:
        return 0.5
    return magnitud * 0.001


@dataclass
class Comprobacion:
    caso: str
    descripcion: str
    calcular: Callable[[], float]
    valor_excel: float | None
    entrada: str = "exacta"
    origen: str = ""
    nota: str = ""

    def evaluar(self) -> tuple[str, float | None, float | None]:
        """Devuelve (estado, calculado, diferencia)."""
        if self.valor_excel is None:
            return "NO_VERIFICABLE", None, None
        calculado = self.calcular()
        diferencia = abs(calculado - self.valor_excel)
        limite = tolerancia(self.valor_excel, self.entrada)
        if diferencia <= limite:
            estado = "OK" if self.entrada == "exacta" else "OK_REDONDEO"
        else:
            estado = "DISCREPA"
        return estado, calculado, diferencia


def variacion(antes: float, despues: float) -> float:
    """Variacion porcentual de antes a despues."""
    return (despues / antes - 1) * 100


def cagr(inicial: float, final: float, anios: int) -> float:
    """Tasa de crecimiento anual compuesta, en porcentaje."""
    return ((final / inicial) ** (1 / anios) - 1) * 100


# ---------------------------------------------------------------------------
# Las comprobaciones, caso por caso.
# `origen` cita el texto del Excel del que sale cada cifra.
# ---------------------------------------------------------------------------

COMPROBACIONES: list[Comprobacion] = [
    # -- P01 -----------------------------------------------------------------
    Comprobacion(
        "P01", "score 2018 -> 2025 (mejora)",
        lambda: 8.20 - 8.08, 0.12,
        origen="Dato A '2018: score 8,08' / Dato B '2025: score 8,20'",
        nota="Diferencia en puntos de indice, no porcentaje.",
    ),
    Comprobacion(
        "P01", "puesto 2018 -> 2025 (empeora)",
        lambda: 22 - 19, 3,
        origen="Dato A 'puesto 19' / Dato B 'puesto 22'",
        nota="El nucleo del caso: el score sube y la posicion baja.",
    ),
    # -- P02 -----------------------------------------------------------------
    Comprobacion(
        "P02", "valor monetario 1S2025 -> 1S2026",
        lambda: variacion(641_000, 58_000_000), 8945.0, "aproximada",
        origen="Dato A '~641.000 EUR' / Dato B '~58 M EUR'",
        nota="Ambas entradas aproximadas; el claim decia 9000%.",
    ),
    Comprobacion(
        "P02", "volumen en toneladas 1S2025 -> 1S2026",
        lambda: variacion(276, 18_798), None,
        origen="Dato A '276 t' / Dato B '18.798 t'",
        nota="El Excel no da cifra para el volumen, solo dice 'no 90 veces'.",
    ),
    # -- P03 -----------------------------------------------------------------
    Comprobacion(
        "P03", "1S2022 vs 1S2021",
        lambda: variacion(897_048, 1_127_147), 25.7,
        origen="Dato A '2021: 897.048' / Dato B '2022: 1.127.147'",
    ),
    Comprobacion(
        "P03", "1S2022 vs 1S2019 (baseline prepandemia)",
        lambda: variacion(1_070_421, 1_127_147), 5.03,
        origen="Dato B '2019: 1.070.421'",
        nota="SOSPECHA: transposicion de digitos, 5,03 por 5,30.",
    ),
    # -- P04 -----------------------------------------------------------------
    Comprobacion(
        "P04", "crecimiento total 1998-2018",
        lambda: variacion(831, 2_431), 192.5,
        origen="Dato A '1998: 831' / Dato B '2018: 2.431'",
    ),
    Comprobacion(
        "P04", "total dividido entre 20 anios (calculo erroneo del claim)",
        lambda: variacion(831, 2_431) / 20, 9.63,
        origen="Contraste 'Dividirlo entre 20 (~9,63%)'",
        nota="Se comprueba que el Excel reproduce bien el error del emisor.",
    ),
    Comprobacion(
        "P04", "CAGR real 1998-2018",
        lambda: cagr(831, 2_431, 20), 5.51,
        origen="Contraste 'CAGR ~5,51%'",
        nota="Es el numero que desmonta el claim del 10% anual.",
    ),
    # -- P05 -----------------------------------------------------------------
    Comprobacion(
        "P05", "autopercepcion clase media abril2018 -> abril2026",
        lambda: 55.9 - 56.9, -1.0,
        origen="Dato A '2018: 56,9%' / Dato B '2026: 55,9%'",
        nota="Caida de 1 pp. El claim afirmaba 66,7% -> 50%.",
    ),
    Comprobacion(
        "P05", "magnitud que afirmaba el claim (dos tercios -> la mitad)",
        lambda: 50.0 - (2 / 3 * 100), -16.67,
        origen="Claim 'dos de cada tres' -> 'uno de cada dos'",
        nota="16,67 pp afirmados contra 1 pp real.",
    ),
    # -- P06 -----------------------------------------------------------------
    Comprobacion(
        "P06", "2018 -> 2025 con categoria homogenea",
        lambda: variacion(79, 147), 86.1,
        origen="Dato A '2018 anual: 79' / Dato B '2025 provisional: 147'",
    ),
    Comprobacion(
        "P06", "147 contra categoria antigua de 31 (el 374% del claim)",
        lambda: variacion(31, 147), 374.0, "citada",
        origen="Contraste 'El 374% sale de comparar 147 con una categoria antigua de 31'",
        nota="El 374% es la cifra del emisor; se comprueba que es reproducible.",
    ),
    # -- P07 -----------------------------------------------------------------
    Comprobacion(
        "P07", "poblacion reclusa extranjera en Espania",
        lambda: 19_939 / 60_938 * 100, 32.7,
        origen="Dato A 'Espania mayo 2025: 19.939 / 60.938'",
    ),
    Comprobacion(
        "P07", "poblacion reclusa extranjera en Cataluna",
        lambda: 4_554 / 8_594 * 100, 53.0,
        origen="Dato B 'Cataluna 2024: 4.554 / 8.594 ~53%'",
        nota="El 50% del claim solo se parece al dato catalan, no al espaniol.",
    ),
    # -- P08  (fuera del alcance de tesis por DEC-013) -----------------------
    Comprobacion(
        "P08", "82% con el denominador sesgado del corte inicial",
        lambda: 104 / 127 * 100, 82.0, "citada",
        origen="Claim '104 de 127'",
        nota="FUERA DE ALCANCE (DEC-013). El 82% es aritmeticamente correcto; "
             "el defecto esta en el denominador, no en la division.",
    ),
    Comprobacion(
        "P08", "denominador correcto incluyendo seguimiento pendiente",
        lambda: 104 / (127 + 905) * 100, None,
        origen="Dato B '905 embarazos tempranos aun sin seguimiento'",
        nota="El Excel no da cifra; se calcula para dimensionar el sesgo.",
    ),
    # -- P09  (fuera del alcance de tesis por DEC-013) -----------------------
    Comprobacion(
        "P09", "+610% relativo", lambda: 610.0, 610.0, "citada",
        origen="Dato A 'Mensaje: +610%'",
        nota="FUERA DE ALCANCE (DEC-013). No hay valores absolutos en el Excel "
             "para recomputarlo: el caso es sobre riesgo relativo vs absoluto.",
    ),
    # -- P10 -----------------------------------------------------------------
    Comprobacion(
        "P10", "caida contra el trimestre base extraordinario",
        lambda: float("nan"), None,
        origen="Dato A '>20.000 M EUR' / Dato B 'media ~7.500 M EUR'",
        nota="NO VERIFICABLE: '>' y '~' no son valores. No se puede comprobar "
             "'un tercio' ni '13.000 millones menos'.",
    ),
    # -- P11 -----------------------------------------------------------------
    Comprobacion(
        "P11", "sociedades constituidas mayo -> diciembre 2018",
        lambda: variacion(8_830, 6_811), -22.87,
        origen="Dato A 'Mayo 2018: 8.830' / Dato B 'Diciembre 2018: 6.811'",
        nota="Diciembre es sistematicamente un mes bajo: baseline estacional.",
    ),
    # -- P12 -----------------------------------------------------------------
    Comprobacion(
        "P12", "acumulado de altas contra stock de hospitalizados",
        lambda: 23_663 / 11_894, None,
        origen="Dato A 'acumulados 23.663' / Dato B 'stock del dia 11.894'",
        nota="La razon no significa nada: las series tienen bases temporales "
             "distintas. Se calcula solo para mostrar la magnitud del error.",
    ),
    # -- P13 -----------------------------------------------------------------
    Comprobacion(
        "P13", "extension de la serie homogeneizada",
        lambda: 2025 - 1961, 64,
        origen="Dato A 'serie desde 1961' / Dato B 'cambio de metodo en 2020'",
        nota="Control importante: el cambio metodologico NO rompio la "
             "comparabilidad porque AEMET recalculo la serie entera.",
    ),
    # -- P14 -----------------------------------------------------------------
    Comprobacion(
        "P14", "deuda en euros 2T2009 -> 2T2022 (multiplicador)",
        lambda: 11_823 / 4_282, 2.76,
        origen="Dato A '2T2009: 4.282 M EUR' / Dato B '2T2022: 11.823 M EUR'",
        nota="'Triplicar' seria x3; es x2,76.",
    ),
    Comprobacion(
        "P14", "deuda como % del PIB (multiplicador)",
        lambda: 17.8 / 7.5, 2.37,
        origen="Dato A '7,5% PIB' / Dato B '17,8% PIB'",
        nota="Segun la metrica elegida el multiplicador cambia: 2,76 o 2,37.",
    ),
    # -- P15 -----------------------------------------------------------------
    Comprobacion(
        "P15", "pluriempleo en Espania frente a la UE",
        lambda: 2.6 - 4.1, -1.5,
        origen="Dato A 'Espania: 2,6%' / Dato B 'UE: 4,1%'",
        nota="Espania esta 1,5 pp por debajo de la media: no lidera.",
    ),
    Comprobacion(
        "P15", "ocupados implicitos en 565.400 al 2,6%",
        lambda: 565_400 / 0.026 / 1_000_000, None,
        origen="Dato A '2,6% de ocupados; 565.400 personas'",
        nota="Coherencia interna: comprueba que el % y el absoluto son "
             "compatibles con la poblacion ocupada espaniola.",
    ),
    # -- P16 -----------------------------------------------------------------
    Comprobacion(
        "P16", "horas extra no pagadas sobre el total",
        lambda: 1_192.7 / 2_645.2 * 100, 45.1,
        origen="Dato A 'total 2.645,2 mil' / Dato B 'no pagadas 1.192,7'",
        nota="45,1% no supera la mitad: el claim es falso por aritmetica.",
    ),
    Comprobacion(
        "P16", "horas extra pagadas sobre el total",
        lambda: 1_452.5 / 2_645.2 * 100, 54.9,
        origen="Dato B 'pagadas 1.452,5'",
    ),
    Comprobacion(
        "P16", "coherencia: pagadas + no pagadas = total",
        lambda: 1_192.7 + 1_452.5, 2_645.2,
        origen="Dato A y Dato B",
        nota="Las tres cifras del Excel son mutuamente consistentes.",
    ),
    # -- P17 -----------------------------------------------------------------
    Comprobacion(
        "P17", "ruta Mediterraneo Occidental",
        lambda: variacion(6_720, 7_860), 17.0,
        origen="Dato A 'Mediterraneo Occidental: 6.720 -> 7.860 (+17%)'",
        nota="Esta ruta SUBE, contra el claim de caida en todas.",
    ),
    Comprobacion(
        "P17", "ruta Africa Occidental / Canarias",
        lambda: variacion(11_400, 3_714), -67.4,
        origen="Dato B 'Africa Occidental/Canarias: 11.400 -> 3.714 (-67,4%)'",
    ),
    Comprobacion(
        "P17", "agregado de las dos rutas",
        lambda: variacion(6_720 + 11_400, 7_860 + 3_714), -36.1,
        origen="Contraste 'Agregadas, las detecciones caen ~36,1%, no 60%'",
        nota="El claim decia 60% en todas las rutas.",
    ),
    # -- P18 -----------------------------------------------------------------
    Comprobacion(
        "P18", "extranjeros como complemento del 31% espanioles",
        lambda: 100 - 31, 69,
        origen="Dato A 'muestra: 95 agresores; 31% espanioles'",
        nota="El 69% del claim es correcto DENTRO de la submuestra de 95 casos "
             "de 2010; el defecto es el universo al que se atribuye.",
    ),
    Comprobacion(
        "P18", "tamanio de la submuestra",
        lambda: 95.0, 95,
        origen="Dato A 'muestra: 95 agresores'",
        nota="95 casos de un anio no sostienen una afirmacion sobre 'todos'.",
    ),
    # -- P19 -----------------------------------------------------------------
    Comprobacion(
        "P19", "tasa de paro juvenil actual contra el minimo historico",
        lambda: 24.5 - 16.9, 7.6,
        origen="Dato B '1T2026: tasa 24,5%; minimo 16,9% en 3T2006'",
        nota="Por tasa el claim es falso: 7,6 pp por encima del minimo. "
             "Por numero absoluto puede ser cierto. METRIC_AMBIGUOUS.",
    ),
    # -- P20  (control negativo) ---------------------------------------------
    Comprobacion(
        "P20", "desempleo Ecuador 1T2025 -> 1T2026",
        lambda: 3.4 - 3.8, -0.4,
        origen="Dato A '1T2025: 3,8%' / Dato B '1T2026: 3,4%'",
        nota="CONTROL NEGATIVO: comparacion interanual homogenea, sin "
             "divergencia. VERITAI debe aprender a NO alertar aqui.",
    ),
]


# ---------------------------------------------------------------------------
# Informe
# ---------------------------------------------------------------------------

ANCHO = 96


def main() -> int:
    print("=" * ANCHO)
    print("  VERITAI - Fase A1: recomputo de la aritmetica del piloto de 20 casos")
    print("=" * ANCHO)

    discrepancias: list[tuple[Comprobacion, float, float]] = []
    no_verificables: list[Comprobacion] = []
    conteo = {"OK": 0, "OK_REDONDEO": 0, "DISCREPA": 0, "NO_VERIFICABLE": 0}
    caso_actual = ""

    for c in COMPROBACIONES:
        if c.caso != caso_actual:
            caso_actual = c.caso
            print(f"\n{c.caso}")

        estado, calculado, diferencia = c.evaluar()
        conteo[estado] += 1

        if estado == "NO_VERIFICABLE":
            no_verificables.append(c)
            print(f"   [  --  ] {c.descripcion}")
            # El Excel no da cifra contra la que comparar, pero si la expresion
            # se puede calcular el valor sirve para dimensionar el problema en
            # el informe. Va etiquetado como informativo, nunca como validado.
            try:
                informativo = c.calcular()
            except Exception:  # noqa: BLE001 - una expresion no calculable es un dato en si
                informativo = float("nan")
            if informativo == informativo:  # descarta NaN
                print(f"            excel: (sin cifra)   calculado {informativo:.4f}"
                      f"  <- informativo, no validado")
            else:
                print("            excel: (sin cifra)   no calculable")
            print(f"            {c.nota}")
            continue

        assert calculado is not None and diferencia is not None
        marca = {"OK": "  OK  ", "OK_REDONDEO": " ~OK  ", "DISCREPA": "DISCREPA"}[estado]
        print(f"   [{marca}] {c.descripcion}")
        print(f"            calculado {calculado:>12.4f}   excel {c.valor_excel:>12.4f}"
              f"   dif {diferencia:.4f}   ({c.entrada})")
        if c.nota:
            print(f"            {c.nota}")
        if estado == "DISCREPA":
            discrepancias.append((c, calculado, diferencia))

    print("\n" + "=" * ANCHO)
    print("  RESUMEN")
    print("=" * ANCHO)
    print(f"  comprobaciones            {len(COMPROBACIONES)}")
    print(f"  cuadran exactamente       {conteo['OK']}")
    print(f"  cuadran dentro de redondeo {conteo['OK_REDONDEO']}")
    print(f"  DISCREPAN                 {conteo['DISCREPA']}")
    print(f"  no verificables           {conteo['NO_VERIFICABLE']}")

    if no_verificables:
        print("\n  No verificables (el Excel no da cifra suficiente):")
        for c in no_verificables:
            print(f"    - {c.caso}  {c.descripcion}")

    if discrepancias:
        print("\n  DISCREPANCIAS QUE HAY QUE CORREGIR EN EL CORPUS:")
        for c, calculado, diferencia in discrepancias:
            print(f"\n    {c.caso}  {c.descripcion}")
            print(f"      excel      {c.valor_excel}")
            print(f"      calculado  {calculado:.4f}")
            print(f"      origen     {c.origen}")
            if c.nota:
                print(f"      nota       {c.nota}")
        return 1

    print("\n  Sin discrepancias.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
