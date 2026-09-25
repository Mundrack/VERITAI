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
