"""Resultado de un test computable."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ResultadoTest:
    nombre: str
    aplicable: bool  # el test tenia lo que necesitaba para ejecutarse
    disparo: bool  # el test detecto la divergencia que busca (2a CONFIRMADA)
    motivo: str  # una frase, para la plantilla y el audit
    calculos: dict[str, float | str | None] = field(default_factory=dict)
    subtipo: str = ""  # "cambio_de_signo" | "valor_atribuido_a_otro_periodo" | ""
    # Senales: se registran y se explican, pero NO disparan ni cambian `context`.
    # Hoy solo "horizonte_largo" (DEC-029, P-21): base declarada lejos de la
    # referencia del emisor y magnitud >= 2x sin cambio de signo.
    senales: tuple[str, ...] = ()
