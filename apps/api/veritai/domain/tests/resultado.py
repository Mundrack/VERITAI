"""Resultado de un test computable."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ResultadoTest:
    nombre: str
    aplicable: bool  # el test tenia lo que necesitaba para ejecutarse
    disparo: bool  # el test detecto la divergencia que busca
    motivo: str  # una frase, para la plantilla y el audit
    calculos: dict[str, float | str | None] = field(default_factory=dict)
    subtipo: str = ""  # "base_no_es_referencia" | "valor_atribuido_a_otro_periodo" | ""
