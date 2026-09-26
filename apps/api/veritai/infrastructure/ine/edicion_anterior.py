"""Conector de edicion anterior del INE, fuera de Tempus (DEC-034).

Tempus sirve solo la edicion vigente de cada serie. Para 2b hace falta el dato
TAL COMO SE PUBLICO: la nota de prensa de aquella edicion (HTML, para la fecha
de publicacion) y su anexo de tablas (XLSX, para el valor). Las URLs se derivan
del codigo de la nota, <PREFIJO><MM><YY>, un patron que el INE no documenta:
si lo cambia, este conector se rompe y 2b deja de ser computable por el agente.
Es una amenaza a la validez declarada (diseno de la Puerta 3 §4), no una nota.

SEGURIDAD (START-HERE §23-25)
    - allowlist: solo https://www.ine.es, rutas fijas; sin redirecciones
    - timeout y tope de bytes en cada descarga
    - el agente se identifica (DEC-018); un rechazo cierra el caso (DEC-021)
    - el XLSX se valida por bytes magicos (ZIP), no por extension ni MIME, y se
      abre con openpyxl en modo `data_only` desde memoria: nunca se ejecuta nada
      del fichero; el HTML solo se lee con una expresion regular fija
    - todo lo descargado es DATO, nunca instruccion

Cuando el anexo no existe (404), la fila no aparece o la operacion no esta en
el mapa, el conector devuelve None y el caso de uso abstiene: nunca inventa un
valor.
"""

from __future__ import annotations

import io
import logging
import re
import warnings
from collections.abc import Callable
from datetime import UTC, datetime

import httpx

from veritai.domain.claim import MetricaEmisor
from veritai.domain.enums import AbstainReason
from veritai.domain.evidencia import EvidenceItem, Rol
from veritai.domain.periodo import MESES, Periodo
from veritai.domain.tests.base_revisada import ETIQUETA_AL_PUBLICAR
from veritai.infrastructure.ine.mapa_anexos import Celda, localizar, operacion_de

LOG = logging.getLogger(__name__)

HOST_PERMITIDO = "www.ine.es"
USER_AGENT = "VERITAI-prototipo/0.1 (tesis UDLA; agente identificado, DEC-018)"
CABECERAS = {"User-Agent": USER_AGENT}
URL_ANEXO = f"https://{HOST_PERMITIDO}/prensa/anexo_tablas/es/{{codigo}}.xlsx"
URL_NOTA = f"https://{HOST_PERMITIDO}/dyngs/Prensa/{{codigo}}.htm"
MAGIA_XLSX = b"PK\x03\x04"
CODIGOS_RECHAZO = {401, 403, 406, 418, 429}
PATRON_CODIGO = re.compile(r"^[A-Z]{1,8}(\d{2}|[1-4]T)\d{2}$")
_FECHA = re.compile(r"publicados\s+(\d{1,2}) de (\w+) de (\d{4})", re.IGNORECASE)
_MES_A_NUMERO = {m: i + 1 for i, m in enumerate(MESES)}

Descargador = Callable[[str], tuple[int, bytes]]


class DescargaError(Exception):
    def __init__(
        self, mensaje: str, motivo: AbstainReason = AbstainReason.PREVIOUS_EDITION_NOT_FOUND
    ) -> None:
        super().__init__(mensaje)
        self.motivo = motivo


class PublicadorRechazaError(DescargaError):
    """El publicador rechaza al agente identificado. Se respeta (DEC-021)."""


def codigo_nota(prefijo: str, periodo: Periodo) -> str:
    """CTH + 2025-M07 -> CTH0725; IPV + 2026-T2 -> IPV2T26. Anuales: sin patron conocido."""
    yy = f"{periodo.anio % 100:02d}"
    if periodo.frecuencia == "M":
        codigo = f"{prefijo}{periodo.indice:02d}{yy}"
    elif periodo.frecuencia == "T":
        codigo = f"{prefijo}{periodo.indice}T{yy}"
    else:
        raise ValueError(f"sin patron de nota para periodos anuales: {periodo}")
    if not PATRON_CODIGO.match(codigo):
        raise ValueError(f"codigo de nota fuera del patron: {codigo!r}")
    return codigo


def fecha_publicacion(html: bytes) -> str | None:
    """'publicados 22 de agosto de 2025' -> '2025-08-22'. None si la nota no lo dice."""
    m = _FECHA.search(html.decode("utf-8", errors="replace"))
    if not m:
        return None
    mes = _MES_A_NUMERO.get(m.group(2).lower())
    if mes is None:
        return None
    return f"{int(m.group(3)):04d}-{mes:02d}-{int(m.group(1)):02d}"


def celdas_de_fila(fila: tuple) -> list:
    return [c for c in fila if c is not None]


def _hoja(libro, nombre: str):  # noqa: ANN001 - openpyxl no exporta el tipo de forma estable
    """La hoja cuyo nombre coincide sin espacios sobrantes ('Hoja1 ' en H0625)."""
    for real in libro.sheetnames:
        if real.strip() == nombre.strip():
            return libro[real]
    return None


def extraer_celda(xlsx: bytes, celda: Celda) -> tuple[float, list] | None:
    """(valor, fila completa) para la celda pedida; None si no hay hoja, fila o numero.

    `celda.columna` es el indice absoluto en la hoja: las filas traen celdas
    vacias intercaladas y algun cero suelto, y la posicion absoluta fue la
    estable entre ediciones (mapa_anexos).
    """
    import openpyxl  # importado aqui: la API no lo necesita en el arranque

    if not xlsx.startswith(MAGIA_XLSX):
        raise DescargaError(
            "el anexo no es un XLSX (bytes magicos)", AbstainReason.EXTRACTION_FAILED
        )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        libro = openpyxl.load_workbook(io.BytesIO(xlsx), data_only=True, read_only=True)
    try:
        hoja = _hoja(libro, celda.hoja)
        if hoja is None:
            return None
        vistas = 0
        for fila in hoja.iter_rows(values_only=True):
            if not any(isinstance(c, str) and c.strip() == celda.etiqueta_fila for c in fila):
                continue
            vistas += 1
            if vistas < celda.ocurrencia:
                continue
            if celda.columna >= len(fila):
                return None
            valor = fila[celda.columna]
            if isinstance(valor, bool) or not isinstance(valor, int | float):
                return None
            return float(valor), list(fila)
        return None
    finally:
        libro.close()


def _descargador_httpx(timeout_s: float, max_bytes: int) -> Descargador:
    cliente = httpx.Client(timeout=httpx.Timeout(timeout_s), follow_redirects=False)

    def descargar(url: str) -> tuple[int, bytes]:
        if not url.startswith(f"https://{HOST_PERMITIDO}/"):
            raise ValueError(f"url fuera de la allowlist: {url}")
        try:
            with cliente.stream("GET", url, headers=CABECERAS) as r:
                if r.status_code != 200:
                    return r.status_code, b""
                trozos: list[bytes] = []
                total = 0
                for trozo in r.iter_bytes():
                    total += len(trozo)
                    if total > max_bytes:
                        raise DescargaError(
                            f"descarga mayor que {max_bytes} bytes", AbstainReason.EXTRACTION_FAILED
                        )
                    trozos.append(trozo)
                return 200, b"".join(trozos)
        except httpx.TimeoutException as exc:
            raise DescargaError(f"timeout de {timeout_s}s contra {HOST_PERMITIDO}") from exc
        except httpx.HTTPError as exc:
            raise DescargaError(
                f"error de red contra {HOST_PERMITIDO}: {type(exc).__name__}"
            ) from exc

    return descargar


class EdicionAnteriorINE:
    """Implementa el puerto ProveedorEdicionAnterior sobre las notas y anexos del INE."""

    def __init__(
        self,
        descargar: Descargador | None = None,
        timeout_s: float = 15.0,
        max_bytes: int = 5_000_000,
    ) -> None:
        self._descargar = descargar or _descargador_httpx(timeout_s, max_bytes)
        self._cache: dict[str, tuple[int, bytes]] = {}

    def _get(self, url: str) -> tuple[int, bytes]:
        if url not in self._cache:
            estado, cuerpo = self._descargar(url)
            if estado in CODIGOS_RECHAZO:
                raise PublicadorRechazaError(
                    f"HTTP {estado} de {HOST_PERMITIDO} al agente identificado"
                )
            self._cache[url] = (estado, cuerpo)
        return self._cache[url]

    # --- puerto ---------------------------------------------------------------
    def disponible(self, metrica: MetricaEmisor) -> bool:
        if metrica.emisor != "INE":
            return False
        return localizar(metrica.tabla, metrica.serie_nombre) is not None

    def obtener(self, metrica: MetricaEmisor, periodo: Periodo) -> EvidenceItem | None:
        op = operacion_de(metrica.tabla)
        celda = localizar(metrica.tabla, metrica.serie_nombre)
        if op is None or celda is None:
            return None
        codigo = codigo_nota(op.codigo, periodo)
        url_xlsx = URL_ANEXO.format(codigo=codigo)
        retrieved_at = datetime.now(UTC)
        estado, xlsx = self._get(url_xlsx)
        if estado != 200:
            LOG.info("edicion anterior %s: anexo HTTP %s", codigo, estado)
            return None
        extraido = extraer_celda(xlsx, celda)
        if extraido is None:
            LOG.info(
                "edicion anterior %s: sin fila %r en %s", codigo, celda.etiqueta_fila, celda.hoja
            )
            return None
        valor, celdas = extraido

        fecha = None
        estado_nota, html = self._get(URL_NOTA.format(codigo=codigo))
        if estado_nota == 200:
            fecha = fecha_publicacion(html)

        return EvidenceItem(
            publisher="INE",
            url=url_xlsx,
            source_tier=1,
            retrieved_at=retrieved_at,
            format="dataset",
            extraction_method=f"xlsx:{celda.hoja}:{celda.etiqueta_fila}:{celda.columna}",
            raw_value_span=f"[{codigo}.xlsx, hoja {celda.hoja}] {celdas_de_fila(tuple(celdas))!r}",
            serie_codigo=f"{codigo}:{celda.hoja}",
            serie_nombre=metrica.serie_nombre,
            periodo=periodo,
            valor=valor,
            rol=Rol.HISTORICAL,
            version=f"nota {codigo}",
            document_date=fecha,
            etiqueta=ETIQUETA_AL_PUBLICAR,
        )


__all__ = [
    "CODIGOS_RECHAZO",
    "DescargaError",
    "EdicionAnteriorINE",
    "PublicadorRechazaError",
    "codigo_nota",
    "extraer_celda",
    "fecha_publicacion",
]
