# PILOT-FAILURES — dónde falló y qué implica

**Fecha:** 2026-09-25 · **Tarea:** 3 de 3

> Catálogo de modos de fallo observados en las dos tareas, con los casos que
> los producen y **qué le exigen al sistema**. De aquí salen los *hard gates*
> de R02 §11 y el enum de abstención definitivo. No hay fallo sin caso.

---

## 1. Fallos de recuperación (los que miden la métrica)

### 1.1 La primaria citada no existe como dato publicado

| Caso | Lo que dice el claim | Lo que hay |
|---|---|---|
| C22 | "según datos del INE a partir de la EPA del primer trimestre de 2026", tasa de abandono por CCAA | El INE no publica esa tasa trimestral: 112 operaciones, 1.039 tablas de la EPA, tablas anuales 69786/71120/12543 revisadas. Solo derivable de microdatos |
| C24 | "Informe de Tendencias de Viaje 2026 de Booking.com" | No está en el newsroom del emisor; cinco medios, mismo texto, sin enlace ni muestra |
| C27 | "encuesta del CIEES" | La encuestadora entrega resultados por WhatsApp y redes; ningún documento público |

**Implica:** `PRIMARY_SOURCE_NOT_FOUND` tiene que distinguir *emisor no
identificado* de *emisor identificado que no publica el valor*. El segundo es
un hallazgo sobre el emisor, reutilizable: la tabla de emisores de R02 §6
debería llevar una columna "publica el valor que la prensa le atribuye".

### 1.2 La edición anterior no está enlazada, o no existe

| Caso | Qué pasó |
|---|---|
| C10 | Ranking fiscal comercial: edición vigente sí, la anterior sin publicar |
| C25 | Barómetro Europ Assistance/Ipsos: la edición 2025 existe (blog, prensa) pero el PDF no está enlazado (dos URL probables → 404); y la pregunta del 55% es **nueva en 2026** |

**Implica:** `PREVIOUS_EDITION_NOT_FOUND` con dos subtipos: *no enlazada* y
*pregunta/indicador nuevo*. El segundo no es recuperable por nadie y debe
abstener sin coste.

### 1.3 El publicador rechaza al agente

| Caso | Dominio | Respuesta | Regla |
|---|---|---|---|
| C09 | `saily.com` | 403 al fetcher y a curl | DEC-018 |
| C30, C31 | `gob.pe` (INEI) | **418** al fetcher, 200 a curl | DEC-021: el primer rechazo cierra |
| C18–C20 | `interior.gob.es` (PDF) | 403 | el **mismo ministerio** publica el PDF y las tablas PC-Axis en su Portal Estadístico: vía dataset, no rodeo |
| C02 | `inclusion.gob.es` | bloqueo | nota idéntica en La Moncloa (emisor oficial) |

**Implica:** el *hard gate* "responde al agente identificado" entra como
filtro de selección de emisores, antes de escribir un conector. Y el sistema
guarda el código HTTP del primer contacto como dato del caso.

### 1.4 Formato hostil: no apareció

0 de 31 con `scan`. Los 16 PDF se extrajeron sin OCR (`pypdf`). DEC-022: es
un hallazgo, no un fallo. Lo que sí apareció en su lugar es 1.1: el fallo de
nivel 5 es "no hay documento", no "el documento es ilegible".

---

## 2. Fallos de verdad y de contexto (los que miden al sistema)

### 2.1 El claim lo contradice su propia primaria, sin que dispare ningún test

| Caso | Claim | Primaria |
|---|---|---|
| C17 | "La tasa de paro juvenil escala hasta el 24,5% en el segundo trimestre" | La EPA 2T2026 da 23,77% y **baja** 0,77 pp; 24,5% es la del 1T. El cuerpo del propio artículo lo dice bien; el titular, no |
| C28 | "Por primera vez, Ecuador tiene cifras de la población LGBTIQ+" | El boletín del INEC recuerda que el Censo 2022 ya dio el 2,4% y que hubo un estudio de caso en 2013 |

**Implica:** el eje `truth` tiene que poder ser `contradicted` con `context =
no_divergence_detected` (DEC-016). Son falsos sin divergencia: fact-checking
clásico, fuera del objeto de la tesis pero dentro de lo que el sistema ve.
La cubeta `claim_falso` existe por esto.

### 2.2 Revisiones de base que cambian la comparación

| Caso | Qué pasó |
|---|---|
| C18 | El Balance de Criminalidad 2T2026 compara contra un 2025 **revisado** (1.211.083) distinto del publicado en 2025 (1.212.268). El +0,5% sería +0,4% contra la cifra original |
| C29 | El Índice de Paz Global publica "España sube 4 puestos" contra el rank 2025 **revisado**; la prensa resta 25 → 27 = "cae 2" contra el publicado |
| C21 | Moncloa compara España 2025 con la UE 2024 ("se reduce a 3,4 puntos"); con años emparejados la brecha subió de 3,4 a 3,7 |

**Implica:** guardar la edición anterior no basta; hay que guardar **qué
versión** de la edición anterior, y decidir explícitamente contra cuál se
compara. Es el argumento más fuerte a favor de la familia "comparación de
base" como clase del prototipo (FINDINGS §5, opción B) y de un campo
`base_version` en el EvidenceBundle.

### 2.3 El titular no está en el cuerpo, o dice otra cosa que la primaria

| Caso | Qué pasó |
|---|---|
| C24 | Titular 60%, cuerpo 59% con otro enunciado |
| C25 | "Elegirá España como destino" cuando la pregunta es "vacaciones ideales"; el destino planeado da 69%, no 55% |
| C31 | "Sube en 6,8%" cuando 6,8% es el **nivel** de la tasa (+0,2 pp) |
| C19 | "Seis veces más" = cociente de dos tasas (2,9/0,5) sobre una base casi nula, y el comparador incluye al comparado |

**Implica:** la unidad de análisis es el **titular** (así se etiquetó); el
sistema debe extraer el claim del titular y contrastarlo con el cuerpo como
segunda fuente, porque el cuerpo a veces corrige al titular.

### 2.4 Ambigüedad de métrica

`METRIC_AMBIGUOUS` en 4 casos del auditado (P02 unidades, P05, P07, P17) y
cerca en C25 y C31. **Implica:** el enum lo lleva (DEC-015) y el prototipo
tiene que abstener en él antes de calcular nada.

---

## 3. Fallos del corpus original (TAREA 1)

Cuatro errores de transcripción en el Excel, documentados como hallazgo y
**no corregidos en el Excel** (DEC-017; el CSV es la fuente de verdad):

| Caso | Error |
|---|---|
| P03 | +5,03 → +5,30 (cálculo) |
| P11 | 8.830 es una subcategoría (S.L.), no el total (8.908) |
| P12 | Las cifras no salen de la primaria citada (ésta da 22.414 y 12.432) |
| P13 | Dato B sin fuente; y estaba etiquetado al revés |

**Implica:** un corpus hecho a mano lleva ~4 errores por 20 filas. El
`raw_value_span` de la primaria por cada número no es burocracia: es lo que
los detecta.

---

## 4. Fallos de herramienta, y cómo se detectaron

| Caso | Fallo | Detección |
|---|---|---|
| C30 | El buscador devolvió un PDF del INEI con el **mismo título** que el informe buscado: edición de mayo de **2003** | Fecha en la primera página; se llegó al informe correcto por la colección de `gob.pe` |
| C07 | La API DataMapper del FMI mezcla agregados (MAE, APQ…) con países en el ranking | Filtrado con `/api/v1/countries`; sin eso, el puesto de España sale mal |
| C11 | El filtro `tv=70:9003` del INE devolvía Castilla y León en vez del total nacional | Se seleccionó "Nacional" por nombre, no por código |
| C14 | El sufijo `_MM` de los PDF del INEGI es el mes de **publicación**, no el de referencia | Comparando `_08` (julio) con `_09` (agosto) |
| C16 | Las tablas antiguas de la EPA terminan en el cambio de base (4247 acaba en 2023-T4) | Se usaron 65334/65218 para 2026 |
| varios | El fetcher reporta su propio prompt como "inyección" | Artefacto; se ignoró |
| varios | El fetcher no lee PDF | `pypdf` en local; `curl` para descargar |
| C22 | Nota errónea en el cronómetro ("tope casi agotado" con 5,2 min) | Corrección como comentario en el log append-only |

**Implica:** cada conector necesita un test de identidad (¿es la edición que
creo?) y de ámbito (¿es el total nacional?). "Mismo título" no es "misma
edición".

---

## 5. Fallos del método, corregidos sobre la marcha

| Fallo | Corrección | Dónde |
|---|---|---|
| La vía de descubrimiento no se registró por candidato | Reconstruida del transcript, 38/38 | `reconstruir_descubrimiento.py`, DEC-020 |
| La cuota por cubetas fija la métrica del lote por construcción | La puerta se mide sobre todos los admitidos | DEC-020 |
| Probé `curl` tras un fallo del fetcher: zona gris | El primer rechazo cierra el caso; C30 y C31 salen | DEC-021 |
| Seis candidatos son hermanos por criba, no sorteos independientes | Declarado; n efectivo 25 recomputado | FINDINGS §3.2 |
| El plan no tenía cubeta para "bloqueado" ni para "claim falso" | Dos cubetas sin objetivo, ratificadas | COLECCION §2 |
| `pilot-crudo-20.csv` iba a tener 31 filas | Dividido en lote (23) y trabajados (31) | TAREA 2 |
| Predicción 1 (30–50%) demasiado pesimista | Registrada como fallida; causa en FINDINGS §3.1 | FINDINGS §8 |

---

## 6. Lo que estos fallos piden del prototipo (Puerta 2)

Ordenado por lo que más casos explica:

1. **`base_version` en el EvidenceBundle** y comparación explícita contra
   publicado vs revisado (2.2: C18, C21, C29).
2. **Abstención con subtipos** para `PRIMARY_SOURCE_NOT_FOUND` y
   `PREVIOUS_EDITION_NOT_FOUND` (1.1, 1.2).
3. **Código HTTP del primer contacto** como dato del caso y filtro de
   emisores (1.3).
4. **Tests de identidad y ámbito** en cada conector (4).
5. **Titular como claim, cuerpo como segunda fuente** (2.3).
6. **`METRIC_AMBIGUOUS` antes de calcular** (2.4).
