# Arquitectura

> Este documento describe **lo que existe hoy**, no lo que se planea. Se
> actualiza cuando cambia la estructura real.
>
> El diseño objetivo del sistema completo está en
> `04-VERITAI-CLAUDE-RESPONSE-R02.md` §2. No lo repito aquí.

**Última actualización:** 2026-09-11

---

## 1. Lo que hay construido

Solo el entorno. Cuatro contenedores, ninguna lógica de dominio.

```
                      docker compose up -d
                              │
   ┌──────────────┬───────────┴───────────┬──────────────┐
   │              │                       │              │
┌──▼───┐    ┌─────▼─────┐           ┌─────▼────┐   ┌─────▼────┐
│  db  │◄───┤  migrate  │           │   api    │◄──┤   web    │
│      │    │ (un uso)  │           │ FastAPI  │   │  Vite    │
│ PG17 │    │           │           │          │   │   TS     │
└──┬───┘    └───────────┘           └────┬─────┘   └─────┬────┘
   │                                     │               │
   │ 127.0.0.1:55432          127.0.0.1:8000   127.0.0.1:5173
   │                                     │               │
   └──── volumen veritai_pgdata          └───────────────┘
         (persiste tras `down`)              /health
```

**Orden de arranque, garantizado por `depends_on`:**

```
db (healthy)  →  migrate (exit 0)  →  api  →  web
```

Si las migraciones fallan, la API **no arranca**. Es deliberado: es preferible
un servicio caído a un servicio corriendo contra un esquema desactualizado.

---

## 2. Estructura del repositorio

```
VERITAI/
├─ 00b … 07-*.md          paquete de documentacion. Fuente de verdad
├─ CLAUDE.md              reglas permanentes del proyecto
├─ README.md              que es VERITAI y como levantarlo
├─ docker-compose.yml     los 4 servicios
├─ docker-compose.override.yml   recarga en caliente para desarrollo
├─ .env.example           plantilla con marcadores. Se versiona
├─ .env                   valores reales. IGNORADO por git
│
├─ apps/
│  ├─ api/
│  │  ├─ Dockerfile               etapas: runtime · dev
│  │  ├─ requirements.txt         rangos con tope superior
│  │  ├─ requirements.lock.txt    pins exactos resueltos en la imagen
│  │  ├─ veritai/
│  │  │  ├─ config.py             configuracion por entorno. SecretStr
│  │  │  ├─ main.py               FastAPI, CORS, ciclo de vida
│  │  │  ├─ api/routes/health.py  /health · /health/live · /health/ready
│  │  │  ├─ db/session.py         motor SQLAlchemy desde DATABASE_URL
│  │  │  ├─ domain/               VACIO. Entidades y reglas de negocio
│  │  │  ├─ application/          VACIO. Casos de uso
│  │  │  └─ infrastructure/       VACIO. Conectores, parsers, clientes
│  │  └─ tests/                   5 tests
│  │
│  └─ web/
│     ├─ Dockerfile               etapas: deps · dev · build
│     ├─ index.html
│     └─ src/
│        ├─ main.ts               panel de estado
│        ├─ estilos.css
│        └─ i18n/                 es.json · en.json · index.ts
│
├─ db/migrations/         000_roles · 001_schema_veritai · 002_rls_baseline
├─ scripts/               migrate.py · init-env.ps1 · init-env.sh
├─ research/              piloto. Vacio salvo su README
├─ docs/                  este registro vivo
└─ migracion-supabase-base-de-datos/
```

Las carpetas `domain/`, `application/` e `infrastructure/` están vacías **a
propósito**: la estructura está definida, el contenido llega tras `PILOT_GO`.

---

## 3. Dirección de las dependencias

```
api  ──►  application  ──►  domain
                              ▲
                              │  implementa los puertos
                        infrastructure
```

El dominio no importa nada de infraestructura. La infraestructura implementa
interfaces definidas en el dominio. Es lo que permitirá sustituir un
`EvidenceProvider` real por uno de prueba sin tocar las reglas.

Hoy no hay nada que verifique esta regla automáticamente. Cuando haya código en
esas carpetas, conviene un test que falle si `domain/` importa de
`infrastructure/`.

---

## 4. La API

Tres endpoints, todos de salud, y cada uno con un trabajo distinto:

| Endpoint | Qué comprueba | Códigos |
|---|---|---|
| `/health/live` | El proceso responde. **Sin tocar la base de datos** | 200 |
| `/health/ready` | Hay base de datos (`select 1`) | 200 / 503 |
| `/health` | Resumen legible: servicio, versión, entorno, base de datos | 200 |

**Por qué `live` no toca la base de datos.** Es el que usa el `HEALTHCHECK` de
Docker. Si dependiera de Postgres, una caída de la base reiniciaría la API en
bucle sin arreglar nada.

### Configuración

Todo por variables de entorno, vía `pydantic-settings`. `DATABASE_URL` es un
`SecretStr`, así que no aparece en `repr()`, ni en logs, ni en trazas de error.
Hay un test que lo comprueba.

`CORS_ALLOWED_ORIGINS` es una lista blanca explícita y un validador **rechaza el
comodín `*`**.

---

## 5. La base de datos

```
esquema veritai          objetos de dominio. VACIO a proposito
esquema veritai_meta     schema_migrations (archivo, sha256, aplicada_en)

roles
  veritai_migrator       DDL. Solo lo usa el servicio `migrate`
  veritai_app            solo DML sobre veritai. Es quien usa la API
  anon                   \
  authenticated           }  compatibilidad con Supabase. NOLOGIN
  service_role           /   service_role tiene bypassrls
```

### Migraciones

SQL plano, numerado, **inmutable**. El runner guarda el `sha256` de cada archivo
aplicado y falla si cambia en disco:

```
ERROR  la migracion 001_schema_veritai.sql ya fue aplicada pero su contenido
       cambio. Las migraciones son inmutables: crea una nueva en vez de
       editar esta.
```

Para corregir algo se escribe una migración nueva. Siempre.

### Persistencia

Volumen nombrado `veritai_pgdata`. Sobrevive a `docker compose down`. Solo se
borra con `down -v`, que hay que teclear a propósito.

---

## 6. El panel web

TypeScript sin framework. Hace una sola cosa: pedir `/health` y pintar el
resultado. Sirve para demostrar que la cadena navegador → API → PostgreSQL está
viva.

**i18n.** Catálogos `es.json` y `en.json`, y una función `t(clave, parametros)`
que sustituye marcadores `{nombre}` en la plantilla. Al cambiar de idioma se
**vuelve a renderizar desde las plantillas del nuevo idioma**; no se traduce el
HTML ya pintado.

**Escapado.** Todo lo que entra en el DOM pasa por `escapar()`, que usa
`textContent`. Ningún dato externo se concatena en crudo.

---

## 7. Preparación para Supabase

El único acoplamiento posible sería el cliente de Supabase, y está prohibido en
el dominio. Lo que cambia el día de la migración:

| | Cambia |
|---|---|
| `DATABASE_URL`, `DATABASE_URL_MIGRATOR` | Sí |
| `DB_USE_POOL` → `false` | Sí |
| Servicio `db` del compose | Se deja de levantar |
| Código Python, migraciones, tests, `api` y `web` | **No** |

El pooler de Supabase en modo *transaction* reparte la conexión entre
transacciones y rompe las sentencias preparadas. Ya está resuelto en
`apps/api/veritai/db/session.py`: con `DB_USE_POOL=false` se usa `NullPool` y
`prepare_threshold=None`.

Detalle completo en
[`../migracion-supabase-base-de-datos/`](../migracion-supabase-base-de-datos/README.md).

---

## 8. Lo que esta arquitectura todavía no responde

Se anota para no olvidarlo cuando llegue la Puerta 2:

- Dónde vive el **audit trail** y con qué esquema
- Cómo se almacenan los artefactos de evidencia (HTML y PDF crudos): filesystem
  con adaptador, o `bytea`, o Supabase Storage
- Dónde corre el LLM local respecto a los contenedores
- Si N0 (regex + encoder ONNX) corre en el navegador, en la API, o en los dos
