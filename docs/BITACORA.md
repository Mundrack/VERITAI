# Bitácora

Registro cronológico de lo que se hizo, con las verificaciones que lo respaldan.

> **Append-only.** Nunca se edita ni se borra una entrada pasada. Si algo
> resultó estar mal, se corrige en una entrada nueva y se dice qué lo cambió.

Formato de cada entrada: qué se hizo · qué se verificó · qué quedó pendiente.

---

## 2026-09-08 — Lectura del paquete y entorno Docker

### Qué se hizo

**Lectura completa del paquete** en el orden indicado: adenda, decisiones,
START-HERE, tesis, proyecto total, R02 y el Excel de 20 casos (7 hojas,
28 columnas, 20 filas).

**Repositorio git inicializado.** No existía. Primer commit con el paquete de
documentación y el `.gitignore` **antes** de que existiera ningún `.env`.

**Entorno de desarrollo local completo en Docker**, en la rama
`feat/entorno-docker-local`. 56 archivos:

- `docker-compose.yml` con cuatro servicios: `db` → `migrate` → `api` → `web`
- API FastAPI con separación `domain` / `application` / `infrastructure`
- Panel web en Vite + TypeScript sin framework, con i18n `es` + `en`
- Tres migraciones SQL planas, numeradas e inmutables
- Runner de migraciones propio (`scripts/migrate.py`)
- Generador de `.env` con contraseñas aleatorias (PowerShell y Bash)
- Carpeta `migracion-supabase-base-de-datos/` con 7 documentos y 2 scripts
- `CLAUDE.md` con las reglas permanentes — **marcado como propuesta**

### Qué se verificó

| Comprobación | Resultado |
|---|---|
| `docker compose up -d` levanta los 4 servicios | ✅ |
| `/health` responde con `base_de_datos: conectada` | ✅ |
| Migraciones idempotentes en la segunda pasada | ✅ `sin migraciones pendientes (3 ya aplicadas)` |
| `veritai_app` intenta `CREATE TABLE` | ✅ `ERROR: permission denied for schema veritai` |
| Escribir, `docker compose down`, `up`, leer | ✅ el dato sobrevivió |
| Roles `anon` / `authenticated` / `service_role` en local | ✅ `service_role` con `bypassrls` |
| `verificar-compatibilidad.sql` | ✅ 0 filas en los bloques bloqueantes |
| `pytest` | ✅ 5 passed |
| `ruff check` | ✅ All checks passed |
| `tsc --noEmit` | ✅ sin errores |
| Vite sirve y transforma `main.ts` | ✅ HTTP 200, `VITE_API_BASE_URL` inyectada |
| La contraseña generada no aparece en el repositorio | ✅ `git grep` vacío |
| `.env` rastreado por git | ✅ no lo está |

### Incidencias resueltas

**Puerto 5432 ocupado.** El primer `docker compose up -d` falló:
`bind: An attempt was made to access a socket in a way forbidden by its access
permissions`. Causa: ya hay un PostgreSQL instalado en Windows escuchando en
5432 (PID 7956). Se cambió el puerto **del host** a `55432`. Dentro de la red de
Docker sigue siendo 5432, así que `DATABASE_URL` no cambia. Ver DEC-007.

### Qué quedó pendiente

- Sin remoto de git y sin `gh` instalado: las ramas existen, los PR no
- `CLAUDE.md` sin aprobar por Mateo
- El piloto sin empezar: TAREA 1, 2 y 3

### Hallazgos de la pre-auditoría de los 20 casos

Verificables leyendo el Excel, sin acceder a ninguna URL. Se detallan en
[`../research/README.md`](../research/README.md). El principal:

> En **18 de 20 casos** la columna `URL contenido / declaración` **es la URL del
> verificador**. Solo P02 (okdiario) y P20 (INEC) apuntan a contenido que no sea
> un artículo de verificación.

Esto agrava el defecto D1 de la adenda: no es solo que los casos se encontraran
a través de verificadores, es que **el contenido original no está registrado**.
Sin la URL del post original no se puede reproducir la entrada del sistema.

---

## 2026-09-11 — Registro vivo del proyecto

### Qué se hizo

Se creó la carpeta `docs/` con el registro vivo del proyecto, en la rama
`docs/registro-vivo-del-proyecto`:

| Archivo | Para qué |
|---|---|
| `docs/README.md` | Índice y reglas de actualización |
| `docs/ESTADO.md` | Foto del proyecto hoy. Se sobrescribe |
| `docs/BITACORA.md` | Este archivo. Append-only |
| `docs/DECISIONES.md` | 12 decisiones registradas con su alternativa descartada |
| `docs/ARQUITECTURA.md` | Qué existe hoy y cómo encaja |
| `docs/GLOSARIO.md` | Vocabulario y enums cerrados |
| `docs/PREGUNTAS-ABIERTAS.md` | Lo que bloquea y quién decide |
| `docs/SEGURIDAD.md` | Controles implementados, no planeados |
| `research/README.md` | Estado del piloto y pre-auditoría de los 20 casos |

**Por qué ahora y no después.** El START-HERE §26 y la adenda D6 dicen que el
aparato completo de `/docs` va después de `PILOT_GO`. Esto no es ese aparato:
no hay ADR formales, ni `THREAT-MODEL.md`, ni `DATA-FLOW.md`. Es el sitio donde
se acumula lo que ya se sabe para que no se pierda entre sesiones. Lo que la
adenda desaconseja es el andamiaje prematuro, no llevar registro.

### Qué se verificó

- Todos los enlaces internos entre documentos apuntan a archivos que existen
- Las cifras citadas (18 de 20, 12 valores de `Truth`, 1 control negativo)
  salen del Excel y se pueden recomputar

### Qué quedó pendiente

Lo mismo que el 2026-09-08. Ninguna pregunta abierta se ha cerrado.

---

## 2026-09-24 — Cierre de `docs/` y tres decisiones de Mateo

### Qué se hizo

**La rama de documentación se rehízo desde `main`.** Estaba mal basada, sobre
`feat/entorno-docker-local`. Son cambios distintos y deben poder revisarse aparte,
así que se borró `docs/registro-vivo-del-proyecto` y se creó `docs/registro-vivo`
desde `main`.

`NOTA` Al cambiar de rama, git se llevó del working tree los 56 archivos del
entorno Docker, que viven en la otra rama. No se perdió nada. El `.env` sobrevivió
porque no está rastreado.

**Se escribieron los 3 documentos que faltaban:** `docs/PREGUNTAS-ABIERTAS.md`,
`docs/SEGURIDAD.md` y `research/README.md`. Con eso `docs/` queda cerrado: 9
archivos, 1520 líneas.

**Tres preguntas abiertas resueltas por Mateo:**

| # | Decisión | Dónde |
|---|---|---|
| P-03 | P08 y P09 **salen** del corpus de tesis. Se registran como `other_observed` y pasan a trabajo futuro | DEC-013 |
| P-04 | **Claude cronometra**, declarado como recuperabilidad-por-agente. Mateo cronometra 5 casos a mano como contraste | DEC-014 |
| P-09 | **Se mantiene abierta a propósito.** Credenciales actuales se conservan; rotar antes de cargar datos reales o de conectar a Supabase en serio | P-09 |

**Merge a `main` con `--no-ff`**, para que el merge quede como un punto explícito
en el historial y no se pierda entre los commits.

### Qué se verificó

- Escaneo de secretos sobre lo commiteado: **limpio**. Ninguna credencial de
  Supabase, ningún `project-ref`, ninguna clave JWT, ni la contraseña del `.env`
  local. Única coincidencia: el prefijo `sb_publishable_...` escrito con puntos
  suspensivos como ejemplo en prosa
- `.env` sigue sin estar rastreado
- 15 de 17 enlaces internos entre documentos resuelven. Los 2 que no apuntan a
  `../migracion-supabase-base-de-datos/`, que está en la rama de Docker

### Qué quedó pendiente

- **Rotar la contraseña de Supabase** (P-09), antes de cargar datos reales
- `CLAUDE.md` sigue como propuesta, sin aprobar. Vive en la rama de Docker
- `feat/entorno-docker-local` **sigue sin fusionar** a `main`
- PR en pausa: no hay remoto ni `gh` instalado

### Nota fuera de alcance

Se diagnosticó un error de hidratación de React que resultó ser de otro proyecto
de Mateo (`OjoDelAmo`, Next.js), no de VERITAI. No se tocó ningún archivo de ese
repositorio. Se deja anotado solo para que la bitácora refleje en qué se gastó
tiempo de la sesión.

---

## 2026-09-24 (tarde) — TAREA 1: auditoría de los 20 casos

### Qué se hizo

Plan aprobado en plan mode, con 8 predicciones escritas antes de ejecutar.
Rama `feat/auditoria-piloto-20` desde `main`.

**Fase A, sin red.** `scripts/auditar_aritmetica.py` recomputa 36 cálculos
desde `Dato A` / `Dato B`: 26 exactos, 4 dentro de redondeo, **1 discrepancia
(P03: +5,03% debe ser +5,30%)**, 5 no verificables.
`scripts/normalizar_a_enums.py` lleva los 20 casos a enums cerrados con
justificación por fila: `truth` pasa de 12 valores a 3.

**Fase B, con red.** 40 URLs (36 únicas) en paralelo, 20:59–21:06, más 8
seguimientos: extracción local de 2 PDFs con `pypdf`, 2 consultas a las APIs
JSON del mismo publicador (INE `wstempus`, Eurostat diseminación), 1 reconsulta
a okdiario, 3 `curl -I` para caracterizar bloqueos.

**Entregados:** `research/AUDIT-PILOT-20.md`, `research/pilot-20-normalizado.csv`
(20 filas, 25 columnas) y los dos scripts.

### Resultado

```
verificado        3    P15 P16 P20
parcial           3    P06 P14 P17
NEEDS_REVIEW     12
fuera_de_alcance  2    P08 P09 (DEC-013)
```

### Qué se verificó

- Los dos scripts corren y validan: cero valores fuera de enum; todo
  `verificado` tiene `raw_value_span` de la primaria; todo `NEEDS_REVIEW` tiene
  motivo escrito
- Los 3 verificados tienen el número literal de la primaria: P15 por API de
  Eurostat, P16 por API del INE, P20 en el HTML del INEC
- Los conteos del informe (18 de 20, 12 → 3, 5 `other_observed`, 4
  `METRIC_AMBIGUOUS`) salen del script, no de memoria

### Hallazgos que no estaban previstos

- **Predicción 2 (link rot) fallida.** Cero enlaces muertos. Los PDFs de 2019 y
  2020 están vivos.
- **Bloqueo de bots:** Newtral 8 de 8 (403 al fetcher, 200 a un navegador),
  Interior con desafío de Cloudflare. Vivo para humanos, cerrado para agentes.
- **Tres errores más de transcripción:** P11 (8.830 es S.L., el total es 8.908),
  P12 (las cifras del Excel no están en la primaria citada; ésta da 22.414 y
  12.432), P13 (Dato B sin fuente).
- **La primaria de P12 tiene en una nota al pie la advertencia metodológica que
  explica el caso** (`¥ datos de prevalencia`). Argumento concreto a favor del
  slot `methodology_items` del EvidenceBundle.
- **P13 estaba etiquetado al revés:** es un control de comparabilidad y tenía
  `divergence_detected`. Corregido a `no_divergence_detected`.
- **`other_observed` (clases 6 y 7) es la categoría más frecuente: 5 de 20.**
  `1_ranking_vs_value`, la canónica, aparece una vez.
- **`METRIC_AMBIGUOUS` en 4 de 20**, no en 2 como se predijo.

### Qué quedó pendiente

- Cinco preguntas nuevas para Mateo, P-10 a P-14 en `PREGUNTAS-ABIERTAS.md`
- Rama sin commitear hasta revisar el diff
- TAREA 2 sin empezar

---

## 2026-09-25 — Revisión de la TAREA 1 y cinco decisiones

### Qué se hizo

**Commit de la auditoría** en `feat/auditoria-piloto-20`, aprobada por Mateo
tal cual: *"El trabajo está bien hecho"*.

**Cinco decisiones de Mateo aplicadas**, DEC-015 a DEC-019:

| | Decisión | Dónde cambió |
|---|---|---|
| P-10 | `METRIC_AMBIGUOUS` entra en el enum | `GLOSARIO.md`, script, CSV (4 filas) |
| P-11 | Sin clase nueva: `truth` y `context` son ejes | **P15 corregido** a `no_divergence_detected`; validación y tabla cruzada en el script |
| P-12 | Aplazada al lote crudo; desglose entregado | `PREGUNTAS-ABIERTAS.md` |
| P-13 | El CSV es la fuente de verdad; el Excel, congelado | `research/README.md` |
| P-14 | No se evaden protecciones anti-bot | `GLOSARIO.md`, `research/README.md` |
| — | Métrica de puerta en dos; decide la del agente | `ESTADO.md`, `GLOSARIO.md`, `research/README.md` |
| — | **P-15 abierta**: `1_ranking_vs_value` aparece 1 vez en 20 | `PREGUNTAS-ABIERTAS.md` |

Addendum en `AUDIT-PILOT-20.md` con la tabla cruzada `truth × context`.

### Corrección de encuadre

El informe decía "5 de 20 son `other_observed`". Dos de esos (P08, P09) lo son
por DEC-013, no por su clase. El dato en alcance es **3 de 18**, y uno (P17)
no es ni clase 6 ni 7: es agregación con subgrupos en sentido contrario, un
tipo nuevo.

### Qué se verificó

- El script de normalización vuelve a salir 0 con el enum ampliado, la
  corrección de P15 y la validación nueva de los dos ejes
- Los conteos del addendum salen de la tabla cruzada que imprime el script

### Qué quedó pendiente

- Fusionar `feat/auditoria-piloto-20` a `main` (con `--no-ff`, como la anterior)
- `feat/entorno-docker-local` sigue sin fusionar
- `CLAUDE.md` vive en la rama de Docker: cuando se fusione, hay que llevarle
  DEC-017 (CSV fuente de verdad) y DEC-018 (anti-bot) a las reglas permanentes
- TAREA 2, plan mode primero

---

## 2026-09-25 — TAREA 2: el lote crudo, recolectado y cronometrado

### Qué se hizo

**Pool de 38 candidatos** por búsqueda web (prensa y comunicación oficial en
español, 2026), repartidos por nivel de emisor y con temas rotados. **Criba con
la regla dura** (dos búsquedas negativas por candidato): 7 rechazados (18,4%),
31 admitidos. Los 31 se trabajaron **en serie y cronometrados** con
`research/scripts/cronometro.py` (hitos t0/t1/t2 en `research/cronometro.log`).

**Cubetas cerradas:** control negativo 7/7, divergencia real 6/6, primaria no
localizable 3/3, edición anterior no localizable 2/2. **Formato hostil 0/2: el
pool se agotó sin un solo PDF escaneado** — todos los PDF encontrados tenían
texto extraíble. Dos cubetas sin objetivo, añadidas al validar porque el plan no
las contemplaba: `bloqueado_por_publicador` (C09) y `claim_falso` (C17, C28).
Lote = 21 casos; 10 excedentes registrados.

**Las dos métricas, medidas por primera vez** (recomputadas por
`validar_lote_crudo.py`, exit 0):

```
                                  sobre los 31 trabajados   sobre el lote (21)
edicion anterior localizada           25/31   80,6%            15/21   71,4%
recuperable-por-agente                25/31   80,6%            15/21   71,4%   <- DECIDE
alcanzable_por_humano (si|probable)   29/31   93,5%            19/21   90,5%
```

Los seis no recuperados: C09 (bloqueado), C10 y C25 (edición anterior), C22,
C24 y C27 (primaria). Ningún caso tocó el tope de tiempo: 1,7 min de media
para localizar, 5,2 máximo.

**Entregables:** `research/COLECCION-LOTE-CRUDO.md`,
`research/pilot-crudo-screening.csv` (38), `research/pilot-crudo-20.csv` (lote),
`research/pilot-crudo-trabajados.csv` (31), `research/cronometro.log`,
`research/evidencia/`, y los tres scripts.

### Qué se encontró

- **La cuota por cubetas fija la métrica del lote por construcción**: 7+6
  recuperables y 3+2 no recuperables dan ~71% antes de mirar un solo caso. La
  tasa natural sobre los 31 admitidos (80,6%) es la que informa. → **P-16**.
- **P-15 sigue abierta:** `1_ranking_vs_value` aparece **1 vez en 12
  divergencias** (C07), más una secundaria (C08). `other_observed` 5,
  `2_baseline_selection` 3.
- **Las revisiones de base son el patrón dominante entre las divergencias
  nuevas**: el Balance de Criminalidad compara contra una base 2025 revisada
  (C18); el Índice de Paz Global publica "sube 4" contra el rank revisado
  mientras la prensa resta "cae 2" contra el publicado (C29); Moncloa compara
  España 2025 con la UE 2024 (C21).
- **El fallo de nivel 5 no es "PDF hostil", es "no hay documento"**: informes
  corporativos que solo existen como nota de prensa (C24), encuestadoras que
  entregan por WhatsApp (C27), un valor atribuido al INE que el INE no publica
  (C22).
- **Zona gris de DEC-018, declarada:** tras un fallo del fetcher se probó
  `curl` con su UA por defecto (sin falsificar). Cuatro dominios volvieron a
  bloquear (registrados); dos respondieron 200 (gob.pe tras un 418, el
  ministerio de Educación tras `socket hang up`). → **P-17**.

### Predicciones vs realidad

De las 9 predicciones escritas antes de ejecutar: 3 confirmadas (4, 8, 9), 1
parcial (5), 5 falladas (1, 2, 3, 6, 7). La mayor: se predijo 30–50% y salió
80,6%. Detalle en `COLECCION-LOTE-CRUDO.md` §5.

### Qué quedó pendiente

- **Mateo:** los 5 casos manuales (C04, C05, C11, C14, C22; semilla
  `20260925`), sin ver los resultados del agente
- Decidir P-16, P-17, P-18 (déficit de formato hostil: ampliar pool o aceptar)
- Commit de `feat/lote-crudo-20` tras revisar el diff; fusionar a `main`
- `feat/entorno-docker-local` sigue sin fusionar
- TAREA 3 cuando estén los 5 de Mateo

---

## 2026-09-25 — Tres decisiones sobre el lote crudo (DEC-020 a DEC-022)

### Qué se hizo

**Commit de la TAREA 2** en `feat/lote-crudo-20` (`cf2946d`), aprobada por
Mateo tal cual. Después, **tres decisiones aplicadas**:

| | Decisión | Qué cambió |
|---|---|---|
| P-16 | Decide la **tasa natural sobre los 31 admitidos**, "la que menos manipulación tiene". La del lote se reporta al lado | `validar_lote_crudo.py` imprime primero la métrica sobre los trabajados; `ESTADO.md`, `GLOSARIO.md`, `research/README.md` reescriben el denominador |
| P-17 | **Un 403/406/418 al primer cliente cierra el caso**, aunque `curl` pase después. "Si el publicador señala que no quiere agentes, se respeta" | C30 y C31 → `bloqueado_por_publicador`; cifra que decide **23/31 = 74,2%** (conservadora), 80,6% se reporta. Regla en `GLOSARIO.md` |
| P-18 | **Formato hostil 0/2 es un hallazgo**: buscando sin sesgo no aparecieron PDFs sin texto. Sin segunda pasada | Nota en la composición del lote (`research/README.md`); lote de 23 |

### Lo que Mateo señaló y queda como obligación para la TAREA 3

*"Predijiste 30–50% y salió 80,6% [...] la herramienta de búsqueda te entregó
los casos fáciles."* Es el sesgo del lote anterior con otra cara. La TAREA 3
lleva una **sección de amenazas a la validez** con la distribución de los 31
por tipo de publicador y por vía de descubrimiento, y la recuperabilidad
desagregada. Adelantado en `COLECCION-LOTE-CRUDO.md` §3: nivel 1 **84,2%**
(16/19), resto **58,3%** (7/12); prensa 20/28, comunicación oficial 3/3; Perú
0/2. *"No cambies el número. Decláralo con su límite."* Hueco detectado: la
vía de descubrimiento no se registró por candidato; hay que reconstruirla del
transcript antes de la TAREA 3.

**P-15 sigue abierta y sube de rango**: 1 de 12 aquí, 1 de 20 en el piloto.
"Dos lotes independientes dicen lo mismo. Eso ya no es ruido, es señal."

### Qué se verificó

- `validar_lote_crudo.py` sale 0 con C30/C31 como bloqueados: lote 23,
  excedentes 8, conservadora 23/31, leniente 25/31
- La selección de los 5 casos de Mateo no cambia: la misma semilla sobre los
  23 ids devuelve C04, C05, C11, C14, C22

### Qué quedó pendiente

- Mateo: sus 5 casos, sin que el agente mire ese CSV
- Reconstruir la vía de descubrimiento por candidato
- Fusionar `feat/lote-crudo-20` y `feat/entorno-docker-local` a `main`
- TAREA 3

---

## 2026-09-25 — Dos merges y la vía de descubrimiento reconstruida

### Qué se hizo

**Merges a `main` con `--no-ff`**, por orden de Mateo: `feat/lote-crudo-20`
(84303a8) y `feat/entorno-docker-local` (26d42da). Sin conflictos. `main`
tiene ahora el paquete, el registro vivo, las dos tareas del piloto y el
entorno Docker. `CLAUDE.md` entra como propuesta (P-02).

**Vía de descubrimiento reconstruida del transcript** (DEC-020), en
`feat/via-descubrimiento`. `scripts/reconstruir_descubrimiento.py` lee el
`.jsonl` de la sesión, ordena las 261 llamadas web y busca, para cada uno de
los 38 candidatos, la primera cuyo resultado contiene su `post_url`. **38 de
38 localizados**: 35 por la URL exacta y 3 por una pista del claim (cifra o
nombre propio) en la consulta anterior a su propia criba; 23 consultas
distintas. Las consultas se clasifican en cinco vías con reglas declaradas en
el script; el resultado va a `pilot-crudo-descubrimiento.csv` y a dos
columnas nuevas del screening y del lote.

### Qué se encontró

```
via                      trabajados   conservadora
busqueda_a_organismo         13        12/13   92,3%
criba_negativa                6         5/6    83,3%
busqueda_de_rankings          5         3/5    60,0%
busqueda_de_encuestas         5         2/5    40,0%
busqueda_por_tema             2         1/2    50,0%
```

- **Lo que Mateo sospechaba, con número:** las consultas que ya nombraban a
  un organismo estadístico dieron 13 casos y 92,3%; las que no (ranking,
  encuesta, tema) dieron 12 casos y 50%. El 74,2% es el promedio de esa
  mezcla, y la mezcla la eligió el barrido y el buscador.
- **Hallazgo que no se veía:** 6 de los 31 trabajados aparecieron en la
  **búsqueda negativa de la criba de otro candidato**. Son cobertura hermana
  del mismo dato (C03 de C02, C05 de C04, C08 de C07, C13 de C12, C17 de
  C16, C31 de C30): no son sorteos independientes, heredan la primaria del
  hermano, y el tamaño muestral efectivo es menor que 31. Entra en la
  sección de amenazas a la validez de la TAREA 3.
- **Un artefacto del método, corregido en el script:** para tres candidatos
  originales (C16, C26, C27) la URL exacta aparece por primera vez en su
  propia criba, porque el barrido los mostró en otro medio o solo en texto.
  Se rastrean a esa consulta anterior por una pista del claim, y el `match`
  lo deja escrito.

### Qué se verificó

- `validar_lote_crudo.py` sale 0 con las columnas nuevas; `lote_crudo.py`
  compila con los 38 campos insertados
- `reconstruir_descubrimiento.py --aplicar` es idempotente

### Qué quedó pendiente

- Commit de `feat/via-descubrimiento` tras revisar el diff; merge a `main`
- Mateo: sus 5 casos
- TAREA 3, plan mode primero, con las tres cuestiones que fijó Mateo:
  alcance honesto (¿nivel 1 con el resto como limitación?), reencuadre del
  objeto de estudio ante P-15 (incluida la opción "revisión de base" como
  clase canónica), y si Perú 0/2 y el bloqueo son señal o muestra
  insuficiente. Termina en `PILOT-DECISION.md` con GO o PIVOT

---

## 2026-09-25 — TAREA 3: la decisión de la Puerta 1

### Qué se hizo

Plan aprobado en plan mode; ejecutado en `feat/tarea-3-decision`.

- **`scripts/pilot40.py` → `PILOT-40.csv`**: los 20 auditados (etiquetas del
  CSV + claim, fecha, emisor y URLs del Excel congelado, solo lectura, sha256
  sin cambios) y los 31 crudos en un esquema común. 51 filas; el nombre es
  el del paquete. El script imprime todos los conteos de los tres informes:
  ningún número tecleado.
- **`PILOT-FINDINGS.md`**: las cinco métricas de R02 §7 (todas verde, con la
  conservadora), la comparación con el lote sesgado, la **sección de amenazas
  a la validez** que pidió Mateo, el alcance honesto, P-15 con cinco
  opciones, Perú/bloqueo, y el hueco humano/agente.
- **`PILOT-FAILURES.md`**: catálogo de fallos con casos y lo que piden del
  prototipo (`base_version`, subtipos de abstención, código HTTP del primer
  contacto, tests de identidad de edición).
- **`PILOT-DECISION.md`**: **`PILOT_GO` con alcance declarado a nivel 1**,
  con el bloque YAML de START-HERE §20.

### Las tres cuestiones de Mateo, resueltas y no rodeadas

1. **Alcance honesto.** "El 74,2% es el promedio de 84,2% (nivel 1, 19
   casos) y 58,3% (resto, 12), con una mezcla que eligió el barrido y el
   buscador." Está escrito así en FINDINGS §3.1. Propuesta: el sistema se
   declara para publicadores de nivel 1; el resto como limitación escrita.
   Tres emisores con criterio explícito: INE, FMI, Interior. → **P-19**.
2. **P-15.** Sobre las 28 divergencias de los dos lotes, `1_ranking_vs_value`
   es 2 (7,1%). Cinco opciones con pros, contras y casos (FINDINGS §5),
   incluida "revisión de base" como canónica (C: novedosa y computable, pero
   2 de 12, tan marginal como ranking). Recomendación: E como objeto
   ("comparabilidad de ediciones"), B como primera clase ("comparación de
   base", 8 + 2 revisiones), A ilustrativa. Decide Mateo.
3. **Perú 0/2.** No alcanza: es un solo dominio (`gob.pe`) y un solo 418. Lo
   que sí se observa, como hipótesis: 3 de los 4 primarios que rechazaron al
   agente son portales gubernamentales centralizados, no institutos de
   estadística en su dominio.

### Hallazgos nuevos del cruce de lotes

- El sesgo D1 escondía la D: 0 de 20 en el Excel, 6 de 31 en crudo.
- Verificado con `raw_value_span` de primaria: 3/20 en la auditoría, 31/31
  (actual) y 25/31 (anterior) en el crudo: 56 spans que cumplen "ningún
  número puede tener como único origen el LLM".
- Sin los seis hermanos por criba: 18/25 = 72,0%. Sigue en verde.
- `other_observed` es 10 de 28: P-12 se decide con este dato.

### Qué se verificó

- `pilot40.py` sale 0: 51 filas, cero valores fuera de enum (enums
  importados de `normalizar_a_enums.py`); las cifras de FINDINGS y DECISION
  están en su salida; `validar_lote_crudo.py` y `normalizar_a_enums.py`
  siguen en 0; enlaces internos resuelven; Excel intacto.

### Qué quedó pendiente

- **Mateo ratifica o no `PILOT_GO`**, y decide P-15 y P-19
- **P-20**: los 5 casos manuales de Mateo llenan FINDINGS §7; si contradicen,
  la decisión se reabre
- Commit tras revisar el diff; merge a `main` con `--no-ff`
- Puerta 2 solo después de la ratificación: prototipo de START-HERE §18 con
  INE como primer conector, sin LLM

---

## 2026-09-25 — Puerta 1 superada: GO ratificado, alcance nivel 1, P-15 casi

### Qué se hizo

Commit de la TAREA 3 (`f1e3c2e`) y, encima, las decisiones de Mateo:

| | Decisión | Dónde |
|---|---|---|
| `PILOT_GO` | **Ratificado.** Puerta 1 cerrada. La Puerta 2 **no arranca** hasta cerrar P-15 | DEC-023; `PILOT-DECISION.md` lleva la ratificación |
| P-19 | Alcance declarado a nivel 1; niveles 3–5 como limitación escrita con su 58,3%; INE, FMI e Interior | DEC-024; P-19 a Cerradas |
| P-15 | Va con la recomendación (E / B / A, C subtipo de B), **pero quiere ver antes** qué implica para el título y la hipótesis | Redacción propuesta en `PREGUNTAS-ABIERTAS.md`, P-15: título nuevo, tres hipótesis con su número, caso definitorio (C29 o C21), taxonomía reordenada (2a/2b/2c), O1 y O3 retocados |
| P-20 | Mateo hace sus 5 casos y los pasa en tabla | Sigue abierta |

Fusionado a `main` con `--no-ff`. **Se para aquí**, por orden de Mateo: nada
de Puerta 2 hasta que cierre P-15.

### Qué quedó pendiente

- Mateo aprueba o corrige la redacción de P-15 → entonces se cierra con su
  DEC y se abre la rama de la Puerta 2
- P-20: los 5 casos en tabla → FINDINGS §7 y, si toca, reabrir la decisión
- P-05 (segundo anotador), P-12 (`other_observed`, 10 de 28), P-02
  (`CLAUDE.md`), P-09 (rotar credenciales antes de datos reales)

---

## 2026-09-25 — P-15 cerrada: el encuadre de la tesis tras el piloto (DEC-025, DEC-026)

### Qué se hizo

Mateo aprobó la dirección E/B/A/C y pidió una **pasada de coherencia sobre
todo el repositorio** con nueve ajustes antes de cerrar. La pasada encontró:

- **Ningún caso pasa los cinco requisitos de canónico con un claim
  divergente.** C29 tiene la divergencia en el claim pero la revisión de base
  se *infiere* del indicador CHANGE del IEP (el PDF no imprime los valores
  revisados ni declara política de revisión); C18 tiene la revisión demostrada
  con dos cifras literales del mismo emisor pero su claim relaya bien; C21 es
  periodo desparejado (2a), no revisión. **Decisión: no se declara canónico**;
  la tesis presenta el par C18 + C29 y el canónico sale de la Puerta 2.
- La URL del Balance 2T2025 (edición anterior de C18) no estaba registrada:
  recuperada del transcript y anotada.
- "Engañoso" en título, problema, hueco, objetivo general y glosario; "sin
  LLM" ambiguo en ESTADO, PILOT-DECISION y el borrador de H2; el `02`
  excluía "redes distintas de X" dando X por entrada, cuando el piloto no
  pudo recolectar de X; O1 decía "español latinoamericano" contra la Opción A.

**Aplicado con DEC-026** (Mateo aprobó título, par C18 + C29 y
`TESIS-ENCUADRE.md` sin tocar el `02`):

| Dónde | Qué |
|---|---|
| `docs/TESIS-ENCUADRE.md` (nuevo) | Título, pregunta de investigación, H1–H3 como proposiciones + evidencia preliminar separada, objetivo general, O1–O6 (cambian O1, O3, O6), definición operacional, alcance, taxonomía, "no hay canónico", qué afirma y qué no |
| `02-1-VeritAI-TESIS.md` | Solo una nota de remisión visible al inicio; el resto intacto |
| `docs/GLOSARIO.md` | Definición de divergencia contextual computable; "caso ilustrativo" y "caso canónico: no hay todavía"; fila "fake news / engañoso" sin intención; enum `clase` con `2b_base_revisada` y las familias |
| `normalizar_a_enums.py`, `lote_crudo.py`, CSVs, `pilot40.py` | Código nuevo `2b_base_revisada`; **solo C29** reetiquetado (2b, secundaria 2a); familia "comparación de base" = 2a + 2b + 2c |
| `README.md`, `CLAUDE.md` §1, `docs/README.md` | El ranking pasa a ilustrativo; definición operacional; enlace al encuadre |
| `PILOT-DECISION.md`, `PILOT-FINDINGS.md` §5, `COLECCION-LOTE-CRUDO.md` §4 | Cierre de P-15, corrección de "sin LLM", C29 |
| `docs/DECISIONES.md` | DEC-025 (sin contaminación entre conjuntos) y DEC-026 |
| `docs/ESTADO.md`, `PREGUNTAS-ABIERTAS.md` | P-15 a Cerradas; la Puerta 2 espera a que Mateo revise P-12 |

### Qué se verificó

- `normalizar_a_enums.py`, `validar_lote_crudo.py` y `pilot40.py` salen 0
  con el enum ampliado; las cifras de FINDINGS §5 coinciden con la salida
  nueva (2a 6, 2b 1, 2c 1: familia 8, sin cambio)
- Enlaces internos resuelven; el `02` solo cambia en la nota; Excel intacto

### Qué quedó pendiente

- **Mateo revisa P-12** (`other_observed`, 10 de 28) antes de la Puerta 2
- **P-20**: los 5 casos manuales
- Fusionar `docs/p15-encuadre` a `main`
- Puerta 2: sin abrir, por orden de Mateo

---

## 2026-09-25 — P-12: el desglose de `other_observed`, con dos correcciones

### Qué se hizo

Merge de `docs/p15-encuadre` a `main` (`c6c47e2`). Después, en
`docs/p12-other-observed`, el desglose que pidió Mateo con sus dos
correcciones previas:

1. **P08 y P09 estaban contados** en "10 de 28" pese a estar fuera de alcance
   por DEC-013. `pilot40.py` imprime ahora la tabla 5b sobre las **26
   divergencias en alcance**: `other_observed` **8 de 26 (30,8%)**. Corregido
   en FINDINGS §5, TESIS-ENCUADRE, GLOSARIO, ESTADO, PILOT-DECISION y en el
   texto de DEC-026 (marcado como corrección).
2. **C03, C05, C08 y C13 son hermanos por criba**: sin ellos, **4 de 21
   (19,0%)**. La mitad del grupo es cobertura hermana de datos ya
   representados.

**Desglose caso a caso** en `PREGUNTAS-ABIERTAS.md`, P-12: tres encajes
limpios en clases existentes (P05 → 2a, P07 → 4, C13 → 2a), uno discutible
(C08 → 1 por su núcleo computable), dos candidatas a clase nueva (P17
agregación con subgrupos en sentido contrario; C10 subtipo 2d "cambio
afirmado sin edición anterior") y dos que no son clase (C03 lectura parcial;
C05 abstención por slot faltante y atribución causal). **Ninguna reetiqueta
hasta que Mateo decida.**

### Qué quedó pendiente

- Mateo decide P-12 con el desglose
- P-20: los 5 casos manuales
- Fusionar `docs/p12-other-observed`
- Puerta 2: sin abrir

---

## 2026-09-25 — P-12 cerrada (DEC-027) y la Puerta 2 a la espera de su plan

### Qué se hizo

Merge de `docs/p12-other-observed` a `main` (`3798414`). En
`docs/p12-cierre`, las decisiones de Mateo sobre el desglose:

| Caso | Decisión | Dónde |
|---|---|---|
| P05, P07 | → `2_baseline_selection`, → `4_denominator`, con la nota del mecanismo | `normalizar_a_enums.py`, `pilot-20-normalizado.csv` |
| C13 | → `2_baseline_selection` (dirección implícita contraria a la edición anterior) | `lote_crudo.py`, CSVs |
| C08 | se queda: reetiquetar subiría la clase ilustrativa por decisión, no por dato | — |
| C03 | → `no_divergence_detected`, clase `none`, cubeta `control_negativo`; lectura alternativa (flujo vs stock) en `notas` | ídem |
| C05 | → abstención con dos motivos `REQUIRED_SLOT_MISSING\|UNSUPPORTED_CLAIM_TYPE`; `insufficient_evidence` / `undetermined`; cubeta nueva `abstencion` | ídem; validadores aceptan `\|` |
| P17, C10 | candidatas sin código; **criterio de reaparición escrito antes de ver datos**: ≥ 3 casos independientes, ≥ 2 emisores, A o B, test computable; se decide una vez | DEC-027, GLOSARIO, TESIS-ENCUADRE |

Los objetivos de cubeta eran la regla de parada de la recolección: C03 deja
control negativo en 8 sobre 7 y `validar_lote_crudo.py` **avisa, no falla**;
la pertenencia al lote no se recompone.

### Números después

```
divergencias en alcance   24 (eran 26)      other_observed   3 de 24 (P17 C08 C10)
familia comparacion de base  10 de 24  41,7%   -> sostiene B sin reetiquetar para lograrlo
2a 8 · 3 5 · 4 4 · 1 2 · 2c 1 · 2b 1      controles negativos crudos 16 de 31
```

Propagado a FINDINGS §2 y §5, TESIS-ENCUADRE (H1, H3), GLOSARIO, DECISION,
COLECCION (notas "tras DEC-027"), ESTADO.

### Qué se verificó

- `normalizar_a_enums.py`, `validar_lote_crudo.py` (con aviso) y `pilot40.py`
  salen 0; las cifras nuevas están en su salida

### Qué quedó pendiente

- **Puerta 2: plan de una página** (clase 2a, emisor INE, 10 casos con
  trazabilidad completa), a aprobar antes de ejecutar
- Fusionar `docs/p12-cierre`
- P-20: los 5 casos manuales

---

## 2026-09-25 (noche) — Puerta 2 ejecutada: prototipo 2a sobre el INE, 10 casos

### Qué se hizo

Merge de `docs/p12-cierre` a `main` (`11b9a00`). Plan de una página aprobado
por Mateo; rama `feat/puerta-2-ine-2a`. Se construyó la cadena completa de
START-HERE §18 restringida a una clase y un emisor, **sin LLM**:

| Pieza | Dónde |
|---|---|
| Dominio: periodos, claim estructurado, bundle con `raw_value_span` y `bundle_hash`, hard gates, **test 2a**, verdad con tolerancias, veredicto, plantilla | `apps/api/veritai/domain/` |
| Caso de uso `AnalizarClaim` | `application/analizar_claim.py` |
| Cliente Tempus (allowlist, UA, timeout, tamaño, 401/403/406/418/429 = rechazo), extractor con spans, `ProveedorINE` | `infrastructure/ine/` |
| Repositorio Postgres (una transacción) y en memoria | `infrastructure/repositorio.py` |
| `POST /analisis` | `api/routes/analisis.py` |
| Migración 003: `claims`, `evidence_bundles`, `evidence_items`, `verdicts`, `audit_log`, RLS forzada | `db/migrations/003_puerta2.sql` |
| 10 casos JSON, ejecutor, resultados | `research/puerta2/` |
| Informe | `research/PUERTA-2-CASOS.md` |

Los 7 casos del piloto con primaria INE se generan desde `PILOT-40.csv` con la
estructura a mano versionada (`generar_casos_piloto.py`). Los 3 nuevos (N01
vivienda +64 % desde 2019; N03 empleo público +17,5 % desde 2T2018; N04
alimentos +37 % 2020–2024) se recolectaron con el método de la TAREA 2 —criba,
cronómetro, vía— en unos 15 minutos; N02 (nacimientos) rechazado por
`cobertura_explainer`.

### Números después

```
10/10 por POST /analisis (HTTP 200)        test 2a: dispara 5 · no dispara 1 (C16) · no aplica 4
truth   supported 4 · mixed 2 · contradicted 1 · insufficient_evidence 3
context divergence 5 · no_divergence 1 · undetermined 4
acuerdo con el corpus (7 del piloto)   truth 4/7 · context 2/7   (dentro del alcance: 4/4 · 2/4)
Postgres  claims 10 · bundles 10 · items 96 (0 sin span) · verdicts 17 (dos corridas) · audit 17
latencia  mediana ~2,1 s · máx 23,5 s (IPC 25333) · 30 ms con caché
```

### Qué se verificó

- `pytest`: **45 passed** en la corrida final (`-p no:warnings`)
- `ruff check .` limpio
- `docker compose up -d --build api`: migración 003 aplicada (`listo: 1
  migraciones aplicadas`), API healthy, `/health` con base conectada
- RLS activada y forzada en las 5 tablas; `veritai_app` sin DDL
- Cada número del veredicto con `raw_value_span` (test automático + conteo en
  Postgres)
- Valores del INE de C16/C17 (24,54 en 2025-T2 y en 2026-T1) comprobados a
  mano contra la API: coincidencia real, no bug
- `git grep` de secretos vacío

### Qué se aprendió (detalle en `PUERTA-2-CASOS.md` §6)

- P04 encontró un bug real: `T3_Periodo: "A"` en tablas anuales. Corregido con test.
- El criterio de magnitud del 2a dispara con toda base declarada de horizonte
  largo (N01, N03, N04) → **P-21**, a decidir antes de la evaluación.
- `undetermined` sin test aplicable (C11) → **P-22**.
- C17: el prototipo lo lee como "valor atribuido a otro periodo" (mecanismo de
  P05); el corpus lo tiene como claim falso. Decide Mateo.
- Tempus sirve solo la edición vigente: 2b no es computable con la API sola.
- P11: el 8.830 de la API coincide con la cifra de S.L. del PDF de 2019 —
  `NEEDS_REVIEW` contra `research/evidencia/`.
- N01 reaparece el mecanismo candidato P17 (subgrupo presentado como total).

### Qué quedó pendiente

- Mateo lee `PUERTA-2-CASOS.md`; decide P-21, P-22 y C17; ratifica o no el
  cierre de la Puerta 2
- Commit en `feat/puerta-2-ine-2a` cuando lo diga; merge `--no-ff` cuando lo diga
- P-20: los 5 casos manuales
- Un archivo `AGENTS.md` apareció sin seguimiento en la raíz (copia de las
  reglas de `CLAUDE.md`, no lo creó el agente): queda sin tocar y sin commitear
  hasta que Mateo diga qué es

---

## 2026-09-25 (noche, 2) — DEC-029 aplicada: señal de horizonte, C11 corregido, Puerta 2 fusionada

### Qué se hizo

Commit `104cf22` en `feat/puerta-2-ine-2a` con el estado que Mateo revisó.
Después, sus decisiones sobre la primera corrida (DEC-029), en un segundo
commit de la misma rama, y merge a `main` con `--no-ff`:

| Decisión | Qué cambió | Dónde |
|---|---|---|
| P-21: magnitud ≥ 2× sin signo = **señal de horizonte**, no divergencia; solo el signo confirma 2a | `ResultadoTest.senales`; subtipos `cambio_de_signo` / `valor_atribuido_a_otro_periodo`; plantilla y `a_dict` muestran la señal; test nuevo | `domain/tests/{resultado,comparacion_base}.py`, `plantilla.py`, `veredicto.py`, `tests/test_comparacion_base.py` |
| P-22: sin test aplicable, `undetermined`; **se corrige el corpus**, no el sistema | C11 `context` → `undetermined` con nota; validador acepta `undetermined` en controles de nivel; CSV y `PILOT-40.csv` regenerados | `lote_crudo.py`, `validar_lote_crudo.py`, `pilot-crudo-*.csv`, `PILOT-40.csv`, FINDINGS |
| C17: no reetiquetar | discrepancia anotada en `notas`; se resuelve en evaluación | `lote_crudo.py` |
| P11: no citar | `NEEDS_REVIEW` en informe, encuadre y ARQUITECTURA; DEC-028 corregida por DEC-029 | docs |
| 2b fuera del prototipo | limitación de la API Tempus (solo edición vigente) | `ARQUITECTURA.md` §8, `TESIS-ENCUADRE.md` |
| `AGENTS.md` | ni leído ni aplicado ni commiteado | — |

Los 10 casos se relanzaron con la imagen nueva; `ejecutar_casos.py` muestra la
señal en su columna. `CLAUDE.md` §2 y §3 recogen el estado y las dos reglas
nuevas (sigue siendo propuesta, P-02).

### Números después

```
test 2a   confirmada 2 (P11 signo · C17 valor de otro periodo) · señal 3 (N01 N03 N04) · sin señal 1 (C16) · n/a 4
context   divergence 2 · no_divergence 4 · undetermined 4
acuerdo con el corpus (7 del piloto)   truth 4/7 · context 3/7   (dentro del alcance: 4/4 · 3/4; C17 registrado)
Postgres  claims 10 · bundles 10 (sin cambios) · items 96 · verdicts 27 (tres corridas) · audit 27
```

### Qué se verificó

- `pytest`: **46 passed**; `ruff check .` limpio (un archivo ajeno que `ruff
  format` querría reformatear se dejó como estaba: `health.py`)
- `validar_lote_crudo.py` y `pilot40.py` salen 0; los CSV cambian solo en las
  filas de C11 y C17
- `docker compose up -d --build api`: `sin migraciones pendientes (4 ya aplicadas)`
- La señal queda en `verdicts.tests` (`senales`) en Postgres; bundles sin cambio

### Qué quedó pendiente

- Cierre formal de la Puerta 2: Mateo no lo declaró con esa palabra; lo que
  pidió después del merge es la media página de lo que falta para la Puerta 3
- P11: cotejar contra `research/evidencia/` antes de citarlo
- P-20: los 5 casos manuales
- Deuda técnica: caché del proveedor sin TTL; test de arquitectura de imports

---

## 2026-09-25 (noche, 3) — Puerta 2 cerrada (DEC-030); diseño de la Puerta 3 propuesto; arnés en paralelo

### Qué se hizo

Mateo declaró cerrada la Puerta 2 con P11 en `NEEDS_REVIEW` como condición
pendiente anotada. En `docs/cierre-puerta-2`: DEC-030, P-23 (el cotejo de
P11), estado en `CLAUDE.md` §2, `ESTADO.md`, `research/README.md` y la cabecera
de `PUERTA-2-CASOS.md`.

Diseño del conjunto de evaluación, **propuesta en una página**:
[`../research/PUERTA-3-DISENO.md`](../research/PUERTA-3-DISENO.md). El número
que manda son los controles con test aplicable, justificado con el límite
superior del IC 95 % de Wilson:

```
n controles   k=0    k=1    k=2      -> con 20 no se evalua H3 ni con 0 errores;
   20        16,1   23,6   30,1         40 es el minimo que tolera 1 falso positivo;
   40         8,8   12,9   16,5         50 tolera 2 con el limite <= 15 %
   50         7,1   10,5   13,5
propuesta: FPR <= 10 % y limite superior IC95 <= 15 %; A = 50 (min 40); total 110 (min 78)
```

Cubetas A–F, criterio de reaparición de P17/C10 operacionalizado (campo
`mecanismo_candidato`, conteo único al congelar la anotación, evaluación
exploratoria si pasa), tope de cuatro jornadas con revisión a la mitad y
pivote de recolección, y lo que se declara como limitación si una cubeta no
llega. **No se recolecta nada hasta que Mateo apruebe.**

En paralelo, en `feat/arnes-evaluacion`, el arnés: cinco métricas de R02 §7
+ FPR con intervalos, con guardia de conjunto (rechaza casos de desarrollo
salvo `--desarrollo`), probado en humo sobre los 10 de la Puerta 2.

### Qué se verificó

- Intervalos de Wilson recalculados con la función del arnés (misma
  aritmética que el diseño)
- Los docs de esta rama no tocan código; los tests siguen en 46

### Qué quedó pendiente

- Mateo: aprobar o corregir el diseño (tasa de H3, 50/40 controles, cubetas,
  tope, doble anotación)
- Fusionar `docs/cierre-puerta-2` y `feat/arnes-evaluacion` cuando lo diga
- Conectores de FMI e Interior, después del diseño
- P-23 (P11), P-20 (5 casos), P-05 (segundo anotador: el diseño propone 25 %)

---

## 2026-09-26 — Puerta 3, jornada 1: 26 casos y revisión intermedia anticipada

### Qué se hizo

Mateo aprobó el diseño (DEC-031) y pidió recolectar con el tope de cuatro
jornadas y aviso en la revisión intermedia. En `feat/puerta-3-recoleccion`:
infraestructura (`lote_evaluacion.py`, `validar_evaluacion.py` con cubetas,
tope de 3 controles por edición, DEC-025 por URL y texto, pausas descontadas
del reloj; `ine_buscar.py`), tres barridos dirigidos a organismo, criba (a) y
(b) para 26 admitidos, y **26 casos trabajados con cronómetro** (E001–E026).
Todo en `research/puerta3/`; estado y orden de reanudación en `PROGRESO.md`.

### Números al parar (`validar_evaluacion.py`)

```
candidatos 31 · admitidos 26 · rechazados 5 (2 duplicados, 1 verificacion directa, 2 explainer)
cubetas   A 11/50 (min 40) · B 0/20 · C 0/15 · D 3/10 · E 11/10 · F 0/5 · O 1 (P17)
emisor    INE 15 (57,7 %) · FMI 9 · Interior 1 · DGT 1        paises ES 18 · CL 3 · AR 2 · MX 2 · EC 1
truth x context   supported/no_div 21 · supported/undetermined 4 · mixed/div 1
reloj     0,7 h de 16 (pausas descontadas) · cronometro por caso media 1,3 min, max 6,5
```

### Dos bloqueos, por eso se para antes de las 8 h

- **`imf.org` devuelve 403 al agente identificado en API, HTML y PDF** (E007,
  una petición por vía) e **`interior.gob.es` devuelve 403 al PDF del Balance**
  (E025). DEC-021: cierra el caso. Los ocho casos del FMI y el de Interior
  quedan en la cubeta E como bloqueados, con anotación humana desde los PDF que
  llegaron por otro cliente (no cuentan para el agente). La DGT sirve su PDF
  de 2026 pero no enlaza 2025 (E026, edición anterior no localizable). **Dos
  de los tres emisores de DEC-024 no son recuperables-por-agente**: hoy solo
  el INE alimenta la cubeta A. Se abre **P-24**.
- **El presupuesto de búsquedas web de la sesión se agotó (200 de 200).** Sin
  búsqueda no hay criba, y sin criba no se admite nada (DEC-018). Tres
  candidatos del INE quedaron sin cribar y no se registran como admitidos.

### Hallazgos menores registrados en los casos

- E002: "la compraventa de viviendas" −6,1 % es la de segunda mano (total
  −5,1 %): mecanismo candidato P17, primera aparición del conjunto de
  evaluación (N01 era desarrollo).
- E016: el 2,6 % del IPI es la serie original; la nota titula con la corregida
  (2,3). Dos cifras del mismo emisor, ambas publicadas.
- E006: "el INE revisa a la baja sus previsiones" es una revisión
  avance→definitivo (2,7 → 2,6): territorio 2b, sin test, `undetermined`.
- ETCL: las tablas 6067/6070 son retrospectivas 2000–2007; dos marcas `t2`
  erróneas quedaron en el cronómetro y se corrigieron con marcas posteriores
  (manda la última). El "récord en 26 años" (E023) exige juntar dos bases.
- `methodology_found` está en `no` con `NEEDS_REVIEW` en todos los INE: no se
  buscó la nota metodológica en esta pasada.

### Qué quedó pendiente

- Mateo: P-24 (FMI e Interior bloqueados: quitar, sustituir o dejar como
  hallazgo) y si se levanta el tope de búsquedas para seguir recolectando
- Reanudar con `P3-PAUSA2 t2`; el orden está en `PROGRESO.md`
- Fusionar `feat/puerta-3-recoleccion` cuando Mateo lo diga

## 2026-09-26 (14:30Z) — Puerta 3, jornada 2 cerrada con B = 0

Jornada 2 = vía divergencia dirigida, tratada como medición (DEC-033). Reloj
`P3-J2`: 13:34:56Z → 14:30:15Z, 0,92 h de las 4 h previstas; se cerró al
agotarse las vetas dirigidas, no el reloj (detalle y tabla en
`research/puerta3/PROGRESO.md`). Pausa `P3-PAUSA3` abierta.

- **B = 0** tras 17 casos trabajados (E027–E043) y 21 candidatos (Q032–Q052).
  Acumulado: A 17, B 0, C 4, D 8, E 11, F 2, O 1 (43 casos, 1,6 h de reloj).
  Regla del diseño §3b: **B = 0 → no se gasta la jornada 3; DEC de replanteo**.
- Único patrón B encontrado: Delegación del Gobierno en Madrid (tasa por mil
  y "4,3 puntos menos desde 2023" frente a +2,6 % interanual en recuento), en
  la edición 2T2026, **vetada por DEC-025** (Q048, rechazado). Reaparece cada
  trimestre; la siguiente edición admisible es 3T2026 (diciembre).
- Mecanismo dominante de la vía divergencia: **2b** (tasa calculada contra la
  edición provisional del año anterior, no la revisada) en teletipos
  regionales sobre la EOH: E031 (Madrid agosto, cuatro tasas reproducidas con
  la base provisional), E042 (Madrid julio), E043 (Baleares julio, **con cambio
  de signo**: +3,8 % frente a −2,3 %). El prototipo no lo cubre (Tempus sin
  ediciones anteriores, DEC-029).
- Dos claims falsos (cubeta F): euribor.com.es atribuye al INE "un desplome
  del 15 %" de hipotecas en abril antes de que el INE publicara abril (E034);
  Fotocasa titula "el mejor julio desde 2007" cuando 2025 y 2007 fueron
  mayores (E038). Una clase 4 (E041): "más del 70 % del aumento" es el 42 %.
- Emisores nuevos con casos: SEPE (E032 A, E039 D; xls y PDF de datos avance,
  HTTP 200; `evolparoseries.xls` no lo abre xlrd, se usó el PDF), Banco de
  España (E033 A; notas HTML, HTTP 200), Portal de Criminalidad (E036 A, E041
  C; tablas 09001–09006 bajo `DatosBalanceAct`, `DatosBalanceAnt/20261` da
  error al agente).
- Correcciones sobre la marcha: Q040 se había rechazado por "nivel 3" y se
  readmitió antes de commitear (el alcance de nivel 1 es de los emisores de
  datos, no de los publicadores); E043 se había marcado A y pasó a C al leer
  que el artículo escribe la base provisional (740.149).
- `methodology_found` sigue en `no` + `NEEDS_REVIEW` en todos los casos
  (pasada aparte, por instrucción de Mateo).

### Qué queda pendiente

- **Mateo:** DEC de replanteo (salidas de DEC-033: ampliar el tope, bajar el
  mínimo de B a 10 con intervalo declarado, o ambas; o redefinir la fuente de
  B: emisores institucionales / ediciones 3T2026). También si quiere completar
  las 3,1 h restantes de la jornada 2 antes de decidir.
- Q034 admitido sin trabajar; pasada de `methodology_found`; P-23 (P11);
  P-20 (los 5 casos de Mateo).
- Fusionar `feat/puerta-3-recoleccion` cuando Mateo lo diga.

## 2026-09-26 (15:00Z) — DEC-034: B pasa a 2b; condición bloqueante cumplida

- Mateo abre el replanteo: **la cubeta B es 2b (base revisada)**; 2a queda
  como clase secundaria con su 0/43. Último reencuadre del objeto. Q048 sigue
  vetado.
- **Condición bloqueante** (tres casos de edición anterior del INE
  recuperables fuera de Tempus): cumplida con cinco ediciones de cuatro
  operaciones (CTH0725, ETDP0725, H0625, SM0725, CTH0825): nota HTML, nota
  PDF y anexo XLSX responden 200 al agente identificado con la URL derivada
  del código de la nota; el valor publicado difiere del vigente en las cinco
  (de +4 sociedades a −24.181 pernoctaciones). Herramienta
  `research/puerta3/edicion_anterior.py`; resúmenes con sha256 en
  `research/evidencia/D2B_*.json`; informe `research/puerta3/RECUPERABILIDAD-2B.md`.
  Límite anotado: INEbase no lista notas anteriores; el patrón de código no
  está documentado por el INE (`NEEDS_REVIEW` para códigos irregulares).
- Validador: B exige `2b_base_revisada`, C admite 2a. Lote: E031, E042 y
  E043 pasan de C a **B = 3**; C = 1. Cada uno lleva ya
  `evidencia_al_publicar` y `evidencia_vigente` con su fecha.
- Dominio: `EvidenciaEdicion` y los dos campos en `Veredicto.a_dict()`
  (null si no hay 2b) y `lineas_ediciones()` en la plantilla, con test
  `tests/test_veredicto_2b.py`. El test 2b y su conector se proponen aparte.
- Corrección de redacción de Mateo aplicada en PROGRESO: el hallazgo de la
  jornada 2 es "2a no apareció en 43 casos recolectados con este método", no
  una afirmación sobre la prensa.

## 2026-09-26 (15:35Z) — Propuesta 2b, amenaza a la validez y jornada 3: B = 4 → sigue

Orden de Mateo ejecutado en su orden:

1. **Propuesta del test 2b y su conector** (`docs/PROPUESTA-2B.md`, sin
   implementar hasta el "ejecuta"): el mapa cubre **8 operaciones del INE**
   (CTH, EOAT, ETDP, H, SM, IPI, FRONTUR, EGATUR; patrón de código verificado
   en las 8, anexo XLSX 200 en las 8) y **se cierra en 8**. Añadir una cuesta
   alrededor de una hora y una entrada declarativa de diez líneas; no se
   añade ninguna durante la evaluación. Fuera: IPRI (sin anexo, 404), las
   trimestrales y lo que no es INE. Resúmenes con sha256 en
   `research/evidencia/D2B_*.json` (IPI0725, IPRI0825, FRONTUR0725,
   EGATUR0725 añadidos).
2. **Jornada 3** (vía divergencia, B = 2b, medición; regla previa en diseño
   §4b): reloj 0,48 h, 14 casos (E044–E057), **B = 4 → sigue**. Acumulado:
   A 25, B 7, C 1, D 9, E 11, F 3, O 1 (57 casos). Método: recomputar por
   CCAA la tasa con la base provisional y con la vigente y buscar en prensa
   las cifras que solo salen con la provisional. Los 7 B vienen de dos
   ediciones de la EOH: concentración anotada en `PROGRESO.md` con propuesta
   de tope por edición para que Mateo decida antes de la jornada 4.
3. **Amenaza a la validez** escrita como tal (no como nota al pie) en el
   diseño §4, el encuadre, `RECUPERABILIDAD-2B.md` y la propuesta §5: si el
   INE cambia el patrón de código de las notas, el conector se rompe.

Otros hallazgos de la jornada: un claim falso (E050, EP Madrid: base
"460.550" que no existe en ninguna edición del INE, con cambio de signo
implícito); dos controles con métrica compuesta (E049, E054: suma de cuatro
encuestas, fuera del prototipo, declarados); en la misma edición y la misma
mañana unas redacciones calculan con la provisional y otras con la vigente
(el mecanismo es del redactor, no de la edición).

---

## 2026-09-27 (17:29Z) — Puerta 3: test 2b implementado; jornada 4 cerrada con B = 1 (cuota cumplida)

### Qué se hizo

**Punto 1 (commit 2f151ef, 2026-09-26).** Test 2b (`domain/tests/base_revisada.py`),
puerto `ProveedorEdicionAnterior`, mapa cerrado de 8 operaciones con columnas
absolutas verificadas contra los anexos (`infrastructure/ine/mapa_anexos.py`),
conector de edición anterior (`infrastructure/ine/edicion_anterior.py`), caso
de uso con orden verdad → 2a → 2b y abstención `PREVIOUS_EDITION_OUT_OF_MAP`
(fallo de cobertura declarado). Diseño §4c (tope de 3 B por edición, E056 pasa
a excedente), §4d (hipótesis confirmada: 2b solo donde el anexo no trae la
tasa por CCAA), §4e (control natural) y §4f (cuota de emisor).

**Jornada 4** (`P3-J4`, 0,9 h de reloj en dos tramos; la sesión quedó
suspendida entre el 26 a las 18:28Z y el 27 a las 17:03Z y se anotó como
`P3-PAUSA5` retroactiva). Nueve casos: E058–E060 (SEPE julio 2026, A), E061–E062
(BdE junio 2026, A), E063 (Portal 1T2026, A), E064 (Portal, D, ranking
recomputado sobre 68 municipios), E065 (EOAT0726, C: 2a valor atribuido a otro
periodo, la frase de junio repetida en el artículo de julio) y E066 (EOAT0526,
**B**: apartamentos de Murcia +60 % con la base provisional, +34,5 % con la
vigente; primer 2b fuera de la EOH).

### Qué se verificó

- 114 tests, `ruff check` y `ruff format --check` limpios (health.py
  reformateado en este commit).
- Validador OK: 66 casos (A 31, B 7 + 1 excedente, C 2, D 10, E 11, F 3, O 1);
  INE 41/66 = 62,1 % (tope 70 %); tope de 3 B por edición respetado (CTH0726
  3, CTH0826 3, EOAT0526 1); controles por edición ≤ 3.
- Nueve PDF mensuales del SEPE, notas del BdE (junio, mayo, marzo de 2026) y
  siete anexos del INE (CTH0325, CTH0425, CTH0526, CTH0626, EOAT0525, EOAT0526
  con HTML) descargados con el agente identificado: todos HTTP 200.
- Unas 25 piezas regionales de marzo a julio cotejadas con las dos bases:
  todas vigente salvo E066. Anexos de 2026 = API de hoy (2026 sin revisar).

### Qué quedó pendiente

- **Decisión de Mateo** (regla §4b, B = 1 ≤ 3): declarar B con intervalo,
  jornada 5 sobre EOAT0826 (30-09) y CTH0926 (23-10), o rastrear redacciones.
- 2b sobre el avance mensual del BdE: el cuadro del PDF no es texto extraíble;
  NEEDS_REVIEW.
- Pasada final de `methodology_found`; P-23; P-20; Q034 sin trabajar;
  regenerar `requirements.lock.txt` desde el contenedor (openpyxl).

---

## 2026-09-27 (18:00Z) — DEC-035: B declarada con 7 e intervalo; predicción sobre EOAT0826 escrita antes del 30-09

### Qué se hizo

Mateo decidió (a) y (b), no (c). Se escribió en el diseño la razón estructural
(§4g: 2b solo existe en 2 de las 8 operaciones del mapa; B acotado por el
universo, no por el esfuerzo), la **predicción P1/P2 sobre `EOAT0826`**
(§4h, con la lectura de cada resultado fijada de antemano), el plan de A hasta
40 sin INE (§4i) y la vía descartada (§4j). DEC-035 en `DECISIONES.md`;
limitación de H1 en `TESIS-ENCUADRE.md`; `OBJETIVO_CUBETA["B"]` = (7, 7);
`CLAUDE.md`, `ESTADO.md` y `PROGRESO.md` actualizados.

### Qué se verificó

- Intervalos con `research/arnes/metricas.wilson`: 7/7 → [64,6; 100];
  6/7 → [48,7; 97,4]; 5/7 → [35,9; 91,8]. FPR 0/31 → límite 11,0 %;
  0/40 → 8,8 %.
- Validador OK con el nuevo objetivo de B (7 de 7).
- La predicción queda fechada por este commit, tres días antes de la edición
  de prueba.

### Qué quedó pendiente

- **Jornada 5 el 30-09 o después**: P1/P2 sobre `EOAT0826`, ≥ 9 A sin INE,
  `CTH0926` opcional. Avisar a Mateo al cerrarla.

---

## 2026-09-27 (18:20Z) — Enmienda a DEC-035: CTH0926 pasa a necesaria; esqueleto de tesis

### Qué se hizo

Mateo aprobó todo y abre la jornada 5 el 30. Dos cambios que no dependen del
INE: **`CTH0926` sube de opcional a necesaria** (diseño §4h y §4i, DEC-035
enmendada, PROGRESO, ESTADO, CLAUDE.md): es la única edición fuera del verano
y sin ella la predicción P1 no separa §4d de la lectura estacional. Y el
**esqueleto del documento de tesis** en `docs/TESIS/` (11 secciones, solo
estructura y qué material del repo alimenta cada una; nada redactado).

### Qué se verificó

- Los nombres y el orden de las 11 secciones quedan como `NEEDS_REVIEW` hasta
  cotejarlos con la plantilla de titulación de la UDLA (P-06: existe, no está
  en el repo). El mapeo de material es por contenido y sobrevive a un cambio
  de nombres.

### Qué quedó pendiente

- Jornada 5: no se abre hasta que Mateo lo diga (30-09 o después); queda
  abierta hasta `CTH0926` (23-10).
- P-06: entregar la plantilla de la UDLA en `docs/TESIS/` para fijar nombres.

---

## 2026-09-27 (19:15Z) — Pasada de metodología (EOH/EOAT) y convenciones marcadas

### Qué se hizo

**La premisa de 2b tiene fuente primaria.** El INE declara por escrito la
política de revisión provisional → definitivo de la EOH, la EOAP y la EOAC en
el Informe Metodológico Estandarizado de cada encuesta (§14.1 y §17), en la
Política de revisión del INE (abril 2015) y en el pie de las notas de la
EOAT. Citas literales, calendario, indicadores MAR/RMAR, URL, sha256 y
consecuencias en `research/puerta3/METODOLOGIA-REVISION-INE.md`; evidencia
en `research/evidencia/METODOLOGIA_*`. Diseño §4k. Los 22 casos EOH/EOAT
pasan a `methodology_found = si`.

**Convenciones marcadas** (diseño §4l y fichas 3, 5 y 9): FPR 10 % / 15 %,
señal de horizonte 2×, tope de 3 por edición (controles y B), cuota de
emisor, regla de jornada, doble anotación, tolerancia de 2b y mínimo de B,
cada una con fecha y commit. No derivan de nada; si aparece literatura, se
añade.

**Condición de evaluabilidad de P1**, añadida al diseño §4h antes del 30-09:
comprobado contra la API que agosto de 2025 (EOAT) y septiembre de 2025 (EOH)
ya están revisados, así que las dos ediciones de la prueba son evaluables.

### Qué se verificó

- Cuatro descargas con el agente identificado, todas 200 (tres IME, un PDF).
- Comparación anexo/API: EOAT0825 34/34 (EOAP) y 26/34 (EOAC) series
  revisadas; CTH0925 98/104. Validador OK.

### Qué quedó pendiente

- La misma pasada para las otras operaciones del INE (siguen en `no`).
- Jornada 5: no se abre hasta que Mateo lo diga.

---

## 2026-09-27 (19:40Z) — DEC-036: eje de manipulación después de la Puerta 3; `IDEAS.md` con I-001

### Qué se hizo

Decisión de alcance de Mateo registrada como DEC-036: el eje de detección
de manipulación entra al proyecto y se construye después de cerrar la Puerta
3, no en paralelo. `docs/EJE-MANIPULACION.md` (qué es y qué no es, preguntas
abiertas sobre corpus, anotadores y evaluación, hueco para papers, decisiones
que lo condicionan). `docs/IDEAS.md` como bitácora de ideas con fecha, origen
y estado, y la regla de paso a `DECISIONES.md` solo con aprobación explícita.
Primera entrada I-001: contraste con búsqueda web (baseline B0 sobre los 7
casos B, español e inglés, 10 primeros resultados), en estudio, con lo que hay
que fijar antes de medirlo. `CLAUDE.md` §11, `docs/README.md` y el encuadre
actualizados.

### Qué se verificó

- Nada de código: solo documentación. Ninguna referencia bibliográfica
  añadida (las pone Mateo).

### Qué quedó pendiente

- I-001: fijar consultas, criterio de "llega" y procedimiento antes de medir;
  esperar el visto bueno de Mateo.
- Jornada 5: no se abre hasta que Mateo lo diga.
