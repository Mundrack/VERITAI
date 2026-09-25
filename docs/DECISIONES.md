# Registro de decisiones

Cada decisión técnica tomada **construyendo**, con la alternativa que se
descartó y por qué. Formato ADR simplificado.

> **Append-only.** Una decisión pasada no se edita. Si se revoca, se añade una
> entrada nueva que dice cuál revoca y qué dato la cambió.

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
