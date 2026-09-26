# PILOT-FINDINGS — lo que el piloto encontró

**Fecha:** 2026-09-25 · **Rama:** `feat/tarea-3-decision` · **Tarea:** 3 de 3

> Todos los números de este documento los imprime
> `scripts/pilot40.py` (salida 0). Ninguno está tecleado a mano. La
> recuperabilidad se reporta **solo sobre el lote crudo** (adenda, TAREA 3) y
> se compara con el lote sesgado; esa comparación es un resultado en sí.

---

## 0. Qué mide y qué no

| | |
|---|---|
| **Denominador** | Los **31 candidatos admitidos por la regla dura** y trabajados (`pilot-crudo-trabajados.csv`), no el lote de 23 por cubetas: la cuota fija el número por construcción (DEC-020) |
| **Conservadora vs leniente** | *Conservadora*: edición anterior localizada **y** publicador que no rechazó al agente; un 403/406/418 al primer cliente cierra el caso aunque otro cliente pase (DEC-021). Es la que decide. *Leniente*: edición anterior localizada, sin mirar cómo. Se reporta al lado |
| **Agente, no humano** | Tiempos y recuperabilidad son del agente (DEC-014, DEC-019). La humana real la dan los 5 casos de Mateo, §7, **pendientes** |
| **Etiquetas provisionales** | `truth`, `context` y `clase` de un solo anotador (el agente), marcadas `agente_provisional`; los `NEEDS_REVIEW` están en `notas` |
| **Los 20 auditados** | Entran en `PILOT-40.csv` para taxonomía, formatos y tests. **No cuentan para recuperabilidad**: salieron de artículos de verificadores (D1) |

---

## 1. Las cinco métricas de R02 §7

Sobre los 31 crudos. La segunda fila manda.

| Métrica | Conservadora | Leniente | Umbral verde | Semáforo |
|---|---|---|---|---|
| Fuente primaria localizada | 25/31 · **80,6%** | 27/31 · 87,1% | >70% | verde |
| **Edición anterior localizada** | 23/31 · **74,2%** | 25/31 · 80,6% | >60% | **verde** |
| Extracción sin intervención extrema (recuperabilidad A o B) | 25/31 · **80,6%** | ídem | >60% | verde |
| Clases de divergencia observadas | **4** de 5 como clase primaria (`1_ranking_vs_value`, `2_baseline_selection`, `3_absolute_vs_relative`, `4_denominator`); `5_methodology_change` solo como secundaria (C29) | | ≥3 | verde |
| Tiempo medio por caso | **agente 2,3 min**, máximo 5,2; tope de 20/15 min nunca tocado | | <20 min | verde (agente) · **humano pendiente** |

Verde en las cinco, con la lectura conservadora. **Lo que sigue es lo que
ese verde no dice.**

---

## 2. Comparación con el lote sesgado

| | Auditado (20, de verificadores) | Crudo (31, sin verificación previa) |
|---|---|---|
| Recuperabilidad | A 8 · B 11 · C 1 · **D 0** | A 15 · B 10 · **D 6** |
| Verificado contra la primaria con `raw_value_span` | **3/20** | actual **31/31** · anterior **25/31** |
| `divergence_detected` | **16/20** (80%) | **10/31** (32%) tras DEC-027; 12/31 en la recolección |
| `truth = contradicted` | 9/20 | 3/31 |
| Formato | html 8 · dataset 6 · pdf 6 | pdf 11 · dataset 9 · api 6 · none 3 · html 2 |

Tres lecturas:

1. **El sesgo D1 escondía la D.** El Excel tenía cero casos con fuente no
   localizable porque alguien —el verificador— ya la había localizado. En
   contenido crudo aparecen 6 de 31, y son la parte informativa del piloto.
2. **El lote auditado no servía para medir tasa de falsos positivos**: 16 de
   20 divergencias. El crudo tiene 16 controles negativos reales sobre 31 (tras DEC-027), y
   es donde un sistema se puede equivocar en la dirección que importa.
3. **"Verificado" cambia de significado.** En la auditoría solo 3 casos
   tenían el número literal de la primaria; en el crudo, 31 de 31 para la
   edición actual y 25 de 31 para la anterior. Es lo que "ningún número puede
   tener como único origen el LLM" exige, y ahora hay 56 spans que lo cumplen.

---

## 3. Amenazas a la validez

Este es el núcleo del documento. Escrito como lo pidió Mateo: sin rodear.

### 3.1 El 74,2% es el promedio de dos poblaciones que no elegí yo

```
nivel 1  (INE, INEC, INEGI, DANE, INEI, Eurostat, FMI, ministerios)   16/19   84,2%
resto    (niveles 3, 4 y 5)                                             7/12   58,3%
                                                                       ------
                                                                       23/31   74,2%
```

**La mezcla la eligió el barrido y el buscador.** 19 de los 31 casos son
estadística oficial de nivel 1 porque el buscador devuelve cobertura de un
IPC o una EPA con más facilidad que un ranking de consultora. Y 21 de 31 son
de España. Por vía de descubrimiento, reconstruida del transcript
(`pilot-crudo-descubrimiento.csv`):

```
consultas que nombraban un organismo, o cribas de esos casos    17/19   89,5%
consultas por ranking, encuesta o tema (sin emisor en la pregunta) 6/12   50,0%
```

Si el pool hubiera salido mitad y mitad, la tasa rondaría el 67%; si hubiera
sido todo nivel 3–5, el 58%. **El número no cambia; se declara con su límite,
y el límite es este.**

### 3.2 Seis de los 31 no son sorteos independientes

C03, C05, C08, C13, C17 y C31 aparecieron en la **búsqueda negativa de la
criba de otro candidato**: son cobertura hermana del mismo dato (C03 de C02,
C05 de C04, C08 de C07, C13 de C12, C17 de C16, C31 de C30) y heredan la
primaria del hermano. Sin ellos:

```
n efectivo 25   conservadora 18/25   72,0%   leniente 19/25   76,0%
```

Sigue en verde, pero el intervalo real es más ancho de lo que "23 de 31"
sugiere.

### 3.3 Un buscador, una sesión, un modelo, un anotador

- El pool es "lo que este buscador devolvió el 25 de septiembre de 2026", no
  una muestra de la prensa en español.
- Todo el trabajo lo hizo un agente en una sesión; las etiquetas son de un
  anotador. Un segundo anotador (P-05) es la única forma de medir acuerdo.
- No controlo el user-agent del fetcher: cumplo DEC-018 no reintentando, pero
  no puedo afirmar que el agente se presente como VERITAI.

### 3.4 Tiempos de agente, no esfuerzo humano

2,3 minutos por caso mide latencia de herramientas más razonamiento en
paralelo por lotes. No dice cuánto tarda una persona. Ver §7.

### 3.5 Formato hostil: 0 de 2 (DEC-022)

Buscando sin sesgo no apareció un solo PDF sin texto. Puede ser que el
fenómeno sea raro, o que el pool no llegara a donde vive (ayuntamientos,
gobiernos provinciales, organismos pequeños). Con estos datos no se
distingue. El fallo de nivel 5 tomó otra forma: **no hay documento** (§6 de
FAILURES).

### 3.6 Lo que la conservadora deja fuera, a propósito

C30 y C31 se leyeron por una vía que DEC-021 descarta (`curl` tras un 418).
Sus valores están en el registro, marcados; no suman. La leniente los cuenta.
La diferencia entre las dos cifras (25 vs 23) es exactamente el coste de
respetar al publicador.

---

## 4. El alcance honesto del sistema

R02 §7: *"Verde solo en 3 emisores es un resultado perfectamente válido. Una
tesis sobre tres emisores bien resueltos es mejor que una sobre cuarenta mal
resueltos."*

**Propuesta.** VERITAI se declara para **publicadores de nivel 1**:
organismos estadísticos y ministerios que publican por API, dataset
descargable o boletín en URL estable. Ahí la recuperabilidad conservadora es
**84,2%** (16/19). Los niveles 3–5 quedan como **limitación declarada y
trabajo futuro**, con su **58,3%** escrito en la tesis, no en una nota al
pie. Es la decisión que Mateo pidió proponer; se registra en P-19.

**Criterio para los emisores del prototipo**, explícito y verificable en
`PILOT-40.csv`: recuperabilidad A, vía API o dataset, al menos una
divergencia observada en el lote, y ningún rechazo al agente (DEC-021).

| Emisor | Vía | Casos | Divergencia observada | Cumple |
|---|---|---|---|---|
| **INE** (API Tempus) | api | C11, C16, C17; P04, P11, P16, P19 en el auditado | En el crudo, dos controles negativos y un claim falso (C17); en el auditado, P11 (`2_baseline_selection`), P04 y P19 (`3_absolute_vs_relative`), P16 (`4_denominator` secundaria) | sí |
| **FMI** (DataMapper API) | api | C07, C08 | C07, **la canónica** (`1_ranking_vs_value`) | sí |
| **Ministerio del Interior** (Portal Estadístico de Criminalidad: PC-Axis + PDF) | dataset/pdf | C18, C19, C20; P03, P06 en el auditado | C19 (`3_absolute_vs_relative`); revisión de base en C18 | sí, por el portal; el PDF en `interior.gob.es` da 403 |
| Eurostat (JSON-stat) | api | C21 | C21 (`2_baseline_selection` en el cuerpo) | reserva |
| AEMET (PDF con patrón de URL por año) | pdf | C23; P13 | ninguna | reserva |
| INEC, INEGI, DANE | pdf/dataset | C04, C05, C12–C15, C28 | C05, C13, C15 | reserva (país) |
| INEI vía `gob.pe` | — | C30, C31 | C31 | **no**: 418 (DEC-021) |

Tres para el prototipo: **INE, FMI e Interior**. Cubren API pura, API con
agregados que hay que filtrar, y dataset + PDF con revisión de base. Cubren
también tres de las cuatro clases observadas.

---

## 5. P-15, de frente

La clase canónica es marginal en dos lotes independientes. Ya no es ruido.

```
clase primaria en las 28 divergencias (16 auditado + 12 crudo)
  other_observed            10   35,7%     (5 + 5)
  2_baseline_selection       6   21,4%     (4 + 2)    2a, tras DEC-026
  3_absolute_vs_relative     5   17,9%     (3 + 2)
  4_denominator              3   10,7%     (2 + 1)
  1_ranking_vs_value         2    7,1%     (1 + 1)    <- la que daba nombre al proyecto
  5_methodology_change       1    3,6%     (1 + 0)    2c
  2b_base_revisada           1    3,6%     (0 + 1)    C29, codigo nuevo (DEC-026)

familias
  comparacion de base   (2a + 2b + 2c)       8
  magnitud mal leida    (3 + 4)              8
  + revision de base latente en la primaria de C18 (control negativo)
```

`NOTA` La tabla original de este documento contaba C29 como
`2_baseline_selection` con `5_methodology_change` secundaria; DEC-026 le da su
código propio, `2b_base_revisada`. Es el único caso reetiquetado y la familia
no cambia de tamaño.

`CORRECCIÓN (P-12, 2026-09-25)` La tabla de 28 incluye a **P08 y P09, fuera
de alcance por DEC-013**. Las proporciones que cuentan son sobre las **26 en
alcance**, y además sin los hermanos por criba (`pilot40.py`, tabla 5b):

```
clase primaria                en alcance (26)      sin hermanos (21)
  other_observed                 8   30,8%            4   19,0%
  2_baseline_selection (2a)      6   23,1%            6   28,6%
  3_absolute_vs_relative         5   19,2%            4   19,0%
  4_denominator                  3   11,5%            3   14,3%
  1_ranking_vs_value             2    7,7%            2    9,5%
  5_methodology_change (2c)      1    3,8%            1    4,8%
  2b_base_revisada               1    3,8%            1    4,8%

familia comparacion de base    8   30,8%            8   38,1%
magnitud mal leida             8   30,8%            7   33,3%
other_observed en alcance: P05 P07 P17 C03 C05 C08 C10 C13; hermanos: C03 C05 C08 C13
```

La mitad de `other_observed` es cobertura hermana de datos ya representados.
El desglose caso a caso, con lo que cada uno necesitaría para entrar en una
clase, está en `docs/PREGUNTAS-ABIERTAS.md`, P-12.

`TRAS DEC-027 (P-12 cerrada, 2026-09-25)` Mateo aceptó tres encajes (P05 →
2a, P07 → 4, C13 → 2a), sacó C03 a `no_divergence_detected` (lectura
alternativa) y C05 a abstención con dos motivos, dejó C08 como está y
convirtió P17 y C10 en candidatas sin código con criterio de reaparición. Las
divergencias en alcance pasan de 26 a **24** (`pilot40.py`, tablas 5 y 5b):

```
clase primaria                en alcance (24)      sin hermanos (21)
  2_baseline_selection (2a)      8   33,3%            7   33,3%
  3_absolute_vs_relative         5   20,8%            4   19,0%
  4_denominator                  4   16,7%            4   19,0%
  other_observed                 3   12,5%            2    9,5%     P17 C08 C10
  1_ranking_vs_value             2    8,3%            2    9,5%
  5_methodology_change (2c)      1    4,2%            1    4,8%
  2b_base_revisada               1    4,2%            1    4,8%

familia comparacion de base   10   41,7%            9   42,9%
magnitud mal leida             9   37,5%            8   38,1%
```

La familia "comparación de base" es ahora la más frecuente por sí sola (10
de 24), lo que sostiene la elección de B como primera familia (DEC-026)
**sin que ningún caso se haya reetiquetado para lograrlo**: los tres encajes
los decidió Mateo sobre el mecanismo de cada caso, y C08 —que habría subido
la clase ilustrativa— se dejó como estaba.

Cinco opciones de reencuadre. Ninguna se decide aquí.

| | Opción | A favor | En contra | La sostienen |
|---|---|---|---|---|
| **A** | Mantener `1_ranking_vs_value` como canónica y aceptar corpus pequeño | Test más limpio (puesto vs valor, dos números y una dirección); contribución más distintiva; C07 es un caso de libro verificado por API | **2 casos en 48**; tesis sobre un fenómeno raro; el corpus de la clase principal no crece buscando neutral | C07, P01 (+ C08 secundaria) |
| **B** | Canónica = **familia "comparación de base"** (`2_baseline_selection` + revisión de base + `5_methodology_change`) | La más frecuente (8 + 2 revisiones); es **exactamente lo que mide la recuperabilidad**: hacen falta dos ediciones; emisores de nivel 1 la producen a diario | Heterogénea: elección de periodo, base revisada y cambio de método son tres tests, no uno; hay que definir cada subtipo | C02, C15, C29, C18, C21; P05, P10, P14, P19 |
| **C** | Canónica = **revisión de base** sola (la opción de Mateo) | Novedosa; computable de forma cruda (valor publicado en t−1 vs valor revisado en t); atada a la capacidad central de VERITAI: guardar ediciones; el emisor la documenta (Interior, IEP) | **2 de 12** en el crudo y 0 claras en el auditado: hoy tan marginal como ranking; exige historial de ≥2 ediciones propias, que el sistema aún no tiene | C18, C29 |
| **D** | Canónica = **magnitud mal leída** (`3_absolute_vs_relative` + `4_denominator`) | 8 de 28; frecuente en prensa; computable con una sola edición | Se acerca al fact-checking aritmético y se aleja de "contexto"; parte de la novedad de la tesis se diluye | C19, C25, C31; P02, P07, P09, P17, P18 |
| **E** | El objeto pasa a ser **"comparabilidad de ediciones"**: toda afirmación que compara dos ediciones de una estadística oficial; las cinco clases son tests bajo ese paraguas, ninguna canónica | Usa las 28; encaja con el título ("divergencia contextual computable"); el prototipo arranca por la más frecuente y `ranking_vs_value` queda como caso ilustrativo | Alcance más ancho para el prototipo, que R02 §18 quiere de **una** clase y **un** emisor; hay que elegir igualmente por dónde empezar | todas |

**Recomendación** (no decisión): **E como objeto de estudio, B como primera
clase del prototipo, A como caso ilustrativo.** Razón: B es la única familia
que a la vez es frecuente y depende de la edición anterior, que es lo que el
piloto acaba de demostrar que se puede recuperar. C es la opción más
interesante intelectualmente, y por eso mismo conviene tenerla como subtipo
de B y no como apuesta única con dos casos.

`CERRADA (DEC-026, 2026-09-25)` Mateo aprobó E / B / A, con C como subtipo
2b, tras una pasada de coherencia con nueve ajustes. **El cotejo de caso
canónico** —cinco requisitos idénticos sobre C29, C21 y C18: primaria
trazable, edición actual, edición anterior, revisión de base demostrable,
reproducible— no lo pasó ninguno con un claim divergente: C29 tiene la
divergencia en el claim pero la revisión se infiere del indicador CHANGE del
IEP, que no imprime los valores 2025 revisados; C18 demuestra la revisión con
dos cifras literales del mismo emisor pero su claim relaya bien; C21 es 2a. No
se declara canónico: la tesis presenta el **par C18 + C29** y el canónico sale
de la Puerta 2. Encuadre completo en `docs/TESIS-ENCUADRE.md`.

---

## 6. Perú 0/2 y el bloqueo por publicador

**No alcanza.** Los dos casos peruanos (C30, C31) son **un solo dominio**
(`gob.pe`) y **un solo rechazo** (418 al fetcher). Es una observación, no
dos, y no dice nada de Perú ni de Latinoamérica. Escribir "Perú bloquea" con
esto sería maquillar en la dirección contraria.

Lo que sí se observa en el conjunto, como **hipótesis** para trabajo futuro:

| Rechazaron al agente | Tipo |
|---|---|
| `gob.pe` (INEI) — 418 | plataforma gubernamental centralizada |
| `interior.gob.es` — 403 al PDF | plataforma gubernamental centralizada (el Portal Estadístico del mismo ministerio respondió 200) |
| `inclusion.gob.es` — bloqueo | plataforma gubernamental centralizada (La Moncloa respondió 200) |
| `saily.com` — 403 | empresa (ranking comercial) |

Tres de los cuatro primarios que rechazaron son **portales gubernamentales
centralizados**, no institutos de estadística en su propio dominio (INE,
INEC, INEGI, DANE, Eurostat, FMI, AEMET, EDUCAbase, todos 200). Cinco
dominios de contenido también bloquearon (Deia, Radio Pichincha, GK, El
Boletín, Enfoque), sin efecto en la métrica. Con cuatro observaciones no se
prueba nada; se apunta que el filtro de selección de emisores de R02 §6
debería incluir "responde al agente identificado" como criterio de entrada.

---

## 7. Humano vs agente — PENDIENTE

`PENDIENTE: 5 casos manuales de Mateo (DEC-014). El agente no mira ese CSV.`

Selección: `random.Random(20260925)` sobre los `case_id` del lote, ver
`COLECCION-LOTE-CRUDO.md` §8. Lo que el agente registró se copia aquí para
que la comparación sea directa cuando lleguen los cinco:

| Caso | Agente: edición anterior | Agente: alcanzable | Agente: localizar / extraer | Humano: minutos | Humano: edición anterior | Humano: URL usada |
|---|---|---|---|---|---|---|
| C04 | sí | sí | 1,5 / 1,1 min | __ | __ | __ |
| C05 | sí | sí | 1,0 / 0,0 min | __ | __ | __ |
| C11 | sí | sí | 1,1 / 1,8 min | __ | __ | __ |
| C14 | sí | sí | 0,4 / 1,8 min | __ | __ | __ |
| C22 | **no** | no | 5,2 / 0,0 min | __ | __ | __ |

Al llegar se calcula: acuerdo por caso en `previous_edition_found`, razón de
tiempos humano/agente, y si algún caso cambia la lectura de la métrica (en
particular C22: si una persona encuentra la tasa trimestral por CCAA que el
agente no encontró, `alcanzable_por_humano` deja de ser inferido). La
decisión de `PILOT-DECISION.md` se revisa si los cinco contradicen §1.

---

## 8. Predicciones contra realidad, las dos tareas

| Tarea | Predicción | Resultado |
|---|---|---|
| 1 | Link rot en 2019–2020 | Fallida: cero enlaces muertos; lo que hay es **bloqueo de bots** |
| 1 | Las 20 filas necesitan normalización | Confirmada: 12 valores de `truth` → 3 |
| 1 | P03 error aritmético | Confirmada; y tres errores de transcripción más |
| 2 | Recuperable-por-agente 30–50% | **Fallida por pesimista**: 74,2% / 80,6%. Causa: pool de nivel 1 (§3.1) |
| 2 | La regla dura rechaza ≥ 1/3 | Fallida: 18,4% |
| 2 | `1_ranking_vs_value` en ≥ 2 de 6 | Fallida: 1 + 1 secundaria |
| 2 | ≥ 2 "primarias" que no existen | Confirmada: 3 |
| 2 | Bloqueo anti-bot en ≥ 2 primarias | Parcial: 1 + 1 con vía alternativa del mismo emisor; con DEC-021, 3 casos |
| 2 | Localizar > 20 min en nivel 4–5 | Fallida: **fallar es rápido** cuando no hay nada que encontrar |
| 2 | Edición anterior será la cubeta más difícil de distinguir | Confirmada: C25 |
| 2 | ≥ 1 caso cambia de cubeta al extraer | Confirmada: C17, C28, C25 |

Once predicciones, cinco confirmadas. Las que fallaron, fallaron en la
misma dirección: **el mundo de nivel 1 es más recuperable de lo que suponía, y
la búsqueda me llevó a él más de lo que suponía.**

---

## 9. Reproducir

```
python research/scripts/pilot40.py                     # PILOT-40.csv + todos los conteos de este documento
python research/scripts/validar_lote_crudo.py          # los 31: metricas, cubetas, enums
python research/scripts/reconstruir_descubrimiento.py  # via de descubrimiento (necesita el transcript)
python research/scripts/normalizar_a_enums.py          # los 20
```

Entradas: `pilot-20-normalizado.csv`, `pilot-crudo-trabajados.csv`,
`pilot-crudo-descubrimiento.csv`, `cronometro.log`, y el Excel congelado en
solo lectura (sha256 `3f00914369…`, sin cambios).
