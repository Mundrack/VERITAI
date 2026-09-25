# VERITAI

Detección de **divergencia contextual computable** en afirmaciones estadísticas
en español. El problema no es la mentira: es el dato verdadero presentado fuera
de contexto.

> *"España cae 16 puestos en el ranking de países más seguros para mujeres."*
> El dato es correcto. La puntuación de España no cambió: 16 países mejoraron la
> suya. Un verificador clásico responde "verdadero" y esa respuesta es inútil.

Este repositorio contiene el paquete de documentación del proyecto, la
investigación del piloto y el entorno de desarrollo local.

---

## Estado: Puerta 1

El proyecto está **antes** de la primera puerta. Hasta que
`research/PILOT-DECISION.md` no exista con `PILOT_GO`, no se escribe código de
producto.

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO
           -> sin esto no se escribe codigo de producto        <- AQUI
PUERTA 2   Prototipo end-to-end, UNA clase y UN emisor,
           10 casos con trazabilidad completa
PUERTA 3   Corpus completo anotado + arnes de evaluacion
PUERTA 4   Evaluacion completa: metricas, ablacion, contrafactuales
```

Lo que hay ahora es **infraestructura**, no producto: la API solo expone
endpoints de salud y la base de datos no tiene ninguna tabla de dominio. Eso es
deliberado.

---

## Levantar el entorno

Requisitos: Docker Desktop. Nada más — ni Python ni Node en la máquina.

```bash
# 1. Generar el .env con contrasenas aleatorias (una sola vez)
.\scripts\init-env.ps1        # PowerShell
./scripts/init-env.sh         # Bash

# 2. Levantar todo
docker compose up -d
```

| Servicio | URL | Qué es |
|---|---|---|
| Web | http://127.0.0.1:5173 | Panel de UI (Vite + TypeScript) |
| API | http://127.0.0.1:8000 | FastAPI |
| API · docs | http://127.0.0.1:8000/docs | OpenAPI interactivo (solo en local) |
| PostgreSQL | `127.0.0.1:55432` | Puerto 55432 en el host para no chocar con un Postgres ya instalado |

Comprobar que la cadena completa está viva:

```bash
curl http://127.0.0.1:8000/health
# {"servicio":"veritai-api","version":"0.1.0","entorno":"local","base_de_datos":"conectada"}
```

### Órdenes habituales

```bash
docker compose ps                       # estado de los servicios
docker compose logs -f api              # logs de la API
docker compose down                     # parar; LOS DATOS SE CONSERVAN
docker compose down -v                  # parar y BORRAR el volumen de Postgres
docker compose run --rm migrate         # aplicar migraciones pendientes
docker compose --profile herramientas up -d adminer   # cliente web de Postgres
```

### Tests

```bash
docker build --target dev -t veritai/api:dev ./apps/api
docker run --rm -e DATABASE_URL="postgresql+psycopg://t:t@127.0.0.1:1/x" \
  veritai/api:dev python -m pytest -v
```

---

## Estructura

```
VERITAI/
├─ 00b … 07-*.md                     paquete de documentacion (fuente de verdad)
├─ apps/
│  ├─ api/                           FastAPI. domain / application / infrastructure
│  └─ web/                           panel de UI. TypeScript sin framework, i18n es+en
├─ db/migrations/                    migraciones SQL planas, numeradas e inmutables
├─ scripts/                          runner de migraciones y generador de .env
├─ research/                         piloto: auditoria, 40 casos, decision
└─ migracion-supabase-base-de-datos/ estrategia y runbook para mover la BD a Supabase
```

Las reglas permanentes del proyecto están en **`CLAUDE.md`**.

---

## Base de datos

PostgreSQL 17 en Docker, con volumen persistente `veritai_pgdata`. Los datos
sobreviven a `docker compose down`; solo se borran con `down -v`.

**No se usa Supabase todavía.** La arquitectura está preparada para migrar
cambiando una variable de entorno: ver
[`migracion-supabase-base-de-datos/`](migracion-supabase-base-de-datos/README.md).

---

## Secretos

Ninguna contraseña, clave ni cadena de conexión vive en el repositorio.

- `.env.example` se versiona y solo contiene marcadores.
- `.env` lo genera `scripts/init-env.*` con contraseñas aleatorias y está en
  `.gitignore`.
- Comprobación: `git check-ignore -v .env` debe responder.

---

## Orden de lectura de la documentación

1. `07-ADENDA-CORRECCIONES-PILOTO.md` — corrige el sesgo del piloto. **Se lee primero**
2. `00b-DECISIONES-MATEO.md` — decisiones cerradas
3. `01-VERITAI-START-HERE-CLAUDE-CODE.md` — arquitectura y reglas
4. `02-1-VeritAI-TESIS.md` — alcance académico *(parcialmente superado por 04 y 00b)*
5. `03-2-VeritAI-PROYECTO-TOTAL.md` — producto completo, fuera del alcance de tesis
6. `04-VERITAI-CLAUDE-RESPONSE-R02.md` — decisiones técnicas cerradas. **Capa vigente**
7. `05-VERITAI-PILOTO-20-CASOS.xlsx` — 20 casos preliminares
