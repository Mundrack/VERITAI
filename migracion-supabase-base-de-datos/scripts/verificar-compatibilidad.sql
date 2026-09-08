-- =============================================================================
-- Comprobacion previa a la migracion a Supabase
--
-- Se ejecuta contra la base de datos LOCAL antes de migrar. Cada bloque que
-- devuelva filas es un bloqueante que hay que resolver con una migracion nueva.
--
--   docker compose exec -T db psql -U veritai_migrator -d veritai \
--     -f /dev/stdin < migracion-supabase-base-de-datos/scripts/verificar-compatibilidad.sql
-- =============================================================================

\echo ''
\echo '=== 1. Tablas sin RLS (BLOQUEANTE) ================================='
\echo 'En Supabase quedarian legibles desde internet con la anon key.'
select c.relname as tabla
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'veritai'
  and c.relkind = 'r'
  and c.relrowsecurity = false;

\echo ''
\echo '=== 2. Tablas con RLS pero sin ninguna politica (revisar) =========='
\echo 'No es un fallo: sin politicas la tabla queda cerrada, que es el'
\echo 'comportamiento correcto por defecto. Solo hay que confirmar que es'
\echo 'lo que se queria.'
select c.relname as tabla
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'veritai'
  and c.relkind = 'r'
  and c.relrowsecurity = true
  and not exists (select 1 from pg_policy p where p.polrelid = c.oid);

\echo ''
\echo '=== 3. Objetos fuera del esquema veritai (BLOQUEANTE) =============='
\echo 'Todo lo de la aplicacion debe vivir en veritai. En public puede'
\echo 'chocar con lo que Supabase ya tiene.'
select n.nspname as esquema, c.relname as objeto, c.relkind as tipo
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind in ('r', 'v', 'm', 'S')
  and c.relname not like 'pg_%';

\echo ''
\echo '=== 4. Extensiones activas (revisar contra la lista de Supabase) ==='
select extname as extension, n.nspname as esquema
from pg_extension e
join pg_namespace n on n.oid = e.extnamespace
where extname <> 'plpgsql'
order by extname;

\echo ''
\echo '=== 5. Columnas timestamp SIN zona horaria (BLOQUEANTE) ============'
\echo 'Deben ser timestamptz. Con timestamp a secas, la hora depende del'
\echo 'servidor y local y Supabase pueden discrepar.'
select table_name as tabla, column_name as columna, data_type as tipo
from information_schema.columns
where table_schema = 'veritai'
  and data_type = 'timestamp without time zone';

\echo ''
\echo '=== 6. Funciones SECURITY DEFINER (revisar) ========================'
\echo 'Se ejecutan con los permisos de quien las creo. En Supabase, donde no'
\echo 'hay superusuario, cambian de comportamiento.'
select p.proname as funcion
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'veritai'
  and p.prosecdef = true;

\echo ''
\echo '=== 7. Migraciones aplicadas ======================================='
select archivo, aplicada_en from veritai_meta.schema_migrations order by archivo;

\echo ''
\echo '=== Fin. Cero filas en los bloques 1, 3 y 5 = listo para migrar ===='
