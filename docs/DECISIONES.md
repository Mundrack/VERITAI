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
