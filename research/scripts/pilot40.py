#!/usr/bin/env python3
"""TAREA 3: une los dos lotes del piloto en research/PILOT-40.csv e imprime
todos los conteos que usan PILOT-FINDINGS, PILOT-FAILURES y PILOT-DECISION.

ENTRADAS (ninguna se modifica)
    research/pilot-20-normalizado.csv        etiquetas de los 20 auditados (DEC-017)
    05-VERITAI-PILOTO-20-CASOS.xlsx           el Excel congelado, SOLO LECTURA, para
                                              claim, fecha, emisor y URLs de los 20
    research/pilot-crudo-trabajados.csv       los 31 crudos (DEC-020), con via de descubrimiento

SALIDA
    research/PILOT-40.csv    51 filas (20 + 31). El nombre es el del paquete
                             (START-HERE §20); el conteo real se declara en README.

REGLAS
    - Los enums se importan de normalizar_a_enums.py: una sola definicion.
    - Los 20 auditados NO cuentan para recuperabilidad: previous_edition_found =
      no_aplica_lote_sesgado (adenda D1). Se unen para taxonomia, formatos y tests.
    - Ningun numero de los informes se teclea: sale de aqui.
    - Codigo de salida 1 si algun valor se sale de enum o falta una fila.
"""

from __future__ import annotations

import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalizar_a_enums import ABSTAIN, CLASE, CONTEXT, FORMATO, RECUPERABILIDAD, TRUTH  # noqa: E402

CSV_20 = RAIZ / "research" / "pilot-20-normalizado.csv"
XLSX_20 = RAIZ / "05-VERITAI-PILOTO-20-CASOS.xlsx"
HOJA_20 = "Piloto_20_Consolidado"
CSV_31 = RAIZ / "research" / "pilot-crudo-trabajados.csv"
CSV_40 = RAIZ / "research" / "PILOT-40.csv"

CAMPOS = [
    "lote", "case_id", "claim_text", "claim_date", "emisor", "emisor_nivel", "pais", "tema",
    "post_url", "primaria_url", "truth", "context", "clase_primaria", "clases_secundarias",
    "abstain_reason", "recuperabilidad", "formato", "previous_edition_found",
    "alcanzable_por_agente", "alcanzable_por_humano", "minutes_to_locate", "minutes_to_extract",
    "cronometrado_por", "descubrimiento_via", "bucket_resultado", "excedente",
    "en_alcance_tesis", "audit_status", "notas",
]
NO_APLICA = "no_aplica_lote_sesgado"

# Umbrales de R02 §7. La segunda fila manda.
UMBRALES = [
    ("Fuente primaria localizada", 70, 40),
    ("Edicion anterior localizada", 60, 30),
    ("Extraccion sin intervencion extrema (A|B)", 60, 30),
]


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:5.1f}%" if d else "   -- "


def semaforo(valor: float, verde: int, ambar: int) -> str:
    return "verde" if valor > verde else ("ambar" if valor >= ambar else "ROJO")


def leer_excel_20() -> dict[str, dict]:
    import openpyxl  # solo lectura; el Excel esta congelado (DEC-017)

    wb = openpyxl.load_workbook(XLSX_20, read_only=True, data_only=True)
    ws = wb[HOJA_20]
    filas = list(ws.iter_rows(values_only=True))
    idx = {nombre: i for i, nombre in enumerate(filas[0])}
    col = {
        "claim_text": "Claim / titular original", "claim_date": "Fecha contenido",
        "emisor": "Autor / emisor", "tema": "Tema", "post_url": "URL contenido / declaración",
        "primaria_url": "URL fuente primaria", "fuente_primaria": "Fuente primaria principal",
    }
    out = {}
    for r in filas[1:]:
        cid = r[idx["ID"]]
        if not cid:
            continue
        d = {k: (str(r[idx[v]]).strip() if r[idx[v]] is not None else "") for k, v in col.items()}
        if hasattr(r[idx["Fecha contenido"]], "date"):
            d["claim_date"] = r[idx["Fecha contenido"]].date().isoformat()
        out[str(cid).strip()] = d
    return out


def filas_20() -> list[dict]:
    excel = leer_excel_20()
    out = []
    with CSV_20.open(encoding="utf-8") as fh:
        for a in csv.DictReader(fh):
            x = excel[a["case_id"]]
            pais = "EC" if "INEC" in x["fuente_primaria"] or "Ecuador" in x["fuente_primaria"] else "ES"
            out.append({
                "lote": "auditado_20", "case_id": a["case_id"],
                "claim_text": x["claim_text"], "claim_date": x["claim_date"], "emisor": x["emisor"],
                "emisor_nivel": "",  # no se asigno en la auditoria; NEEDS_REVIEW
                "pais": pais, "tema": x["tema"], "post_url": x["post_url"], "primaria_url": x["primaria_url"],
                "truth": a["truth"], "context": a["context"], "clase_primaria": a["clase_primaria"],
                "clases_secundarias": a["clases_secundarias"], "abstain_reason": a["abstain_reason"],
                "recuperabilidad": a["recuperabilidad"], "formato": a["formato"],
                "previous_edition_found": NO_APLICA, "alcanzable_por_agente": "", "alcanzable_por_humano": "",
                "minutes_to_locate": "", "minutes_to_extract": "", "cronometrado_por": "",
                "descubrimiento_via": "articulo_de_verificador",  # D1: los 20 salieron de verificadores
                "bucket_resultado": "", "excedente": "",
                "en_alcance_tesis": a["en_alcance_tesis"], "audit_status": a["audit_status"],
                "notas": ("nivel de emisor no asignado en la auditoria (NEEDS_REVIEW); pais inferido de la "
                          "fuente primaria; claim, fecha, emisor y URLs copiados del Excel congelado. | "
                          + a["audit_notas"]),
            })
    return out


def filas_31() -> list[dict]:
    out = []
    with CSV_31.open(encoding="utf-8") as fh:
        for c in csv.DictReader(fh):
            f = {k: c.get(k, "") for k in CAMPOS}
            f["lote"] = "crudo_31"
            f["en_alcance_tesis"] = "si"
            f["audit_status"] = "agente_provisional"
            out.append(f)
    return out


def validar(filas: list[dict]) -> list[str]:
    errores = []
    enums = {"truth": TRUTH, "context": CONTEXT, "clase_primaria": CLASE, "recuperabilidad": RECUPERABILIDAD,
             "formato": FORMATO}
    for f in filas:
        for campo, permitido in enums.items():
            if f[campo] not in permitido:
                errores.append(f"{f['case_id']}: {campo}='{f[campo]}' fuera de enum")
        if f["abstain_reason"] and f["abstain_reason"] not in ABSTAIN:
            errores.append(f"{f['case_id']}: abstain_reason='{f['abstain_reason']}' fuera de enum")
        for campo in ("claim_text", "post_url", "truth", "context"):
            if not f[campo]:
                errores.append(f"{f['case_id']}: {campo} vacio")
    ids = [f["case_id"] for f in filas]
    if len(ids) != len(set(ids)):
        errores.append("case_id repetido")
    if sum(1 for f in filas if f["lote"] == "auditado_20") != 20 or sum(1 for f in filas if f["lote"] == "crudo_31") != 31:
        errores.append("faltan filas: se esperan 20 + 31")
    return errores


def rec_cons(c: dict) -> bool:
    return c["previous_edition_found"] == "si" and c["alcanzable_por_agente"] == "si"


def rec_len(c: dict) -> bool:
    return c["previous_edition_found"] == "si"


def resumen(auditados: list[dict], crudos: list[dict], crudos_full: list[dict]) -> None:
    n = len(crudos)
    print("\n" + "=" * 84)
    print("  VERITAI - TAREA 3: conteos para FINDINGS / FAILURES / DECISION")
    print("=" * 84)
    print(f"  PILOT-40.csv: {len(auditados)} auditados + {n} crudos = {len(auditados) + n} filas")

    # --- 1. las cinco metricas de R02 §7, sobre los 31 -----------------------------
    print(f"\n--- 1. Las cinco metricas de R02 §7, sobre los {n} crudos (DEC-020) ---")
    prim_c = sum(1 for c in crudos_full if c["current_edition_found"] == "si" and c["alcanzable_por_agente"] == "si")
    prim_l = sum(1 for c in crudos_full if c["current_edition_found"] == "si")
    ant_c = sum(map(rec_cons, crudos)); ant_l = sum(map(rec_len, crudos))
    ab = sum(1 for c in crudos if c["recuperabilidad"] in ("A", "B"))
    clases = {c["clase_primaria"] for c in crudos if c["context"] == "divergence_detected"} - {"none", "other_observed"}
    minutos = [float(c["minutes_to_locate"] or 0) + float(c["minutes_to_extract"] or 0) for c in crudos]
    filas = [
        ("Fuente primaria localizada", prim_c, prim_l, 70, 40),
        ("Edicion anterior localizada  <- MANDA", ant_c, ant_l, 60, 30),
        ("Extraccion sin intervencion extrema (rec. A|B)", ab, ab, 60, 30),
    ]
    print(f"  {'metrica':48} {'conservadora':>14} {'leniente':>12}   semaforo (cons.)")
    for nombre, kc, kl, v, a in filas:
        print(f"  {nombre:48} {kc:2}/{n} {pct(kc, n)} {kl:2}/{n} {pct(kl, n)}   {semaforo(100 * kc / n, v, a)}")
    print(f"  {'Clases de divergencia observadas (>=3 verde)':48} {len(clases):>14}   {sorted(clases)}")
    print(f"  {'Tiempo medio por caso, AGENTE (<20 min verde)':48} {statistics.mean(minutos):>11.1f} min   max {max(minutos):.1f} | humano: PENDIENTE (5 casos de Mateo)")

    # --- 2. comparacion con el lote sesgado ------------------------------------------
    print(f"\n--- 2. Comparacion con el lote sesgado (20 auditados vs {n} crudos) ---")
    for campo in ("recuperabilidad", "formato", "truth", "context"):
        a = Counter(f[campo] for f in auditados); c = Counter(f[campo] for f in crudos)
        print(f"  {campo:16} auditados {dict(sorted(a.items()))}")
        print(f"  {'':16} crudos    {dict(sorted(c.items()))}")
    ver = sum(1 for f in auditados if f["audit_status"] == "verificado")
    span_ant = sum(1 for c in crudos_full if c["raw_value_span_anterior"].strip())
    span_act = sum(1 for c in crudos_full if c["raw_value_span_actual"].strip())
    print(f"  verificado contra primaria con raw_value_span: auditados {ver}/20 | crudos actual {span_act}/{n}, anterior {span_ant}/{n}")
    print(f"  recuperabilidad D: auditados {sum(1 for f in auditados if f['recuperabilidad'] == 'D')}/20 | crudos {sum(1 for f in crudos if f['recuperabilidad'] == 'D')}/{n}")
    print(f"  divergence_detected: auditados {sum(1 for f in auditados if f['context'] == 'divergence_detected')}/20 | crudos {sum(1 for f in crudos if f['context'] == 'divergence_detected')}/{n}")

    # --- 3. amenazas a la validez -----------------------------------------------------
    print(f"\n--- 3. Amenazas a la validez: recuperabilidad conservadora desagregada ({n} crudos) ---")
    for campo, etiqueta in (("emisor_nivel", "nivel de emisor"), ("descubrimiento_via", "via de descubrimiento"),
                            ("pais", "pais"), ("bucket_resultado", "cubeta")):
        print(f"  por {etiqueta}:")
        for k in sorted({c[campo] for c in crudos}, key=str):
            g = [c for c in crudos if c[campo] == k]
            print(f"    {str(k):32} {sum(map(rec_cons, g)):2}/{len(g):<2} {pct(sum(map(rec_cons, g)), len(g))}")
    n1 = [c for c in crudos if c["emisor_nivel"] == "1"]; resto = [c for c in crudos if c["emisor_nivel"] != "1"]
    print(f"  nivel 1: {sum(map(rec_cons, n1))}/{len(n1)} {pct(sum(map(rec_cons, n1)), len(n1))} | resto: {sum(map(rec_cons, resto))}/{len(resto)} {pct(sum(map(rec_cons, resto)), len(resto))}")
    org = [c for c in crudos if c["descubrimiento_via"] in ("busqueda_a_organismo", "criba_negativa")]
    otras = [c for c in crudos if c not in org]
    print(f"  via organismo+criba: {sum(map(rec_cons, org))}/{len(org)} {pct(sum(map(rec_cons, org)), len(org))} | ranking+encuesta+tema: {sum(map(rec_cons, otras))}/{len(otras)} {pct(sum(map(rec_cons, otras)), len(otras))}")
    hermanos = [c for c in crudos if c["descubrimiento_via"] == "criba_negativa"]
    indep = [c for c in crudos if c["descubrimiento_via"] != "criba_negativa"]
    print(f"  hermanos por criba (no independientes): {len(hermanos)} {[c['case_id'] for c in hermanos]}")
    print(f"  n efectivo sin hermanos: {len(indep)} | conservadora {sum(map(rec_cons, indep))}/{len(indep)} {pct(sum(map(rec_cons, indep)), len(indep))} | leniente {sum(map(rec_len, indep))}/{len(indep)}")
    print(f"  ES: {sum(1 for c in crudos if c['pais'] == 'ES')}/{n} | nivel 1: {len(n1)}/{n}")
    blo = [c["case_id"] for c in crudos_full if c["via_de_acceso"] == "bloqueado"]
    print(f"  bloqueados por publicador (via_de_acceso=bloqueado): {len(blo)} {blo}")
    print(f"  formato hostil (scan): {sum(1 for c in crudos if c['formato'] == 'scan')}/{n}")

    # --- 4/5. clases y abstenciones, los dos lotes juntos ----------------------------
    div20 = [f for f in auditados if f["context"] == "divergence_detected"]
    div31 = [f for f in crudos if f["context"] == "divergence_detected"]
    print(f"\n--- 5. P-15: clases en las divergencias, dos lotes ({len(div20)} + {len(div31)} = {len(div20) + len(div31)}) ---")
    tot = Counter(f["clase_primaria"] for f in div20 + div31)
    for clase, k in sorted(tot.items(), key=lambda x: -x[1]):
        k20 = sum(1 for f in div20 if f["clase_primaria"] == clase); k31 = k - k20
        print(f"  {clase:26} {k:2}/{len(div20) + len(div31)}  {pct(k, len(div20) + len(div31))}   (auditado {k20}, crudo {k31})")
    sec = Counter(s.strip() for f in div20 + div31 for s in f["clases_secundarias"].split(",") if s.strip())
    print(f"  secundarias: {dict(sec)}")
    print(f"  familia 'comparacion de base' (2a 2_baseline + 2b base_revisada + 2c 5_methodology): "
          f"{tot.get('2_baseline_selection', 0) + tot.get('2b_base_revisada', 0) + tot.get('5_methodology_change', 0)}")
    print(f"  familia 'magnitud mal leida' (3_absolute_vs_relative + 4_denominator): {tot.get('3_absolute_vs_relative', 0) + tot.get('4_denominator', 0)}")
    # P-12: el mismo conteo sobre las divergencias EN ALCANCE (sin P08/P09, DEC-013) y,
    # ademas, sin los hermanos por criba (no independientes), que es el denominador honesto.
    alc = [f for f in div20 + div31 if f["en_alcance_tesis"] == "si"]
    sin_h = [f for f in alc if f["descubrimiento_via"] != "criba_negativa"]
    print(f"\n--- 5b. P-12: clases en las divergencias EN ALCANCE ({len(alc)}; sin DEC-013) y sin hermanos ({len(sin_h)}) ---")
    ta = Counter(f["clase_primaria"] for f in alc); th = Counter(f["clase_primaria"] for f in sin_h)
    print(f"  {'clase':26} {'en alcance':>16} {'sin hermanos':>18}")
    for clase, _ in sorted(ta.items(), key=lambda x: -x[1]):
        print(f"  {clase:26} {ta[clase]:2}/{len(alc)} {pct(ta[clase], len(alc))}   {th.get(clase, 0):2}/{len(sin_h)} {pct(th.get(clase, 0), len(sin_h))}")
    oo = [f["case_id"] for f in alc if f["clase_primaria"] == "other_observed"]
    ooh = [f["case_id"] for f in alc if f["clase_primaria"] == "other_observed" and f["descubrimiento_via"] == "criba_negativa"]
    print(f"  other_observed en alcance: {oo} | de ellos hermanos por criba: {ooh}")
    print(f"  fuera de alcance (DEC-013) contados en la tabla de 28: {[f['case_id'] for f in div20 + div31 if f['en_alcance_tesis'] != 'si']}")
    print("  abstain_reason, dos lotes:", dict(Counter(f["abstain_reason"] for f in auditados + crudos if f["abstain_reason"])))
    print("  truth x context, dos lotes:", dict(sorted(Counter((f["truth"], f["context"]) for f in auditados + crudos).items())))

    # --- 7. hueco humano/agente --------------------------------------------------------
    print("\n--- 7. Humano vs agente: PENDIENTE. Casos de Mateo: C04 C05 C11 C14 C22 (semilla 20260925) ---")
    for c in crudos:
        if c["case_id"] in ("C04", "C05", "C11", "C14", "C22"):
            print(f"  {c['case_id']}  agente: anterior={c['previous_edition_found']} alc={c['alcanzable_por_agente']} "
                  f"loc={c['minutes_to_locate']} ext={c['minutes_to_extract']} min | humano: __ __ __")


def main() -> int:
    auditados = filas_20()
    with CSV_31.open(encoding="utf-8") as fh:
        crudos_full = list(csv.DictReader(fh))
    crudos = filas_31()
    filas = auditados + crudos
    errores = validar(filas)
    if errores:
        print("VIOLACIONES:"); [print("  -", e) for e in errores]
        return 1
    with CSV_40.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(filas)
    resumen(auditados, crudos, crudos_full)
    print(f"\n  Escrito: {CSV_40.name} ({len(filas)} filas). Cero valores fuera de enum.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
