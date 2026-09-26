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

**Divergencia contextual computable** *(DEC-026)*
Una afirmación estadística la presenta cuando (1) sus números son verificables
contra una fuente primaria oficial y llevan `raw_value_span`; (2) la
comparación que establece —periodos, bases, magnitudes, denominadores,
posiciones— difiere de la que la propia fuente sostiene con sus ediciones; y
(3) esa diferencia se decide con un test determinístico sobre los valores
recuperados. Independiente de `truth`; **no afirma intención**.

**Caso ilustrativo**
*"España cae 16 puestos en el ranking de países más seguros para mujeres."* El
dato es correcto: la puntuación de España no cambió, 16 países mejoraron la suya.
`truth: supported` + `context: divergence_detected`. Es `1_ranking_vs_value`,
**2 de 24 divergencias en alcance** en el piloto (tras DEC-027): ilustra el
fenómeno, no lo representa.

**Caso canónico**
No hay todavía (DEC-026). Se cotejaron C29, C21 y C18 contra cinco requisitos
idénticos —primaria trazable, edición actual, edición anterior, revisión de base
demostrable, reproducible— y ninguno los cumple todos con un claim divergente.
La tesis presenta el **par C18 + C29** (mecanismo demostrado + efecto sobre un
claim). El canónico de la familia "comparación de base" sale de la Puerta 2,
cumpliendo los cinco requisitos sobre datos no usados en el piloto.

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

**Recuperable-por-humano / recuperable-por-agente** *(DEC-019, 2026-09-25)*
La métrica de la Puerta 1 se parte en dos y **se reportan ambas**:

```
recuperable-por-humano   una persona con navegador localiza la edicion anterior
recuperable-por-agente   el sistema la localiza sin evadir ninguna proteccion
```

**La segunda es la que decide**, porque VERITAI es un agente. La primera es
contexto y validez externa. No son el mismo número: la auditoría del piloto
encontró páginas vivas para un navegador y cerradas para un fetcher (403 de
Newtral en 8 de 8, desafío de Cloudflare en Interior, tablas que solo cargan
por JS). Medir solo la humana es lo que el Excel hacía, y por eso salió 20 de 20.

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
El lote sesgado tenía 1 de 20; el lote crudo, 16 de 31 (tras DEC-027). En la
Puerta 2, C16 es el control con test aplicable; C11 es un nivel correcto sin
test que aplicar (P-22).

**Conjunto de desarrollo / conjunto de evaluación**
Dos conjuntos de claims que **no se mezclan** (DEC-025). El de **desarrollo**
sirve para construir, depurar y hacer regresión: todo lo que pasó por el
piloto (P01–P20, C01–C31, candidatos rechazados, los 5 manuales) y los casos
nuevos de la Puerta 2 (N01, N03, N04). El de **evaluación** es el que mide: se
recolecta después, con el mismo método, y **nada** que haya servido para
diseñar un test entra en él. Cada JSON de claim lleva `conjunto: desarrollo |
evaluacion`.

**Claim estructurado**
Lo que el sistema recibe: tipo (`cambio_entre_periodos`, `nivel`, `umbral`,
`extremo_historico`, `crecimiento_compuesto`, `otro`), métrica del emisor
(tabla y nombre exacto de serie), periodo objetivo, periodo base, valores y
cambio afirmados, dirección. En la Puerta 2 se escribe **a mano** y queda
versionado en `research/puerta2/casos/`; el LLM no participa.

**`raw_value_span` / `bundle_hash`**
El span es el fragmento **literal** de la primaria del que salió cada número
(en el INE, el objeto JSON del dato con `Fecha`, `T3_TipoDato`, `T3_Periodo`,
`Anyo`, `Valor`). El hash es sha256 sobre publicador, URL, serie, periodo, span
y versión de todos los items del bundle: si cambia lo extraído, cambia el hash
(P04 lo demostró al corregir el periodo anual). Un test automático falla si un
número del veredicto no tiene span.

**Test 2a (periodo o base elegida)**
Determinístico, definido antes de correr casos (DEC-028). Dispara por **(B)**
valor atribuido a otro periodo de la ventana, o por **(A)** base que no es
referencia del emisor y cuya recomputación contra esa referencia cambia de
signo o difiere ≥ 2× en magnitud. Lo que dispara por magnitud en horizontes
largos declarados está en discusión (P-21).

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
1_ranking_vs_value        test 1 · ranking vs valor (ilustrativo, DEC-026)
2_baseline_selection      familia 2 · 2a periodo o base elegida
2b_base_revisada          familia 2 · 2b base revisada (nuevo, DEC-026; C29)
3_absolute_vs_relative    test 3 · absoluto vs relativo
4_denominator             test 4 · denominador
5_methodology_change      familia 2 · 2c cambio de metodo
none                      control negativo
other_observed            lo que no encaje, con nota libre (3 de 24 en alcance tras DEC-027: P17 C08 C10)
```

`NOTA` **Familia 2, "comparación de base"** *(DEC-026)*: 2a, 2b y 2c son la
primera familia que se implementa y evalúa. Los códigos `2_baseline_selection`
y `5_methodology_change` se conservan con su nombre; `2b_base_revisada` es el
único código nuevo. Solo C29 cambió de etiqueta.

`NOTA` **Candidatas a clase, sin código** *(DEC-027)*: "agregación con
subgrupos en sentido contrario" (P17) y subtipo 2d "cambio afirmado sin
edición anterior" (C10). **No se crean con n = 1.** Criterio de reaparición,
fijado antes de ver los datos: ≥ 3 casos independientes (no hermanos, ≥ 2
emisores) en el conjunto de evaluación, con primaria y edición anterior
localizadas (A o B) y test computable sin juicio humano. Se decide una sola
vez, al cerrar la anotación de ese conjunto.

`NOTA` **Varios motivos de abstención** se separan con `|`
(`REQUIRED_SLOT_MISSING|UNSUPPORTED_CLAIM_TYPE`, C05), igual que las clases
secundarias.

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
METRIC_AMBIGUOUS                # anadido 2026-09-25 (DEC-015): el claim no dice
                                # que metrica usa y el veredicto cambia segun cual
                                # se elija. 4 de 20 en el piloto: "valor o volumen",
                                # "euros o % PIB", "tasa o numero", "lider en que"
```

`NOTA` R02 §11: los motivos reales de abstención se descubren en el piloto, no se
inventan después. `METRIC_AMBIGUOUS` es el primero descubierto. Otros tres
candidatos con un solo caso cada uno (`SCOPE_NOT_RESOLVABLE`,
`GROUPS_NOT_HOMOGENEOUS`, `SAMPLE_NOT_REPRESENTATIVE`) **no** entran con n=1.

`NOTA` **Bloqueo anti-bot** *(DEC-018)*: cuando un publicador bloquea al agente
—403, desafío de Cloudflare, `robots.txt`— **no se evade**. Se registra
`PRIMARY_SOURCE_NOT_FOUND` con el subtipo `bloqueado_por_publicador`, y ese es el
resultado. Ni user-agents falsos, ni saltarse desafíos, ni scraping contra quien
bloquea explícitamente.

`NOTA` **El primer rechazo cierra el caso** *(DEC-021)*: un 403, 406, 418 o
desafío al primer cliente con el que el agente se presenta cierra el caso como
**no recuperable-por-agente**, aunque otro cliente honesto —por ejemplo `curl`
con su user-agent por defecto— obtenga 200 después. Solo un error de red
(`ECONNREFUSED`, `socket hang up`, timeout) admite un reintento, porque no es
una señal del publicador. Lo que se hubiera leído por la vía descartada se
conserva como registro, marcado, pero no suma en la métrica.

`NOTA` **Denominador de la métrica** *(DEC-020)*: la tasa que decide la Puerta 1
se calcula sobre **todos los candidatos admitidos y trabajados**
(`pilot-crudo-trabajados.csv`), no sobre el lote por cubetas, cuya cuota fija
el número por construcción. La del lote se reporta al lado.

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
alcanzable_por_humano       # anadidos 2026-09-25 (DEC-019). Se rellenan los dos.
alcanzable_por_agente       # <- este es el que entra en la metrica de la puerta
```

`NOTA` **`clase = none` no es un tercer estado** *(DEC-016)*. `truth` y `context`
son ejes independientes (R02 §10) y van poblados en las 20 filas. Un claim
correcto y bien enmarcado (P20) y un claim falso sin divergencia contextual (P15,
P16) comparten `context = no_divergence_detected`; lo que los distingue es
`truth`. Con los dos ejes poblados, la tasa de falsos positivos se mide sin
añadir clases.

---

## Términos que NO se usan

| No usar | Usar |
|---|---|
| "Falso" / "verdadero" a secas | `truth` + `context`, separados |
| "Fake news", "engañoso" | afirmación con **divergencia contextual**, o el estado concreto (`truth` / `context`); nunca una intención del autor |
| "Score de confianza" como salida única | `truth` + `context` + motivo de abstención |
| "El sistema cree que…" | el sistema no cree: aplica una regla sobre unos valores |
| "Detectar desinformación" | detectar divergencia contextual computable |

El proyecto **no juzga la intención del autor**. Es una decisión cerrada, no una
cautela de redacción: nada en la arquitectura puede medir intención.
