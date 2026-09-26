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
