-- =============================================================================
-- 002 - Linea base de Row Level Security
-- =============================================================================
-- REGLA DEL PROYECTO, sin excepciones:
--
--     Toda tabla creada en el esquema veritai nace con RLS activado.
--
-- POR QUE DESDE EL DIA UNO, con cero tablas todavia:
--   En Supabase, PostgREST expone las tablas usando la anon key, que es
--   publica por diseno (viaja en el frontend). Una tabla sin RLS queda
--   legible desde internet. Activar RLS despues de la migracion significa
--   auditar tablas ya escritas; activarlo como convencion desde el principio
--   cuesta cero.
--   En el Postgres local RLS es practicamente inerte, porque la API se conecta
--   con veritai_app, que no es dueno de las tablas. Es decir: no molesta ahora
--   y evita un agujero despues.
--
-- Esta migracion no crea tablas de dominio a proposito. El proyecto esta en la
-- Puerta 1 (research/PILOT-DECISION.md) y las tablas de dominio se anaden
-- despues de PILOT_GO, no antes.
-- =============================================================================

-- Vista de cumplimiento: lista las tablas del esquema que NO tienen RLS.
-- Sirve como comprobacion previa a la migracion y como test en CI.
create or replace view veritai.v_cumplimiento_rls as
select
    c.relname                                    as tabla,
    c.relrowsecurity                             as rls_activado,
    c.relforcerowsecurity                        as rls_forzado_al_dueno,
    (select count(*) from pg_policy p where p.polrelid = c.oid) as politicas
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'veritai'
  and c.relkind = 'r';

comment on view veritai.v_cumplimiento_rls is
    'Toda fila con rls_activado = false es un bloqueante para migrar a Supabase.';

grant select on veritai.v_cumplimiento_rls to veritai_app;
