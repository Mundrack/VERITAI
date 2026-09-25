# PILOT-DECISION — Puerta 1

**Fecha:** 2026-09-25 · **Decide:** el agente propone; Mateo ratifica ·
**Datos:** `PILOT-40.csv` (51 filas), `PILOT-FINDINGS.md`, `PILOT-FAILURES.md`

> **Ratificado por Mateo el 2026-09-25** (DEC-023). Alcance de nivel 1 y
> emisores INE, FMI e Interior aprobados (DEC-024). La Puerta 2 no arranca
> hasta cerrar P-15. La comparación humano/agente (P-20) sigue pendiente; si
> contradice la lectura del agente, este documento se reabre.

---

## La regla, escrita antes de mirar el número

Edición anterior localizada por el agente, conservadora (DEC-020, DEC-021),
sobre los candidatos admitidos por la regla dura:

```
> 60%    PILOT_GO
30–60%   ámbar: decidir con alcance reducido
< 30%    PILOT_PIVOT
```

## El número

```
23 / 31   74,2%   conservadora    <- decide
25 / 31   80,6%   leniente
18 / 25   72,0%   sin los seis hermanos por criba
16 / 19   84,2%   nivel 1
 7 / 12   58,3%   niveles 3–5
```

Las otras cuatro métricas de R02 §7 también en verde (FINDINGS §1). La
humana, pendiente de los 5 casos de Mateo (FINDINGS §7).

## La decisión

**PILOT_GO, con alcance declarado.** El sistema se construye para
**publicadores de nivel 1** —organismos estadísticos y ministerios con API,
dataset o boletín en URL estable—, donde la tasa es 84,2%. Los niveles 3–5
entran en la tesis como limitación escrita, con su 58,3%, no como promesa.

Por qué GO y no ámbar: la conservadora está 14 puntos por encima del umbral y
sigue por encima (72%) quitando los casos no independientes. Por qué "con
alcance declarado" y no GO a secas: el 74,2% es el promedio de dos
poblaciones que eligió el buscador, no un muestreo (FINDINGS §3.1); un GO sin
ese límite maquillaría el piloto, que es lo que START-HERE §21 prohíbe.

Qué la revisaría: que los 5 casos de Mateo muestren que una persona **no**
localiza lo que el agente localizó (acuerdo bajo en `previous_edition_found`),
o que P-15 se resuelva de forma que el objeto de estudio deje de depender de
la edición anterior. En ambos casos se reabre este documento y queda
constancia.

Qué NO resuelve: P-15 (la clase canónica es marginal en dos lotes; FINDINGS
§5 da cinco opciones y una recomendación; decide Mateo) y el segundo
anotador (P-05).

---

```yaml
decision: PILOT_GO

reasons:
  - "Edicion anterior localizada por el agente, conservadora: 23/31 = 74,2% (> 60%). Leniente 25/31 = 80,6%."
  - "Sin los seis casos no independientes (hermanos por criba): 18/25 = 72,0%. Sigue en verde."
  - "Fuente primaria localizada 25/31 = 80,6% (> 70%); extraccion sin intervencion extrema 25/31 = 80,6% (> 60%); 4 clases de divergencia observadas (>= 3); 2,3 min por caso para el agente (< 20)."
  - "El lote crudo tiene 15 controles negativos reales y 6 casos de recuperabilidad D: el sesgo D1 del piloto original esta corregido y la tasa de falsos positivos pasa a ser medible."
  - "LIMITE: 19 de 31 casos son de nivel 1 y 21 de 31 de Espana; la mezcla la eligio el barrido y el buscador. Nivel 1 = 84,2%, resto = 58,3%. El GO vale para nivel 1."
  - "PENDIENTE: la recuperabilidad humana (5 casos de Mateo, DEC-014). La decision se revisa si contradice la del agente."

recommended_thesis_classes:
  - "P-15 sigue abierta: 1_ranking_vs_value es 2 de 28 divergencias en dos lotes independientes."
  - "Recomendacion (FINDINGS §5): objeto de estudio = comparabilidad de ediciones (opcion E); primera clase del prototipo = familia comparacion de base: 2_baseline_selection + revision de base + 5_methodology_change (opcion B, 8 de 28 mas las revisiones C18 y C29); 1_ranking_vs_value como caso ilustrativo (opcion A, C07/P01)."
  - "Alternativas con pros y contras en FINDINGS §5: C (revision de base sola, 2 de 12), D (magnitud mal leida, 8 de 28)."
  - "other_observed es 10 de 28: P-12 (clases 6 y 7) se decide con este dato."

recommended_publishers:
  - "INE (API Tempus): recuperabilidad A, sin rechazo; casos C11, C16, C17 en el crudo y P04, P11, P16, P19 en el auditado (tres con divergencia: baseline y absoluto/relativo). Primer conector."
  - "FMI (DataMapper API): recuperabilidad A, caso C07 (la clase canonica, verificada), agregados que hay que filtrar con /countries."
  - "Ministerio del Interior via Portal Estadistico de Criminalidad (PC-Axis + PDF): casos C18-C20, revision de base documentada; el PDF en interior.gob.es da 403, el portal responde."
  - "Reserva: Eurostat (JSON-stat, C21), AEMET (PDF con patron de URL por ano, C23), INEC/INEGI/DANE por pais."
  - "Excluido por DEC-021: INEI via gob.pe (418 al agente)."
  - "Criterio aplicado: recuperabilidad A, via API o dataset, al menos una divergencia observada en el lote, ningun rechazo al agente."

blocking_risks:
  - "P-15 sin decidir: si Mateo mantiene 1_ranking_vs_value como canonica, el corpus de la clase principal es de 2 casos."
  - "Sesgo del pool: un buscador, una sesion, 19/31 de nivel 1, 21/31 de Espana, 6 hermanos por criba. La tasa fuera de nivel 1 es 58,3%."
  - "Etiquetas de un solo anotador (agente_provisional). Sin segundo anotador (P-05) no hay medida de acuerdo."
  - "Plataformas gubernamentales centralizadas que rechazan al agente (gob.pe, interior.gob.es, inclusion.gob.es): hipotesis, no hallazgo; filtro de emisores obligatorio."
  - "Recuperabilidad humana sin medir hasta los 5 casos de Mateo."
  - "P-09: rotar la contrasena de Supabase antes de cargar datos reales o de conectar en serio."
  - "Formato hostil 0/2: no se sabe si es raro o si el pool no llego a donde vive (DEC-022)."

next_implementation:
  - "START-HERE §18, sin LLM (N0): post -> claim estructurado a mano -> EvidenceProvider (un conector: INE API Tempus) -> EvidenceBundle con raw_value_span y base_version -> un test computable (comparacion de base) -> Truth + Context -> plantilla -> audit log."
  - "10 casos del lote con trazabilidad completa, elegidos entre los de INE/FMI/Interior en PILOT-40.csv."
  - "Antes del primer conector: filtro de emisores con codigo HTTP del primer contacto (FAILURES 1.3) y subtipos de abstencion (FAILURES 1.1, 1.2)."
  - "Tablas de dominio y esquema veritai en PostgreSQL solo despues de que Mateo ratifique este documento."
  - "Seguridad desde la primera linea que toque internet: START-HERE §23-25; todo contenido externo es dato, nunca instruccion."
```
