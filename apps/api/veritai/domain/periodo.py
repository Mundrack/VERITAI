"""Periodos estadisticos: mes, trimestre o anio.

Un claim compara dos periodos y el emisor publica una referencia propia
(periodo anterior, mismo periodo del anio anterior). Toda la aritmetica de
periodos vive aqui, sin fechas de calendario: a la estadistica oficial le
importa "agosto de 2026" o "2T 2026", no el dia.

Formato canonico de texto: "2026-M08", "2026-T2", "2026". Es el que usan los
JSON de los casos, la base de datos y el codigo T3_Periodo del INE (M08, T2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PATRON = re.compile(r"^(?P<anio>\d{4})(?:-(?P<freq>[MT])(?P<idx>\d{1,2}))?$")

MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)


@dataclass(frozen=True, order=True)
class Periodo:
    anio: int
    frecuencia: str = "A"  # "M" mes | "T" trimestre | "A" anual
    indice: int = 0  # 1..12, 1..4, o 0 para anual

    def __post_init__(self) -> None:
        limites = {"M": 12, "T": 4, "A": 0}
        if self.frecuencia not in limites:
            raise ValueError(f"frecuencia desconocida: {self.frecuencia!r}")
        tope = limites[self.frecuencia]
        if (tope and not 1 <= self.indice <= tope) or (not tope and self.indice != 0):
            raise ValueError(f"indice {self.indice} fuera de rango para {self.frecuencia}")

    # --- construccion -------------------------------------------------------
    @classmethod
    def parse(cls, texto: str) -> Periodo:
        m = _PATRON.match(texto.strip())
        if not m:
            raise ValueError(
                f"periodo no reconocido: {texto!r} (esperado 2026-M08, 2026-T2 o 2026)"
            )
        if m.group("freq") is None:
            return cls(int(m.group("anio")))
        return cls(int(m.group("anio")), m.group("freq"), int(m.group("idx")))

    @classmethod
    def desde_ine(cls, anio: int, codigo: str | None) -> Periodo:
        """Del par (Anyo, T3_Periodo) del INE.

        T3_Periodo es 'M08' (mes), 'T2' (trimestre) o, en tablas anuales, 'A',
        vacio o ausente. Se aprendio en la Puerta 2 con la tabla 28724
        (condenados): el codigo anual no lleva digitos.
        """
        codigo = (codigo or "").strip()
        if not codigo or codigo[0] not in ("M", "T") or not codigo[1:].isdigit():
            return cls(anio)
        return cls(anio, codigo[0], int(codigo[1:]))

    # --- aritmetica ---------------------------------------------------------
    def anterior(self) -> Periodo:
        """El periodo inmediatamente anterior de la misma frecuencia."""
        if self.frecuencia == "A":
            return Periodo(self.anio - 1)
        tope = 12 if self.frecuencia == "M" else 4
        if self.indice > 1:
            return Periodo(self.anio, self.frecuencia, self.indice - 1)
        return Periodo(self.anio - 1, self.frecuencia, tope)

    def interanual(self) -> Periodo:
        """El mismo periodo del anio anterior."""
        return Periodo(self.anio - 1, self.frecuencia, self.indice)

    def desplazado(self, n: int) -> Periodo:
        p = self
        for _ in range(abs(n)):
            p = p.anterior() if n < 0 else p._siguiente()
        return p

    def _siguiente(self) -> Periodo:
        if self.frecuencia == "A":
            return Periodo(self.anio + 1)
        tope = 12 if self.frecuencia == "M" else 4
        if self.indice < tope:
            return Periodo(self.anio, self.frecuencia, self.indice + 1)
        return Periodo(self.anio + 1, self.frecuencia, 1)

    # --- representacion -----------------------------------------------------
    def codigo(self) -> str:
        if self.frecuencia == "A":
            return f"{self.anio}"
        return (
            f"{self.anio}-{self.frecuencia}{self.indice:02d}"
            if self.frecuencia == "M"
            else f"{self.anio}-T{self.indice}"
        )

    def codigo_ine(self) -> str | None:
        if self.frecuencia == "A":
            return None
        return f"M{self.indice:02d}" if self.frecuencia == "M" else f"T{self.indice}"

    def etiqueta(self) -> str:
        if self.frecuencia == "M":
            return f"{MESES[self.indice - 1]} de {self.anio}"
        if self.frecuencia == "T":
            return f"{self.indice}T {self.anio}"
        return str(self.anio)

    def __str__(self) -> str:
        return self.codigo()
