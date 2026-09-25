# 03 — Variables de entorno: mapeo local ↔ Supabase

Esta es la tabla que se consulta el día de la migración. Nada más.

---

## Las que cambian

| Variable | Valor local | Valor con Supabase |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://veritai_app:<pass>@db:5432/veritai` | `postgresql+psycopg://postgres.<ref>:<pass>@aws-0-<region>.pooler.supabase.com:6543/postgres` |
| `DATABASE_URL_MIGRATOR` | `postgresql+psycopg://veritai_migrator:<pass>@db:5432/veritai` | `postgresql+psycopg://postgres:<pass>@db.<ref>.supabase.co:5432/postgres` |
| `DB_USE_POOL` | `true` | **`false`** (obligatorio con el pooler en modo *transaction*) |
| `DB_POOL_SIZE` | `5` | Irrelevante con `DB_USE_POOL=false` |

`<ref>` es la referencia del proyecto Supabase. `<region>` la región donde se
creó. Las dos aparecen en *Project Settings → Database*.

`ATENCIÓN` Fíjate en el prefijo del usuario: el pooler exige
`postgres.<ref>` como nombre de usuario, mientras que la conexión directa usa
solo `postgres`. Es un error clásico y el mensaje que devuelve no lo explica.

---

## Las que dejan de usarse

Estas solo alimentan el contenedor local de PostgreSQL. Cuando el servicio `db`
deje de levantarse, quedan sin efecto. **No hace falta borrarlas** — conviene
conservarlas para poder volver a local (ver `05-ROLLBACK.md`).

```
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_PORT
VERITAI_APP_DB_USER
VERITAI_APP_DB_PASSWORD
```

---

## Las que no cambian

```
VERITAI_ENV
LOG_LEVEL
API_PORT
CORS_ALLOWED_ORIGINS
WEB_PORT
VITE_API_BASE_URL
VITE_DEFAULT_LOCALE
```

---

## Las que aparecerían más adelante

Solo si algún día se usan Auth, Storage o Realtime. **Hoy no existen y no deben
crearse "por si acaso".**

| Variable | Para qué | Dónde puede vivir |
|---|---|---|
| `SUPABASE_URL` | Endpoint del proyecto | Backend y frontend |
| `SUPABASE_ANON_KEY` | Clave pública, sujeta a RLS | Frontend. Es pública por diseño |
| `SUPABASE_SERVICE_ROLE_KEY` | Clave que **salta RLS** | **Solo backend.** Jamás en el navegador, jamás en la extensión, jamás en el repositorio |

`RIESGO` La `service_role key` equivale a acceso total a la base de datos. Si
alguna vez aparece en el frontend, en un commit o en un log, hay que rotarla de
inmediato desde el panel de Supabase (START-HERE §23, "Secretos").

---

## Regla de oro

> Ninguno de estos valores se escribe en un archivo versionado.
> `.env.example` lleva marcadores; `.env` lleva los valores y está en
> `.gitignore`.

Comprobación rápida antes de cualquier commit:

```bash
git check-ignore -v .env      # tiene que responder con la linea de .gitignore
git grep -nE "(supabase\.co|service_role|eyJ[A-Za-z0-9_-]{20,})" -- . ':!*.md'
```

El segundo comando busca hosts de Supabase y claves JWT en el código. Debe salir
vacío.
