# 05 — Volver atrás

La migración a Supabase es **reversible por diseño**. Ese es el motivo de todas
las reglas de `00-ESTRATEGIA-MIGRACION.md`.

---

## Volver a local: procedimiento

1. Restaurar en el `.env` los valores locales que nunca se borraron:

```dotenv
DATABASE_URL=postgresql+psycopg://veritai_app:<pass>@db:5432/veritai
DATABASE_URL_MIGRATOR=postgresql+psycopg://veritai_migrator:<pass>@db:5432/veritai
DB_USE_POOL=true
```

2. Levantar todo otra vez:

```bash
docker compose up -d
```

3. Si el volumen local se había borrado, recrear el esquema y cargar el volcado:

```bash
docker compose run --rm migrate
docker compose exec -T db psql -U veritai_migrator -d veritai < datos.sql
```

**Tiempo estimado: minutos.** No hay que tocar código.

---

## Por qué funciona

Porque no hay nada que deshacer en el código:

| | |
|---|---|
| Consultas escritas contra PostgREST | ninguna |
| Dependencias del SDK de Supabase | ninguna |
| Migraciones en un formato propietario | ninguna |
| Lógica que dependa de Auth, Storage o Realtime | ninguna |

Lo único específico de Supabase es el **valor** de dos variables de entorno.

---

## Qué haría irreversible la migración

Se documenta para reconocerlo a tiempo:

- introducir `supabase-py` o `supabase-js` en el código de dominio;
- usar Supabase Auth como única fuente de identidad sin un puerto que la aísle;
- guardar archivos solo en Supabase Storage, sin un adaptador local equivalente;
- depender de Edge Functions para lógica de negocio;
- usar `pg_net`, `pgsodium` o cualquier extensión que no exista en un Postgres
  estándar.

Ninguna de estas está prohibida para siempre. Lo que está prohibido es
adoptarlas **sin decidirlo a propósito** y sin escribir aquí el coste de salida.
