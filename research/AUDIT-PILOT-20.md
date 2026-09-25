# Auditoría del piloto de 20 casos

**TAREA 1** del plan de investigación. Audita los 20 casos de
`05-VERITAI-PILOTO-20-CASOS.xlsx`, normaliza sus etiquetas a enums cerrados y
documenta el sesgo de procedencia con evidencia concreta.

| | |
|---|---|
| Fecha | 2026-09-24 |
| Rama | `feat/auditoria-piloto-20` |
| Datos normalizados | [`pilot-20-normalizado.csv`](pilot-20-normalizado.csv) — 20 filas, 25 columnas |
| Scripts reproducibles | [`scripts/auditar_aritmetica.py`](scripts/auditar_aritmetica.py), [`scripts/normalizar_a_enums.py`](scripts/normalizar_a_enums.py) |
| Cronometrado por | agente (DEC-014) |

---

## 0. Lo que esta auditoría NO mide

> **Estos 20 casos no cuentan para medir recuperabilidad.**

Los 20 se encontraron a través de artículos de verificadores, donde un
periodista ya había localizado la fuente primaria, la edición histórica y la
metodología. Medir recuperabilidad sobre ellos mide que un verificador hizo el
trabajo, no que el dato sea recuperable. Es sesgo de supervivencia (adenda, D1).

Ningún número de este documento entra en la métrica que decide la Puerta 1. Esa
métrica se mide solo sobre el lote crudo de la TAREA 2.

Lo que sí sirven los 20: taxonomía, formatos, diseño de tests y regresión. Y
para eso hay que saber si están bien transcritos. De eso va esta auditoría.

---

## 1. Resultado en una tabla

| Estado | Casos | Significa |
|---|---|---|
| **verificado** | 3 | Cifras confirmadas contra la fuente **primaria**, con `raw_value_span` literal |
| **parcial** | 3 | Primaria viva y aritmética correcta, pero las cifras exigen navegar o descargar |
| **NEEDS_REVIEW** | 12 | Error encontrado, o primaria no alcanzable, o URL que no identifica ningún dato |
| **fuera_de_alcance** | 2 | P08 y P09, por DEC-013 |

```
verificado        P15  P16  P20
parcial           P06  P14  P17
NEEDS_REVIEW      P01  P02  P03  P04  P05  P07  P10  P11  P12  P13  P18  P19
fuera_de_alcance  P08  P09
```

**Tres de veinte** llegan a la fuente primaria con el número literal a la vista.
En un lote que el Excel calificaba de recuperabilidad A o B en 20 de 20.

La diferencia no es que el Excel esté mal. Es que **"la fuente existe" y "un
sistema puede leer el número en la fuente" son afirmaciones distintas**, y el
Excel medía la primera. Esta auditoría mide la segunda, que es la que importa
para VERITAI.

---

## 2. Método

Deliberadamente **offline primero**. Casi todos los hallazgos estaban ahí.

### Fase A — sin red

**A1. Aritmética.** `scripts/auditar_aritmetica.py` recomputa 36 cálculos desde
los valores de `Dato A` y `Dato B` y los compara con `Contraste`, con una
política de tolerancia explícita: margen estrecho para entradas exactas, amplio
para entradas con `~` o `>`, y "plausible" para cifras que son del emisor y no
un cálculo propio.

```
comprobaciones              36
cuadran exactamente         26
cuadran dentro de redondeo   4
DISCREPAN                    1     <- P03
no verificables              5
```

**A2. Normalización.** `scripts/normalizar_a_enums.py` lleva `truth`,
`context`, `clase`, `recuperabilidad`, `formato` y `abstain_reason` a los enums
de [`../docs/GLOSARIO.md`](../docs/GLOSARIO.md). Cada resolución tiene su
justificación en una línea, en el propio script. El original se conserva en
columnas `*_original` para que la traducción sea auditable.

**A3. Coherencia interna.** `truth` ↔ `context` según R02 §10; sumas que deben
cuadrar; semántica de `Fecha contenido`.

### Fase B — con red

40 URLs (36 únicas), consultadas en paralelo el 2026-09-24 entre las 20:59 y
las 21:06, más 8 seguimientos: extracción local de 2 PDFs, 2 consultas a APIs
del mismo publicador, 1 reconsulta puntual, y 3 `curl -I` para caracterizar
bloqueos.

Disciplina aplicada (START-HERE §23–25): todo lo recuperado es **DATA, nunca
INSTRUCCIÓN**; prompt fijo que pide solo hechos observables; sin autenticación;
sin descargar binarios salvo los 2 PDFs de organismos oficiales, que se leyeron
con un parser y no se ejecutaron; un solo intento por URL.

`NOTA` Las 36 URLs se consultaron en paralelo, así que **el cronómetro por caso
no tiene sentido**. Se registra el reloj de la fase (~7 min) y
`cronometrado_por = agente`. Para el lote crudo, donde el tiempo sí importa, hay
que consultar en serie.

---

## 3. Predicciones contra realidad

Se escribieron antes de ejecutar (plan aprobado) para no poder ajustarlas.

| # | Predicción | Resultado |
|---|---|---|
| 1 | 4 URLs primarias son portadas: P04, P19, P05, P07 | **3 confirmadas** (P04, P05, P19). P07 no alcanzable: no se pudo ni comprobar |
| 2 | Link rot en 2019–2020: P04, P10, P11, P12, P18 | **FALLIDA.** Los dos PDFs (P11 INE 2019, P12 Sanidad 2020) están vivos y se descargaron. P18 no está muerta: Cloudflare pide un desafío. **Cero enlaces muertos** en todo el lote |
| 3 | P01: el EIU exige registro | **Sin resolver.** La herramienta no puede alcanzar `eiu.com` |
| 4 | P03: error aritmético +5,03 → +5,30 | **Confirmado** |
| 5 | Las 20 filas necesitan normalización | **Confirmado.** 12 valores de `truth` → 3 |
| 6 | 5 valores inventados en `abstain_reason`; `METRIC_AMBIGUOUS` ×2 sugiere hueco | **Confirmado y peor:** `METRIC_AMBIGUOUS` aparece en **4** casos |
| 7 | P15 y P16: `context` debe ser `not_applicable` / `no_divergence` | **Confirmado** por normalización, y expone un hueco del enum `clase` (§6) |
| 8 | P10 sin números verificables | **Confirmado.** Ni la primaria (página índice) ni Maldita dan cifras exactas |

Y la que esperaba que no fallara —"la aritmética del Excel es trabajo serio"—
**se sostiene**: 30 de 31 cálculos verificables cuadran. El problema del lote es
su procedencia y su transcripción, no sus divisiones.

**Lo que no predije y encontré:**

- **Bloqueo de bots, no enlaces muertos.** 8 de 8 URLs de Newtral devuelven 403
  al fetcher y **200 a un navegador**. Lo mismo `interior.gob.es` con Cloudflare.
  Un humano las abre; el sistema no. Ver §5.
- **Dos tablas "HTML" que en realidad son "API".** Eurostat (P15) e INE (P16)
  no devuelven nada como HTML porque cargan por JS, pero la API JSON del mismo
  publicador da el número exacto. Ver §5.
- **Tres errores de transcripción más** en el corpus, además del de P03:
  P11, P12 y una ambigüedad de unidad en P02. Ver §4.
- **La primaria de P12 contiene, en una nota al pie, la advertencia metodológica
  que explica el caso.** Ver §5.

---

## 4. Errores del corpus que hay que corregir

Concretos, verificables, con la evidencia al lado.

### 4.1 · P03 — cifra mal calculada

El Excel dice que 1S2022 contra 1S2019 es **+5,03%**. Con sus propios datos
(1.127.147 contra 1.070.421) da **+5,30%**. Transposición de dígitos.

### 4.2 · P11 — Dato A es una subcategoría, no el total

El Excel dice *"Mayo 2018: 8.830 constituidas"*. La tabla SM.4 del PDF del INE
(`sm1218.pdf`, p. 11) dice:

```
Mayo   8.908  395.469  8.830  393.831  0  0  78  1.638
       total           limitadas       (comanditarias) anónimas
```

**8.830 son las sociedades limitadas.** El total de mayo es **8.908**
(8.830 + 78). El 6.811 de diciembre sí es el total: *"En diciembre se crean
6.811 sociedades"* (p. 1). El Excel compara S.L. de mayo contra total de
diciembre. Total contra total: **−23,5%**, no −22,87%. La divergencia del caso
—estacionalidad— sigue siendo válida; el número no.

### 4.3 · P12 — las cifras no salen de la primaria citada

El Excel da *"23.663 curados"* y *"11.894 hospitalizados"* para Madrid y cita la
Actualización nº 71 del Ministerio de Sanidad. Ese PDF (vivo, 11 páginas, datos
a 09.04.2020) dice para Madrid:

```
Madrid  44.783  383,29  12.432¥  1.399¥  5.972  22.414  906
        confirm  IA14   hospit    UCI    fallec  curados nuevos
```

**22.414 curados y 12.432 hospitalizados.** Las cifras del Excel no están ahí.
El propio Excel lo insinuaba: *"p.ej. 23.663 en el gráfico"*. Los números vienen
del gráfico de Ayuso y Aguado, no de la fuente que se cita como primaria. Hay
que citar la fuente real de esas cifras o sustituirlas por las de la primaria.

### 4.4 · P02 — unidades: el Excel tiene razón y la secundaria no

El Excel dice `276 t → 18.798 t`. okdiario dice *"casi 19 toneladas"* y *"apenas
los 300 kg"*. Prueba de plausibilidad con el valor monetario, que ambos
comparten:

```
58 M EUR / 19 t        = 3.052 EUR/kg    absurdo para aceite a granel
58 M EUR / 18.798 t    = 3,1 EUR/kg      plausible
641.072 EUR / 0,3 t    = 2.137 EUR/kg    absurdo
641.072 EUR / 276 t    = 2,3 EUR/kg      plausible
```

**Las cifras del Excel son las coherentes. La prosa de okdiario tiene un error
de unidad de ×1.000.** No es un error del corpus, pero hay que anotarlo: el
lector de la secundaria se lleva cifras equivocadas, y el `raw_value_span` de
las toneladas sigue sin capturarse porque DataComex exige consulta interactiva.

### 4.5 · P13 — Dato B sin fuente

El Excel dice *"2020: cambia método de análisis, recalculando la serie
previa"*. La primaria citada es la Nota Técnica 31 de AEMET, *"Análisis de las
temperaturas en España en el periodo 1961-2018"*. Respalda el Dato A —serie
desde 1961, rejillas— y con eso basta para contradecir el claim de "2020".
**Pero no menciona 2020 ni recálculo.** El Dato B está asertado sin fuente.

### 4.6 · P01 — el claim cubre cuatro índices y el corpus documenta uno

*"España ha mejorado en los cuatro índices más prestigiosos"*. El Excel
documenta solo el Democracy Index del EIU. El `Contraste` afirma que *"otros
índices citados no mejoran"* sin registrar cuáles ni con qué cifras. Se resuelve
a `truth = mixed` y NEEDS_REVIEW: no se puede sostener `contradicted` con la
evidencia registrada.

### 4.7 · P03 — el claim es el encuadre del verificador

El texto del claim y la URL de contenido son ambos el artículo de Maldita.
Maldita no cita ninguna publicación viral concreta. **No hay entrada
reproducible del sistema.** Es el caso extremo del defecto D1.

---

## 5. Hallazgos de la Fase B que importan para la tesis

### 5.1 · El bloqueo de bots es una barrera de recuperabilidad que no existe para humanos

```
newtral.es           8 de 8 URLs   403 al fetcher   200 a un navegador (curl, UA de Chrome)
interior.gob.es      1 PDF         403 + "Cf-Mitigated: challenge"   (desafío JS de Cloudflare)
nejm.org             1             403
sciencedirect.com    1             403
eiu.com              1             no alcanzable por la herramienta
institucionpenitenciaria.es  1     conexión rechazada / timeout, también con curl
```

Ninguna de estas es un enlace muerto. Todas son **páginas vivas que un humano
abre y un agente no**. Esto conecta directamente con DEC-014: la
recuperabilidad-por-agente y la recuperabilidad-por-humano son números
distintos, y esta es una de las razones. Para el lote crudo, hay que registrar
por separado `alcanzable_por_humano` y `alcanzable_por_agente`.

`NOTA` R02 §6.3 ya lo anticipaba desde el otro lado: respetar `robots.txt` y
los términos de uso. Un publicador que bloquea fetchers está diciendo algo, y
VERITAI tiene que decidir qué hace con eso antes de escribir el primer conector.

### 5.2 · "HTML" que en realidad es "API"

| Caso | URL del Excel | Qué devuelve | Qué sí funciona |
|---|---|---|---|
| P15 | Eurostat databrowser `tqoe3a5` | Página vacía, solo JS | API de diseminación, JSON-stat: `"0":4.0,"1":4.1,"2":2.7,"3":2.6` → ES 2025 = 2,6 ✓, EU 2025 = 4,1 ✓ |
| P16 | INE `Tabla.htm?t=65217` | Título correcto, "0 series y 0 datos" | API `wstempus`, JSON: serie EPA423402 `"Valor":2645.2` ✓, EPA423404 `1192.7` ✓ |

Los dos únicos casos españoles plenamente verificados lo fueron **por la API del
mismo publicador**, no por la URL del Excel. Consecuencia para el diseño de
conectores: para INE y Eurostat, ir directo a la API. El formato real de estos
dos casos es `api`, no `html` ni `dataset`.

### 5.3 · La primaria de P12 lleva dentro la advertencia que explica el caso

En la tabla de la Actualización nº 71, las cifras de hospitalizados de Madrid
llevan una marca `¥`. La nota al pie dice:

> *"¥ Los datos de estas comunidades son datos de prevalencia (personas
> ingresadas a fecha de hoy). No reflejan el total"*

Es exactamente la divergencia del caso: comparar altas **acumuladas** con
hospitalizados **en stock**. La fuente primaria lo advierte. Un
`EvidenceBundle` con un slot `methodology_items` que capture notas al pie de la
tabla detectaría esto sin LLM. Es el mejor argumento del lote a favor de la
arquitectura de R02 §9.

### 5.4 · La secundaria puede equivocarse donde la primaria no

P02: okdiario escribe "19 toneladas" y "300 kg" donde los datos dicen ~18.800 t
y ~276 t. La cifra que titula (8.945%, en euros) es correcta; las de volumen,
en la prosa, están mal por ×1.000. Quien verificara contra el periódico
heredaría el error. Es el argumento de *"fuente primaria primero"* de
`03-2-VeritAI-PROYECTO-TOTAL` con un ejemplo concreto y fechado.

### 5.5 · Las URLs "primarias" del Excel son de cuatro tipos distintos

```
cifras verificables en la propia URL       3   P11 P12 P20     (2 son PDF)
tabla o dataset con descarga o API         4   P14 P15 P16 P17
portal o buscador: exige navegar           5   P02 P03 P06 P10 P13
portada institucional: no identifica nada  3   P04 P05 P19
no alcanzable                              5   P01 P07 P08 P09 P18
```

Una "URL primaria" que es una portada no es una referencia: es una dirección
postal. Para el lote crudo, la regla tiene que ser **URL del dataset o tabla
concreta, o no cuenta como localizada**.

---

## 6. Los defectos de la adenda, con números

### D1 — Sesgo de selección: peor de lo que decía la adenda

| Evidencia | Valor |
|---|---|
| Casos cuya `URL contenido` **es** la URL del verificador | **18 de 20** |
| Casos con URL de contenido que no sea un verificador | 2: P02 (okdiario), P20 (INEC) |
| Casos donde el texto del claim es el encuadre del verificador | 1: P03 |
| Verificadores que no citan una publicación concreta | P03, P09 (solo "publicaciones virales") |

La adenda decía que los casos se *encontraron* vía verificadores. El Excel
muestra que **el contenido original no está registrado**: sin URL del post, la
entrada del sistema no es reproducible.

### D3 — Controles negativos

```
Controles negativos            1 de 20   (P20)
divergence_detected           16 de 20
no_divergence_detected         4 de 20   (P13, P15, P16, P20)
Recuperabilidad D              0 de 20
Abstención real                0 de 20
```

Con un negativo, la tasa de falsos positivos no se puede medir. Un matiz: tras
normalizar, **P13 pasa a `no_divergence_detected`** (§7) y P15 también (DEC-016,
ver addendum), así que hay cuatro casos donde el sistema no debe alertar. Solo
P20 es un control negativo puro (`truth = supported`); los otros tres son claims
falsos sin divergencia contextual (`truth = contradicted`). La distinción vive en
el eje `truth`, no en una clase nueva.

### D4 — Vocabulario

| Columna | Antes | Después |
|---|---|---|
| `truth` | **12** valores distintos | 3: `contradicted` 9, `supported` 6, `mixed` 5 |
| `context` | valores dobles (`not_applicable / simple ranking contradiction`) | 2: `divergence_detected` 16, `no_divergence_detected` 4 |
| `clase` | compuestos: `2 + 3`, `4/7`, `1/3`, `CONTROL NEGATIVO` | primaria + secundarias separadas |
| `recuperabilidad` | 8 filas `A/B`, 1 `B/C` | `B` 11, `A` 8, `C` 1 |

Distribución de clase primaria tras normalizar:

```
other_observed           5    P05 P07 P08 P09 P17   (clases 6 y 7, fuera de tesis)
2_baseline_selection     4    P02 P03 P10 P11
3_absolute_vs_relative   3    P04 P14 P19
none                     3    P15 P16 P20
5_methodology_change     2    P06 P13
4_denominator            2    P12 P18
1_ranking_vs_value       1    P01
```

`ATENCIÓN` **Cinco de veinte caen en `other_observed`.** Las clases 6 y 7, que
se dejaron fuera de la tesis, son la categoría más frecuente del lote. La
adenda decía que la frecuencia decidiría si reabrir esa decisión. Este es el
dato; la decisión es de Mateo.

`ATENCIÓN` La clase canónica de la tesis, `1_ranking_vs_value`, aparece **una
vez**. El lote no está balanceado hacia el caso que da nombre al proyecto.

### D5 — Tiempos

`minutes_to_locate` y `minutes_to_extract` no existen como columnas en el
consolidado. Esta auditoría tampoco los rellena por caso: la consulta fue
paralela. Se añade `cronometrado_por` como campo obligatorio y se anota el reloj
de la fase.

### Defecto nuevo — `abstain_reason` también estaba sin controlar

La adenda solo señaló `truth` y `clase`. La columna `Posible abstención` tenía
**5 valores inventados** fuera del enum de R02 §11 más prosa libre. Tras
mapearlos al más cercano, quedan como **candidatos a extender el enum**:

```
METRIC_AMBIGUOUS            4 casos   P02 P14 P15 P19    "¿valor o volumen?", "¿euros o % PIB?",
                                                         "¿tasa o número?", "¿líder en qué?"
SCOPE_NOT_RESOLVABLE        1 caso    P07                ámbito geográfico del claim
GROUPS_NOT_HOMOGENEOUS      1 caso    P17                subgrupos con tendencias opuestas
SAMPLE_NOT_REPRESENTATIVE   1 caso    P18                universo de la muestra ≠ universo del claim
```

R02 §11 dice que los motivos reales de abstención *se descubren en el piloto*.
**`METRIC_AMBIGUOUS` aparece en uno de cada cinco casos.** Hoy se mapea a
`SOURCE_VERSION_AMBIGUOUS`, que no significa lo mismo. Es el candidato más
fuerte a entrar en el enum.

---

## 7. Correcciones de etiqueta que cambian el sentido del caso

Tres casos donde normalizar no fue solo limpiar sintaxis.

**P13 — de `divergence_detected` a `no_divergence_detected`.** La propia
columna de notas del Excel dice que el propósito del caso es *"evitar que
VERITAI genere falsos positivos simplemente porque detectó cambio de
metodología"*. AEMET recalculó la serie desde 1961: la comparabilidad se
mantiene y **no hay divergencia real**. Etiquetarlo `divergence_detected`
convierte el control en un falso positivo. Es el caso más importante del lote
para la tasa de falsos positivos y estaba etiquetado al revés.

**P15 y P16 — `clase = none` con el claim falso.** Cuando `context` es
`not_applicable` o `no_divergence_detected` porque el claim es simplemente falso
por aritmética, no hay clase de divergencia. Se pone `none`. Pero `none` es
también el valor del control negativo (P20). **El enum `clase` mezcla dos cosas
distintas**: "no hay distorsión porque el claim está bien" y "no hay distorsión
contextual porque el claim es falso sin más". Hay que separarlas.

**P17 — de `contradicted / mixed` a `mixed`, y no a `contradicted`.** El techo
del claim (*"hasta el 60%"*) se cumple en una ruta (−67,4% en Canarias); el
universal (*"todas las rutas"*) es falso porque el Mediterráneo Occidental sube
un 17%. Es genuinamente mixto.

---

## 8. Semántica de `Fecha contenido`

En 9 de 20 casos la fecha difiere de la del artículo del verificador, casi
siempre 1–5 días antes. Como en 18 de 20 la URL de contenido *es* el
verificador, la columna guarda unas veces la fecha del claim y otras la de la
verificación, sin decir cuál. No es un error de dato: es una columna con dos
significados. Para el lote crudo: `claim_date` y `verification_date` separadas,
o una sola con la semántica escrita en la cabecera.

---

## 9. Ficha por caso

Resumen. El detalle completo, con justificación de cada etiqueta y notas de las
dos fases, está en el CSV.

| ID | Alcance | truth | context | clase | recup | Primaria | Estado | Hallazgo clave |
|---|---|---|---|---|---|---|---|---|
| P01 | sí | mixed | divergence | 1_ranking_vs_value | B | no alcanzable | NEEDS_REVIEW | Claim cubre 4 índices, corpus documenta 1 |
| P02 | sí | supported | divergence | 2_baseline | A | portal | NEEDS_REVIEW | Sin span de primaria; okdiario erra unidades ×1000 |
| P03 | sí | supported | divergence | 2_baseline | A | portal | NEEDS_REVIEW | +5,03% debe ser +5,30%; claim = encuadre de Maldita |
| P04 | sí | contradicted | divergence | 3_abs_vs_rel | C | portada INE | NEEDS_REVIEW | URL no identifica tabla |
| P05 | sí | contradicted | divergence | other_observed | B | portada CIS | NEEDS_REVIEW | URL no identifica barómetro |
| P06 | sí | contradicted | divergence | 5_methodology | B | portal | parcial | Portal vivo, cifras exigen navegar |
| P07 | sí | contradicted | divergence | other_observed | B | no alcanzable | NEEDS_REVIEW | Servidor no responde |
| P08 | **no** | contradicted | divergence | other_observed | B | 403 | fuera_de_alcance | DEC-013. Informativo: con denominador completo, 10,1% |
| P09 | **no** | mixed | divergence | other_observed | B | 403 | fuera_de_alcance | DEC-013 |
| P10 | sí | supported | divergence | 2_baseline | A | página índice | NEEDS_REVIEW | `>20.000` y `~7.500` no son valores |
| P11 | sí | supported | divergence | 2_baseline | B | **PDF verificado** | NEEDS_REVIEW | 8.830 es S.L., total es 8.908 |
| P12 | sí | supported | divergence | 4_denominator | B | **PDF, cifras ≠** | NEEDS_REVIEW | Primaria da 22.414 / 12.432; nota `¥` explica el caso |
| P13 | sí | contradicted | **no_divergence** | 5_methodology | A | soporte parcial | NEEDS_REVIEW | Etiqueta corregida; Dato B sin fuente |
| P14 | sí | mixed | divergence | 3_abs_vs_rel | A | tablas + CSV | parcial | Cifras en la descarga |
| P15 | sí | contradicted | no_divergence | none | A | **API verificada** | **verificado** | ES 2,6 / EU 4,1 |
| P16 | sí | contradicted | no_divergence | none | A | **API verificada** | **verificado** | 2.645,2 / 1.192,7 |
| P17 | sí | mixed | divergence | other_observed | B | mapa + dataset | parcial | Cifras en el fichero mensual |
| P18 | sí | contradicted | divergence | 4_denominator | B | Cloudflare | NEEDS_REVIEW | Desafío JS |
| P19 | sí | mixed | divergence | 3_abs_vs_rel | B | portada INE | NEEDS_REVIEW | URL no identifica tabla |
| P20 | sí | supported | no_divergence | none | A | **HTML verificado** | **verificado** | Control negativo; 3,4% / 3,8% literales |

---

## 10. Limitaciones de esta auditoría

- **No mide recuperabilidad.** Repetido a propósito.
- **El fetcher no siempre devuelve citas literales.** Para varios artículos de
  verificadores (P04, P10) confirmó la presencia de cifras enumerando las que
  se le pidieron, sin citar la frase. Esas confirmaciones son débiles y así se
  marcan. Para capturar `raw_value_span` con rigor hace falta el texto crudo de
  la página, no un resumen.
- **El fetcher marca como "inyección" su propio prompt.** En 7 respuestas
  reportó una instrucción dirigida a una IA y en las que dio detalle, citaba el
  prompt de la auditoría. Se descartan como artefacto. Una posible instrucción
  oculta en `cis.es` no se pudo confirmar ni descartar.
- **Tiempo por caso no medido.** Consulta paralela. Para el lote crudo, en
  serie.
- **Cinco fuentes no alcanzables** desde esta herramienta y esta red. Que un
  humano las abra no está en duda; que VERITAI pueda, sí.
- **Las 18 URLs de verificadores no se verificaron a fondo.** Se comprobó que
  existen y el título; los 403 de Newtral impidieron más. No cambia nada: son
  secundarias y el hallazgo D1 no depende de su contenido.

---

## 11. Preguntas que abre

Ninguna la decide esta auditoría. Registradas en
[`../docs/PREGUNTAS-ABIERTAS.md`](../docs/PREGUNTAS-ABIERTAS.md).

1. **¿Extender el enum de abstención con `METRIC_AMBIGUOUS`?** Uno de cada
   cinco casos lo necesita.
2. **¿Separar en `clase` el control negativo del "falso sin divergencia"?**
   P15/P16 contra P20.
3. **¿Reabrir las clases 6 y 7?** `other_observed` es la categoría más
   frecuente del lote (5 de 20). La adenda dijo que la frecuencia decidiría.
4. **¿Cómo se corrigen P03, P11, P12 y P13?** El Excel es el dato de partida y
   no se toca. ¿Una v2 del Excel, o el CSV normalizado pasa a ser la fuente de
   verdad?
5. **¿Qué hace VERITAI con los publicadores que bloquean fetchers?** Antes del
   primer conector.

---

## 12. Reproducir

```bash
python research/scripts/auditar_aritmetica.py      # sale 1 mientras P03 no se corrija
python research/scripts/normalizar_a_enums.py      # regenera el CSV, sale 1 si hay valor fuera de enum
```

Requiere `openpyxl` (lectura del Excel) y `pypdf` (los dos PDFs de la Fase B).
Los PDFs descargados no se versionan: son artefactos de organismos públicos y
se recuperan con las URLs del CSV.

---

## Addendum 2026-09-25 — Revisión de Mateo

El informe de arriba es lo que la auditoría encontró el 2026-09-24. Esto es lo
que Mateo decidió al revisarlo, y lo que cambió en el CSV como consecuencia.
Las decisiones completas están en [`../docs/DECISIONES.md`](../docs/DECISIONES.md).

| Pregunta | Decisión | Efecto en el CSV |
|---|---|---|
| P-10 | **`METRIC_AMBIGUOUS` entra en el enum** (DEC-015) | P02, P14, P15, P19: `abstain_reason` pasa de `SOURCE_VERSION_AMBIGUOUS` a `METRIC_AMBIGUOUS`. Dejan de ser "candidatos" en §6 |
| P-11 | **No se añade clase.** `truth` y `context` son ejes independientes (DEC-016) | **P15: `context` corregido de `not_applicable` a `no_divergence_detected`.** La propuesta de §7 de "separar" queda revocada: la separación ya existe en `truth` |
| P-12 | **Aplazada al lote crudo.** Desglose de los 5 `other_observed` en P-12 | Sin cambio. Nota: "5 de 20" mezclaba DEC-013 con taxonomía; el dato en alcance es 3 de 18 |
| P-13 | **El CSV es la fuente de verdad; el Excel queda congelado** con sus 4 errores (DEC-017) | Sin cambio. Los errores de §4 se quedan como hallazgo |
| P-14 | **No se evaden protecciones anti-bot. Nunca** (DEC-018) | Sin cambio en datos. El `curl -I` con user-agent de Chrome de §5.1 fue diagnóstico y no se repite: un 403 al agente identificado ya es la respuesta |
| — | **La métrica de la puerta se parte en dos**; decide la del agente (DEC-019) | Sin cambio aquí. Aplica al lote crudo |
| — | **P-15 abierta:** la clase canónica aparece 1 vez en 20 | Registrado antes de la TAREA 2 |

Tabla cruzada `truth × context` tras la corrección, que es lo que hace medible
la tasa de falsos positivos:

```
contradicted  x  divergence_detected        6    P04 P05 P06 P07 P08 P18
contradicted  x  no_divergence_detected     3    P13 P15 P16
supported     x  divergence_detected        5    P02 P03 P10 P11 P12     <- "verdadero pero"
supported     x  no_divergence_detected     1    P20                     <- control negativo
mixed         x  divergence_detected        5    P01 P09 P14 P17 P19
```

La fila `no_divergence_detected` (4 casos) es donde el sistema no debe alertar.
`truth` dice por qué en cada uno.
