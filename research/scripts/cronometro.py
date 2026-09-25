#!/usr/bin/env python3
"""Cronometro del lote crudo. Anota hitos por caso en research/cronometro.log.

POR QUE EXISTE
    DEC-014: los tiempos los cronometra el agente y se declaran como
    recuperabilidad-por-agente. Un reloj mental no es un dato. Cada hito queda
    con timestamp UTC en un log append-only, y los minutos del CSV se derivan
    de ahi, nunca se teclean.

HITOS
    t0   claim admitido, empieza LOCALIZAR
    t1   primaria localizada o abandonada, empieza EXTRAER
    t2   extraccion terminada o abandonada

USO
    python research/scripts/cronometro.py C01 t0 "SEPE paro agosto"
    python research/scripts/cronometro.py C01 t1
    python research/scripts/cronometro.py C01 t2 "abandonado: 403"
    python research/scripts/cronometro.py --resumen
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "cronometro.log"
HITOS = ("t0", "t1", "t2")


def ahora() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def leer() -> dict[str, dict[str, dt.datetime]]:
    """case_id -> {hito: timestamp}. Si un hito se repite, gana el ultimo."""
    marcas: dict[str, dict[str, dt.datetime]] = {}
    if not LOG.exists():
        return marcas
    for linea in LOG.read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        ts, case_id, hito, *_ = linea.split("\t")
        marcas.setdefault(case_id, {})[hito] = dt.datetime.fromisoformat(ts)
    return marcas


def minutos(case_id: str) -> tuple[float | None, float | None]:
    """(minutes_to_locate, minutes_to_extract), None si falta un hito."""
    m = leer().get(case_id, {})
    loc = (m["t1"] - m["t0"]).total_seconds() / 60 if {"t0", "t1"} <= m.keys() else None
    ext = (m["t2"] - m["t1"]).total_seconds() / 60 if {"t1", "t2"} <= m.keys() else None
    return loc, ext


def anotar(case_id: str, hito: str, nota: str) -> None:
    ts = ahora()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{ts}\t{case_id}\t{hito}\t{nota}\n")
    print(f"{ts}  {case_id}  {hito}  {nota}".rstrip())


def resumen() -> None:
    marcas = leer()
    if not marcas:
        print("sin hitos todavia")
        return
    print(f"{'caso':6} {'localizar':>10} {'extraer':>9}   hitos")
    for case_id in sorted(marcas):
        loc, ext = minutos(case_id)
        f = lambda v: f"{v:8.1f} m" if v is not None else "      -- "
        print(f"{case_id:6} {f(loc):>10} {f(ext):>9}   {' '.join(sorted(marcas[case_id]))}")


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--resumen":
        resumen()
        return 0
    if len(sys.argv) < 3 or sys.argv[2] not in HITOS:
        print(__doc__)
        return 2
    anotar(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
