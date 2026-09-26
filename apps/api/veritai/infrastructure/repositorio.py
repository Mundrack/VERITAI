"""Repositorios: PostgreSQL (produccion) y memoria (tests).

Trazabilidad completa en una transaccion: claim, bundle, items, veredicto y
una fila de audit_log. SQL plano con parametros ligados (nunca f-strings con
datos), sobre el esquema veritai (migracion 003).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from sqlalchemy import Engine, text

from veritai.domain.claim import ClaimEstructurado
from veritai.domain.evidencia import EvidenceBundle
from veritai.domain.veredicto import Veredicto

SQL_CLAIM = text("""
    insert into veritai.claims (
        claim_id, texto, fuente_url, conjunto, tipo, origen_case_id,
        metrica, periodo_objetivo, periodo_base, valores, notas)
    values (
        :claim_id, :texto, :fuente_url, :conjunto, :tipo, :origen_case_id,
        cast(:metrica as jsonb), :periodo_objetivo, :periodo_base,
        cast(:valores as jsonb), :notas)
    on conflict (claim_id) do update set
        texto = excluded.texto, fuente_url = excluded.fuente_url,
        conjunto = excluded.conjunto, tipo = excluded.tipo, metrica = excluded.metrica,
        periodo_objetivo = excluded.periodo_objetivo, periodo_base = excluded.periodo_base,
        valores = excluded.valores, notas = excluded.notas
""")

SQL_BUNDLE = text("""
    insert into veritai.evidence_bundles (bundle_hash, claim_id, completeness, missing_slots)
    values (:bundle_hash, :claim_id, :completeness, cast(:missing as jsonb))
    on conflict (bundle_hash) do nothing
""")

SQL_ITEMS_EXISTEN = text("select count(*) from veritai.evidence_items where bundle_hash = :h")

SQL_ITEM = text("""
    insert into veritai.evidence_items (
        bundle_hash, rol, etiqueta, publisher, url, source_tier, retrieved_at, document_date,
        version, format, extraction_method, serie_codigo, serie_nombre, periodo, valor,
        raw_value_span)
    values (
        :bundle_hash, :rol, :etiqueta, :publisher, :url, :source_tier, :retrieved_at,
        :document_date, :version, :format, :extraction_method, :serie_codigo, :serie_nombre,
        :periodo, :valor, :raw_value_span)
""")

SQL_VERDICT = text("""
    insert into veritai.verdicts (
        claim_id, bundle_hash, truth, context, clase_primaria, abstain_reasons, tests,
        comparaciones, numeros_usados, explicacion)
    values (
        :claim_id, :bundle_hash, :truth, :context, :clase, cast(:abstain as jsonb),
        cast(:tests as jsonb), cast(:comparaciones as jsonb), cast(:numeros as jsonb),
        :explicacion)
    returning id
""")

SQL_AUDIT = text("""
    insert into veritai.audit_log (claim_id, bundle_hash, verdict_id, accion, detalle, duracion_ms)
    values (:claim_id, :bundle_hash, :verdict_id, 'analizar_claim', cast(:detalle as jsonb), :ms)
""")


def _claim_a_json(claim: ClaimEstructurado) -> dict[str, Any]:
    d = asdict(claim)
    d["tipo"] = claim.tipo.value
    d["metrica"]["referencia_principal"] = claim.metrica.referencia_principal.value
    d["periodo_objetivo"] = str(claim.periodo_objetivo)
    d["periodo_base"] = None if claim.periodo_base is None else str(claim.periodo_base)
    d["unidad_cambio"] = None if claim.unidad_cambio is None else claim.unidad_cambio.value
    d["direccion_afirmada"] = (
        None if claim.direccion_afirmada is None else claim.direccion_afirmada.value
    )
    return d


class RepositorioMemoria:
    """Guarda en listas. Para tests y para inspeccionar sin Postgres."""

    def __init__(self) -> None:
        self.analisis: list[dict[str, Any]] = []

    def guardar_analisis(
        self,
        claim: ClaimEstructurado,
        bundle: EvidenceBundle,
        veredicto: Veredicto,
        duracion_ms: int,
    ) -> int:
        self.analisis.append(
            {
                "claim": _claim_a_json(claim),
                "bundle_hash": bundle.bundle_hash,
                "items": len(bundle.items),
                "veredicto": veredicto.a_dict(),
                "duracion_ms": duracion_ms,
            }
        )
        return len(self.analisis)


class RepositorioPostgres:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def guardar_analisis(
        self,
        claim: ClaimEstructurado,
        bundle: EvidenceBundle,
        veredicto: Veredicto,
        duracion_ms: int,
    ) -> int:
        c = _claim_a_json(claim)
        v = veredicto.a_dict()
        valores = {
            k: c[k]
            for k in (
                "valor_objetivo",
                "valor_base",
                "cambio_afirmado",
                "unidad_cambio",
                "direccion_afirmada",
                "etiquetas_corpus",
            )
        }
        with self.engine.begin() as conn:
            conn.execute(
                SQL_CLAIM,
                {
                    "claim_id": claim.claim_id,
                    "texto": claim.texto,
                    "fuente_url": claim.fuente_url,
                    "conjunto": claim.conjunto,
                    "tipo": claim.tipo.value,
                    "origen_case_id": claim.origen_case_id,
                    "metrica": json.dumps(c["metrica"], ensure_ascii=False),
                    "periodo_objetivo": c["periodo_objetivo"],
                    "periodo_base": c["periodo_base"],
                    "valores": json.dumps(valores, ensure_ascii=False),
                    "notas": claim.notas,
                },
            )
            conn.execute(
                SQL_BUNDLE,
                {
                    "bundle_hash": bundle.bundle_hash,
                    "claim_id": claim.claim_id,
                    "completeness": bundle.completeness.value,
                    "missing": json.dumps(bundle.missing_slots),
                },
            )
            existen = conn.execute(SQL_ITEMS_EXISTEN, {"h": bundle.bundle_hash}).scalar_one()
            if not existen:
                for item in bundle.items:
                    conn.execute(
                        SQL_ITEM,
                        {
                            "bundle_hash": bundle.bundle_hash,
                            "rol": item.rol.value,
                            "etiqueta": item.etiqueta,
                            "publisher": item.publisher,
                            "url": item.url,
                            "source_tier": item.source_tier,
                            "retrieved_at": item.retrieved_at,
                            "document_date": item.document_date,
                            "version": item.version,
                            "format": item.format,
                            "extraction_method": item.extraction_method,
                            "serie_codigo": item.serie_codigo,
                            "serie_nombre": item.serie_nombre,
                            "periodo": str(item.periodo),
                            "valor": item.valor,
                            "raw_value_span": item.raw_value_span,
                        },
                    )
            verdict_id = conn.execute(
                SQL_VERDICT,
                {
                    "claim_id": claim.claim_id,
                    "bundle_hash": bundle.bundle_hash,
                    "truth": v["truth"],
                    "context": v["context"],
                    "clase": v["clase_primaria"],
                    "abstain": json.dumps(v["abstain_reasons"]),
                    "tests": json.dumps(v["tests"], ensure_ascii=False),
                    "comparaciones": json.dumps(v["comparaciones"], ensure_ascii=False),
                    "numeros": json.dumps(v["numeros_usados"], ensure_ascii=False),
                    "explicacion": v["explicacion"],
                },
            ).scalar_one()
            conn.execute(
                SQL_AUDIT,
                {
                    "claim_id": claim.claim_id,
                    "bundle_hash": bundle.bundle_hash,
                    "verdict_id": verdict_id,
                    "ms": duracion_ms,
                    "detalle": json.dumps(
                        {
                            "items": len(bundle.items),
                            "truth": v["truth"],
                            "context": v["context"],
                            "abstain_reasons": v["abstain_reasons"],
                        }
                    ),
                },
            )
        return int(verdict_id)
