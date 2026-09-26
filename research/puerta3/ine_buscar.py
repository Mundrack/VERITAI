#!/usr/bin/env python3
"""Localiza tablas y series del INE en la API Tempus, para la recoleccion.

Es infraestructura de busqueda, no el conector del sistema: sirve para que el
agente encuentre el id de tabla y el nombre exacto de serie que van al JSON del
caso. Respeta las mismas reglas que el conector (solo servicios.ine.es, agente
identificado, sin reintentos ante rechazo; DEC-018, DEC-021).

USO
    python research/puerta3/ine_buscar.py operaciones compraventa      # operaciones cuyo nombre contiene el texto
    python research/puerta3/ine_buscar.py tablas 6                    # tablas de la operacion (por Id numerico)
    python research/puerta3/ine_buscar.py series 6150 "Total Nacional" # series de una tabla cuyo nombre contiene el texto (nult=3)
"""

from __future__ import annotations

import json
import sys
import urllib.request

BASE = "https://servicios.ine.es/wstempus/js/ES"
UA = {"User-Agent": "VERITAI-prototipo/0.1 (tesis UDLA; agente identificado, DEC-018)"}


def pedir(ruta: str) -> list | dict:
    req = urllib.request.Request(f"{BASE}/{ruta}", headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:  # noqa: S310 - host fijo, https
        return json.load(r)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) < 2:
        print(__doc__)
        return 2
    que, *resto = argv
    if que == "operaciones":
        texto = " ".join(resto).lower()
        for op in pedir("OPERACIONES_DISPONIBLES"):
            if texto in op["Nombre"].lower():
                print(f"{op['Id']:>6}  {op.get('Codigo', ''):8}  {op['Nombre']}")
    elif que == "tablas":
        for t in pedir(f"TABLAS_OPERACION/{resto[0]}"):
            print(f"{t['Id']:>6}  {t.get('Periodicidad', {}).get('Nombre', ''):10}  {t['Nombre']}")
    elif que == "series":
        tabla, texto = resto[0], " ".join(resto[1:]).lower()
        for s in pedir(f"DATOS_TABLA/{tabla}?nult=3&tip=A"):
            if texto in s["Nombre"].lower():
                datos = [(d["Anyo"], d["T3_Periodo"], d["Valor"]) for d in s["Data"]]
                print(f"{s['COD']:12} {s['Nombre']!r}  {s.get('T3_Unidad', '')}  {datos}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
