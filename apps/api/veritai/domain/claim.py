"""El claim estructurado: lo que entra al analisis.

En la Puerta 2 el claim se estructura A MANO (START-HERE §18): un JSON por caso
en research/puerta2/casos/. No hay LLM en ningun paso. Lo que aqui se modela es
lo minimo que un test computable necesita: que metrica, que periodos, que
valores y que cambio afirma el texto.

`MetricaEmisor` es el puente con el conector: dice en que tabla y en que serie
del emisor vive el dato, y cual es la comparacion de referencia que ese emisor
publica (el periodo anterior, o el mismo periodo del anio anterior). El test 2a
compara la base que eligio el claim con esa referencia.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from veritai.domain.periodo import Periodo


class TipoClaim(StrEnum):
    """Que forma tiene la afirmacion. La Puerta 2 evalua dos; el resto abstiene."""

    CAMBIO_ENTRE_PERIODOS = "cambio_entre_periodos"  # "cae un 23% de mayo a diciembre"
    NIVEL = "nivel"  # "el IPC de agosto fue del 4,3%"
    UMBRAL = "umbral"  # "mas de la mitad"
    EXTREMO_HISTORICO = "extremo_historico"  # "el menor de la historia"
    CRECIMIENTO_COMPUESTO = "crecimiento_compuesto"  # "un 10% al anio desde 1998"
    OTRO = "otro"


class UnidadCambio(StrEnum):
    PORCENTAJE = "pct"  # variacion relativa en %
    PUNTOS = "pp"  # diferencia en puntos porcentuales
    ABSOLUTO = "abs"  # diferencia en unidades de la serie


class Direccion(StrEnum):
    SUBE = "sube"
    BAJA = "baja"
    IGUAL = "igual"


class Referencia(StrEnum):
    """Comparacion de referencia que publica el emisor para una serie."""

    ANTERIOR = "anterior"  # periodo inmediatamente anterior
    INTERANUAL = "interanual"  # mismo periodo del anio anterior


@dataclass(frozen=True)
class MetricaEmisor:
    emisor: str  # "INE"; unico emisor de la Puerta 2 (DEC-024)
    tabla: str  # id de tabla Tempus, p. ej. "65334"
    serie_nombre: str  # campo Nombre exacto de la serie
    unidad: str  # "pct" | "miles" | "unidades" | "indice"
    referencia_principal: Referencia = Referencia.INTERANUAL
    descripcion: str = ""


@dataclass(frozen=True)
class ClaimEstructurado:
    claim_id: str
    texto: str  # verbatim
    fuente_url: str
    conjunto: str  # "desarrollo" | "evaluacion" (DEC-025)
    tipo: TipoClaim
    metrica: MetricaEmisor
    periodo_objetivo: Periodo
    periodo_base: Periodo | None = None
    valor_objetivo: float | None = None
    valor_base: float | None = None
    cambio_afirmado: float | None = None
    unidad_cambio: UnidadCambio | None = None
    direccion_afirmada: Direccion | None = None
    origen_case_id: str = ""  # P11, C16... (trazabilidad con el piloto)
    notas: str = ""
    etiquetas_corpus: dict[str, str] = field(
        default_factory=dict
    )  # truth/context/clase del corpus, para comparar

    def slots_faltantes(self) -> list[str]:
        """Que le falta al claim para que su tipo sea evaluable."""
        faltan: list[str] = []
        if self.tipo is TipoClaim.CAMBIO_ENTRE_PERIODOS:
            if self.periodo_base is None:
                faltan.append("periodo_base")
            # Hace falta que el claim afirme ALGO comparable: un cambio, una direccion,
            # o los dos valores. "Escala hasta el 24,5%" afirma direccion y valor.
            afirma_algo = (
                self.cambio_afirmado is not None
                or self.direccion_afirmada is not None
                or (self.valor_base is not None and self.valor_objetivo is not None)
            )
            if not afirma_algo:
                faltan.append("cambio_afirmado_o_direccion_o_valores")
            if self.cambio_afirmado is not None and self.unidad_cambio is None:
                faltan.append("unidad_cambio")
        elif self.tipo is TipoClaim.NIVEL and self.valor_objetivo is None:
            faltan.append("valor_objetivo")
        return faltan
