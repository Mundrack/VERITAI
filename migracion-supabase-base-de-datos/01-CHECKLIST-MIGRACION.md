# 01 — Checklist del día de la migración

Runbook. Se sigue en orden y no se salta ningún paso.

**Tiempo estimado:** 1–2 horas la primera vez.
**Requisito previo:** cuenta y proyecto de Supabase ya creados.

---

## Fase 0 — Antes de tocar nada

- [ ] El entorno local levanta correctamente: `docker compose up -d` y
      `curl http://127.0.0.1:8000/health` devuelve `base_de_datos: conectada`
- [ ] Los tests pasan
- [ ] El repositorio está limpio: `git status` sin cambios sin commitear
- [ ] Se trabaja en una rama: `git switch -c feat/migracion-supabase`
- [ ] **Volcado completo de la base de datos local**, guardado fuera del
      proyecto: `./scripts/exportar-a-supabase.sh`

`RIESGO` Sin el volcado del último punto no hay vuelta atrás. No es opcional.

---

## Fase 1 — Comprobación de compatibilidad

- [ ] Ejecutar `scripts/verificar-compatibilidad.sql` contra la base local:

```bash
docker compose exec -T db psql -U veritai_migrator -d veritai \
  -f /dev/stdin < migracion-supabase-base-de-datos/scripts/verificar-compatibilidad.sql
```

- [ ] Cero tablas sin RLS
- [ ] Cero objetos fuera del esquema `veritai`
- [ ] Cero extensiones activas que Supabase no permita
- [ ] Cero columnas `timestamp` sin zona horaria

Cualquier fila devuelta se arregla **con una migración nueva**, nunca editando
una migración ya aplicada.

---

## Fase 2 — Preparar el proyecto Supabase

- [ ] Anotar la referencia del proyecto (`<ref>`) y la región
- [ ] Copiar las dos cadenas de conexión de *Project Settings → Database*:
      la directa (5432) y la del pooler en modo *transaction* (6543)
- [ ] Comprobar que la conexión directa es alcanzable desde tu red
      (`03-VARIABLES-DE-ENTORNO.md`, nota sobre IPv6). Si no lo es, usar el
      pooler también para migrar
- [ ] Guardar la contraseña de la base de datos en un gestor de contraseñas.
      **No en el repositorio, no en un chat, no en un archivo suelto**

---

## Fase 3 — Aplicar el esquema

- [ ] Editar el `.env` **local** (no versionado) con los valores nuevos:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres.<ref>:<pass>@aws-0-<region>.pooler.supabase.com:6543/postgres
DATABASE_URL_MIGRATOR=postgresql+psycopg://postgres:<pass>@db.<ref>.supabase.co:5432/postgres
DB_USE_POOL=false
```

- [ ] Ensayo en seco, que no escribe nada:

```bash
docker compose run --rm migrate python /scripts/migrate.py --dir /migrations --dry-run
```

- [ ] Aplicar de verdad:

```bash
docker compose run --rm migrate
```

- [ ] Verificar en el panel de Supabase que existe el esquema `veritai` y que
      la tabla `veritai_meta.schema_migrations` tiene las tres filas

---

## Fase 4 — Migrar los datos

Solo si ya hay datos. Mientras el proyecto esté en la Puerta 1, no los hay.

- [ ] Volcar solo datos, sin esquema:

```bash
docker compose exec -T db pg_dump -U veritai_migrator -d veritai \
  --data-only --schema=veritai --column-inserts > datos.sql
```

- [ ] Cargar contra Supabase con `psql` usando la conexión **directa**
- [ ] Verificar recuentos tabla por tabla, origen contra destino

---

## Fase 5 — Levantar la aplicación contra Supabase

- [ ] Dejar de levantar el contenedor de PostgreSQL:

```bash
docker compose up -d api web        # sin el servicio db
```

- [ ] `curl http://127.0.0.1:8000/health/ready` → `estado: listo`
- [ ] Los tests siguen pasando
- [ ] Revisar los logs de la API: ni un error de conexión, ni una sentencia
      preparada duplicada (si aparecen, `DB_USE_POOL` no está en `false`)

---

## Fase 6 — Seguridad, antes de dar la migración por buena

- [ ] `select * from veritai.v_cumplimiento_rls where rls_activado = false;`
      devuelve **cero filas**
- [ ] La `service_role key` no aparece en ningún archivo del repositorio:

```bash
git grep -nE "(service_role|eyJ[A-Za-z0-9_-]{20,})" -- . ':!*.md'
```

- [ ] El `.env` sigue sin estar rastreado: `git check-ignore -v .env`
- [ ] Rotar la contraseña de la base de datos si en algún momento del proceso
      quedó pegada en un log, en un historial de terminal o en un chat

---

## Fase 7 — Cierre

- [ ] Anotar la fecha de la migración y la referencia del proyecto en este archivo
- [ ] Commit y pull request de la rama
- [ ] Mantener el volcado local al menos un mes
- [ ] Programar volcados periódicos desde Supabase (el plan gratuito tiene
      retención corta y el corpus anotado es trabajo manual irrecuperable)
