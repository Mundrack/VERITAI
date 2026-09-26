"""La regla que define la arquitectura, como assert:

    ningun numero del veredicto puede tener como unico origen el LLM.

Cada numero que aparece en la explicacion y viene de la evidencia tiene que
estar en `numeros_usados` con un `raw_value_span` que contenga ese numero.
"""

from __future__ import annotations

import re

from tests.dobles import ProveedorFalso, serie_trimestral
from veritai.application.analizar_claim import AnalizarClaim
from veritai.domain.claim import (
    ClaimEstructurado,
    Direccion,
    MetricaEmisor,
    Referencia,
    TipoClaim,
    UnidadCambio,
)
from veritai.domain.periodo import Periodo

NOMBRE = "Tasa de paro. Menores de 25."
METRICA = MetricaEmisor("INE", "65334", NOMBRE, "pct", Referencia.ANTERIOR)
SERIE = serie_trimestral({"2026-T2": 23.77, "2026-T1": 24.54, "2025-T4": 23.01, "2025-T2": 25.1})


def _numeros(texto: str) -> set[str]:
    return {m.replace(",", ".") for m in re.findall(r"\d+(?:[.,]\d+)?", texto)}


def test_todo_numero_de_la_evidencia_lleva_span() -> None:
    caso = AnalizarClaim(ProveedorFalso({NOMBRE: SERIE}))
    for kw in (
        dict(
            valor_objetivo=23.77,
            cambio_afirmado=-0.77,
            unidad_cambio=UnidadCambio.PUNTOS,
            direccion_afirmada=Direccion.BAJA,
        ),
        dict(
            valor_objetivo=24.5,
            unidad_cambio=UnidadCambio.PUNTOS,
            direccion_afirmada=Direccion.SUBE,
        ),
    ):
        claim = ClaimEstructurado(
            claim_id="T",
            texto="t",
            fuente_url="https://x.test/",
            conjunto="desarrollo",
            tipo=TipoClaim.CAMBIO_ENTRE_PERIODOS,
            metrica=METRICA,
            periodo_objetivo=Periodo.parse("2026-T2"),
            periodo_base=Periodo.parse("2026-T1"),
            **kw,
        )
        v = caso.ejecutar(claim)
        assert v.numeros_usados, "un veredicto con evidencia tiene que declarar sus numeros"
        for n in v.numeros_usados:
            assert n.raw_value_span and str(n.valor).rstrip("0").rstrip(".") in n.raw_value_span, n
        # todo valor de evidencia citado en la explicacion esta declarado
        valores_evidencia = {str(x) for x in SERIE.values() if x is not None}
        citados = _numeros(v.explicacion) & valores_evidencia
        declarados = {str(n.valor) for n in v.numeros_usados}
        assert citados <= declarados, (citados, declarados)
