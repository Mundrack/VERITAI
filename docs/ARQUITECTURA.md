# Arquitectura

> Este documento describe **lo que existe hoy**, no lo que se planea. Se
> actualiza cuando cambia la estructura real.
>
> El diseño objetivo del sistema completo está en
> `04-VERITAI-CLAUDE-RESPONSE-R02.md` §2. No lo repito aquí.

**Última actualización:** 2026-09-25 (Puerta 2, rama `feat/puerta-2-ine-2a`)

---

## 1. Lo que hay construido

Cuatro contenedores y, desde la Puerta 2, la primera lógica de dominio: un
análisis end-to-end de **una clase (2a) sobre un emisor (INE)**, sin LLM.

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

### El flujo de análisis (Puerta 2)

```
POST /analisis  (JSON del claim, estructurado a mano)
      │
      ▼
ClaimEstructurado ───► ProveedorINE ───► EvidenceBundle ───► hard gates ───► test 2a ───► verdad
  domain/claim.py     infrastructure/    domain/evidencia   domain/          domain/tests/  domain/
                      ine/proveedor.py   (spans literales,  abstencion.py    comparacion_   verdad.py
                      + tempus.py        bundle_hash)                        base.py
                      + extractor.py
      │
      ▼
Veredicto (truth · context · clase · abstain_reasons · tests · numeros_usados)
      │                                                    domain/veredicto.py
      ├─► explicación por plantilla numérica              domain/plantilla.py
      └─► claims · evidence_bundles · evidence_items · verdicts · audit_log
                                                           infrastructure/repositorio.py
```

Todo lo orquesta `application/analizar_claim.py`. El proveedor y el
repositorio se inyectan en el ciclo de vida de la API (`main.py`) y llegan a
la ruta por `app.state`; los tests los sustituyen por dobles
(`tests/dobles.py`) sin tocar el dominio.

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
│  │  │  ├─ api/routes/analisis.py  POST /analisis (pydantic, limites de tamano)
│  │  │  ├─ db/session.py         motor SQLAlchemy desde DATABASE_URL
│  │  │  ├─ domain/               enums · periodo · claim · evidencia · abstencion
│  │  │  │                        · verdad · veredicto · plantilla · puertos (Protocol)
│  │  │  │  └─ tests/comparacion_base.py   el test 2a, deterministico
│  │  │  ├─ application/          analizar_claim.py: el caso de uso
│  │  │  └─ infrastructure/       ine/{tempus,extractor,proveedor}.py · repositorio.py
│  │  └─ tests/                   45 tests + dobles.py + fixtures/ (JSON real del INE)
│  │
│  └─ web/
│     ├─ Dockerfile               etapas: deps · dev · build
│     ├─ index.html
│     └─ src/
│        ├─ main.ts               panel de estado
│        ├─ estilos.css
│        └─ i18n/                 es.json · en.json · index.ts
│
├─ db/migrations/         000_roles · 001_schema_veritai · 002_rls_baseline · 003_puerta2
├─ scripts/               migrate.py · init-env.ps1 · init-env.sh
├─ research/              piloto (TAREAS 1-3) y puerta2/ (casos JSON, ejecutor, resultados)
├─ docs/                  este registro vivo
└─ migracion-supabase-base-de-datos/
```

Las carpetas `domain/`, `application/` e `infrastructure/` se llenaron en la
Puerta 2 **solo con lo que el prototipo necesita**: una clase, un emisor. No
hay conectores de FMI ni de Interior, ni N0, ni LLM.

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

Sigue sin haber un test que verifique esta regla automáticamente; hoy se cumple
por revisión: `domain/` no importa de `infrastructure/`, de `application/` ni
de `api/`; `infrastructure/` implementa los `Protocol` de `domain/puertos.py`
(`ProveedorEvidencia`, `Repositorio`). Un test que falle si `domain/` importa
hacia fuera sigue siendo deuda.

---

## 4. La API

Tres endpoints de salud y uno de dominio:

| Endpoint | Qué hace | Códigos |
|---|---|---|
| `/health/live` | El proceso responde. **Sin tocar la base de datos** | 200 |
| `/health/ready` | Hay base de datos (`select 1`) | 200 / 503 |
| `/health` | Resumen legible: servicio, versión, entorno, base de datos | 200 |
| `POST /analisis` | Recibe un claim estructurado (JSON validado por pydantic: emisor `INE`, tabla `^\d{1,8}$`, periodos parseados, texto ≤ 2000, etiquetas acotadas), lo analiza y devuelve veredicto + evidencia + `persistido` + `duracion_ms` | 200 / 422 (JSON inválido) / 503 (proveedor no inicializado) / 500 (excepción no prevista, solo el nombre del tipo) |

`POST /analisis` no acepta URLs ni texto libre como fuente: el claim ya viene
estructurado y la única red que toca es `servicios.ine.es`, por allowlist.

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
esquema veritai          claims · evidence_bundles · evidence_items · verdicts · audit_log
                         (003_puerta2; CHECK con los enums del glosario; RLS activada Y forzada;
                          audit_log solo insert/select para veritai_app)
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

Respondido en la Puerta 2:

- ~~Dónde vive el **audit trail** y con qué esquema~~ → `veritai.audit_log`,
  una fila por análisis (claim, bundle_hash, veredicto, duración), solo
  insert/select para la aplicación.
- ~~Cómo se almacenan los artefactos de evidencia~~ → **a medias**: el span
  literal de cada número va en `evidence_items.raw_value_span`; la respuesta
  JSON completa del INE se guarda opcionalmente en disco
  (`EVIDENCIA_CACHE_DIR`). HTML y PDF crudos siguen sin decidir.

Limitación conocida del conector INE *(DEC-029)*:

- **La API Tempus sirve solo la edición vigente** de cada serie. El span
  conserva `T3_TipoDato` (provisional / definitivo), pero una **base revisada
  (2b) no se puede demostrar desde la API**: hace falta la nota de prensa o el
  PDF de la edición anterior. Por eso 2b quedó fuera del prototipo y P11 (cuyo
  valor de la API no cuadra con el PDF de 2019) sigue en `NEEDS_REVIEW`.

Sigue sin responder:

- Dónde corre el LLM local respecto a los contenedores
- Si N0 (regex + encoder ONNX) corre en el navegador, en la API, o en los dos
- Frescura de la caché del proveedor INE: vive en la instancia de la API y
  solo se invalida al pedir un periodo más antiguo; un servicio de larga vida
  necesita TTL o descarga por petición
- Un test de arquitectura que falle si `domain/` importa hacia fuera
