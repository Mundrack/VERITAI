# Registro de decisiones

Cada decisión técnica tomada **construyendo**, con la alternativa que se
descartó y por qué. Formato ADR simplificado.

> **Append-only una vez fusionada** (Mateo, 2026-09-27; `CLAUDE.md` §3).
> Mientras la rama donde se escribió una DEC no esté fusionada en `main`, la
> DEC se puede corregir en su sitio dejando una nota de registro. Una vez
> fusionada, una decisión no se edita: se corrige con una entrada nueva que
> dice cuál supersede y qué dato la cambió.

**Esto no incluye las decisiones cerradas del paquete** (`00b-DECISIONES-MATEO.md`
y `04-VERITAI-CLAUDE-RESPONSE-R02.md`). Esas son la fuente de verdad y no se
reabren salvo que los datos del piloto las contradigan.

---

## DEC-001 · La aplicación solo conoce `DATABASE_URL`

**Fecha:** 2026-09-08 · **Estado:** vigente

**Contexto.** Hay que desarrollar en local con PostgreSQL en Docker y migrar
después a Supabase sin reescribir código.

**Decisión.** El código accede a la base de datos exclusivamente por una cadena
de conexión en la variable `DATABASE_URL`, usando SQLAlchemy sobre psycopg.
Queda **prohibido importar `supabase-py` o `supabase-js` en el código de
dominio**.

**Por qué.** Supabase no es otra base de datos: *es* PostgreSQL, y entrega una
cadena de conexión estándar. Si el código habla SQL, migrar es cambiar el valor
de una variable. Si habla PostgREST, migrar es reescribir la capa de datos, y
volver atrás es imposible.

**Alternativa descartada.** Usar el cliente de Supabase, incluso envuelto en un
repositorio propio. Es más cómodo de escribir, pero no se puede ejecutar contra
un Postgres normal, así que los tests dejarían de correr sin Supabase.

**Excepción prevista.** Auth, Storage y Realtime no tienen equivalente en un
Postgres pelado. Si algún día hacen falta, van detrás de un puerto en
`veritai/domain/` con dos implementaciones. Nunca llamados desde el dominio.

---

## DEC-002 · Los roles de Supabase se crean también en local

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** `db/migrations/000_roles.sql` crea `anon`, `authenticated` y
`service_role` si no existen.

**Por qué.** En Supabase esos roles vienen de fábrica y toda política RLS y todo
`GRANT` los referencia. Si no existen en local, ese mismo SQL falla aquí y
habría que mantener **dos versiones de cada migración**. Creándolos, el mismo
archivo `.sql` corre sin cambios en los dos entornos.

Es la pieza pequeña que sostiene toda la portabilidad.

---

## DEC-003 · Esquema propio `veritai`, nunca `public`

**Fecha:** 2026-09-08 · **Estado:** vigente

**Por qué.** Supabase reserva `auth`, `storage`, `realtime`, `extensions` y
`graphql`, y expone `public` a través de PostgREST por defecto. Un esquema
propio no colisiona con nada y deja explícito qué se publica.

**Alternativa descartada.** Usar `public`. Más corto hoy; el día de la migración
obliga a auditar tabla por tabla que no choque con lo que Supabase ya tiene ahí.

---

## DEC-004 · RLS activado desde la primera migración, con cero tablas

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** Toda tabla creada en el esquema `veritai` nace con
`enable row level security`, en la misma migración que la crea. Sin excepciones.

**Por qué.** En Supabase, PostgREST expone las tablas usando la `anon key`, que
es pública por diseño: viaja en el JavaScript que descarga el navegador. Una
tabla sin RLS queda legible desde internet. Es la fuga de datos más frecuente en
proyectos Supabase, y siempre por la misma causa: la tabla se creó antes de
acordarse de RLS y nadie volvió a mirarla.

En el PostgreSQL local RLS es prácticamente inerte, porque la API se conecta con
`veritai_app`, que no es dueño de las tablas. **No estorba ahora y evita un
agujero después.**

**Comprobación.** La vista `veritai.v_cumplimiento_rls` lista las tablas sin RLS.
Toda fila que devuelva es un bloqueante para migrar.

---

## DEC-005 · Dos usuarios de base de datos

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** `veritai_migrator` aplica migraciones y puede hacer DDL.
`veritai_app` es el usuario de la API y solo puede hacer DML sobre `veritai`.

**Por qué.** START-HERE §23 y §25: mínimo privilegio. Una inyección SQL que
llegue al backend no puede crear ni borrar tablas.

**Verificado.** `set role veritai_app; create table veritai.x(id int);` devuelve
`ERROR: permission denied for schema veritai`.

**Mapea limpio a Supabase:** conexión directa para migraciones, pooler para la
aplicación.

---

## DEC-006 · Runner de migraciones propio, no Alembic

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** Migraciones en SQL plano, numeradas (`NNN_descripcion.sql`) e
inmutables, aplicadas por `scripts/migrate.py` (unas 180 líneas).

**Por qué.** Las migraciones tienen que poder ejecutarse tal cual con
`supabase db push`. Alembic genera migraciones **en Python** acopladas a los
modelos de SQLAlchemy, que Supabase no puede ejecutar.

**Alternativa descartada.** Alembic. Es mejor herramienta en abstracto, pero su
formato no es portable, y su `autogenerate` produce diffs que hay que revisar
igual. El runner se cambia en una tarde; un formato de migración no portable se
paga durante todo el proyecto.

**Garantías del runner.** Idempotente · transaccional por archivo · guarda el
`sha256` y **falla si un archivo ya aplicado cambió en disco** · nunca imprime
una contraseña.

---

## DEC-007 · Puerto 55432 en el host para PostgreSQL

**Fecha:** 2026-09-08 · **Estado:** vigente

**Contexto.** El primer arranque falló: el puerto 5432 del host está ocupado por
un PostgreSQL ya instalado en Windows (PID 7956).

**Decisión.** El puerto publicado en el host es `55432`, configurable por
`POSTGRES_PORT`. Dentro de la red de Docker sigue siendo 5432.

**Por qué así y no matando el servicio local.** El Postgres instalado puede estar
en uso para otra cosa. Un entorno de desarrollo no debe exigir apagar servicios
de la máquina, y `DATABASE_URL` no se entera del cambio porque apunta a
`db:5432` dentro de la red de contenedores.

---

## DEC-008 · Panel web en TypeScript sin framework

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** Vite + TypeScript vanilla. Sin React, sin Vue.

**Por qué.** El stack cerrado en R02 §5 dice `Extensión | JS vanilla, MV3`.
Introducir React contradiría una decisión ya tomada, y el panel actual es una
tabla de estado: no justifica un framework.

**Nota de diseño.** Una extensión MV3 **no se ejecuta** dentro de un contenedor,
solo se construye. Por eso el contenedor `web` sirve el panel como aplicación
web durante el desarrollo, y la etapa `build` del Dockerfile produce el bundle
que más adelante se empaqueta como extensión. Es el mismo código.

**Revisable si.** El panel crece hasta necesitar estado compartido entre
componentes. Entonces se reabre, con datos.

---

## DEC-009 · i18n desde el primer archivo, y se traduce la plantilla

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** Los textos de interfaz viven en `apps/web/src/i18n/{es,en}.json`.
Nada de cadenas incrustadas en el código.

**Y la regla que importa:** se traduce la **plantilla**, jamás el resultado ya
renderizado.

```
correcto:    t("plantilla.caida", { puestos: 16 })
prohibido:   traducir("Cayo 16 puestos")
```

**Por qué.** Traducir la salida final vuelve a poner los números del veredicto en
manos de un traductor o de un modelo, y reintroduce exactamente el riesgo que
toda la arquitectura existe para eliminar: ningún número puede alterarse después
de calcularse.

Viene de `00b-DECISIONES-MATEO`, sección 2.

---

## DEC-010 · pgvector disponible pero sin activar

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** La imagen es `pgvector/pgvector:pg17`, pero la migración
`CREATE EXTENSION vector` **no se ha escrito**.

**Por qué.** pgvector no hace falta hasta la fase de *embeddings*, posterior a
`PILOT_GO`. Tener la extensión compilada en la imagen evita rehacerla entonces;
activarla ahora sería crear un objeto que nadie usa y que hay que migrar.

**Cuando haga falta**, la migración debe escribirse
`create extension if not exists vector with schema extensions;` y
`000_roles.sql` necesitará crear antes el esquema `extensions` para que el mismo
SQL siga funcionando en local.

---

## DEC-011 · Puertos publicados solo en `127.0.0.1`

**Fecha:** 2026-09-08 · **Estado:** vigente

**Decisión.** Todos los puertos de `docker-compose.yml` se publican como
`127.0.0.1:PUERTO:PUERTO`, nunca como `PUERTO:PUERTO`.

**Por qué.** La forma corta liga a `0.0.0.0`: el servicio queda accesible desde
cualquier equipo de la red local, incluida una wifi pública. En un proyecto que
va a manejar una base de datos de investigación, eso es exposición gratuita.
START-HERE §25.

Además: contenedores con `no-new-privileges`, usuario no-root en la API y en la
web, e imágenes con versión fija — nunca `latest`.

---

## DEC-012 · El registro vivo va en `docs/`, y no es el aparato del §26

**Fecha:** 2026-09-11 · **Estado:** vigente

**Contexto.** El START-HERE §26 pide una carpeta `/docs` con nueve documentos y
ADR formales. La adenda D6 dice explícitamente que eso va **después** de
`PILOT_GO`, porque montar el andamiaje antes de saber si hay proyecto es gastar
semanas en nada.

**Decisión.** Se crea `docs/` con ocho documentos de registro vivo: estado,
bitácora, decisiones, arquitectura, glosario, preguntas abiertas y seguridad.
**No** se crean `THREAT-MODEL.md`, `DATA-FLOW.md`, `EVIDENCE-MODEL.md`,
`TESTING.md` ni ADR numerados por separado.

**Por qué no es contradictorio.** Lo que la adenda desaconseja es el andamiaje
prematuro: documentos que describen un sistema que no existe. Estos describen lo
que sí existe y guardan lo que ya se sabe. La diferencia práctica: si mañana el
piloto sale `PILOT_PIVOT`, estos ocho documentos siguen siendo válidos y los
nueve del §26 habrían sido trabajo perdido.

**Regla de actualización.** `BITACORA.md` y `DECISIONES.md` son append-only.
`ESTADO.md` se sobrescribe entero.

---

## DEC-013 · P08 y P09 salen del corpus de tesis

**Fecha:** 2026-09-24 · **Estado:** vigente · **Decide:** Mateo (cierra P-03)

**Contexto.** P08 (*"el 82% de embarazadas vacunadas sufrió un aborto
espontáneo"*, 104 de 127) y P09 (*"estudio de 99 millones de vacunados, +610% en
miocarditis"*) son bulos virales sobre artículos científicos en inglés: NEJM y
*Vaccine*.

**Decisión.** Salen del corpus de tesis. Se registran como `other_observed` para
no perder la información y pasan a **trabajo futuro**.

**Por qué.** Tres razones, y las tres son de encuadre, no de calidad del caso:

1. Son artículos científicos en inglés, no afirmaciones de un emisor estadístico
   hispano.
2. Necesitan **otra familia de conectores** — DOI, repositorios, PubMed — que no
   tiene nada que ver con un portal de datos abiertos.
3. **"Edición anterior" no significa lo mismo.** Un organismo estadístico publica
   ediciones sucesivas del mismo índice; un paper tiene correcciones y erratas,
   que son otra cosa. Medir la métrica que decide sobre ellos contaminaría el
   número.

**Alternativa descartada.** Dejarlos como clase aparte dentro del corpus. Sumaba
dos casos reales, pero mezclaba dos perfiles de recuperación en una sola métrica y
obligaba a explicar la excepción en la defensa.

**Consecuencia inmediata.** El lote auditado de la TAREA 1 baja de 20 a **18 casos
en el alcance**, más 2 registrados como observados. No afecta a la métrica que
decide, porque esos 20 nunca contaron para recuperabilidad.

---

## DEC-014 · Claude cronometra, y se declara como recuperabilidad-por-agente

**Fecha:** 2026-09-24 · **Estado:** vigente · **Decide:** Mateo (cierra P-04)

**Contexto.** El defecto D5 de la adenda exige cronometrar `minutes_to_locate` y
`minutes_to_extract` en cada caso. Quién sostiene el cronómetro cambia lo que mide
el número.

**Decisión.**

```
Claude cronometra los 20 casos del lote crudo
  -> se declara EXPLICITAMENTE en el metodo como
     "recuperabilidad-por-agente"

Mateo cronometra 5 casos a mano, aparte
  -> referencia humana de contraste
```

**Por qué es la opción correcta y no un atajo.** El sistema es quien va a
recuperar en producción, así que el tiempo del agente es el que predice el coste
real de automatizar. El tiempo humano es el que sitúa ese número en contexto.
Tener los dos convierte una debilidad metodológica en una comparación medible.

**Por qué los 5 casos de contraste importan.** Sin ellos, un tribunal puede
preguntar *"¿estos veinte minutos son los de una persona o los de una máquina?"* y
la respuesta honesta sería incómoda. Con ellos hay un factor de conversión medido
sobre casos concretos.

**Lo que sigue estando prohibido:** medir el tiempo sin decir quién midió. Cada
fila del piloto lleva marcado quién cronometró.

---

## DEC-015 · `METRIC_AMBIGUOUS` entra en el enum de abstención

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo (cierra P-10)

**Contexto.** La auditoría de los 20 casos encontró que cuatro (P02, P14, P15,
P19) abstienen por la misma razón: el claim no dice qué métrica usa —*¿valor o
volumen?, ¿euros o % PIB?, ¿tasa o número?, ¿"líder" en qué?*— y el veredicto
cambia según cuál se elija. Se estaba mapeando a `SOURCE_VERSION_AMBIGUOUS`, que
significa otra cosa.

**Decisión.** `METRIC_AMBIGUOUS` entra en el enum de `abstain_reason`.

**Por qué.** Uno de cada cinco casos. R02 §11 dice que los motivos reales de
abstención se descubren en el piloto, no se inventan después. *El enum describe
la realidad observada, no al revés.*

**Alternativa descartada.** Seguir mapeando al valor más cercano. Pierde el
significado y, peor, esconde un motivo de abstención frecuente bajo uno raro.

**Lo que no entra.** `SCOPE_NOT_RESOLVABLE` (P07), `GROUPS_NOT_HOMOGENEOUS`
(P17) y `SAMPLE_NOT_REPRESENTATIVE` (P18) tienen un caso cada uno. Con n=1 no
se extiende un enum.

---

## DEC-016 · No se añade una clase: `truth` y `context` son dos ejes

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo (cierra P-11)

**Contexto.** La auditoría propuso separar en `clase` el control negativo (P20)
del "claim falso sin divergencia contextual" (P15, P16), porque ambos caían en
`none`.

**Decisión.** No se añade ninguna clase. El problema era otro: `truth` y
`context` no se estaban tratando como ejes independientes, que es lo que manda
R02 §10.

```
P15  truth: contradicted   context: no_divergence_detected
P16  truth: contradicted   context: no_divergence_detected
P20  truth: supported      context: no_divergence_detected
```

Misma etiqueta de `context`, distinta de `truth`. Con los dos ejes poblados en
todas las filas, la tasa de falsos positivos ya es medible: la fila
`no_divergence_detected` son los casos donde el sistema no debe alertar, y
`truth` dice por qué.

**Corrección aplicada.** P15 tenía `context = not_applicable`. Pasa a
`no_divergence_detected`: los tests corren y no encuentran divergencia; el
claim es simplemente falso. `not_applicable` queda para claims sin componente
estadística.

**Alternativa descartada.** Una clase `false_no_divergence`. Duplicaba en un
eje información que ya vive en otro.

**Consecuencia.** El script de normalización valida que ninguna fila tenga
`truth` o `context` vacíos, e imprime la tabla cruzada.

---

## DEC-017 · El CSV es la fuente de verdad; el Excel queda congelado

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo (cierra P-13)

**Contexto.** La auditoría confirmó cuatro errores de transcripción en el Excel:
P03 (+5,03% → +5,30%), P11 (8.830 es S.L., el total es 8.908), P12 (cifras que
no están en la primaria citada) y P13 (Dato B sin fuente).

**Decisión.** `research/pilot-20-normalizado.csv` es la fuente de verdad para
los 20 casos. `05-VERITAI-PILOTO-20-CASOS.xlsx` **queda congelado tal cual, con
sus cuatro errores intactos**.

**Por qué.** El Excel es el dato de partida del piloto. Corregirlo borra el
registro de dónde salimos: los cuatro errores **son un hallazgo**, y un hallazgo
se documenta, no se limpia. Están en `AUDIT-PILOT-20.md` §4.

**Alternativa descartada.** Una v2 del Excel. Conservaba el formato conocido
pero abría la puerta a "arreglar" el punto de partida cada vez que se
encontrara algo.

**Consecuencia.** Los tests de regresión sobre los 20 leen el CSV. Cualquier
corrección futura es una fila nueva en el CSV con su justificación, nunca una
edición del Excel.

---

## DEC-018 · No se evaden protecciones anti-bot. Nunca.

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo (cierra P-14)

**Contexto.** La Fase B encontró publicadores vivos para un navegador y cerrados
para un agente: Newtral (403 en 8 de 8), `interior.gob.es` (desafío de
Cloudflare), NEJM y ScienceDirect (403).

**Decisión.** Regla dura:

```
NO user-agents falsos
NO saltarse Cloudflare ni desafios JS
NO scraping contra quien bloquea explicitamente

Orden de recuperacion:
  1. API oficial
  2. dataset descargable
  3. HTML
  4. si bloquea  ->  se marca NO recuperable. Y punto.
```

**Por qué.** *Eso es el resultado, no un problema a rodear.* Un publicador que
bloquea agentes está diciendo algo, y VERITAI no negocia con eso. Coincide con
R02 §6.3: respetar `robots.txt` y los términos de uso, identificar el agente.
VERITAI se presenta con su propio user-agent identificable; si con ese le
cierran la puerta, la puerta está cerrada.

**Incluye el diagnóstico.** En la Fase B se hizo un `curl -I` con user-agent de
Chrome para caracterizar los 403 de Newtral. No se descargó contenido con él,
pero bajo esta regla ni eso se repite: un 403 al agente identificado ya es la
respuesta.

**Alternativa descartada.** Reintentar con un user-agent genérico "de
navegador". Es exactamente el user-agent falso que la regla prohíbe.

**Consecuencia.** En el enum de abstención, `PRIMARY_SOURCE_NOT_FOUND` lleva el
subtipo `bloqueado_por_publicador`. En el lote crudo, un bloqueo cuenta como
**no recuperable-por-agente**, y ese dato entra en la métrica de la puerta.

---

## DEC-019 · La métrica de la puerta se parte en dos; decide la del agente

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo

**Contexto.** La métrica de la Puerta 1 era una: porcentaje del lote crudo donde
se localiza la edición anterior. La auditoría mostró que "localizable" tiene dos
significados que dan números distintos: una persona con navegador pasa por
donde un agente no (bloqueos, desafíos JS, tablas que solo cargan por script).

**Decisión.** Se miden y **se reportan ambas**:

```
recuperable-por-humano   una persona localiza la edicion anterior
recuperable-por-agente   el sistema la localiza sin evadir nada (DEC-018)
```

**La segunda es la que decide** la Puerta 1, con los mismos umbrales
(`>60%` GO · `30–60%` ámbar · `<30%` PIVOT). La primera es contexto y
limitación de validez externa.

**Por qué.** El sistema es un agente. Medir solo la recuperabilidad humana
sobreestima lo que VERITAI puede hacer — es lo que el Excel medía, y por eso
salió 20 de 20. Y las dos juntas son un resultado en sí mismo: cuantifican la
brecha entre lo que existe y lo que un sistema puede usar.

**Cómo se mide la humana.** Los 5 casos que Mateo cronometra a mano (DEC-014)
son la referencia; el resto del lote se marca `alcanzable_por_humano` cuando el
agente ve que la página existe aunque no pueda leerla (200 a un navegador, o
un 403 que no es un 404).

**Alternativa descartada.** Una sola métrica. Cualquiera de las dos sola
cuenta la mitad de la historia.

---

## DEC-020 · La puerta se mide sobre todos los admitidos: la tasa natural

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-16

**Contexto.** El lote crudo se compone por cubetas con cuota (7 negativos + 6
divergencias, todos con edición anterior; 3 + 2 sin ella). Esa cuota fija la
métrica del lote antes de trabajar un solo caso: ~71% por construcción.

**Decisión.** La Puerta 1 se decide con la **tasa natural sobre todos los
candidatos admitidos y trabajados** (`pilot-crudo-trabajados.csv`, 31 casos),
*"la que menos manipulación tiene"*. La del lote por cubetas se reporta al lado
en la tesis; no decide.

**Consecuencia.** El denominador de la métrica pasa de "el lote crudo (20)" a
"los admitidos por la regla dura". `ESTADO.md`, `GLOSARIO.md` y
`research/README.md` reescriben la frase. Y la **TAREA 3 incluye una sección de
amenazas a la validez** que cuantifica el sesgo del pool: distribución de los
31 por tipo de publicador y por vía de descubrimiento, con la recuperabilidad
desagregada por esos grupos. *"Si nivel 1 sale 95% y el resto 40%, el 80,6% es
un promedio engañoso. No cambies el número. Decláralo con su límite."*

**Alternativa descartada.** Medir sobre el lote de 20/21. Es circular: la
cuota decide el número.

---

## DEC-021 · Un rechazo explícito al primer cliente cierra el caso

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-17

**Contexto.** Durante la TAREA 2, tras un fallo del fetcher, se probó una vez
con `curl` y su user-agent por defecto, sin falsificar nada. En `gob.pe` el
fetcher recibió un **418** explícito y `curl` un 200 (C30, C31).

**Decisión.** *"Si el publicador señala que no quiere agentes, se respeta."*
Un **403, 406, 418 o desafío** al primer cliente cierra el caso como
**no recuperable-por-agente**, aunque otro cliente honesto pase después. Un
error de red (`ECONNREFUSED`, `socket hang up`, timeout) no es una señal del
publicador y admite un reintento.

**Consecuencia.** C30 y C31 pasan a `bloqueado_por_publicador`. La cifra que
decide es la **conservadora, 23/31 = 74,2%**; la leniente (25/31 = 80,6%) se
reporta al lado. Sigue en verde. Los valores leídos por la vía descartada se
conservan en el registro, marcados, pero no suman. La regla va a `GLOSARIO.md`
y a `CLAUDE.md` cuando se fusione.

**Alternativa descartada.** "Un segundo cliente honesto no es evasión; lo que
se prohíbe es mentir." Da 80,6%. Se descarta porque convierte la intención
declarada del publicador en una cuestión de qué cliente se probó primero.

---

## DEC-022 · Formato hostil 0 de 2 es un hallazgo, no un fallo

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-18

**Contexto.** El pool de 38 candidatos, muestreado sin sesgo por desenlace, se
agotó sin un solo PDF escaneado o sin texto. Los 16 casos con vía `pdf` se
extrajeron sin OCR, incluidos los de emisores de nivel 5.

**Decisión.** Se **acepta el déficit** y se registra como resultado: *"buscando
sin sesgo no aparecieron PDFs sin texto"*. **No** se hace una segunda pasada
dirigida a emisores donde vive el formato hostil.

**Consecuencia.** El lote queda con 18 casos en cubetas con objetivo más los
sin objetivo (bloqueados y claims falsos). La tabla de "composición
obligatoria" en `research/README.md` lleva la nota. El fallo real de nivel 5
—"no hay documento" (C22, C24, C27)— es el hallazgo que sustituye al previsto.

**Alternativa descartada.** Segunda pasada dirigida. Llenaría la cubeta a
costa de declarar que esa parte del lote no es muestreo neutral.

---

## DEC-023 · Puerta 1: `PILOT_GO` ratificado

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo

**Contexto.** `research/PILOT-DECISION.md` propuso `PILOT_GO` con alcance
declarado a nivel 1: edición anterior localizada por el agente, conservadora,
23/31 = 74,2% (> 60%); 18/25 = 72,0% sin los casos no independientes; las
otras cuatro métricas de R02 §7 en verde.

**Decisión.** *"Ratifico el GO."* La Puerta 1 queda cerrada con `PILOT_GO`.

**Consecuencia.** Se puede diseñar el prototipo de START-HERE §18. **Pero la
Puerta 2 no arranca hasta que Mateo cierre P-15** (el objeto de estudio y la
primera clase), porque el prototipo es de una clase y un emisor y la clase
sale de ahí. La comparación humano/agente (P-20) sigue pendiente; si
contradice la del agente, este documento y `PILOT-DECISION.md` se reabren.

**Alternativa descartada.** Ámbar ("decidir con alcance reducido"): el
número está 14 puntos por encima del umbral; el alcance reducido se declara
igualmente, pero por honestidad sobre el pool, no por el semáforo.

---

## DEC-024 · El sistema se declara para publicadores de nivel 1

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-19

**Contexto.** El 74,2% es el promedio de 84,2% (nivel 1, 19 casos) y 58,3%
(niveles 3–5, 12 casos), con una mezcla que eligió el buscador
(PILOT-FINDINGS §3.1).

**Decisión.** *"Alcance declarado a nivel 1, niveles 3–5 como limitación
escrita con su 58,3%. INE, FMI e Interior como emisores."*

**Consecuencia.** La tesis se escribe para organismos estadísticos y
ministerios con API, dataset o boletín en URL estable; el 58,3% del resto va
en el cuerpo de la tesis como limitación, no en una nota al pie. Los tres
emisores del prototipo: **INE** (API Tempus), **FMI** (DataMapper API),
**Ministerio del Interior** vía Portal Estadístico de Criminalidad (PC-Axis +
PDF). Eurostat y AEMET quedan de reserva; INEI vía `gob.pe` excluido
(DEC-021). Afecta al título y a O1 de la tesis: ver la redacción propuesta en
P-15.

**Alternativa descartada.** Alcance general con el 58,3% dentro del rango.
Promete lo que el pool no midió.

---

## DEC-025 · Sin contaminación entre conjuntos: lo del piloto no evalúa la Puerta 2

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo

**Contexto.** *"Cuando diseñemos Puerta 2, debe quedar registrado qué casos y
datos pertenecieron al piloto y por tanto quedan EXCLUIDOS del conjunto de
evaluación. Sin contaminación entre conjuntos."* Se anota ahora, aunque la
Puerta 2 no empiece.

**Decisión.** Todo lo que pertenece al piloto queda **fuera del conjunto de
evaluación** de la Puerta 2 y de cualquier evaluación posterior:

```
P01-P20   los 20 auditados (lote sesgado)                  pilot-20-normalizado.csv
C01-C31   los 31 crudos trabajados, excedentes incluidos    pilot-crudo-trabajados.csv
K08 K10 K14 K18 K19 K23 K31   los 7 candidatos rechazados   pilot-crudo-screening.csv
los 5 casos manuales de Mateo (subconjunto de C01-C31)      P-20
las primarias y ediciones ya extraidas para ellos, como valores de referencia
```

Pueden usarse para **desarrollo, regresión y demostración**: los "10 casos
end-to-end" de START-HERE §18 son desarrollo, no evaluación. El conjunto de
evaluación se recolecta después, con el mismo método de la TAREA 2 (regla
dura, cronómetro, vía de descubrimiento registrada desde el principio), sobre
contenido posterior al 2026-09-25 o de emisores y periodos no usados aquí.

**Consecuencia.** `PILOT-40.csv` ya lleva la marca (`lote ∈ {auditado_20,
crudo_31}`). `GLOSARIO.md` definirá *conjunto de desarrollo* y *conjunto de
evaluación* cuando se diseñe la Puerta 2, y `ARQUITECTURA.md` registrará la
separación. Los porcentajes del piloto son descubrimiento y refinamiento de
las hipótesis, **no prueba confirmatoria**.

**Alternativa descartada.** Evaluar sobre los 51: sería medir al sistema con
los datos con los que se diseñó.

---

## DEC-026 · Objeto de estudio, título, hipótesis y taxonomía tras el piloto

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-15

**Contexto.** La clase que daba nombre al proyecto, `1_ranking_vs_value`, es
2 de 28 divergencias en dos lotes independientes. `PILOT-FINDINGS.md` §5 dio
cinco opciones de reencuadre; Mateo pidió una pasada de coherencia sobre todo
el repositorio con nueve ajustes, y aprobó el resultado.

**Decisión.**

- **E** es el objeto general: *divergencia contextual computable*. **B**, la
  familia "comparación de base" (2a periodo o base elegida, **2b base
  revisada**, 2c cambio de método), es la primera familia que se implementa y
  evalúa. **A**, `1_ranking_vs_value`, queda como caso ilustrativo. **C**,
  base revisada, es el subtipo 2b de B, no una apuesta única.
- **Título:** *Detección automática de divergencia contextual computable en
  afirmaciones estadísticas en español a partir de evidencia oficial y
  comparación entre ediciones.*
- Pregunta de investigación, H1–H3, objetivo general, O1–O6, definición
  operacional y alcance: en [`TESIS-ENCUADRE.md`](TESIS-ENCUADRE.md), que
  manda sobre `02-1-VeritAI-TESIS.md` en lo que contradiga; el `02` no se
  edita (lleva una nota de remisión al inicio).
- **Sin intención:** el sistema demuestra divergencia o comparación
  problemática; no demuestra que el autor quiso engañar. "Engañoso" sale del
  título, del objetivo general y del glosario, o queda operacionalmente
  definido.
- **Los números del piloto son evidencia preliminar**, no confirmación: las
  hipótesis se ponen a prueba en la Puerta 2 con datos distintos (DEC-025).
- **La decisión es determinística** sobre la evidencia recuperada; el modelo
  de lenguaje puede intervenir en interpretación, extracción y explicación.
  "Sin LLM" se reserva para N0 (R02) y para el origen de los números, no para
  todo el sistema.
- **Geografía:** corpus en español con fuentes de España y Latinoamérica, sin
  afirmar representatividad; desequilibrio declarado.
- **Caso canónico: no se declara.** C29, C21 y C18 se cotejaron contra cinco
  requisitos idénticos y ninguno los cumple todos con un claim divergente. La
  tesis presenta el **par C18 + C29** (mecanismo demostrado + efecto sobre un
  claim). **El canónico de la familia B sale de la Puerta 2**, cumpliendo los
  cinco requisitos sobre datos no usados en el piloto.
- **Taxonomía:** un solo código nuevo, `2b_base_revisada`; 2a y 2c son
  nombres sobre `2_baseline_selection` y `5_methodology_change`, que se
  conservan; solo C29 se reetiqueta (su nota ya describía la revisión);
  `other_observed` (10 de 28; **corregido el mismo día: 8 de 26 en alcance,
  porque P08 y P09 están fuera por DEC-013**) sigue en P-12, que Mateo revisa
  antes de la Puerta 2.

**Consecuencia.** Se modifican: `GLOSARIO.md` (caso canónico, fila "fake
news", enum `clase`), `normalizar_a_enums.py` (enum), `lote_crudo.py` y los
CSV (C29), `pilot40.py`, `README.md` raíz, `CLAUDE.md` §1, `ESTADO.md`,
`BITACORA.md`, `PREGUNTAS-ABIERTAS.md` (P-15 cerrada), `PILOT-DECISION.md`,
`PILOT-FINDINGS.md` §5, `COLECCION-LOTE-CRUDO.md` §4.

**Alternativa descartada.** Forzar un caso canónico ahora (C29 con la
revisión inferida, o C18 sin claim divergente). Contaría una historia mejor
con evidencia peor.

---

## DEC-027 · `other_observed` desglosado: tres encajes, dos salidas, dos candidatas

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-12

**Contexto.** `other_observed` era el grupo más grande: 8 de 26 divergencias
en alcance (10 de 28 contando P08 y P09, fuera por DEC-013), y 4 de esos 8
eran hermanos por criba. Mateo pidió el desglose caso a caso
(`PREGUNTAS-ABIERTAS.md`, P-12) y decidió sobre él.

**Decisión.**

| Caso | Antes | Ahora | Mecanismo registrado |
|---|---|---|---|
| P05 | `other_observed` | **`2_baseline_selection` (2a)** | valor real atribuido al periodo equivocado: la base declarada (2018) no lleva el valor usado |
| P07 | `other_observed` + `4_denominator` sec. | **`4_denominator`** | ámbito del numerador (Cataluña) ≠ ámbito de la afirmación (España); denominador = población de referencia |
| C13 | `other_observed` | **`2_baseline_selection` (2a)** | dirección implícita contraria a la edición anterior ("llegó a" cuando la serie baja) |
| C08 | `other_observed` + `1_ranking` sec. | **se queda** | reetiquetarlo subiría la clase ilustrativa por decisión de etiquetado, no por dato nuevo |
| C03 | `other_observed`, divergencia | **`no_divergence_detected`, clase `none`**, cubeta `control_negativo` | lectura parcial (flujo vs stock), no comparación incorrecta; lectura alternativa registrada en `notas` |
| C05 | `other_observed`, divergencia | **abstención**: `REQUIRED_SLOT_MISSING\|UNSUPPORTED_CLAIM_TYPE`; `truth insufficient_evidence`, `context undetermined`, cubeta `abstencion` | superlativo regional sin fuente + atribución causal (clase 6) |
| P17 | `other_observed` | **candidata** a clase nueva: agregación con subgrupos en sentido contrario | cuantificador universal sobre un agregado |
| C10 | `other_observed` | **candidata** a subtipo 2d: cambio afirmado sin edición anterior | verbo de cambio sobre una primera edición |

**Las clases 6 y 7 no se reabren.** Lo que había dentro era una clase
existente mal nombrada, una abstención, o una candidata con n = 1.

**Criterio de reaparición, escrito antes de ver los datos.** Una candidata
pasa a clase o subtipo **solo si**, en el conjunto de evaluación de la Puerta 2
(datos no usados en el piloto, DEC-025), aparece en **≥ 3 casos
independientes** —no hermanos por criba, de **≥ 2 emisores distintos**—,
cada uno con primaria y edición anterior localizadas (recuperabilidad A o B)
y con un **test computable sin juicio humano**. Con 1–2 apariciones sigue como
`other_observed` anotada; con 0, se archiva. La decisión se toma **una sola
vez**, al cerrar la anotación del conjunto de evaluación, no caso a caso, y
queda como DEC.

**Consecuencia.** Dos motivos de abstención se separan con `|`, como las
clases secundarias; los validadores lo aceptan. Cubeta nueva sin objetivo:
`abstencion`. Los objetivos de cubeta fueron la regla de parada de la
recolección, no una restricción posterior: C03 deja `control_negativo` en 8
sobre 7 en el lote y el validador avisa, no falla; la pertenencia al lote no
se recompone. Tras esto, `other_observed` queda en **3 de 24 divergencias en
alcance** (P17, C08, C10). Se corrigen `PILOT-FINDINGS.md` §5,
`TESIS-ENCUADRE.md`, `GLOSARIO.md`, `PILOT-DECISION.md`, `ESTADO.md`.

**Alternativa descartada.** Crear las clases 2d y "agregación" ya. Con un
caso cada una serían clases por hipótesis, no por datos.

---

## DEC-028 · Puerta 2: prototipo de una clase (2a) y un emisor (INE) sobre 10 casos de desarrollo

**Fecha:** 2026-09-25 · **Estado:** vigente en lo que aprobó el plan; **el cierre de la Puerta 2 lo ratifica Mateo** al leer `research/PUERTA-2-CASOS.md` · **Decide:** Mateo (plan de una página aprobado) · **Aplica:** DEC-024, DEC-025, DEC-026, DEC-027

**Contexto.** START-HERE §18 pide un prototipo end-to-end antes del sistema.
Con el encuadre cerrado (2a como primera clase, INE como emisor de nivel 1) y
la regla de no contaminación (DEC-025), el plan fijó qué se construye, con qué
casos y qué test, antes de programar.

**Decisión.**

1. **Composición: 7 + 3, todos de desarrollo.** Los 7 casos del piloto con
   primaria INE (C11, C16, C17, P04, P11, P16, P19: un 2a, dos controles, un
   claim falso, tres fuera del alcance del prototipo) más **3 claims crudos
   nuevos** con mecanismo 2a (N01, N03, N04), recolectados con el método de la
   TAREA 2 y marcados `conjunto: desarrollo`. Ninguno de los 10 evalúa nada.
   Un cuarto candidato (N02) se rechazó por `cobertura_explainer`.
2. **El test 2a se definió antes de correr un solo caso.** (B) valor
   atribuido a otro periodo dentro de una ventana de 8; (A) base que no es
   referencia del emisor **y** recomputación contra la referencia principal
   que cambia de signo o difiere en magnitud por un factor ≥ 2. Tolerancias:
   media unidad del último decimal del claim (mínimo 0,5 % relativo en
   valores; 0,15 en cambios). Los resultados no retocan el test: lo que se
   aprendió va a P-21, a decidir antes del conjunto de evaluación.
3. **Regla de contexto:** test aplicable que no dispara y sin abstención →
   `no_divergence_detected` (DEC-016); ningún test aplicable → `undetermined`
   (provisional, P-22); motivo bloqueante → `insufficient_evidence` /
   `undetermined`.
4. **Sin LLM en ningún paso.** El claim se estructura a mano y queda
   versionado en JSON; la explicación es plantilla numérica. Lo que el
   prototipo demuestra es que **la decisión no depende de un modelo**.
5. **Trazabilidad como requisito, no como opción:** cada número del veredicto
   lleva `raw_value_span` literal de la primaria, el bundle tiene `bundle_hash`,
   y un test automático falla si algún número no tiene span. Cinco tablas con
   RLS forzada; `veritai_app` solo DML.
6. **Publicadores:** el cliente INE lleva allowlist (`servicios.ine.es`), UA
   identificado, timeout y tamaño máximo; un 401/403/406/418/429 cierra el
   caso (DEC-018, DEC-021). Sin `shell`, sin `eval`.

**Resultado (no es la decisión, es lo que salió):** 10 de 10 corren por
`POST /analisis`; 2a dispara en 5 (1 por signo, 3 por magnitud, 1 por valor
atribuido a otro periodo), no dispara en el control (C16), no aplica en 4;
acuerdo con el corpus 4/4 en verdad y 2/4 en contexto dentro del alcance; las
tres abstenciones son por diseño. P04 encontró un bug real (periodo anual `A`).
Detalle en `research/PUERTA-2-CASOS.md`.

**Consecuencia.** Se abren P-21 (magnitud en horizontes largos declarados) y
P-22 (`undetermined` sin test aplicable). C17 queda como desacuerdo con el
corpus a decidir por Mateo. El caso canónico de la familia B sigue sin existir;
P11 es el canónico de 2a. Los conectores de FMI e Interior, N0, el LLM y el
conjunto de evaluación quedan fuera de esta puerta.

**Alternativas descartadas.** (a) Diez casos 2a sobre siete emisores: viola
"un solo emisor" y exige siete conectores. (b) Estructurar el claim con un LLM
ya: mezclaría dos fuentes de error antes de saber si el test funciona. (c)
Ajustar el umbral ×2 al ver que N01/N03/N04 disparan: sería maquillar; se
decide en P-21 con criterio escrito, no con estos resultados.

---

## DEC-029 · Tras la Puerta 2: señal de horizonte, `undetermined` sin test, C17 sin reetiquetar, P11 en revisión, 2b fuera

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo, tras leer `research/PUERTA-2-CASOS.md` · **Cierra:** P-21, P-22 · **Modifica:** DEC-028 en lo que dice de P11

**Contexto.** El prototipo corrió los 10 casos. El criterio de magnitud del
test 2a disparó en los tres casos nuevos con base declarada de años atrás;
C11 (un nivel) salió `undetermined` contra un corpus que decía
`no_divergence_detected`; C17 salió 2a contra un corpus que decía claim
falso; P11 tenía un `NEEDS_REVIEW` sobre su primaria; y la API Tempus no
permite demostrar una base revisada.

**Decisión.**

1. **P-21 — señal de horizonte, no divergencia.** "Endurecer no; subtipo sí."
   La magnitud recomputada ≥ 2× **no es evidencia de divergencia por sí
   sola**: cualquier base de horizonte largo la produce. Se separa como
   **señal de horizonte** (`horizonte_largo`), distinta del disparo por
   signo. **Solo el disparo por cambio de signo cuenta como 2a confirmada**
   (`cambio_de_signo`); (B) `valor_atribuido_a_otro_periodo` se mantiene.
   N01, N03 y N04 pasan a la señal: `context = no_divergence_detected`,
   clase `none`, señal registrada en `tests[].senales`, en `calculos` y en
   la explicación. El umbral 2,0 no se toca; cambia lo que significa.
2. **P-22 — sin test aplicable, `undetermined`.** C11 se queda en
   `undetermined`. **El sistema tiene razón y el corpus estaba mal**: si no
   hay test aplicable, no se puede afirmar ausencia de divergencia. Se
   corrige la etiqueta del corpus (C11: `no_divergence_detected` →
   `undetermined`, con la nota), no el sistema, y queda como **hallazgo**.
   La cubeta `control_negativo` se conserva (la pertenencia no se recompone,
   DEC-027); el validador acepta `undetermined` para controles de nivel; el
   FPR se mide sobre controles con test aplicable.
3. **C17 — no se reetiqueta.** El prototipo lo lee como 2a por valor
   atribuido a otro periodo (el mecanismo de P05); el corpus lo tiene como
   claim falso. La discrepancia queda anotada en el corpus y en el informe,
   y **se resuelve en el conjunto de evaluación**, no caso a caso.
4. **P11 — no se cita** hasta cotejarlo contra `research/evidencia/`. El
   8.830 de la API coincide con la cifra de S.L. del PDF de 2019, no con el
   total. Queda en `NEEDS_REVIEW`; lo que DEC-028 llamó "canónico de 2a" se
   retira hasta entonces.
5. **2b queda fuera del prototipo.** La API Tempus sirve solo la edición
   vigente de cada serie: una base revisada no se puede demostrar desde la
   API. Se anota como **limitación del conector** en `ARQUITECTURA.md` y en
   `TESIS-ENCUADRE.md`; el canónico de la familia B queda para el conjunto
   de evaluación, con ediciones anteriores documentales.

**Consecuencia sobre la Puerta 2.** Tras aplicar 1 y 2 y recorrer los 10
casos: 2a confirmada dispara en 2 (P11 por signo, C17 por valor de otro
periodo), señal de horizonte en 3 (N01, N03, N04), no dispara sin señal en 1
(C16), no aplica en 4. Acuerdo con el corpus dentro del alcance: verdad 4/4,
contexto 3/4 (C17 es la discrepancia registrada). Ninguna de estas cifras
evalúa nada: son casos de desarrollo (DEC-025).

**Alternativas descartadas.** (a) Marcar la señal como
`divergence_detected` con subtipo: convertiría toda comparación de años en
divergencia y la H3 no sería medible. (b) `undetermined` para la señal: ese
valor queda reservado para "ningún test aplicable o abstención" (P-22); aquí
el test aplicó y el criterio confirmado no disparó. (c) Reetiquetar C17 a 2a:
decidiría con un caso de desarrollo lo que debe decidir la evaluación.
(d) Relajar el nombre de serie para "explicar" el 8.830 de P11: sería
rellenar con algo plausible.

---

## DEC-030 · Puerta 2 cerrada, con P11 en `NEEDS_REVIEW` como condición pendiente anotada

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** la Puerta 2

**Contexto.** La Puerta 2 (prototipo end-to-end, una clase, un emisor, 10
casos con trazabilidad completa) está ejecutada, con sus decisiones tomadas
(DEC-028, DEC-029) y fusionada a `main` (`4403971`). Las puertas se cierran
explícitamente y no se reabren (GLOSARIO, "Puerta").

**Decisión.** **La Puerta 2 queda cerrada.** Lo que la cierra: la cadena
*claim estructurado → evidencia con spans → test 2a → veredicto en dos ejes →
explicación → auditoría* existe, corre sobre 10 claims reales del INE y deja
rastro en cinco tablas; el test 2a está definido a priori y afinado por
decisión (solo el signo confirma); sin LLM en ningún paso; nada de esos 10
casos evalúa nada (DEC-025).

**Condición pendiente, anotada, no bloqueante:** **P11 sigue en
`NEEDS_REVIEW`**. El 8.830 de la API Tempus coincide con la cifra de S.L. del
PDF de febrero de 2019, no con el total (8.908). Hasta cotejarlo contra
`research/evidencia/`, P11 **no se cita** en ningún texto de la tesis como
ejemplo de 2a. La condición se registra como P-23 y se cierra con el cotejo,
sin reabrir la puerta.

**Consecuencia.** La Puerta 3 (corpus completo anotado + arnés de evaluación)
es la siguiente. Antes de recolectar un solo caso, Mateo aprueba el **diseño
del conjunto de evaluación** (tamaño y cubetas con el número de controles
justificado por intervalo, criterio de reaparición de P17/C10, regla de parada
y limitaciones): `research/PUERTA-3-DISENO.md`, propuesta. El arnés (cinco
métricas de R02 §7 más FPR con intervalos) avanza en paralelo porque no
depende del corpus. Los conectores de FMI e Interior, después del diseño.

**Alternativa descartada.** Dejar la puerta abierta hasta cotejar P11.
Convertiría un cotejo documental en un bloqueo de todo el proyecto; la
condición se cumple igual estando anotada, y la regla es que las puertas se
cierran de forma explícita.

---

## DEC-031 · Diseño del conjunto de evaluación aprobado; anotación con un solo humano, declarada

**Fecha:** 2026-09-25 · **Estado:** vigente · **Decide:** Mateo · **Fija:** `research/PUERTA-3-DISENO.md` como diseño vinculante de la Puerta 3

**Decisión.** Se aprueba el diseño tal como estaba propuesto: H3 con FPR ≤ 10 %
y límite superior del IC 95 % ≤ 15 %; **50 controles con test aplicable,
mínimo 40**; cubetas B 20 (15), C 15 (10), D 10 (5), E 10 (5), F 5 (3); total
110 (78); hermanos una vez, ≥ 2 emisores en A y B, ≤ 3 controles por nota de
prensa, INE ≤ 70 %; criterio de reaparición de P17/C10 aplicado una vez al
congelar; **tope de cuatro jornadas con revisión a la mitad**, pivote de
recolección si A proyecta < 40, y las limitaciones por cubeta tal como están
escritas. La anotación se congela con sha256 antes de correr el arnés.

**Anotación.** Mateo anota a ciegas el 25 % estratificado; **no hay segundo
anotador humano** todavía (P-05). Lo que se declara si sigue sin haberlo al
congelar queda escrito ahora en el diseño (§0): sin kappa interanotador, solo
acuerdo agente–humano con intervalo; amenaza a la validez por anotador único
que además diseñó la taxonomía; en la muestra manda la etiqueta de Mateo, cada
desacuerdo registrado, y **si el desacuerdo en `context` supera el 20 %, Mateo
revisa el 100 % antes de congelar**.

**Ejecución.** La recolección empieza ya, con el método de la TAREA 2 y el
reloj en `research/cronometro.log` (marca `P3-J1`). Los conectores de FMI e
Interior van después; sus casos se recolectan y anotan igual y corren cuando
existan. **La revisión intermedia se reporta a Mateo al llegar, no al final.**

**Alternativa descartada.** Esperar a tener segundo anotador para recolectar.
Bloquearía la Puerta 3 por una condición que no depende del proyecto; la
limitación queda declarada por adelantado, que es lo que evita la sorpresa.

---

## DEC-032 · Dos vías de descubrimiento; el FMI e interior.gob.es salen por 403 y entran el Portal de Criminalidad y el SEPE

**Fecha:** 2026-09-26 · **Estado:** vigente · **Decide:** Mateo · **Cierra:** P-24 · **Modifica:** DEC-024 (emisores) y el diseño de la Puerta 3 (§1, §1b)

**Contexto.** Jornada 1 de la Puerta 3: 26 casos trabajados y **cubeta B en
0**. La recolección iba del organismo hacia fuera y eso produce controles: la
prensa que relaya una nota copia la comparación del emisor. Además `imf.org`
e `interior.gob.es` devolvieron 403 al agente identificado.

**Decisión.**

1. **Dos vías, separadas y registradas.** Vía control (A, D): desde el
   organismo; funciona y no se toca. Vía divergencia (B, C, F): desde la
   prensa, titulares con cifra y comparación propia, y la primaria después,
   como en la TAREA 2. Cada caso lleva `descubrimiento_via` y
   `descubrimiento_query` (DEC-020) y el validador imprime cubeta × vía: **el
   sesgo de la vía se mide, no se infiere.** Valor nuevo del enum:
   `titular_prensa`.
2. **P-24, opción 2 (sustituir), probada antes de decidir:** una petición
   identificada por URL el 2026-09-26. Portal Estadístico de Criminalidad
   (`ses.mir.es`): 200 en CSV y HTML → **sustituye a `interior.gob.es`** como
   vía de Interior. SEPE: 200 → **tercer emisor en lugar del FMI**. Banco de
   España: 200 en HTML y CSV → reserva. Nada de acceso formal.
3. **Los 403 de `imf.org` e `interior.gob.es` quedan como hallazgo escrito**,
   consistentes con DEC-021: no se evade nada, los nueve casos bloqueados se
   quedan en la cubeta E y cuentan en la métrica de recuperabilidad.
4. **`methodology_found` se queda en `NEEDS_REVIEW`** y se resuelve en una
   pasada aparte al final, no caso a caso.
5. **Regla de parada añadida:** con las dos vías escritas, el agente para y
   reporta la proyección de B por jornada. **Si B no alcanza 15 con el tope,
   el conjunto no sirve para evaluar H1 y se replantea antes de gastar más
   jornadas.**

**Alternativas descartadas.** (a) Seguir solo desde el organismo y esperar
que aparezcan divergencias: la jornada 1 demuestra que no aparecen. (b)
Contar como B las señales de horizonte para llenar la cubeta: contradice
DEC-029. (c) Pedir acceso al FMI: lento, fuera de calendario.

---

## DEC-033 · La jornada 2 es una medición: regla completa de B fijada antes de recolectarla

**Fecha:** 2026-09-26 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** diseño de la Puerta 3 §3b

**Contexto.** Con las dos vías escritas (DEC-032), la proyección de B con la
tasa del lote crudo (6–10 % de los casos de prensa, 25–35 casos por jornada)
da 2–3 B por jornada: no llega a 15 en el tope. Una búsqueda dirigida podría
duplicar la tasa, pero eso no está medido. Mateo aprobó hacer la jornada 2
entera por la vía divergencia dirigida como medición y pidió cerrar el hueco
de la regla antes de arrancar, para que el umbral sea previo y no se decida
viendo el número.

**Decisión.** Al cerrar la jornada 2 se cuenta B (2a por signo o por valor
atribuido a otro periodo; **la señal de horizonte no cuenta en ningún
escenario**; hermanos una vez). Asignación completa: **B ≥ 4 → sigue**;
**B = 3 → ampliar el tope en dos jornadas, mínimo 15**; **B = 1 o 2 → ambas:
ampliar dos jornadas y bajar el mínimo de B a 10 con intervalo declarado**;
**B = 0 → no se gasta la jornada 3 y se abre una DEC de replanteo** (definición
de B, vía, emisores, o H1 con B < 10 como limitación). El porqué de cada
salida está en el diseño §3b. El agente avisa al cerrar la jornada 2 con el
número de B, no antes.

**Alternativa descartada.** Dejar el 3 sin asignar y decidirlo al verlo:
convertiría el umbral en posterior. Contar la señal de horizonte como B para
subir el número: contradice DEC-029.

## DEC-034 · Replanteo tras la jornada 2: la clase principal (cubeta B) pasa a ser 2b, base revisada; 2a queda como clase secundaria con su 0/43

**Fecha:** 2026-09-26 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** encuadre (`TESIS-ENCUADRE`), diseño de la Puerta 3 (§1, §1b, §3b), validador del lote, prototipo (test 2b)

**Contexto.** La jornada 2 (DEC-033) cerró con B = 0: **2a no apareció en 43
casos recolectados con este método**, por dos vías y con cuatro emisores. El
hallazgo es sobre la muestra y el método, no sobre la prensa. 2b (base
revisada) apareció sola, sin buscarla, en tres lotes independientes: C18
(latente en la primaria) y C29 en el lote crudo, y en la jornada 2 tres
teletipos regionales sobre la EOH que calculan la tasa contra la edición
provisional del año anterior (E031, E042, E043), uno con cambio de signo
(Baleares, residentes: +3,8 % publicado frente a −2,3 % con la edición
vigente).

**Decisión.**

1. La cubeta B del conjunto de evaluación es **`2b_base_revisada`**. 2a
   (`2_baseline_selection`) no desaparece: pasa a la cubeta C como clase
   secundaria y conserva su resultado de **0/43**, que es un hallazgo
   publicable por sí mismo.
2. **Condición bloqueante, cumplida antes de recolectar nada más:** demostrar
   con tres casos que la edición anterior de una estadística del INE es
   recuperable por el agente fuera de Tempus. Resultado: cinco ediciones de
   cuatro operaciones (EOH julio y agosto 2025, ETDP julio 2025, Hipotecas
   junio 2025, Sociedades julio 2025); nota HTML, nota PDF y anexo XLSX
   responden 200 al agente identificado con la URL derivada del código de la
   nota, y en las cinco el valor publicado difiere del vigente. Detalle,
   límites y herramienta: `research/puerta3/RECUPERABILIDAD-2B.md`.
3. **Q048** (Delegación del Gobierno en Madrid) sigue vetado por DEC-025. No
   se rescata.
4. El veredicto de 2b lleva **dos campos separados**, `evidencia_al_publicar`
   y `evidencia_vigente`, cada uno con su fecha (la de publicación de la
   edición y la de consulta de la vigente). La distinción existía en el
   diseño y no en la salida.
5. **Este es el último reencuadre del objeto.** Si 2b no funciona, se declara
   el alcance con lo que haya y la tesis se escribe con el resultado negativo
   documentado.
6. Se ajusta el prototipo: test 2b sobre dos ediciones, con un conector de
   edición anterior fuera de Tempus. Se propone antes de implementarlo.

**Consecuencias inmediatas.** Validador: B exige `divergence_detected` +
`2b_base_revisada`; C admite 2a. Lote: E031, E042 y E043 pasan de C a B
(B = 3 de 15; C = 1). Diseño §1/§1b/§3b, encuadre y `CLAUDE.md` actualizados.
La regla de DEC-033 (B por jornada) se reevalúa con B = 2b en la siguiente
jornada, con la tasa observada en la jornada 2 (3 de 17 casos de prensa).

**Alternativas descartadas.** Bajar el mínimo de B a 10 manteniendo 2a: con
0/43 no hay tasa que proyectar. Ampliar el tope con 2a: gastar jornadas en
una clase que no aparece con este método. Redefinir el alcance hacia emisores
institucionales para salvar 2a: cambia el objeto más que la clase, y Q048
muestra que las ediciones admisibles no llegan hasta diciembre.

---

## DEC-035 · La cubeta B se declara con 7 casos e intervalo; la jornada 5 es una prueba de predicción sobre EOAT0826 y completa A hasta 40 sin INE

**Fecha:** 2026-09-27 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** diseño de la Puerta 3 (§1, §3, §4g–§4j), lote y validador (`OBJETIVO_CUBETA`), encuadre (`TESIS-ENCUADRE`, H1), `CLAUDE.md`

**Contexto.** La jornada 4 cerró con B = 1 (E066, EOAT0526) tras cumplir la
cuota de emisor (INE 62,1 %). Por la regla de §4b (B ≤ 3) se paró. El conjunto
tiene 7 B contables (más E056 excedente) en tres ediciones de dos operaciones.
Unas 25 piezas regionales de las ediciones de marzo a junio se cotejaron
contra las dos bases y todas usaban la vigente. La hipótesis de §4d (2b solo
donde el anexo no trae la tasa por CCAA) se cumple en las dos operaciones sin
tasa y en ninguna de las seis con tasa.

**Decisión.**

1. **B se declara con 7 casos y su intervalo** (Wilson 95 %: 7/7 → [64,6;
   100]; 6/7 → [48,7; 97,4]). El mínimo de 15 baja a 7. **Razón estructural,
   escrita en el diseño (§4g):** 2b solo existe en 2 de las 8 operaciones del
   mapa, así que B está acotado por el universo y no por el esfuerzo de
   recolección. Queda como **limitación explícita de H1**: la tesis afirma
   que el fenómeno existe, es computable y se detecta con ese intervalo; no
   afirma su frecuencia.
2. **Jornada 5 = prueba de predicción, no recolección.** La predicción sobre
   `EOAT0826` (30-09) queda escrita en §4h **antes** de la publicación, con
   fecha y commit: P1 (aparece al menos un 2b entre las piezas con tasa
   propia) y P2 (ninguno en las seis operaciones con tasa publicada), con la
   lectura de cada resultado fijada de antemano.
3. **En la misma jornada se completa A hasta 40**, lo que sostiene H3 (hoy
   31), **sin emisor INE** por la cuota (§4i).
4. **`CTH0926` (23-10) es opcional:** se recolecta si el calendario lo
   permite; nada se bloquea por esperarlo. **Enmienda del mismo día (Mateo,
   2026-09-27): `CTH0926` pasa a necesaria.** Es la única edición fuera del
   verano y sin ella §4d no se separa de la lectura estacional (§4h). La
   jornada 5 y el cierre de la Puerta 3 esperan a esa edición.
5. **Vía (c) descartada:** rastrear las redacciones que ya mostraron el
   mecanismo sesga lo que el control natural de §4e pretende medir. Anotado
   en §4j con la razón.

**Consecuencias.** `OBJETIVO_CUBETA["B"]` pasa a (7, 7); el total del diseño
pasa de 110 (78) a 97 (70). El encuadre añade la limitación de H1. Se avisa a
Mateo al cerrar la jornada 5 con el resultado de P1 y P2 y el número de A.

**Alternativas descartadas.** Mantener el mínimo en 15 y ampliar jornadas:
la tasa observada en las ediciones de primavera es cero, y el tope de tres
por edición ya está lleno en las dos ediciones que sí lo producen. Bajar a 10:
no hay universo del que sacar los tres que faltan sin la vía (c). Rastrear
redacciones (vía c): sesgo declarado arriba.

---

## DEC-036 · El eje de detección de manipulación entra al proyecto, después de cerrar la Puerta 3; `IDEAS.md` como antesala de las decisiones

**Fecha:** 2026-09-27 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** `docs/EJE-MANIPULACION.md`, `docs/IDEAS.md`, `CLAUDE.md` §11, encuadre (alcance)

**Contexto.** Hasta hoy la "retórica general" estaba en la lista de lo que no
se implementa todavía (`CLAUDE.md` §11) y el eje de persuasión solo aparecía
como trabajo futuro. Mateo toma la decisión de alcance.

**Decisión.**

1. **El eje de detección de manipulación entra al proyecto**, no solo a
   trabajo futuro. Detecta técnicas de lenguaje persuasivo con enum cerrado
   y fragmento literal; **nunca afirma intención del autor**.
2. **Se construye después de cerrar la Puerta 3, no en paralelo.** Cerrar la
   Puerta 3 incluye la jornada 5, `CTH0926`, el congelado del conjunto, el
   arnés y su DEC de cierre.
3. Documento vivo: `docs/EJE-MANIPULACION.md` (qué es y qué no, preguntas
   abiertas, papers, decisiones que lo condicionan).
4. **`docs/IDEAS.md`** es la bitácora de ideas que todavía no son decisiones,
   con fecha, origen y estado. Lo que Mateo traiga de otra IA o de un paper
   entra ahí primero. **Nada pasa de `IDEAS.md` a `DECISIONES.md` sin
   aprobación explícita de Mateo.**

**Consecuencias.** `CLAUDE.md` §11: "retórica general" deja de ser un
"todavía" incondicional y pasa a "eje de manipulación, después de la Puerta
3, con enum cerrado". Primera entrada de `IDEAS.md`: I-001, contraste con
búsqueda web (baseline B0), en estudio.

**Alternativas descartadas.** Construirlo en paralelo: dispersa la Puerta 3
cuando le quedan dos ediciones y el congelado. Dejarlo solo como trabajo
futuro: Mateo lo descarta; el eje forma parte del alcance del proyecto.

---

## DEC-037 · El eje de manipulación tampoco emite estados del lector ni efectos de difusión

**Fecha:** 2026-09-27 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** `docs/EJE-MANIPULACION.md` §1, `docs/IDEAS.md` I-002 §3, `CLAUDE.md` §11

**Contexto.** La pasada de literatura 1 para el futuro eje de manipulación
(`docs/IDEAS.md` I-002) dejó en su §3, como propuesta, ampliar la regla de
intención.

**Decisión.** **El eje no emite estados del lector ni efectos de difusión**,
además de no emitir intención del autor (DEC-036). No dice que el lector
sienta miedo, crea o sea persuadido, ni que el texto vaya a difundirse más.
Su salida se limita a técnica del enum, span literal y explicación por
plantilla.

**Razón anotada.** Tannenbaum et al. 2015 separan el miedo representado en
el mensaje, una propiedad del contenido, del miedo que siente el receptor
("depicted fear versus experienced fear"), y solo 71 de 248 estudios
midieron lo segundo (manuscrito p. 3, nota 2).

**Alternativa descartada.** Mantener la ampliación como propuesta abierta
en I-002: Mateo la aprueba.

**Nota de registro.** La primera redacción de esta entrada (commit
`1c564cb`) juntaba esta regla con la de citas y enumeraba como consecuencias
los cambios de documentación de la misma instrucción. Por indicación de
Mateo (2026-09-27) queda solo esta regla: la de citas es DEC-038 y los
cambios de documentación constan en `docs/BITACORA.md`. Es una corrección
del registro el mismo día, antes de fusionar la rama; no revoca nada.

---

## DEC-038 · Ninguna fuente que dependa de una traducción propia sin verificar entra en la tesis

**Fecha:** 2026-09-27 · **Estado:** vigente · **Decide:** Mateo · **Aplica:** toda la tesis (`docs/TESIS/`), `docs/IDEAS.md`, `docs/EJE-MANIPULACION.md` §3 y §4, `CLAUDE.md` §3

**Contexto.** En la pasada I-002, la guía de anotación en árabe de Hasanain,
Ahmed & Alam 2024 (anexo D, p. 2744) se usó como respaldo de la separación
entre el eje de técnicas y la veracidad. Se leyó con una traducción del
agente, marcada NEEDS_REVIEW.

**Decisión.** **Ninguna fuente que dependa de una traducción propia sin
verificar entra en la tesis.** Si alguien la verifica, se añade.

**Consecuencias.** La guía árabe se retira como respaldo y su traducción se
borra de I-002. La separación de ejes se apoya solo en SemEval 2020 (p. 1378;
fig. 8, p. 1407).

**Alternativa descartada.** Citar la guía con la marca NEEDS_REVIEW: Mateo
la retira por esta regla.
