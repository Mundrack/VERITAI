-- =============================================================================
-- 001 - Esquema de la aplicacion
-- =============================================================================
-- Se usa un esquema propio "veritai" en lugar de "public".
--
-- POR QUE NO public:
--   Supabase reserva auth, storage, realtime, extensions y graphql, y expone
--   public a traves de PostgREST por defecto. Un esquema propio no colisiona
--   con nada y deja explicito que se publica y que no.
--
-- ALTERNATIVA DESCARTADA: usar public. Mas corto de escribir hoy, pero el dia
-- de la migracion habria que auditar tabla por tabla que no choque con lo que
-- Supabase ya tiene ahi.
-- =============================================================================

create schema if not exists veritai;

comment on schema veritai is
    'Objetos de dominio de VERITAI. Portable entre Postgres local y Supabase.';

-- Minimo privilegio: se revoca todo lo que Postgres concede por defecto
-- y despues se concede solo lo necesario. START-HERE 23 y 25.
revoke all on schema veritai from public;

-- El usuario de la aplicacion puede entrar al esquema, pero NO crear objetos.
-- El DDL es exclusivo del usuario de migraciones.
grant usage on schema veritai to veritai_app;

-- Los roles de Supabase todavia no reciben nada. Cuando exista una tabla que
-- deba ser legible desde el cliente, se le concede permiso de forma explicita
-- y acompanada de su politica RLS. Nunca por defecto.

-- Los objetos que cree el usuario de migraciones a partir de ahora no otorgan
-- permisos a public automaticamente.
alter default privileges in schema veritai revoke all on tables from public;
alter default privileges in schema veritai revoke all on sequences from public;
alter default privileges in schema veritai revoke all on functions from public;
