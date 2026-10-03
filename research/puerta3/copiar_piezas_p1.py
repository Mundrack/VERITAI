"""Copia local de las siete piezas contadas en P1 sobre EOAT0826 (diseno §4h).

Encargo de Mateo del 2026-10-03: incorporar al registro de P1 las direcciones de
las siete piezas con su fecha de consulta y guardar copia local de cada una "si
el robots.txt lo permite, aplicando su Crawl-delay".

QUE HACE, por pieza:
  1. Pide el robots.txt del dominio UNA sola vez, con el agente identificado
     (DEC-018), y lo guarda tal cual en research/evidencia/.
  2. Decide si la ruta esta permitida (RFC 9309: el grupo propio si existe y, si
     no, el grupo "*"; gana la regla mas larga; Allow gana los empates).
  3. Espera el Crawl-delay que el sitio declare para ese grupo; si no declara
     ninguno, la pausa de cortesia del proyecto.
  4. Descarga la pagina sin seguir redirecciones a otro sitio, con tiempo maximo
     y tope de bytes, y la guarda con un nombre interno y su sha256.
  5. Comprueba que las cifras anotadas en §4h aparecen en el texto guardado.

QUE NO HACE:
  - No busca piezas ni cambia el conteo, el criterio o el veredicto de P1.
  - No evade nada (DEC-018). Un 401/403/406/418/429 o un desafio cierran esa
    copia como no recuperable por el agente, y no se reintenta (DEC-021). Solo un
    error de red admite un reintento.
  - No guarda copia si el robots.txt veta la ruta a nuestro agente. Tampoco si
    se la veta, con un grupo propio, a los agentes de Anthropic: este script lo
    ejecuta un agente de ese proveedor, y presentarse con el nombre del proyecto
    no cambia a quien no quiere leer el sitio. Mateo confirmo ese criterio el
    2026-10-03: esas copias las guarda una persona, a mano, desde su navegador.

COPIAS A MANO. Si una persona deja en research/evidencia/ el fichero que este
script espera para una pieza que el agente no puede pedir, el script la anota
en el resumen como guardada por una persona, con su sha256, y comprueba las
cifras. No hace ninguna peticion para eso.

La pieza 4 (El Nuevo Digital Murcia, caso E078) ya tiene copia del 2026-10-02
(J5_E078_elnuevodigitalmurcia.htm): no se vuelve a pedir.

Uso:
    python research/puerta3/copiar_piezas_p1.py --solo-robots   consulta y decide
    python research/puerta3/copiar_piezas_p1.py                 ademas, descarga

El robots.txt de cada dominio se pide una vez: la segunda orden reutiliza el que
guardo la primera. Salidas, en research/evidencia/:
    J5_P1_robots_<dominio>.txt     el robots.txt tal como llego
    J5_P1_<n>_<cabecera>.htm       la copia de cada pieza
    J5_P1_EOAT0826_piezas.json     resumen: direcciones, fechas, estados, sha256
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import UTC, datetime
from html import unescape
from pathlib import Path

UA = "VERITAI-prototipo/0.1 (tesis UDLA; agente identificado, DEC-018)"
NOMBRE_DEL_AGENTE = "veritai-prototipo"
# Los nombres con que Anthropic documenta a sus agentes, mas los dos antiguos que
# siguen apareciendo en los robots.txt de la prensa.
NOMBRES_DE_ANTHROPIC = ("claudebot", "claude-user", "claude-searchbot", "claude-web", "anthropic-ai")
TIMEOUT_S = 60
MAX_BYTES_PAGINA = 5 * 1024 * 1024
MAX_BYTES_ROBOTS = 512 * 1024  # RFC 9309 pide leer al menos 500 KiB
PAUSA_DE_CORTESIA_S = 3.0  # la misma que el 2026-10-02 con la pieza de Murcia
CRAWL_DELAY_MAXIMO_S = 120.0  # por encima no se espera: se anota y no se copia
REDIRECCIONES_MAXIMAS = 2
RECHAZOS = {401, 403, 406, 418, 429}  # DEC-021
SENALES_DE_DESAFIO = ("just a moment", "attention required", "captcha", "access denied", "are you a robot")
POR_EL_AGENTE = "el agente identificado"
POR_UNA_PERSONA = "una persona, a mano, desde su navegador (decision de Mateo del 2026-10-03); el agente no pide la pagina"

AQUI = Path(__file__).resolve().parent
EVIDENCIA = AQUI.parent / "evidencia"
RESUMEN = EVIDENCIA / "J5_P1_EOAT0826_piezas.json"

# Primera consulta: sesion 3 de la jornada 5, con la herramienta de lectura web del
# agente. Horas en UTC, del registro de aquella sesion (2026-10-01 por la noche, local).
PIEZAS = [
    {
        "n": 1,
        "pieza": "Europa Press, Andalucia",
        "leida_en": "Ultima Hora",
        "comunidad": "Andalucía",
        "url": "https://www.ultimahora.es/noticias/comunidades/2026/10/01/2720069/"
        "pernoctaciones-extrahoteleras-crecen-andalucia-agosto-superan-tres-millones.html",
        "primera_consulta_utc": "2026-10-02T02:25:50Z",
        "fichero": "J5_P1_1_europapress_andalucia_ultimahora.htm",
        "cifras": [r"20,3\s?(%|por ciento)", r"11,7\s?(%|por ciento)", r"2,04\s?(%|por ciento)", r"2,9\s?(%|por ciento)"],
    },
    {
        "n": 2,
        "pieza": "El Conciso (A. Ruiz)",
        "leida_en": "El Conciso",
        "comunidad": "Andalucía",
        "url": "https://www.elconciso.es/coyuntura/andalucia-viajeros-pernoctaciones-extrahoteleros-agosto_0_2008120049.html",
        "primera_consulta_utc": "2026-10-02T02:25:52Z",
        "fichero": "J5_P1_2_elconciso.htm",
        "cifras": [r"20,3\s?(%|por ciento)", r"271\.489 viajeros, un 2\s?(%|por ciento)"],
    },
    {
        "n": 3,
        "pieza": "ifomo (M. Alonso)",
        "leida_en": "ifomo",
        "comunidad": "Cantabria",
        "url": "https://www.ifomo.es/articulo/cantabria/"
        "cantabria-pernoctaciones-extrahoteleras-cantabria-bajan-54-agosto-viajeros-crecen-84/20261001103627360120.html",
        "primera_consulta_utc": "2026-10-02T02:25:54Z",
        "fichero": "J5_P1_3_ifomo.htm",
        "cifras": [
            r"apartamentos, un 8\s?(%|por ciento) menos",
            r"campings, concretamente 606\.447, un 5,4\s?(%|por ciento) menos",
        ],
    },
    {
        "n": 4,
        "pieza": "El Nuevo Digital Murcia (F. A.)",
        "leida_en": "El Nuevo Digital Murcia",
        "comunidad": "Región de Murcia",
        "url": "https://elnuevodigitalmurcia.es/art/9286/"
        "apartamentos-camping-y-casas-rurales-perdieron-en-agosto-un-30-de-viajeros-y-un-23-de-pernoctaciones",
        "primera_consulta_utc": "2026-10-02T02:25:59Z",
        "fichero": "J5_E078_elnuevodigitalmurcia.htm",
        "copia_previa": {
            "descargada_utc": "2026-10-02T02:28:21Z",
            "nota": "copia de la sesion 3 (caso E078), con robots.txt consultado antes; no se vuelve a pedir",
        },
        "cifras": [r"un 17\s?(%|por ciento) menos", r"\(-44\s?%\)"],
    },
    {
        "n": 5,
        "pieza": "Europa Press, Galicia",
        "leida_en": "Galicia Press",
        "comunidad": "Galicia",
        "url": "https://www.galiciapress.es/articulo/ultima-hora/2026-10-01/"
        "6035271-viajeros-alojados-casas-rurales-gallegas-aumentan-16-agosto",
        "primera_consulta_utc": "2026-10-02T02:27:12Z",
        "fichero": "J5_P1_5_europapress_galicia_galiciapress.htm",
        "cifras": [
            r"4,3\s?(%|por ciento) más",
            r"11,5\s?(%|por ciento) más",
            r"4,4\s?(%|por ciento) menos",
            r"cayeron un 6,6\s?(%|por ciento)",
        ],
    },
    {
        "n": 6,
        "pieza": "Europa Press, Illes Balears",
        "leida_en": "Ultima Hora",
        "comunidad": "Illes Balears",
        "url": "https://www.ultimahora.es/noticias/local/2026/10/01/2719959/"
        "pernoctaciones-apartamentos-turisticos-bajan-agosto-baleares-viajeros-suben.html",
        "primera_consulta_utc": "2026-10-02T02:27:14Z",
        "fichero": "J5_P1_6_europapress_baleares_ultimahora.htm",
        "cifras": [r"3,59\s?(%|por ciento)", r"\b9\s?(%|por ciento)"],
    },
    {
        "n": 7,
        "pieza": "ACN",
        "leida_en": "Via Empresa",
        "comunidad": "Cataluña",
        "url": "https://www.viaempresa.cat/es/economia/catalunya-record-turistas-extrahoteleros-agosto-mas-121-millones_2241311_102.html",
        "primera_consulta_utc": "2026-10-02T02:27:15Z",
        "fichero": "J5_P1_7_acn_viaempresa.htm",
        "cifras": [r"5,92\s?(%|por ciento)", r"5\.440\.058", r"1\.461\.194"],
    },
]


# --- red ---------------------------------------------------------------------------


class _SinRedireccion(urllib.request.HTTPRedirectHandler):
    """Ninguna redireccion se sigue sola: se decide a mano, y solo dentro del mismo sitio."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ARG002
        return None


ABRIR = urllib.request.build_opener(_SinRedireccion)
_ultima_peticion: dict[str, float] = {}


def ahora() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def pedir(url: str, tope: int) -> dict:
    """Un GET con el agente identificado. Un rechazo no se reintenta; un error de red, una vez."""
    partes = urllib.parse.urlsplit(url)
    if partes.scheme != "https" or not partes.hostname:
        raise ValueError(f"solo se piden direcciones https: {url!r}")
    host = partes.hostname
    for intento in (1, 2):
        peticion = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*;q=0.8"})  # noqa: S310
        cuando = ahora()
        try:
            with ABRIR.open(peticion, timeout=TIMEOUT_S) as r:  # noqa: S310 - solo https, comprobado arriba
                crudo = r.read(tope + 1)
                _ultima_peticion[host] = time.monotonic()
                if len(crudo) > tope:
                    return {"url": url, "cuando_utc": cuando, "http": r.status, "error": "supera el tope de bytes"}
                return {
                    "url": url,
                    "cuando_utc": cuando,
                    "http": r.status,
                    "content_type": r.headers.get("Content-Type", ""),
                    "bytes": len(crudo),
                    "sha256": hashlib.sha256(crudo).hexdigest(),
                    "crudo": crudo,
                }
        except urllib.error.HTTPError as e:
            _ultima_peticion[host] = time.monotonic()
            return {"url": url, "cuando_utc": cuando, "http": e.code, "location": e.headers.get("Location", "")}
        except Exception as e:  # noqa: BLE001 - red: ECONNREFUSED, socket hang up, timeout
            _ultima_peticion[host] = time.monotonic()
            if intento == 2:
                return {"url": url, "cuando_utc": cuando, "http": None, "error": f"red: {type(e).__name__}: {e}"}
            time.sleep(PAUSA_DE_CORTESIA_S)
    raise AssertionError("inalcanzable")


def esperar(host: str, segundos: float) -> float:
    """Espera lo que falte para que hayan pasado `segundos` desde la ultima peticion a ese host."""
    ultima = _ultima_peticion.get(host)
    if ultima is None:
        return 0.0
    falta = segundos - (time.monotonic() - ultima)
    if falta > 0:
        time.sleep(falta)
        return round(falta, 1)
    return 0.0


def mismo_sitio(a: str, b: str) -> bool:
    """El mismo host, o solo cambia el prefijo www."""
    return a.removeprefix("www.") == b.removeprefix("www.")


# --- robots.txt (RFC 9309) -----------------------------------------------------------


def grupos_de(texto: str) -> list[dict]:
    grupos: list[dict] = []
    actual: dict | None = None
    en_cabecera = False
    for linea in texto.splitlines():
        linea = linea.split("#", 1)[0].strip()
        if ":" not in linea:
            continue
        campo, valor = (p.strip() for p in linea.split(":", 1))
        campo = campo.lower()
        if campo == "user-agent":
            if actual is None or not en_cabecera:
                actual = {"agentes": [], "reglas": [], "crawl_delay": None}
                grupos.append(actual)
            actual["agentes"].append(valor.lower())
            en_cabecera = True
        elif actual is not None and campo in ("allow", "disallow"):
            en_cabecera = False
            if valor:
                actual["reglas"].append((campo, valor))
        elif actual is not None and campo == "crawl-delay":
            en_cabecera = False
            try:
                actual["crawl_delay"] = float(valor.replace(",", "."))
            except ValueError:
                pass
        # Cualquier otro campo (Sitemap, Host...) se ignora y no parte un grupo (RFC 9309 §2.2.4).
    return grupos


def grupo_para(grupos: list[dict], token: str, con_comodin: bool = True) -> tuple[str | None, list, float | None]:
    """El grupo mas especifico cuyo agente casa con `token`; si no hay, el de "*"."""
    casan = sorted({a for g in grupos for a in g["agentes"] if a != "*" and a in token}, key=len, reverse=True)
    elegido = casan[0] if casan else ("*" if con_comodin else None)
    if elegido is None:
        return None, [], None
    reglas, pausa = [], None
    for g in grupos:
        if elegido in g["agentes"]:
            reglas.extend(g["reglas"])
            if g["crawl_delay"] is not None:
                pausa = g["crawl_delay"]
    if not any(elegido in g["agentes"] for g in grupos):
        return None, [], None
    return elegido, reglas, pausa


def _patron(regla: str) -> re.Pattern[str]:
    final = regla.endswith("$")
    cuerpo = regla[:-1] if final else regla
    return re.compile("".join(".*" if c == "*" else re.escape(c) for c in cuerpo) + ("$" if final else ""))


def permitida(reglas: list, ruta: str) -> tuple[bool, str]:
    """Gana la regla mas larga que casa; en empate, Allow. Sin regla que case, permitido."""
    mejor: tuple[int, int, str, str] | None = None
    for campo, valor in reglas:
        if _patron(valor).match(ruta):
            candidato = (len(valor), 1 if campo == "allow" else 0, campo, valor)
            if mejor is None or candidato[:2] > mejor[:2]:
                mejor = candidato
    if mejor is None:
        return True, "ninguna regla casa"
    return mejor[2] == "allow", f"{mejor[2]}: {mejor[3]}"


def consultar_robots(host: str) -> dict:
    """Pide https://<host>/robots.txt una vez (o reutiliza el guardado) y lo deja interpretado."""
    guardado = EVIDENCIA / f"J5_P1_robots_{host}.txt"
    meta = EVIDENCIA / f"J5_P1_robots_{host}.json"
    if meta.exists():  # ya se pidio, saliera lo que saliera: no se pide otra vez
        info = json.loads(meta.read_text(encoding="utf-8"))
        info["reutilizado"] = True
        info["texto"] = guardado.read_text(encoding="utf-8", errors="replace") if guardado.exists() else ""
        return info

    url = f"https://{host}/robots.txt"
    cadena = []
    r = pedir(url, MAX_BYTES_ROBOTS)
    for _ in range(REDIRECCIONES_MAXIMAS):
        if r.get("http") not in (301, 302, 303, 307, 308):
            break
        destino = urllib.parse.urljoin(r["url"], r.get("location", ""))
        partes = urllib.parse.urlsplit(destino)
        cadena.append({"http": r["http"], "a": destino})
        if partes.scheme != "https" or not mismo_sitio(partes.hostname or "", host):
            r = {"url": destino, "cuando_utc": r["cuando_utc"], "http": r["http"], "error": "redirige fuera del sitio"}
            break
        esperar(urllib.parse.urlsplit(r["url"]).hostname or host, PAUSA_DE_CORTESIA_S)
        r = pedir(destino, MAX_BYTES_ROBOTS)

    info: dict = {"host": host, "url": r["url"], "cuando_utc": r["cuando_utc"], "http": r.get("http"), "redirecciones": cadena}
    crudo = r.get("crudo")
    texto = ""
    if r.get("error"):
        info["estado"] = "inalcanzable"
        info["detalle"] = r["error"]
    elif r["http"] in RECHAZOS:
        info["estado"] = "rechazo"
        info["detalle"] = f"HTTP {r['http']} al agente identificado (DEC-021): el dominio queda cerrado"
    elif r["http"] == 200 and crudo is not None:
        texto = crudo.decode("utf-8", errors="replace")
        info.update({"bytes": r["bytes"], "sha256": r["sha256"], "content_type": r["content_type"]})
        if "<html" in texto[:3000].lower() or "<!doctype" in texto[:3000].lower():
            info["estado"] = "no_es_robots"
            info["detalle"] = "la respuesta es HTML, no un robots.txt: no se interpreta como permiso"
        else:
            info["estado"] = "leido"
            guardado.write_bytes(crudo)
            info["guardado_en"] = f"research/evidencia/{guardado.name}"
    elif r["http"] is not None and 400 <= r["http"] < 500:
        info["estado"] = "sin_robots"
        info["detalle"] = f"HTTP {r['http']}: el sitio no publica robots.txt (RFC 9309, sin restricciones)"
    else:
        info["estado"] = "inalcanzable"
        info["detalle"] = f"HTTP {r.get('http')}: no se asume permiso"
    meta.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    info["reutilizado"] = False
    info["texto"] = texto
    return info


def decidir(robots: dict, url: str) -> dict:
    """Si la ruta se puede pedir, con que grupo, con que pausa, y que dice el sitio de los agentes de IA."""
    partes = urllib.parse.urlsplit(url)
    ruta = partes.path + (f"?{partes.query}" if partes.query else "")
    if robots["estado"] == "sin_robots":
        return {"permitido": True, "motivo": robots["detalle"], "grupo": None, "crawl_delay_s": None, "pausa_s": PAUSA_DE_CORTESIA_S}
    if robots["estado"] != "leido":
        return {"permitido": False, "motivo": robots.get("detalle", robots["estado"]), "grupo": None, "crawl_delay_s": None}

    grupos = grupos_de(robots["texto"])
    grupo, reglas, crawl_delay = grupo_para(grupos, NOMBRE_DEL_AGENTE)
    si, regla = permitida(reglas, ruta)

    lector = urllib.robotparser.RobotFileParser()
    lector.parse(robots["texto"].splitlines())
    segun_stdlib = lector.can_fetch(UA, url)

    vetos = []
    for token in NOMBRES_DE_ANTHROPIC:
        g, r, _ = grupo_para(grupos, token, con_comodin=False)
        if g is not None:
            ok, por = permitida(r, ruta)
            if not ok:
                vetos.append({"agente": g, "regla": por})

    decision = {
        "grupo": grupo,
        "regla": regla,
        "segun_urllib_robotparser": segun_stdlib,
        "crawl_delay_s": crawl_delay,
        "vetos_a_agentes_de_anthropic": vetos,
    }
    if not si:
        decision.update({"permitido": False, "motivo": f"el robots.txt veta la ruta al grupo {grupo!r} ({regla})"})
    elif not segun_stdlib:
        decision.update({"permitido": False, "motivo": "las dos lecturas del robots.txt no coinciden: no se asume permiso"})
    elif vetos:
        nombres = ", ".join(v["agente"] for v in vetos)
        motivo = f"el robots.txt veta la ruta a agentes de Anthropic ({nombres}): el agente no la pide"
        decision.update({"permitido": False, "motivo": motivo, "veto_a_anthropic": True})
    elif crawl_delay is not None and crawl_delay > CRAWL_DELAY_MAXIMO_S:
        decision.update({"permitido": False, "motivo": f"Crawl-delay de {crawl_delay} s, por encima del maximo que se espera"})
    else:
        decision.update({"permitido": True, "motivo": "permitido", "pausa_s": max(crawl_delay or 0.0, PAUSA_DE_CORTESIA_S)})
    return decision


# --- copia -----------------------------------------------------------------------


def texto_visible(crudo: bytes) -> str:
    t = crudo.decode("utf-8", errors="replace")
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = unescape(re.sub(r"<[^>]+>", " ", t)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t)


def comprobar_cifras(crudo: bytes, patrones: list[str]) -> list[dict]:
    texto = texto_visible(crudo)
    resultado = []
    for patron in patrones:
        m = re.search(patron, texto)
        entrada = {"patron": patron, "encontrada": m is not None}
        if m:
            entrada["contexto"] = texto[max(0, m.start() - 60) : m.end() + 40].strip()
        resultado.append(entrada)
    return resultado


def copiar(pieza: dict, decision: dict) -> dict:
    host = urllib.parse.urlsplit(pieza["url"]).hostname or ""
    esperado = esperar(host, decision["pausa_s"])
    r = pedir(pieza["url"], MAX_BYTES_PAGINA)
    cadena = []
    for _ in range(REDIRECCIONES_MAXIMAS):
        if r.get("http") not in (301, 302, 303, 307, 308):
            break
        destino = urllib.parse.urljoin(r["url"], r.get("location", ""))
        partes = urllib.parse.urlsplit(destino)
        cadena.append({"http": r["http"], "a": destino})
        if partes.scheme != "https" or partes.hostname != host:
            return {"copiada": False, "http": r["http"], "redirecciones": cadena, "motivo": "redirige a otro host: no se sigue"}
        esperar(host, decision["pausa_s"])
        r = pedir(destino, MAX_BYTES_PAGINA)

    copia: dict = {
        "cuando_utc": r["cuando_utc"],
        "http": r.get("http"),
        "espera_previa_s": esperado,
        "redirecciones": cadena,
        "url_final": r["url"],
    }
    crudo = r.get("crudo")
    if r.get("error"):
        copia.update({"copiada": False, "motivo": r["error"]})
    elif r["http"] in RECHAZOS:
        copia.update({"copiada": False, "motivo": f"HTTP {r['http']} al agente identificado: cerrada, sin reintento (DEC-021)"})
    elif r["http"] != 200 or crudo is None:
        copia.update({"copiada": False, "motivo": f"HTTP {r.get('http')}"})
    elif any(s in texto_visible(crudo)[:600].lower() for s in SENALES_DE_DESAFIO):
        copia.update({"copiada": False, "motivo": "la respuesta parece un desafio anti-bot: no se guarda ni se salta (DEC-018)"})
    else:
        (EVIDENCIA / pieza["fichero"]).write_bytes(crudo)
        copia.update(
            {
                "copiada": True,
                "por": POR_EL_AGENTE,
                "bytes": r["bytes"],
                "sha256": r["sha256"],
                "content_type": r["content_type"],
                "guardado_en": f"research/evidencia/{pieza['fichero']}",
                "cifras_de_4h_en_el_texto": comprobar_cifras(crudo, pieza["cifras"]),
            }
        )
    return copia


def copia_a_mano(pieza: dict, decision: dict) -> dict:
    """Una copia que dejo una persona en la carpeta de evidencia: se anota, sin pedir nada a la red."""
    destino = EVIDENCIA / pieza["fichero"]
    crudo = destino.read_bytes()
    return {
        "copiada": True,
        "por": POR_UNA_PERSONA,
        "por_que_no_el_agente": decision["motivo"],
        "fichero_guardado_utc": datetime.fromtimestamp(destino.stat().st_mtime, UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "anotada_utc": ahora(),
        "bytes": len(crudo),
        "sha256": hashlib.sha256(crudo).hexdigest(),
        "guardado_en": f"research/evidencia/{pieza['fichero']}",
        "cifras_de_4h_en_el_texto": comprobar_cifras(crudo, pieza["cifras"]),
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--solo-robots", action="store_true", help="consulta los robots.txt y decide; no descarga ninguna pagina")
    args = ap.parse_args()

    previo = json.loads(RESUMEN.read_text(encoding="utf-8")) if RESUMEN.exists() else {}
    previas = {p["n"]: p for p in previo.get("piezas", [])}
    robots_por_host: dict[str, dict] = {}
    salida = []
    for pieza in PIEZAS:
        host = urllib.parse.urlsplit(pieza["url"]).hostname or ""
        entrada = {k: pieza[k] for k in ("n", "pieza", "leida_en", "comunidad", "url", "primera_consulta_utc")}
        entrada["primera_consulta_como"] = "herramienta de lectura web del agente (sesion 3 de la jornada 5)"

        if "copia_previa" in pieza:
            crudo = (EVIDENCIA / pieza["fichero"]).read_bytes()
            entrada["copia"] = {
                "copiada": True,
                "por": POR_EL_AGENTE,
                "cuando_utc": pieza["copia_previa"]["descargada_utc"],
                "nota": pieza["copia_previa"]["nota"],
                "bytes": len(crudo),
                "sha256": hashlib.sha256(crudo).hexdigest(),
                "guardado_en": f"research/evidencia/{pieza['fichero']}",
                "cifras_de_4h_en_el_texto": comprobar_cifras(crudo, pieza["cifras"]),
            }
            salida.append(entrada)
            print(f"{pieza['n']}. {pieza['pieza']}: copia previa, {len(crudo)} bytes")
            continue

        if host not in robots_por_host:
            robots_por_host[host] = consultar_robots(host)
        robots = robots_por_host[host]
        decision = decidir(robots, pieza["url"])
        entrada["robots"] = {k: v for k, v in robots.items() if k not in ("texto",)} | {"decision": decision}
        print(
            f"{pieza['n']}. {pieza['pieza']} [{host}] robots: {robots['estado']} (HTTP {robots.get('http')}) -> "
            f"{'permitido' if decision['permitido'] else 'NO'}: {decision['motivo']}; Crawl-delay: {decision.get('crawl_delay_s')}"
        )

        ya = previas.get(pieza["n"], {}).get("copia")
        destino = EVIDENCIA / pieza["fichero"]
        if ya and ya.get("copiada") and destino.exists():
            # Ya esta anotada de una pasada anterior: no se pide otra vez. La comprobacion
            # de cifras si se repite, sobre el fichero guardado.
            entrada["copia"] = ya
            entrada["copia"].setdefault("por", POR_EL_AGENTE)
            crudo = destino.read_bytes()
            if hashlib.sha256(crudo).hexdigest() != ya["sha256"]:
                raise RuntimeError(f"{pieza['fichero']} ha cambiado desde que se anoto")
            entrada["copia"]["cifras_de_4h_en_el_texto"] = comprobar_cifras(crudo, pieza["cifras"])
        elif not decision["permitido"] and decision.get("veto_a_anthropic") and destino.exists():
            entrada["copia"] = copia_a_mano(pieza, decision)
            print(f"   copia a mano, de una persona: {entrada['copia']['bytes']} bytes, sha256 {entrada['copia']['sha256'][:16]}")
        elif not decision["permitido"]:
            entrada["copia"] = {"copiada": False, "motivo": decision["motivo"]}
            if decision.get("veto_a_anthropic"):
                entrada["copia"]["quien_la_guarda"] = POR_UNA_PERSONA
                entrada["copia"]["fichero_esperado"] = f"research/evidencia/{pieza['fichero']}"
        elif args.solo_robots:
            entrada["copia"] = {"copiada": False, "motivo": "pasada de solo robots: todavia no se ha pedido la pagina"}
        else:
            entrada["copia"] = copiar(pieza, decision)
            c = entrada["copia"]
            print(f"   copia: HTTP {c.get('http')} | {'guardada, ' + str(c.get('bytes')) + ' bytes' if c['copiada'] else c['motivo']}")
        salida.append(entrada)

    resumen = {
        "que_es": "Direcciones, fechas de consulta y copias locales de las siete piezas contadas en P1 sobre EOAT0826 (diseno 4h)",
        "generado_utc": ahora(),
        "agente": UA,
        "convencion": "robots.txt una vez por dominio antes de cualquier otra peticion; Crawl-delay del sitio o, si no declara, "
        f"{PAUSA_DE_CORTESIA_S} s de cortesia; un rechazo cierra la copia (DEC-018, DEC-021)",
        "piezas": salida,
    }
    RESUMEN.write_text(json.dumps(resumen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"resumen: research/evidencia/{RESUMEN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
