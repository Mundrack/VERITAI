# 02 — Diferencias entre el PostgreSQL local y Supabase

Supabase es PostgreSQL, pero no es *un PostgreSQL vacío*. Estas son las
diferencias que importan, y qué se hizo en el diseño local para absorberlas.

---

## 1. Roles

| | Local (contenedor) | Supabase |
|---|---|---|
| Superusuario | `veritai_migrator` (dueño del contenedor) | No existe. El rol más alto es `postgres`, y **no es superusuario** |
| `anon`, `authenticated`, `service_role` | Los crea `000_roles.sql` | Vienen de fábrica |
| Usuario de la aplicación | `veritai_app`, sin DDL | Se crea igual, con la misma migración |

`ATENCIÓN` En Supabase no hay superusuario. Cualquier sentencia que lo requiera
falla. En la práctica esto afecta a: crear extensiones fuera de la lista
permitida, `COPY ... FROM PROGRAM`, y modificar parámetros del servidor.

`scripts/verificar-compatibilidad.sql` detecta estos casos antes de migrar.

---

## 2. Extensiones

| | Local | Supabase |
|---|---|---|
| Dónde se instalan | Esquema `public` por defecto | Esquema `extensions` por convención |
| `pgvector` | Disponible en la imagen, **sin activar** | Disponible, se activa desde el panel o con SQL |
| Cualquier extensión | Se puede compilar e instalar | Solo las de la lista permitida de Supabase |

**Decisión tomada:** `pgvector` viene en la imagen local pero la extensión **no
se crea todavía**. No hace falta hasta la fase de *embeddings*, que es posterior
a `PILOT_GO`. Cuando llegue, la migración que la active debe escribirse así:

```sql
create extension if not exists vector with schema extensions;
```

y `000_roles.sql` necesitará una línea previa `create schema if not exists
extensions;` para que ese mismo SQL también funcione en local.

---

## 3. Conexiones: directa vs. pooler

Supabase ofrece **tres** cadenas de conexión distintas y elegir mal es la causa
más habitual de fallos raros.

| Modo | Puerto | Para qué | En VERITAI |
|---|---|---|---|
| Directa | `5432` | Migraciones, DDL, herramientas | `DATABASE_URL_MIGRATOR` |
| Pooler *transaction* | `6543` | Aplicación, muchas conexiones cortas | `DATABASE_URL` |
| Pooler *session* | `5432` vía pooler | Casos que necesitan estado de sesión | No se usa |

`RIESGO` El pooler en modo *transaction* **reparte la misma conexión física
entre transacciones distintas**. Las sentencias preparadas del cliente se pierden
entre una y otra, y aparecen errores del estilo `prepared statement "_pg3_0"
already exists` que no se reproducen en local.

**Ya está resuelto en el código.** `apps/api/veritai/db/session.py`:

```python
if settings.db_use_pool:
    ...pool normal de SQLAlchemy...
else:
    opciones["poolclass"] = NullPool
    opciones["connect_args"] = {"prepare_threshold": None}   # <- la clave
```

Es decir: al migrar se pone `DB_USE_POOL=false` en el `.env` y no se toca ni una
línea de Python.

`ATENCIÓN` La conexión directa (puerto 5432) de Supabase es **IPv6** en los
proyectos nuevos. Si la red desde la que se migra no tiene IPv6, hay que usar el
pooler también para las migraciones, o contratar el add-on de IPv4.

---

## 4. Límites de conexiones

| | Local | Supabase (plan gratuito) |
|---|---|---|
| Conexiones directas | ~100 | ~60, compartidas con el panel y el propio Supabase |
| Vía pooler | — | Muchas más, pero cada una es más frágil |

`DB_POOL_SIZE` está en 5 por defecto justamente por esto. En local sobra; en
Supabase, con varios procesos, un pool de 20 agota la cuota enseguida.

---

## 5. Row Level Security

| | Local | Supabase |
|---|---|---|
| Efecto real de no tener RLS | Ninguno: solo se conecta `veritai_app` | **La tabla queda legible desde internet** con la `anon key` |

Es la diferencia más peligrosa de toda esta lista, y la razón de que RLS sea
obligatorio desde la primera tabla. Detalle en `04-RLS-Y-SEGURIDAD.md`.

---

## 6. Copias de seguridad

| | Local | Supabase |
|---|---|---|
| Responsable | Tú, con `scripts/exportar-a-supabase.sh` | Supabase, con retención según el plan |
| Plan gratuito | — | Retención corta. **No sustituye a un volcado propio** |

`ACCIÓN` Después de migrar, mantener un volcado periódico propio. El corpus
anotado del piloto es trabajo manual de semanas y no debe existir en un solo
sitio (R02 §14, riesgo 4).

---

## 7. Zona horaria y `now()`

Ambos entornos usan UTC. Todas las columnas de fecha del proyecto deben ser
`timestamptz`, nunca `timestamp`. Ya es así en `veritai_meta.schema_migrations`.
