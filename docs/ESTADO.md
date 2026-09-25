# Estado del proyecto

> **Este documento se sobrescribe entero en cada actualización.** Es una foto,
> no un historial. El historial está en [`BITACORA.md`](BITACORA.md).

**Última actualización:** 2026-09-24

---

## Dónde estamos

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO        <-- AQUI, sin superar
           sin esto no se escribe codigo de producto

PUERTA 2   prototipo end-to-end, UNA clase y UN emisor,
           10 casos con trazabilidad completa

PUERTA 3   corpus completo anotado + arnes de evaluacion

PUERTA 4   evaluacion completa: metricas, ablacion,
           sondas contrafactuales
```

**La métrica que decide, y es una sola:**

> Porcentaje de casos del lote **crudo** (20 nuevos, sin artículo de verificación
> previo) donde se localiza la **edición anterior** del dato.
>
> `>60%` verde → PILOT_GO · `30–60%` ámbar → alcance reducido · `<30%` rojo → PILOT_PIVOT

**Valor actual de esa métrica: sin medir.** El lote crudo no existe todavía.

---

## Qué funciona hoy

Entorno de desarrollo local completo en Docker. Se levanta con un comando y no
requiere nada instalado en la máquina aparte de Docker.

```bash
docker compose up -d
```

| Servicio | Dirección | Estado |
|---|---|---|
| Web (Vite + TypeScript) | http://127.0.0.1:5173 | funcionando |
| API (FastAPI) | http://127.0.0.1:8000 | funcionando, healthy |
| API · OpenAPI | http://127.0.0.1:8000/docs | solo en local |
| PostgreSQL 17 | `127.0.0.1:55432` | funcionando, healthy |

Verificación de la cadena completa:

```
$ curl http://127.0.0.1:8000/health
{"servicio":"veritai-api","version":"0.1.0","entorno":"local","base_de_datos":"conectada"}
```

### Comprobado, no supuesto

| Comprobación | Resultado | Fecha |
|---|---|---|
| `docker compose up -d` levanta los 4 servicios | ✅ | 2026-09-08 |
| Cadena web → API → PostgreSQL | ✅ `base_de_datos: conectada` | 2026-09-08 |
| Migraciones idempotentes en la segunda pasada | ✅ `sin migraciones pendientes` | 2026-09-08 |
| `veritai_app` no puede hacer DDL | ✅ `permission denied for schema veritai` | 2026-09-08 |
| Los datos sobreviven a `down` y `up` | ✅ | 2026-09-08 |
| Roles de Supabase presentes en local | ✅ `anon`, `authenticated`, `service_role` | 2026-09-08 |
| `verificar-compatibilidad.sql` | ✅ 0 filas en los 3 bloques bloqueantes | 2026-09-08 |
| Tests de la API | ✅ 5 passed | 2026-09-08 |
| `ruff check` | ✅ sin avisos | 2026-09-08 |
| `tsc --noEmit` | ✅ sin errores | 2026-09-08 |
| Ninguna contraseña real en el repositorio | ✅ `git grep` vacío | 2026-09-08 |

---

## Qué NO existe todavía, a propósito

| | Por qué |
|---|---|
| Tablas de dominio en la base de datos | Puerta 1. Llegan después de `PILOT_GO` |
| Endpoints que no sean de salud | Ídem |
| Cualquier LLM, local o remoto | R02 §15: no elegir modelo antes del piloto |
| Conectores a fuentes primarias | Se eligen con los datos del piloto, no antes |
| La extensión MV3 | El panel web es el mismo código; se empaqueta más tarde |
| pgvector activado | La imagen lo trae; la extensión no hace falta hasta *embeddings* |
| El aparato completo de `/docs` y los ADR formales | Adenda D6: después de `PILOT_GO` |

---

## Base de datos

PostgreSQL 17 en Docker, volumen persistente `veritai_pgdata`. Los datos
sobreviven a `docker compose down`; solo se borran con `down -v`.

```
esquema veritai        vacio a proposito. Las tablas llegan tras PILOT_GO
esquema veritai_meta   schema_migrations: 3 migraciones aplicadas
roles                  veritai_migrator (DDL) · veritai_app (solo DML)
                       anon · authenticated · service_role (compatibilidad Supabase)
```

**Supabase no se usa todavía.** La cuenta del proyecto sigue en configuración.
La arquitectura está preparada para migrar cambiando `DATABASE_URL`: ver
[`../migracion-supabase-base-de-datos/`](../migracion-supabase-base-de-datos/README.md).

---

## Estado de git

```
main                          paquete + este registro vivo (fusionado --no-ff)
│
├─ docs/registro-vivo         FUSIONADO a main
│
└─ feat/entorno-docker-local  entorno Docker completo   <- SIN FUSIONAR
```

`ATENCIÓN` Como `docs/` se fusionó antes que el entorno, **`main` contiene
documentos que describen archivos que todavía no están en `main`**: los enlaces a
`../migracion-supabase-base-de-datos/` no resuelven, y `CLAUDE.md` tampoco está.
Se arregla fusionando `feat/entorno-docker-local`, que ya está revisado y
verificado.

`ATENCIÓN` No hay remoto configurado y `gh` no está instalado, así que las ramas
existen pero **no hay pull requests**. Ver
[`PREGUNTAS-ABIERTAS.md`](PREGUNTAS-ABIERTAS.md), P-01.

Nada se ha subido a ningún servidor.

---

## Lo siguiente

En orden, y sin saltarse pasos:

1. **Resolver P-01 y P-02** de `PREGUNTAS-ABIERTAS.md` (remoto de git, aprobación
   de `CLAUDE.md`). Son de Mateo, no se pueden asumir.
2. **TAREA 1 — auditar los 20 casos existentes** → `research/AUDIT-PILOT-20.md`.
   La pre-auditoría ya está hecha y documentada en
   [`../research/README.md`](../research/README.md); falta verificar URLs y
   normalizar etiquetas a los enums cerrados.
3. **TAREA 2 — recolectar 20 casos crudos.** Es el trabajo caro y el que no se
   puede falsear. Sin él no hay métrica.
4. **TAREA 3 — decidir** → `research/PILOT-DECISION.md` con `PILOT_GO` o
   `PILOT_PIVOT`.

No se avanza a la Puerta 2 hasta entregar `PILOT-DECISION.md`.
