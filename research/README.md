# Investigación — el piloto

Esta carpeta contiene el piloto de viabilidad. **Es lo único que puede abrir la
Puerta 1.** Sin `PILOT-DECISION.md` no se escribe código de producto.

**Última actualización:** 2026-09-24

---

## La métrica que decide

> Porcentaje de casos del lote **crudo** donde se localiza la **edición anterior**
> del dato.

```
> 60%     verde   ->  PILOT_GO
30-60%    ambar   ->  decidir con alcance reducido
< 30%     rojo    ->  PILOT_PIVOT
```

**Valor actual: sin medir.** El lote crudo no existe todavía.

No es la fuente primaria actual. No es la búsqueda. Es la **edición anterior**,
porque toda la tesis depende de comparar dos períodos — y los emisores publican
la edición vigente de forma prominente mientras archivan, renombran o eliminan
las anteriores.

`NOTA` Si sale por debajo del 30%, eso **sigue siendo un hallazgo publicable**:
nadie ha medido ese número para el contexto hispanohablante. Pero hay que
conocerlo antes de escribir el sistema, no después.

---

## Entregables

| Archivo | Tarea | Estado |
|---|---|---|
| [`AUDIT-PILOT-20.md`](AUDIT-PILOT-20.md) | TAREA 1 — auditar los 20 existentes | **entregado** 2026-09-24 |
| [`pilot-20-normalizado.csv`](pilot-20-normalizado.csv) | TAREA 1 — los 20 con enums cerrados | **entregado** 2026-09-24 |
| `scripts/auditar_aritmetica.py`, `scripts/normalizar_a_enums.py` | TAREA 1 — reproducibilidad | **entregado** |
| `PILOT-40.xlsx` o `.csv` | TAREA 2 — 20 crudos + los 20 auditados | **pendiente** |
| `PILOT-FINDINGS.md` | TAREA 3 | **pendiente** |
| `PILOT-FAILURES.md` | TAREA 3 | **pendiente** |
| `PILOT-DECISION.md` | TAREA 3 — `PILOT_GO` o `PILOT_PIVOT` | **pendiente** |

---

## Pre-auditoría de los 20 casos existentes

Hallazgos obtenidos **leyendo el Excel, sin acceder a ninguna URL**. Son
verificables y recomputables. La auditoría completa (TAREA 1) tiene que verificar
además las URLs y normalizar las etiquetas.

### El hallazgo principal: D1 es peor de lo que dice la adenda

> **En 18 de 20 casos, la columna `URL contenido / declaración` ES la URL del
> verificador.**

Solo dos casos apuntan a contenido que no sea un artículo de verificación:

| Caso | `URL contenido` |
|---|---|
| P02 | `okdiario.com` (medio) |
| P20 | `ecuadorencifras.gob.ec` (INEC, fuente oficial) |

P03 es el caso extremo: el claim **y** la URL son ambos el artículo de Maldita.

**Por qué esto agrava D1.** La adenda dice que los casos se *encontraron* a través
de verificadores. El Excel muestra algo más grave: **el contenido original no está
registrado**. Sin la URL del post original no se puede reproducir la entrada del
sistema, ni medir cuánto trabajo cuesta partir de contenido crudo — que es
exactamente lo que el piloto existe para medir.

Consecuencia práctica: estos 20 casos sirven para taxonomía, formatos, diseño de
tests y regresión. **No sirven para medir recuperabilidad.** Es sesgo de
supervivencia.

### Vocabulario sin controlar (defecto D4, confirmado)

**`Truth preliminar`: 12 valores distintos en 20 filas.** Muestra:

```
"supported (si se refiere a valor)"
"supported (el +25,7% existe)"
"contradicted in temporal attribution"
"supported under one metric"
"supported values / invalid comparison"
"contradicted by scope"
"mixed / overclaimed"
"supported approximately"
"contradicted / mixed"
```

No son etiquetas: es texto libre. No se puede contar.

**`Clase candidata` con valores compuestos:** `"2 + 3"`, `"1 + 3"`, `"4/7"`,
`"3/4"`, `"1/3"`. Tampoco contable.

**`Recuperabilidad`: 8 filas con `"A/B"`.** Un enum de 4 valores con 7 valores
observados. Y **cero casos con `D`**, lo que por sí solo delata el sesgo: si
ningún caso tiene la fuente no localizable, es porque alguien ya la localizó.

Los enums cerrados a los que hay que normalizar están en
[`../docs/GLOSARIO.md`](../docs/GLOSARIO.md).

### Faltan los tiempos (defecto D5, confirmado)

`minutes_to_locate` y `minutes_to_extract` **no existen como columnas** en la hoja
`Piloto_20_Consolidado`. Están definidas en el schema de R02 §8 pero nunca se
instanciaron. Sin ellas no se puede estimar el esfuerzo de automatizar ni
justificar qué emisores priorizar.

### Faltan controles negativos (defecto D3, confirmado)

```
Controles negativos:              1 de 20   (5%)   -> solo P20
Casos con divergence_detected:   17 de 20   (85%)
Casos con recuperabilidad D:      0 de 20   (0%)
Casos con abstencion real:        0 de 20   (0%)
```

Con un solo negativo, la **tasa de falsos positivos** —la métrica crítica de todo
el proyecto— es literalmente inmedible. Un sistema evaluado solo sobre casos
distorsionados parece perfecto y en producción marca todo.

### Dos casos que salen del alcance — resuelto

P08 (*82% de embarazadas, 104 de 127*) y P09 (*99 millones de vacunados, +610%*)
son bulos virales sobre artículos científicos en inglés: NEJM y *Vaccine*.
Encajan en la taxonomía, pero su fuente primaria es literatura científica, no un
organismo que publique ediciones sucesivas — así que "edición anterior" no
significa lo mismo para ellos, y necesitarían otra familia de conectores.

`DECISIÓN (2026-09-24)` **Salen del corpus de tesis.** Se registran como
`other_observed` y pasan a trabajo futuro. Ver DEC-013.

**Consecuencia para la TAREA 1:** el lote auditado son **18 casos en el alcance**
más 2 registrados como observados. No afecta a la métrica que decide, porque estos
20 nunca contaron para recuperabilidad.

---

## Composición obligatoria del lote crudo (TAREA 2)

Sin cuota geográfica: español en general, emisores elegidos por recuperabilidad
(Opción A, cerrada en `00b-DECISIONES-MATEO`).

| Tipo | Cantidad |
|---|---|
| Afirmaciones estadísticas **correctamente enmarcadas** (negativos) | 7 |
| Divergencia real esperada | 6 |
| Fuente primaria **no localizable** | 3 |
| Edición anterior **no localizable** | 2 |
| Formato hostil (PDF escaneado, sin datos abiertos) | 2 |

**Regla dura, sin excepciones:** el caso **no entra** si existe un artículo de
verificación sobre esa afirmación — Maldita, Newtral, AFP Factual, Ecuador
Chequea, Chequeado o cualquier otro. Hay que buscar contenido crudo:
publicaciones de redes, titulares de prensa con cifras, declaraciones públicas.

> Los 7 negativos y los 5 de fallo de recuperación son los que dan valor al
> piloto. Son también los que es tentador evitar. No se evitan.

### Campos obligatorios por caso

```
fuente primaria encontrada       (si/no)
edicion anterior encontrada      (si/no)   <- la metrica que decide
serie historica encontrada       (si/no)
metodologia encontrada           (si/no)
formato                          api | dataset | html | pdf | scan | none
recuperabilidad                  A | B | C | D
minutes_to_locate
minutes_to_extract
cronometrado_por                 agente | humano       <- obligatorio
truth, context, clase            enums cerrados
abstain_reason                   cuando no se pueda resolver
raw_value_span                   de cada numero usado
```

### Quién cronometra

`DECISIÓN (2026-09-24)` Los 20 casos del lote crudo los cronometra **Claude**, y
el número se declara explícitamente en el método como
**recuperabilidad-por-agente**. Mateo cronometra **5 casos a mano, aparte**, como
referencia humana de contraste. Ver DEC-014.

Por eso `cronometrado_por` es un campo obligatorio: medir el tiempo sin decir quién
midió no es defendible.

---

## Cómo se reporta

`PILOT-FINDINGS.md` reporta la recuperabilidad **solo sobre el lote crudo**, y la
compara con la del lote sesgado. **Esa comparación es un resultado en sí mismo**:
cuantifica cuánto trabajo hace un verificador humano antes de que el dato sea
recuperable.

---

## La regla que gobierna esta carpeta

> No intentes demostrar que VERITAI funciona. Intenta descubrir honestamente
> dónde funciona y dónde falla. Un fallo temprano es un resultado útil. No
> maquilles el piloto para que valide la idea.
>
> — START-HERE §21

Si un dato no se puede verificar, se marca `NEEDS_REVIEW`. Nunca se rellena con
algo plausible.
