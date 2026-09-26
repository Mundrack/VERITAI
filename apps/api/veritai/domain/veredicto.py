"""El veredicto: dos ejes, motivos, tests, y cada numero con su origen.

`numeros_usados` es la lista de (valor, raw_value_span, item) de todo numero
que aparece en la explicacion. Un test automatico (tests/test_trazabilidad.py)
comprueba que ningun numero del veredicto carece de span: es la regla
"ningun numero puede tener como unico origen el LLM", convertida en assert.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from veritai.domain.enums import AbstainReason, Clase, Context, Truth
from veritai.domain.tests.resultado import ResultadoTest
from veritai.domain.verdad import Comparacion


@dataclass(frozen=True)
class NumeroUsado:
    valor: float
    raw_value_span: str
    item_id: str
    etiqueta: str


@dataclass
class Veredicto:
    claim_id: str
    truth: Truth
    context: Context
    clase_primaria: Clase
    abstain_reasons: list[AbstainReason] = field(default_factory=list)
    tests: list[ResultadoTest] = field(default_factory=list)
    comparaciones: list[Comparacion] = field(default_factory=list)
    numeros_usados: list[NumeroUsado] = field(default_factory=list)
    explicacion: str = ""
    bundle_hash: str = ""
    generado_en: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def abstiene(self) -> bool:
        return self.truth is Truth.INSUFFICIENT_EVIDENCE and self.context is Context.UNDETERMINED

    def a_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "truth": self.truth.value,
            "context": self.context.value,
            "clase_primaria": self.clase_primaria.value,
            "abstain_reasons": [m.value for m in self.abstain_reasons],
            "tests": [
                {
                    "nombre": t.nombre,
                    "aplicable": t.aplicable,
                    "disparo": t.disparo,
                    "subtipo": t.subtipo,
                    "motivo": t.motivo,
                    "calculos": t.calculos,
                }
                for t in self.tests
            ],
            "comparaciones": [
                {
                    "que": c.que,
                    "afirmado": c.afirmado,
                    "evidencia": c.evidencia,
                    "tolerancia": c.tolerancia,
                    "cuadra": c.cuadra,
                }
                for c in self.comparaciones
            ],
            "numeros_usados": [
                {
                    "valor": n.valor,
                    "raw_value_span": n.raw_value_span,
                    "item_id": n.item_id,
                    "etiqueta": n.etiqueta,
                }
                for n in self.numeros_usados
            ],
            "explicacion": self.explicacion,
            "bundle_hash": self.bundle_hash,
            "generado_en": self.generado_en.isoformat(),
        }
