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
