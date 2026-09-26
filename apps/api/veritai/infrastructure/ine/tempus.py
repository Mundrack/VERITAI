"""Cliente HTTP de la API Tempus del INE.

SEGURIDAD (START-HERE §23-25), desde la primera linea que toca internet:
    - allowlist: solo servicios.ine.es, solo HTTPS; la tabla es un entero
    - timeout y tope de bytes: una respuesta enorme o lenta no tumba la API
    - el agente se identifica con un User-Agent propio y NO se disfraza
      (DEC-018); un 403/406/418 cierra el caso (DEC-021), no se reintenta
    - el JSON se trata como DATO: se parsea con `json`, nunca se evalua

El cliente devuelve el texto crudo ademas del JSON parseado: el extractor
necesita el texto para capturar el `raw_value_span` literal.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx

from veritai.domain.enums import AbstainReason

LOG = logging.getLogger(__name__)

HOST_PERMITIDO = "servicios.ine.es"
BASE_URL = f"https://{HOST_PERMITIDO}/wstempus/js/ES"
USER_AGENT = "VERITAI-prototipo/0.1 (tesis UDLA; agente identificado, DEC-018)"
PATRON_TABLA = re.compile(r"^\d{1,8}$")
CODIGOS_RECHAZO = {401, 403, 406, 418, 429}


CABECERAS = {"User-Agent": USER_AGENT, "Accept": "application/json"}


class TempusError(Exception):
    def __init__(
        self, mensaje: str, motivo: AbstainReason = AbstainReason.PRIMARY_SOURCE_NOT_FOUND
    ) -> None:
        super().__init__(mensaje)
        self.motivo = motivo


class PublicadorRechazaError(TempusError):
    """El publicador senala que no quiere agentes. Se respeta (DEC-021)."""


@dataclass(frozen=True)
class RespuestaTempus:
    url: str
    texto: str
    retrieved_at: datetime
    estado: int


class ClienteTempus:
    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout_s: float = 15.0,
        max_bytes: int = 5_000_000,
        cliente: httpx.Client | None = None,
        cache_dir: Path | None = None,
    ) -> None:
        if not base_url.startswith(f"https://{HOST_PERMITIDO}/"):
            raise ValueError(f"base_url fuera de la allowlist: {base_url}")
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.max_bytes = max_bytes
        self.cache_dir = cache_dir
        self._cliente = cliente or httpx.Client(
            timeout=httpx.Timeout(timeout_s),
            follow_redirects=False,
        )

    def url_datos_tabla(self, tabla: str, nult: int) -> str:
        if not PATRON_TABLA.match(tabla):
            raise ValueError(f"id de tabla invalido: {tabla!r}")
        if not 1 <= nult <= 2000:
            raise ValueError(f"nult fuera de rango: {nult}")
        return f"{self.base_url}/DATOS_TABLA/{tabla}?nult={nult}&tip=A"

    def datos_tabla(self, tabla: str, nult: int) -> RespuestaTempus:
        url = self.url_datos_tabla(tabla, nult)
        retrieved_at = datetime.now(UTC)
        try:
            # Las cabeceras van en cada peticion: el agente se identifica aunque el
            # cliente HTTP venga inyectado (tests, o un cliente compartido).
            with self._cliente.stream("GET", url, headers=CABECERAS) as r:
                if r.status_code in CODIGOS_RECHAZO:
                    raise PublicadorRechazaError(
                        f"HTTP {r.status_code} de {HOST_PERMITIDO} al agente identificado"
                    )
                if r.status_code != 200:
                    raise TempusError(f"HTTP {r.status_code} de {HOST_PERMITIDO}")
                trozos: list[bytes] = []
                total = 0
                for trozo in r.iter_bytes():
                    total += len(trozo)
                    if total > self.max_bytes:
                        raise TempusError(
                            f"respuesta mayor que {self.max_bytes} bytes",
                            AbstainReason.EXTRACTION_FAILED,
                        )
                    trozos.append(trozo)
        except httpx.TimeoutException as exc:
            raise TempusError(f"timeout de {self.timeout_s}s contra {HOST_PERMITIDO}") from exc
        except httpx.HTTPError as exc:
            raise TempusError(
                f"error de red contra {HOST_PERMITIDO}: {type(exc).__name__}"
            ) from exc

        texto = b"".join(trozos).decode("utf-8", errors="replace")
        if self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            nombre = f"ine_{tabla}_{retrieved_at.strftime('%Y%m%dT%H%M%SZ')}.json"
            (self.cache_dir / nombre).write_text(texto, encoding="utf-8")
        LOG.info("INE tabla %s: %d bytes", tabla, len(texto))
        return RespuestaTempus(url=url, texto=texto, retrieved_at=retrieved_at, estado=200)

    def cerrar(self) -> None:
        self._cliente.close()
