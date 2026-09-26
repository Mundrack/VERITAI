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


@dataclass(frozen=True)
class EvidenciaEdicion:
    """Un valor con su edicion y su fecha (DEC-034).

    El veredicto de 2b (base revisada) lleva dos de estas, separadas: la
    evidencia **al publicar** (la edicion con la que se calculo el claim, con
    su fecha de publicacion) y la evidencia **vigente** (la edicion que sirve
    hoy el emisor, con su fecha de consulta). La distincion existia en el
    diseno y no en la salida.
    """

    valor: float
    raw_value_span: str
    edicion: str  # p. ej. "INE CTH0725 (julio 2025, datos provisionales)"
    fecha: str  # ISO YYYY-MM-DD: publicacion (al publicar) o consulta (vigente)
    url: str = ""
    item_id: str = ""

    def a_dict(self) -> dict:
        return {
            "valor": self.valor,
            "raw_value_span": self.raw_value_span,
            "edicion": self.edicion,
            "fecha": self.fecha,
            "url": self.url,
            "item_id": self.item_id,
        }


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
    # DEC-034: solo los rellena el test 2b; en el resto van a null.
    evidencia_al_publicar: EvidenciaEdicion | None = None
    evidencia_vigente: EvidenciaEdicion | None = None
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
                    "senales": list(t.senales),
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
            "evidencia_al_publicar": (
                self.evidencia_al_publicar.a_dict() if self.evidencia_al_publicar else None
            ),
            "evidencia_vigente": (
                self.evidencia_vigente.a_dict() if self.evidencia_vigente else None
            ),
            "bundle_hash": self.bundle_hash,
            "generado_en": self.generado_en.isoformat(),
        }
