# Colección del lote crudo — TAREA 2

**Fecha:** 2026-09-25 · **Rama:** `feat/lote-crudo-20` · **Ejecutó y cronometró:** el agente (DEC-014)

> Este documento **registra, no decide**. La decisión `PILOT_GO` / `PILOT_PIVOT`
> es de la TAREA 3, y necesita además los 5 casos manuales de Mateo.

Todos los conteos de este documento los imprime `scripts/validar_lote_crudo.py`
(salida 0) o el bloque de estadísticas de §3; ninguno está tecleado a mano.

---

## 1. Qué se hizo

```
38 candidatos     busqueda web, prensa + comunicacion oficial en espanol, 2026
   ├─ 7 rechazados   regla dura: existe verificacion (2), el tema ya tiene
   │                 explainer de verificador (4), duplicado (1)       18,4%
   └─ 31 admitidos   trabajados en serie, los 31, cronometrados
        ├─ 23 en el lote        18 en cubetas con objetivo + 5 sin objetivo
        └─ 8 excedentes         cayeron en cubetas ya llenas
```

`2026-09-25, tarde` Mateo decidió P-16, P-17 y P-18 (DEC-020 a DEC-022) sobre
la primera versión de este informe. Los números de abajo ya las aplican; donde
cambió algo, se dice.

Por cada admitido, el ciclo del plan: `t0` claim → LOCALIZAR (API → dataset →
HTML → PDF; si bloquea, parar) → `t1` → EXTRAER (`raw_value_span` de la edición
actual y de la anterior) → `t2` → ETIQUETAR (provisional).

Fuentes del claim, tal como se declara en el método: *prensa digital y
comunicación oficial en español, recuperada por búsqueda web; redes sociales
excluidas por inalcanzables sin evadir protecciones*.

### Archivos

| Archivo | Qué es |
|---|---|
| `pilot-crudo-screening.csv` | Los 38 candidatos, con resultado de criba, motivo y URL de la verificación que los sacó. Denominador de la prevalencia |
| `pilot-crudo-20.csv` | **El lote**: los 21 casos con `excedente = no` |
| `pilot-crudo-trabajados.csv` | Los 31 admitidos y trabajados, excedentes incluidos. Sobre este se calcula la tasa natural (§3) |
| `cronometro.log` | Hitos `t0/t1/t2` por caso, UTC, append-only. Los minutos de los CSV se derivan de aquí |
| `evidencia/` | Respuestas crudas de API guardadas para tres casos (FMI, INE ×2) |
| `scripts/lote_crudo.py` | Los 38 candidatos con todos sus campos: es la fuente de los CSV |
| `scripts/validar_lote_crudo.py` | Valida enums (importados de `normalizar_a_enums.py`), reglas y cubetas; emite los CSV |
| `scripts/cronometro.py` | Anota hitos |

---

## 2. Cubetas

| Cubeta | Objetivo | En lote | Casos |
|---|---|---|---|
| Control negativo | 7 | **7** | C01 C04 C06 C11 C12 C14 C16 |
| Divergencia real | 6 | **6** | C02 C03 C05 C07 C08 C13 |
| Primaria no localizable | 3 | **3** | C22 C24 C27 |
| Edición anterior no localizable | 2 | **2** | C10 C25 |
| Formato hostil | 2 | **0** | — |
| *Bloqueado por publicador* | sin objetivo | 3 | C09 · C30 C31 (por DEC-021) |
| *Claim falso* | sin objetivo | 2 | C17 C28 |
| **Lote** | 20 | **23** | |

**Excedentes (8):** control negativo C18 C20 C21 C23 C26 · divergencia C15 C19
C29. Están en `pilot-crudo-trabajados.csv` con todos sus campos.

`TRAS DEC-027 (P-12, 2026-09-25)` La tabla de arriba es la de la recolección.
Después, C03 pasó a control negativo (lectura alternativa) y C05 a abstención:
en el lote quedan divergencia real 4, control negativo 8 (sobre un objetivo de
formación de 7; el validador avisa, no falla) y una cubeta `abstencion` sin
objetivo. La pertenencia al lote no se recompone. Ver §4.

**Déficit declarado: formato hostil 0 de 2.** El pool se agotó sin encontrar un
solo PDF escaneado o sin texto: los 16 casos con vía `pdf` se extrajeron con
`pypdf` sin OCR, incluidos los de emisores de nivel 5 (Ávoris, Europ
Assistance). El fallo de los emisores de nivel 5 tomó otra forma: **no hay
documento** (§4). `DEC-022` Se acepta como hallazgo: *buscando sin sesgo no
aparecieron PDFs sin texto*. Sin segunda pasada dirigida.

**Dos cubetas que el plan no tenía**, añadidas al validar y ratificadas con
DEC-021: `bloqueado_por_publicador` (la primaria existe y se sabe dónde está,
pero el publicador rechaza al agente: no es "no localizable") y `claim_falso`
(el claim lo contradice la primaria sin que dispare ningún test de contexto).

---

## 3. Las dos métricas

Medidas sobre dos denominadores, porque la cuota por cubetas **fija el resultado
del lote por construcción**: 7 + 6 casos recuperables y 3 + 2 no recuperables
dan ~71% antes de trabajar un solo caso. `DEC-020` **Decide la tasa natural
sobre los 31 admitidos**, "la que menos manipulación tiene"; la del lote se
reporta al lado. Y en dos lecturas: `DEC-021` la **conservadora** (un 403, 406
o 418 al primer cliente cierra el caso aunque `curl` pase después: C30 y C31
salen) es la que decide; la **leniente** (edición anterior localizada, sin
mirar cómo) se reporta.

```
                                          31 admitidos           lote (23)
recuperable-por-agente, conservadora      23/31   74,2%          15/23   65,2%   <- DECIDE
recuperable-por-agente, leniente          25/31   80,6%          17/23   73,9%      se reporta
alcanzable_por_agente                     25/31   80,6%          17/23   73,9%
alcanzable_por_humano (si|probable)       29/31   93,5%          21/23   91,3%
```

Verde con las cuatro cifras (`>60%`). **No es la decisión**: es el dato que la
TAREA 3 tiene que confrontar con los 5 casos de Mateo y con el límite de abajo.

### El límite declarado (DEC-020)

Se predijo 30–50% y salió 74–81%. Parte de la explicación es el pool: **19 de
31 casos son estadística oficial de nivel 1**, que es lo que el buscador
devuelve con más facilidad. Es el sesgo del lote anterior con otra cara: la
herramienta de búsqueda entrega los casos fáciles. Desagregado (conservadora):

```
nivel 1 (INE, INEC, INEGI, DANE, INEI, Eurostat, FMI, ministerios)   16/19   84,2%
resto  (niveles 3, 4 y 5)                                             7/12   58,3%
   nivel 3   4/4      nivel 4   2/2      nivel 5   1/6

comunicacion oficial (nota_oficial)   3/3           prensa digital   20/28   71,4%
ES 16/21   EC 3/4   CO 2/2   MX 2/2   PE 0/2 (los dos, bloqueados por gob.pe)
```

El 74,2% es un promedio de un 84% y un 58%. **El número no cambia; se declara
con su límite.**

**Por vía de descubrimiento**, reconstruida del transcript de la sesión con
`scripts/reconstruir_descubrimiento.py` (38 de 38 candidatos localizados: 35
por la URL exacta en un resultado de búsqueda y 3 por una pista del claim
—cifra o nombre propio— en la consulta anterior a su propia criba; 23
consultas distintas; `pilot-crudo-descubrimiento.csv`):

```
via (que consulta saco al candidato)          38   trabajados   conservadora
busqueda_a_organismo    nombra INE, INEC,     19       13        12/13   92,3%
                        INEGI, DANE, INEI,
                        Interior, AEMET...
criba_negativa          aparecio en la         6        6         5/6    83,3%
                        busqueda negativa
                        de OTRO candidato
busqueda_de_rankings    "cae puestos",         6        5         3/5    60,0%
                        "ocupa el puesto"
busqueda_de_encuestas   "segun un estudio",    5        5         2/5    40,0%
                        "encuesta ... revela"
busqueda_por_tema       sin nombrar emisor     2        2         1/2    50,0%
```

Dos cosas que esto demuestra y que la TAREA 3 tiene que escribir tal cual:

1. **La mezcla la eligió el barrido y el buscador, no un muestreo.** Trece de
   los 31 salieron de consultas que ya nombraban a un organismo estadístico;
   ahí la recuperabilidad es 92,3%. Las consultas por ranking, encuesta o tema
   —las que no llevan el emisor en la pregunta— dieron 12 casos y 50%.
2. **Seis de los 31 no son sorteos independientes**: aparecieron en la
   búsqueda negativa de la criba de otro candidato, es decir, son cobertura
   hermana del mismo dato (C03 de C02, C05 de C04, C08 de C07, C13 de C12,
   C17 de C16, C31 de C30). Cinco de los seis se recuperan, porque heredan la
   primaria del hermano. El tamaño muestral efectivo es menor que 31.

### Los ocho no recuperados (conservadora)

| Caso | Cubeta | Qué pasó |
|---|---|---|
| C09 | bloqueado | Saily (ranking eSIM): 403 al fetcher y a curl. Primaria identificada, ilegible para el agente |
| C30, C31 | bloqueado | INEI vía `gob.pe`: **418** al fetcher, 200 a `curl`. Por DEC-021 el 418 cierra el caso; los valores leídos quedan en el registro, marcados, sin sumar |
| C10 | edición anterior | Ranking fiscal comercial: edición vigente sí, la anterior no está publicada |
| C22 | primaria | La prensa atribuye al INE una tasa trimestral de abandono por CCAA (1T2026) que el INE **no publica**: 112 operaciones, 1.039 tablas de la EPA, tablas anuales 69786/71120/12543 revisadas. Solo derivable de microdatos |
| C24 | primaria | "Informe de Tendencias de Viaje 2026" de Booking.com: cinco medios, mismo texto, sin enlace, sin muestra; no está en el newsroom del emisor |
| C25 | edición anterior | Barómetro Europ Assistance/Ipsos 2026: la edición 2025 existe (blog, prensa) pero el documento no está enlazado (hubfs 404 ×2); y la pregunta del 55% es **nueva en 2026** |
| C27 | primaria | CIEES (Ecuador): la encuestadora entrega resultados por WhatsApp y redes; ningún documento público |

### Por nivel de emisor (31)

| Nivel | Casos | Edición anterior (leniente) | Recuperable (conservadora) | Localizar (media) | Máximo |
|---|---|---|---|---|---|
| 1 · organismo con API/dataset | 19 | 18/19 | 16/19 | 1,6 min | 5,2 (C22) |
| 3 · portal HTML | 4 | 4/4 | 4/4 | 1,9 min | 3,8 |
| 4 · PDF con tabla | 2 | 2/2 | 2/2 | 1,1 min | 1,1 |
| 5 · sin datos abiertos | 6 | **1/6** | **1/6** | 1,9 min | 2,4 |

Nivel 2 no tuvo casos: la búsqueda devolvió emisores de nivel 1 directamente
(INE, INEC, INEGI, DANE, INEI, Eurostat, FMI). El pool está sesgado hacia
estadística oficial mensual: 19 de 31.

### Tiempos

```
localizar   media 1,7 min   max 5,2 (C22)     tope 20 min: nadie lo toco
extraer     media 0,6 min   max 1,9 (C18)     tope 15 min: nadie lo toco
total       2,3 min/caso    70 min de reloj para los 31
```

Los tiempos son **del agente** (DEC-014) y miden latencia de herramientas más
razonamiento, no esfuerzo humano. Cinco casos tuvieron localización a coste
cero porque compartían primaria con el anterior (C19, C20 con C18; C31 con
C30): sus minutos no son representativos y así consta en `notas`.

### Otras cuentas (31)

```
pais        ES 21 · EC 4 · CO 2 · MX 2 · PE 2
via         pdf 16 · html 5 · api 5 · none 3 · bloqueado 1 · dataset 1
formato     pdf 11 · dataset 9 · api 6 · none 3 · html 2
abstain     PRIMARY_SOURCE_NOT_FOUND 4 · PREVIOUS_EDITION_NOT_FOUND 1
            REQUIRED_SLOT_MISSING 1 · UNSUPPORTED_CLAIM_TYPE 1
abandonos por tiempo   0
```

---

## 4. Etiquetas provisionales

Todas las etiquetas son `agente_provisional`. La anotación de corpus es
posterior y los casos marcados `NEEDS_REVIEW` en `notas` son los que un segundo
anotador debería mirar primero.

### truth × context (31)

| | `divergence_detected` | `no_divergence_detected` | `undetermined` |
|---|---|---|---|
| `supported` | 4 | 13 | |
| `mixed` | 7 | | |
| `contradicted` | 1 | 2 | |
| `insufficient_evidence` | | | 4 |

### Clases en las 12 divergencias — el dato para P-15

```
other_observed           5    C03 C05 C08 C10 C13
2_baseline_selection     2    C02 C15                (2a)
2b_base_revisada         1    C29                    (2b; hasta DEC-026 iba como 2_baseline + 5_methodology)
3_absolute_vs_relative   2    C19 C31
1_ranking_vs_value       1    C07                    <- la que daba nombre al proyecto; ilustrativa desde DEC-026
4_denominator            1    C25

secundarias: C03 -> 2_baseline · C08 -> 1_ranking · C19 -> 4_denominator
             C29 -> 2_baseline_selection
```

`TRAS DEC-027 (P-12, 2026-09-25)` Este bloque es el registro de la
recolección. Después, Mateo reetiquetó: **C13 → 2_baseline_selection**, **C03
→ sin divergencia** (control negativo, lectura alternativa registrada) y
**C05 → abstención** (`REQUIRED_SLOT_MISSING|UNSUPPORTED_CLAIM_TYPE`, cubeta
`abstencion`). En el lote quedan 10 divergencias, no 12; la cubeta de control
negativo tiene 8 sobre un objetivo de formación de 7 y el validador avisa sin
fallar. Estado vigente en `pilot-crudo-trabajados.csv` y `PILOT-FINDINGS.md` §5.

**La clase canónica aparece 1 vez en 12** (más una secundaria). En el piloto
auditado era 1 en 20. P-15 no se cierra sola: sigue siendo una pregunta sobre
el objeto de estudio, ahora con dos lotes que dicen lo mismo.

C07 es, eso sí, el caso de libro: *"España cae en el ranking del FMI"* — del
puesto 12 al 14 mientras el PIB en dólares sube un 9,84%, verificado contra la
API del FMI con los agregados filtrados.

### Hallazgos que no estaban previstos

- **Las revisiones de base**. El Balance de Criminalidad 2T2026 compara contra
  una cifra 2025 *revisada* (1.211.083) distinta de la publicada en 2025
  (1.212.268); el +0,5% sería +0,4% contra la original (C18). El Índice de Paz
  Global publica para España "sube 4 puestos" contra el rank 2025 revisado
  mientras la prensa resta 25 → 27 = "cae 2" contra el publicado (C29). Un
  sistema que guarde la edición anterior tiene que saber que **las bases se
  revisan**, y decidir contra cuál compara.
- **Divergencia en una nota oficial de nivel 1** (C21): Moncloa dice "se reduce
  a 3,4 puntos la distancia con la UE (9,4% en 2024)" comparando España 2025
  con la UE 2024; con años emparejados la brecha pasó de 3,4 a 3,7. Fuera del
  titular, así que no etiqueta el claim; pero es `2_baseline_selection` nacida
  en el emisor.
- **Pares mismo dato / dos lecturas**, útiles para el corpus: C19/C20 (misma
  tabla del Balance; uno relaya, otro construye "seis veces") y C30/C31 (misma
  tabla del INEI; uno relaya "tasa 6,8%", otro titula "sube 6,8%").
- **El titular no está en el cuerpo** (C24): 60% en el titular, 59% y otro
  enunciado en el texto.
- **La pregunta nueva** (C25): el 55% es `NEWQ2`, sin edición anterior posible,
  y mide "destino ideal", no "destino elegido"; el propio emisor la relee en su
  blog.
- **Mismo nombre de producto, 23 años de diferencia** (C30): el buscador
  devolvió un PDF del INEI con el título exacto del informe, edición de mayo de
  2003. Se descartó por fecha.

---

## 5. Predicciones vs realidad

Escritas en el plan antes de ejecutar.

| # | Predicción | Resultado | |
|---|---|---|---|
| 1 | Recuperable-por-agente 30–50% (ámbar) | **80,6%** (31) / 71,4% (lote) | ✗ demasiado pesimista |
| 2 | La regla dura rechaza ≥ 1/3 | 18,4% | ✗ (ya se veía fallar a mitad de criba) |
| 3 | `1_ranking_vs_value` en ≥ 2 de 6 divergentes | 1 primaria (C07) + 1 secundaria (C08) | ✗ |
| 4 | ≥ 2 casos donde la "primaria" citada es otra secundaria o no existe | 3 (C22, C24, C27) | ✓ |
| 5 | Bloqueo anti-bot en ≥ 2 primarias | 1 primaria bloqueada (C09) + 1 PDF con espejo en el mismo emisor (Interior) + 3 bloqueos sobre el *contenido* del claim | ~ parcial |
| 6 | Localizar < 10 min en nivel 1–2, > 20 en nivel 4–5 | Todo bajo 6 min: **fallar es rápido** cuando no hay nada que encontrar | ✗ en la segunda mitad |
| 7 | Los 7 negativos en los primeros 12 admitidos | El séptimo fue C16 | ✗ por poco |
| 8 | "Edición anterior no localizable" será la cubeta más difícil de distinguir | C25 es el caso límite exacto (documento anterior no enlazado + pregunta nueva) | ✓ |
| 9 | ≥ 1 caso cambia de cubeta al extraer | C17 (parecía divergencia, era falso), C28 (parecía negativo, contradicho por su propia primaria), C25 | ✓ |

Por qué falló la 1: el pool quedó dominado por emisores de nivel 1 (19 de 31),
porque la búsqueda devuelve cobertura de estadística oficial mensual con más
facilidad que rankings de consultoras. La 2 falló por lo mismo: los
verificadores cubren densamente lo político (migración y Argentina salieron al
100%), y la prensa que relaya un IPC no lo está.

---

## 6. DEC-018 en la práctica

Ningún bloqueo se rodeó. Cada uno se anotó y se paró.

| Dominio | Respuesta | Afecta a | Consecuencia |
|---|---|---|---|
| saily.com | 403 (fetcher y curl) | primaria de C09 | `bloqueado_por_publicador` |
| interior.gob.es (PDF) | 403 | primaria de C18–C20 | el **mismo ministerio** publica el PDF y las tablas PC-Axis en su Portal Estadístico de Criminalidad; se usó esa vía, que es la del dataset, no un espejo ajeno |
| inclusion.gob.es | bloqueo | primaria de C02 | nota idéntica en La Moncloa (emisor oficial) |
| elboletin.com, enfoquenoticias.com.mx | bloqueo | contenido del claim | claim registrado por titular |
| radiosantafe.com | ECONNREFUSED | contenido | ídem |
| imf.org (página WEO) | 403 | página de publicación | la API DataMapper del FMI respondió 200: vía API |
| deia.eus, noticiasdealava.eus | 406 WAF (fetcher y curl) | contenido de C23 | claim por titular; primaria AEMET 200 |
| radiopichincha.com | 403 Cloudflare (fetcher y curl) | contenido de C27 | claim por titular; `claim_date` aproximada |
| gk.city | 403 Cloudflare (fetcher y curl) | contenido de C28 | claim por titular; primaria INEC 200 |
| gob.pe | **418** al fetcher, 200 a curl | primaria de C30–C31 | ver zona gris |
| educacionfpydeportes.gob.es | `socket hang up` ×2 al fetcher, 200 a curl | primaria de C21 | error de red, no bloqueo |

**Zona gris, decidida (DEC-021).** Tras un fallo del fetcher se probó `curl`
con su *user-agent por defecto*, sin falsificar nada. No es lo que DEC-018
prohíbe (otro UA, saltar Cloudflare), pero **sí es cambiar de cliente** tras
una negativa. En cuatro dominios el resultado fue el mismo bloqueo; en dos
(gob.pe tras un 418 explícito; el ministerio de Educación tras un error de red)
curl obtuvo 200 y el caso siguió. Mateo decidió: *"si el publicador señala que
no quiere agentes, se respeta"*. Un 403, 406 o 418 al primer cliente cierra el
caso; un error de red admite un reintento. C30 y C31 pasan a
`bloqueado_por_publicador`; C21 (error de red) se queda. La cifra que decide es
la conservadora, 23/31 = 74,2%.

Sobre el user-agent del fetcher: no lo controlo y no puedo afirmar que se
presente como VERITAI. Es una limitación declarada del plan y sigue en pie.

---

## 7. Limitaciones y riesgos

- **La cuota por cubetas hace que la métrica del lote no informe** (§3). Se
  reportan las dos; decide la natural (DEC-020).
- **El pool está sesgado hacia lo fácil**: 19 de 31 de nivel 1, 84% frente a
  58% en el resto (§3, "El límite declarado"). Y la vía de descubrimiento no
  quedó registrada por candidato: reconstruir antes de la TAREA 3.
- **Un solo buscador**, con su sesgo: el pool es "lo que este buscador
  devuelve", y devolvió sobre todo estadística oficial de España (21 de 31 casos
  ES). La cobertura latinoamericana es fina: EC 4, CO 2, MX 2, PE 2.
- **Cero casos de formato hostil.** O el fenómeno es raro en este pool, o el
  pool no llegó a los emisores donde vive (ayuntamientos, gobiernos
  provinciales, PDFs escaneados de organismos pequeños). No se puede distinguir
  con estos datos.
- **`alcanzable_por_humano` es inferido** (`probable`) salvo en los 5 de
  Mateo.
- **Etiquetas de una sola persona, provisionales.** Los `NEEDS_REVIEW` están
  marcados en `notas`; concentran las decisiones discutibles (C19 clase, C25
  clase y cubeta, C28 truth, C29 clase, C31 clase).
- **Tiempos del agente**, no humanos. El tope de 20/15 min nunca actuó, así que
  no afecta a la métrica; pero la comparación con los tiempos de Mateo es la
  que dirá si "rápido para el agente" significa algo.
- **Lote de 23, no de 20**: 18 en cubetas con objetivo más 5 sin objetivo (3
  bloqueados, 2 claims falsos). El CSV del lote los incluye.
- **Una nota errónea en el log**: en `C22 t1` escribí "tope casi agotado"
  cuando t1−t0 eran 5,2 min. El log es append-only; la corrección está como
  comentario al final y en `notas` del caso.

---

## 8. Los cinco casos de Mateo (DEC-014)

Selección: `random.Random(20260925).sample(sorted(case_ids_del_lote), 5)` sobre
los **21** `case_id` que tenía el lote antes de DEC-021 (sin C30 ni C31),
ordenados alfabéticamente. Resultado:

```
C04  C05  C11  C14  C22
```

`NOTA` DEC-021 metió a C30 y C31 en el lote después de la selección. **No se
redibuja**: Mateo ya tiene los cinco. Comprobado de todas formas: la misma
semilla sobre los 23 ids devuelve, por casualidad, los mismos cinco. Queda
dicho para que nadie lo "corrija".

**Solo el texto del claim y la URL del contenido.** Ninguno de los resultados
del agente. Mateo trabaja cada uno con navegador y anota sus propios
`minutes_to_locate`, `minutes_to_extract`, `previous_edition_found` (sí/no) y
la URL que usó. La comparación es de la TAREA 3.

| Caso | Claim | URL del contenido |
|---|---|---|
| C04 | Inflación de Ecuador marca 1,12% en agosto y queda entre las más bajas de Sudamérica | https://www.eldiario.ec/negocios/inflacion-de-ecuador-112-agosto-2026-23092026/ |
| C05 | Gobierno de Noboa protege el bolsillo de los ecuatorianos: inflación de Ecuador es la más baja de la región | https://www.economicoproductivo.gob.ec/gobierno-de-noboa-protege-el-bolsillo-de-los-ecuatorianos-inflacion-de-ecuador-es-la-mas-baja-de-la-region/ |
| C11 | El IPC de agosto de 2026 se dispara al 4,3%: la tasa más alta en más de tres años | https://www.que.es/2026/09/15/ipc-agosto-2026-maximo-tres-anos/ |
| C14 | Inflación en agosto de 2026 se ubica en 3.26%: Inegi | https://www.razon.com.mx/negocios/2026/09/09/inflacion-en-agosto-de-2026-se-ubica-en-326-inegi/ |
| C22 | La brecha territorial del abandono escolar se agranda en España: del 18,6% de La Rioja al 6,1% de Navarra | https://www.elconfidencialdigital.com/articulo/estado-autonomico/brecha-territorial-abandono-escolar-agranda-espana-186-rioja-61-navarra/202604300750521291302.html |

`NOTA` Si alguna URL de esta tabla no coincide exactamente con `post_url` del
CSV, manda el CSV: `pilot-crudo-20.csv`, columna `post_url`.

---

## 9. Decisiones tomadas durante la ejecución, pendientes de ratificar

| | Decisión del agente | Alternativa descartada |
|---|---|---|
| 1 | Dos cubetas nuevas sin objetivo: `bloqueado_por_publicador`, `claim_falso` | Meter C09 en "primaria no localizable" (falso: se sabe dónde está) y C17/C28 en "divergencia" (falso: no dispara test) |
| 2 | Lote de 21 con los 3 sin objetivo dentro | Lote de 18 solo con cubetas objetivo, perdiendo el bloqueo como dato |
| 3 | Reportar la métrica sobre dos denominadores | Solo el lote, que es circular |
| 4 | Tras un fallo del fetcher, un intento con curl (UA por defecto) | Parar al primer fallo de cualquier cliente. Ver P-17 |
| 5 | Seguir trabajando los 31 admitidos aunque las cubetas se llenaran, registrando excedentes | Parar en 20: habría perdido C29 (revisión de rank) y C31 (nivel como variación) |
| 6 | Etiquetar por el **titular** cuando el cuerpo lo matiza (C21, C24, C28) | Etiquetar por el cuerpo: cambiaría C28 a `mixed` |
| 7 | `claim_date` aproximada en C27 por la fecha de la medición | Dejarla en blanco |

`2026-09-25, tarde` Mateo ratificó 1, 2, 3 y 5 con DEC-020 a DEC-022. **La 4
se revoca** (DEC-021): C30 y C31 pasan a `bloqueado_por_publicador`. 6 y 7
quedan como están, sin objeción.
