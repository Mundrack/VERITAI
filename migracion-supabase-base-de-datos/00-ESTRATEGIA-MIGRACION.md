# 00 — Estrategia de migración

## El contrato de portabilidad

Todo lo que sigue son reglas del proyecto, no recomendaciones. Cada una existe
porque romperla convierte una migración de una tarde en una reescritura.

### Regla 1 — Se habla SQL, no PostgREST

```
PERMITIDO      SQLAlchemy / psycopg sobre DATABASE_URL
PROHIBIDO      supabase-py, supabase-js, o cualquier cliente que hable
               la API REST de Supabase, dentro del codigo de dominio
```

**Por qué.** El cliente de Supabase es cómodo: `supabase.table("casos").select()`
se escribe más rápido que una consulta. Pero esa comodidad es exactamente el
acoplamiento: PostgREST no existe fuera de Supabase, así que el día que haya que
salir —por precio, por latencia, por cierre del servicio, o simplemente para
correr los tests sin red— hay que reescribir cada consulta del proyecto.

**Alternativa descartada:** usar el cliente de Supabase y envolverlo en un
repositorio propio. Suena razonable, pero no elimina el problema: sigue siendo
imposible ejecutarlo contra un Postgres normal, y los tests dejan de poder correr
sin Supabase.

**Excepción prevista.** Si algún día se usan Auth, Storage o Realtime, esos sí
son servicios propios de Supabase y no tienen equivalente en un Postgres pelado.
Cuando llegue el caso, se aíslan detrás de un puerto (una interfaz) en
`veritai/domain/` con dos implementaciones —local y Supabase—, igual que
`EvidenceProvider`. Nunca se llaman desde el dominio directamente.

### Regla 2 — Migraciones en SQL plano, numeradas e inmutables

```
db/migrations/000_roles.sql
db/migrations/001_schema_veritai.sql
db/migrations/002_rls_baseline.sql
```

- **SQL plano**, para que `supabase db push` pueda ejecutarlas tal cual.
- **Numeradas**, para que el orden sea total y no dependa de un grafo.
- **Inmutables**: una migración aplicada no se edita nunca. El runner guarda su
  `sha256` y falla si el archivo cambió. Para corregir algo se escribe una
  migración nueva.

**Alternativa descartada:** Alembic. Genera migraciones en Python acopladas a los
modelos de SQLAlchemy. Supabase no las puede ejecutar, y el `autogenerate`
produce diffs que hay que revisar igual. El runner propio son 180 líneas
(`scripts/migrate.py`) y mantiene el formato portable.

### Regla 3 — Esquema propio, nunca `public`

Todo vive en el esquema `veritai`. Supabase reserva `auth`, `storage`,
`realtime`, `extensions` y `graphql`, y publica `public` a través de PostgREST
por defecto. Un esquema propio no colisiona con nada y deja explícito qué se
expone.

### Regla 4 — Los roles de Supabase existen también en local

`db/migrations/000_roles.sql` crea `anon`, `authenticated` y `service_role` si no
están. En Supabase ya existen y la migración no hace nada. Resultado: **el mismo
archivo `.sql` corre en los dos entornos sin ramificar.**

Es la pieza pequeña que sostiene todo lo demás: sin ella, cada `GRANT ... TO
authenticated` obligaría a mantener dos versiones de cada migración.

### Regla 5 — RLS activado desde la primera tabla

Ver `04-RLS-Y-SEGURIDAD.md`. Resumen: en Supabase, una tabla sin RLS es una tabla
legible desde internet.

### Regla 6 — Ningún valor de conexión en el código

Host, puerto, usuario, contraseña, nombre de base de datos: todo por variables de
entorno. El código no contiene ni una cadena de conexión, ni siquiera como valor
por defecto para desarrollo.

---

## Qué cambia y qué no el día de la migración

| | Cambia |
|---|---|
| `DATABASE_URL` y `DATABASE_URL_MIGRATOR` | **Sí**, apuntan a Supabase |
| `DB_USE_POOL` | **Sí**, pasa a `false` si se usa el pooler en modo transaction |
| Servicio `db` de `docker-compose.yml` | Se deja de levantar |
| Código Python | **No** |
| Migraciones SQL | **No** |
| Modelos y consultas | **No** |
| Tests | **No** |
| Servicios `api` y `web` | **No** — siguen en Docker, como pediste |

Docker no desaparece con la migración. Lo único que sale del `docker compose` es
el contenedor de PostgreSQL.
