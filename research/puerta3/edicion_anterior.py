"""Edicion anterior de una nota del INE, fuera de Tempus (condicion bloqueante de DEC-034).

Tempus sirve solo la edicion vigente de cada serie. Para 2b (base revisada) hace
falta el dato TAL COMO SE PUBLICO en su momento: la nota de prensa de aquella
edicion (HTML y PDF) y su anexo de tablas (xlsx). Este script deriva sus URLs
del codigo de la nota, las descarga con el agente identificado (DEC-018) y
extrae la fila pedida del anexo, para compararla con la serie vigente de la API.

Codigo de nota del INE: <OPERACION><MM><YY> para mensuales (CTH0725 = Coyuntura
Turistica Hotelera, julio 2025) y <OPERACION><n>T<YY> para trimestrales
(IPV2T26). Las tres rutas, comprobadas en la jornada 2:

    https://www.ine.es/dyngs/Prensa/<CODIGO>.htm          nota HTML
    https://www.ine.es/dyngs/Prensa/<CODIGO>.pdf          nota PDF
    https://www.ine.es/prensa/anexo_tablas/es/<CODIGO>.xlsx   anexo de tablas

Uso:
    python edicion_anterior.py CTH 2025-07 --fila "Madrid, Comunidad de" --hoja EOH_Hoja3 \
        --serie EOT1766 --periodo 2025-M07
    python edicion_anterior.py ETDP 2025-07 --fila TOTAL --serie ETDP1826 --periodo 2025-M07

Guarda las descargas en el directorio de evidencia (por defecto research/evidencia/)
como D2B_<CODIGO>.<ext> y escribe un resumen JSON con estado HTTP, tamano, sha256,
fecha de publicacion (leida de la nota) y la fila extraida.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from html import unescape
from pathlib import Path

UA = "VERITAI-prototipo/0.1 (tesis UDLA; agente identificado, DEC-018)"
HOST = "https://www.ine.es"
API = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/"
TIMEOUT = 60
MAX_BYTES = 20 * 1024 * 1024
AQUI = Path(__file__).resolve().parent
EVIDENCIA = AQUI.parent / "evidencia"

RUTAS = {
    "html": HOST + "/dyngs/Prensa/{codigo}.htm",
    "pdf": HOST + "/dyngs/Prensa/{codigo}.pdf",
    "xlsx": HOST + "/prensa/anexo_tablas/es/{codigo}.xlsx",
}


def codigo_nota(operacion: str, periodo: str) -> str:
    """CTH + 2025-07 -> CTH0725; IPV + 2026-T2 -> IPV2T26."""
    m = re.fullmatch(r"(\d{4})-(\d{2})", periodo)
    if m:
        return f"{operacion}{m.group(2)}{m.group(1)[2:]}"
    m = re.fullmatch(r"(\d{4})-T([1-4])", periodo)
    if m:
        return f"{operacion}{m.group(2)}T{m.group(1)[2:]}"
    raise ValueError(f"periodo no reconocido: {periodo!r} (usa YYYY-MM o YYYY-Tn)")


def descargar(url: str) -> dict:
    """GET con agente identificado, timeout y tope de bytes. Un rechazo no se reintenta (DEC-021)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                return {"url": url, "http": r.status, "error": "supera el tope de bytes"}
            return {
                "url": url,
                "http": r.status,
                "content_type": r.headers.get("Content-Type", ""),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw": raw,
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "http": e.code, "error": f"HTTP {e.code}"}
    except Exception as e:  # red: ECONNREFUSED, timeout...
        return {"url": url, "http": None, "error": f"red: {e}"}


def fecha_publicacion_html(raw: bytes) -> str | None:
    txt = unescape(re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "replace")))
    txt = re.sub(r"\s+", " ", txt)
    m = re.search(r"publicados (\d{1,2} de \w+ de \d{4})", txt)
    return m.group(1) if m else None


def titular_html(raw: bytes) -> str | None:
    txt = unescape(re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "replace")))
    txt = re.sub(r"\s+", " ", txt)
    m = re.search(r"Principales resultados (.{20,300}?\.)", txt)
    return m.group(1) if m else None


def fila_xlsx(raw: bytes, fila: str, hoja: str | None) -> list[dict]:
    import warnings

    import openpyxl

    warnings.filterwarnings("ignore")
    wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
    hallazgos = []
    for ws in wb.worksheets:
        if hoja and ws.title != hoja:
            continue
        cabecera = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            vals = [c for c in row if c is not None]
            if i < 12 and vals:
                cabecera.append(" | ".join(str(v) for v in vals[:8]))
            if any(isinstance(c, str) and c.strip().lower() == fila.strip().lower() for c in row):
                hallazgos.append({"hoja": ws.title, "fila_idx": i, "cabecera": cabecera[:8], "valores": vals})
    return hallazgos


def serie_api(cod: str, periodo: str) -> dict:
    """Valor vigente en Tempus para un periodo YYYY-Mmm, para contrastar con la edicion anterior."""
    r = descargar(f"{API}{cod}?nult=30")
    if "raw" not in r:
        return {"serie": cod, "error": r.get("error")}
    s = json.loads(r["raw"])
    for d in s["Data"]:
        if f"{d['Anyo']}-M{d['FK_Periodo']:02d}" == periodo:
            return {"serie": cod, "nombre": s.get("Nombre"), "periodo": periodo, "valor": d["Valor"],
                    "consultado": datetime.now(UTC).isoformat(timespec="seconds")}
    return {"serie": cod, "periodo": periodo, "error": "periodo no servido"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("operacion")
    ap.add_argument("periodo", help="YYYY-MM o YYYY-Tn de la EDICION que se quiere recuperar")
    ap.add_argument("--fila", help="etiqueta de la fila a extraer del anexo (p. ej. 'Madrid, Comunidad de')")
    ap.add_argument("--hoja", help="hoja del anexo; si falta se buscan todas")
    ap.add_argument("--serie", help="codigo de serie Tempus para contrastar (p. ej. EOT1766)")
    ap.add_argument("--periodo-serie", help="periodo YYYY-Mmm de la serie; por defecto el de la edicion")
    ap.add_argument("--formatos", default="html,pdf,xlsx")
    ap.add_argument("--evidencia", default=str(EVIDENCIA))
    args = ap.parse_args()

    codigo = codigo_nota(args.operacion, args.periodo)
    out_dir = Path(args.evidencia)
    out_dir.mkdir(parents=True, exist_ok=True)
    resumen: dict = {"codigo": codigo, "consultado": datetime.now(UTC).isoformat(timespec="seconds"),
                     "agente": UA, "descargas": {}}
    for fmt in args.formatos.split(","):
        url = RUTAS[fmt].format(codigo=codigo)
        r = descargar(url)
        entrada = {k: v for k, v in r.items() if k != "raw"}
        if "raw" in r:
            destino = out_dir / f"D2B_{codigo}.{fmt if fmt != 'html' else 'htm'}"
            destino.write_bytes(r["raw"])
            entrada["guardado_en"] = str(destino.relative_to(AQUI.parent.parent)) if destino.is_relative_to(AQUI.parent.parent) else str(destino)
            if fmt == "html":
                entrada["fecha_publicacion"] = fecha_publicacion_html(r["raw"])
                entrada["titular"] = titular_html(r["raw"])
            if fmt == "xlsx" and args.fila:
                entrada["filas"] = fila_xlsx(r["raw"], args.fila, args.hoja)
        resumen["descargas"][fmt] = entrada
        estado = f"HTTP {entrada.get('http')}"
        print(f"{fmt:5s} {estado:9s} {entrada.get('bytes', '-'):>8} bytes  {url}")
    if args.serie:
        resumen["vigente"] = serie_api(args.serie, args.periodo_serie or args.periodo.replace("-", "-M"))
        v = resumen["vigente"]
        print(f"API   {v.get('serie')} {v.get('periodo')}: {v.get('valor', v.get('error'))}")
    if args.fila:
        for f in resumen["descargas"].get("xlsx", {}).get("filas", []):
            print(f"xlsx  hoja {f['hoja']} fila {f['fila_idx']}: {f['valores'][:9]}")
    print(f"nota  publicada: {resumen['descargas'].get('html', {}).get('fecha_publicacion')} | "
          f"{resumen['descargas'].get('html', {}).get('titular')}")
    (out_dir / f"D2B_{codigo}.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1, default=str),
                                                encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
