# Glosario y enums cerrados

Vocabulario del proyecto. **Si un término está aquí, se usa exactamente así.**

La segunda mitad del documento son los **enums cerrados**: listas de valores
permitidos que no admiten variantes. Vienen del defecto D4 de la adenda, donde
se comprobó que el piloto de 20 casos tenía **12 valores distintos de `Truth` en
20 filas**, con etiquetas como `"supported (si se refiere a valor)"`.

> Una etiqueta con paréntesis explicativos no es una etiqueta: es texto libre y
> no se puede contar. Los matices van al campo `notas`.

**Última actualización:** 2026-09-11

---

## Conceptos

**Divergencia contextual computable**
El objeto de la tesis. Una afirmación estadística literalmente correcta cuyo
marco no se sostiene al recuperar el dato original, **y donde esa discrepancia
se puede detectar con una regla determinista**, no con un juicio. El "computable"
es lo que separa la tesis de la crítica de medios.

**Caso canónico**
*"España cae 16 puestos en el ranking de países más seguros para mujeres."* El
dato es correcto: la puntuación de España no cambió, 16 países mejoraron la suya.
`truth: supported` + `context: divergence_detected`.

**Truth**
¿La afirmación literal es correcta? Máquina de estados **independiente** de
`context`.

**Context**
¿Los datos muestran divergencia? Máquina de estados **independiente** de `truth`.

> **Regla que no se relaja:** que ningún test haya disparado produce
> `no_divergence_detected`, **nunca** `supported`. No haber encontrado una
> distorsión entre las tres o cinco que sabemos buscar no es evidencia de que no
> exista ninguna. Colapsarlas genera sobreconfianza (R02 §10).

**Fuente primaria**
El organismo que **produjo** el dato, no quien lo reporta. Diez medios repitiendo
el mismo cable de agencia son una fuente, no diez. Un verificador puede ayudar a
encontrar el origen, pero la evidencia final apunta al productor del dato.

**Edición anterior**
La publicación previa del mismo índice o estadística. **Es la métrica que decide
si hay tesis.** Los emisores publican la edición vigente de forma prominente y
archivan, renombran o eliminan las anteriores — pero toda la tesis depende de
comparar dos períodos.

**EvidenceBundle**
El conjunto de artefactos del mismo publicador necesarios para resolver un claim:
edición actual, ediciones históricas y notas metodológicas. Tiene
`completeness` (`complete` / `partial` / `insufficient`) y `missing_slots`, que
alimenta directamente el motivo de abstención.

**`raw_value_span`**
El texto **literal** de la fuente de donde salió un número. Es lo que convierte
la regla *"ningún número puede originarse en el LLM"* de intención a test
automatizable. Sin él la regla no se puede verificar.

**Hard gate**
Comprobación determinista que, si falla, produce abstención con razón explícita.
No es un umbral de confianza.

> *"No puedo comparar los períodos porque la metodología cambió"* es mejor
> respuesta que *"incertidumbre 0.34"*.

**N0**
El filtro de entrada: ¿este texto contiene una afirmación estadística? **No es un
LLM** — es regex de alto recall más un encoder pequeño en ONNX. Debe ser
evaluable con su propio F1, entrenado sobre el corpus propio. Eso es una
contribución; un prompt no lo es.

**Lote sesgado / lote crudo**
Los **20 casos existentes** salieron todos de artículos de verificadores, donde
un periodista ya había localizado la fuente primaria. Son el lote sesgado y **no
cuentan para medir recuperabilidad**. El **lote crudo** son los 20 nuevos,
recolectados de contenido sin verificación previa. La recuperabilidad se mide
solo sobre ese.

**Puerta**
Hito que sustituye al calendario. Se cierra explícitamente y no se reabre. Sin
fecha límite externa, el riesgo deja de ser "no llego" y pasa a ser "no termino
nunca"; las puertas son la mitigación.

**Control negativo**
Afirmación estadística **correctamente enmarcada**. Sin controles negativos no se
puede medir la tasa de falsos positivos, que es la métrica crítica del proyecto.
El piloto actual tiene 1 de 20.

---

## Enums cerrados

### `truth`

```
supported
contradicted
mixed
insufficient_evidence
not_applicable
```

### `context`

```
divergence_detected
no_divergence_detected
undetermined
not_applicable
```

### `clase` (taxonomía)

```
1_ranking_vs_value
2_baseline_selection
3_absolute_vs_relative
4_denominator
5_methodology_change
none                  # control negativo
other_observed        # lo que no encaje, con nota libre
```

`NOTA` Las clases 6 (correlación/causalidad) y 7 (cifra real, marco falso) se
acordó dejarlas fuera de la tesis, pero aparecen en varios casos. Se registran
como `other_observed` para no perder la información. Su frecuencia decidirá si
vale la pena reabrir esa decisión.

`NOTA` La taxonomía **no está congelada**. El objetivo es quedarse con 3 a 5
clases, decidido **después** del piloto. No hay que forzar cinco si los datos
dicen que solo tres son suficientemente frecuentes y automatizables.

### `abstain_reason`

```
UNSUPPORTED_CLAIM_TYPE
REQUIRED_SLOT_MISSING
PRIMARY_SOURCE_NOT_FOUND
PREVIOUS_EDITION_NOT_FOUND      # se espera que sea el mas frecuente
PERIOD_NOT_COMPARABLE
METHODOLOGY_NOT_COMPARABLE
SOURCE_VERSION_AMBIGUOUS
CONFLICTING_PRIMARY_VALUES
EXTRACTION_FAILED
```

### `recuperabilidad`

```
A   fuente primaria y datos estructurados recuperables
B   fuente encontrada; tabla o PDF razonablemente extraible
C   fuente localizada pero requiere trabajo manual importante
D   fuente primaria no localizada o no recuperable razonablemente
```

`ATENCIÓN` Valores compuestos como `"A/B"` **no son válidos**. En el piloto
actual hay 8 filas con `"A/B"`, lo que deja un enum de 4 valores con 7 valores
observados. Hay que resolver cada caso a un solo valor.

### `formato`

```
api | dataset | html | pdf | scan | none
```

Jerarquía de preferencia, de mejor a peor: `api` > `dataset` > `html` > `pdf` >
`scan`. **La posición en esta jerarquía es criterio de selección de emisores**,
no un problema de ingeniería a resolver después. Tres emisores de nivel 1–2 valen
más que veinte de nivel 4.

### Campos booleanos de recuperación

Se miden **por separado**, porque son números distintos:

```
current_edition_found
previous_edition_found      # <- la que decide
historical_series_found
methodology_found
```

---

## Términos que NO se usan

| No usar | Usar |
|---|---|
| "Falso" / "verdadero" a secas | `truth` + `context`, separados |
| "Fake news" | afirmación estadística engañosa, o el estado concreto |
| "Score de confianza" como salida única | `truth` + `context` + motivo de abstención |
| "El sistema cree que…" | el sistema no cree: aplica una regla sobre unos valores |
| "Detectar desinformación" | detectar divergencia contextual computable |

El proyecto **no juzga la intención del autor**. Es una decisión cerrada, no una
cautela de redacción: nada en la arquitectura puede medir intención.
