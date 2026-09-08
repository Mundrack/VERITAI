-- =============================================================================
-- 000 - Roles estandar de Supabase
-- =============================================================================
-- POR QUE EXISTE ESTE ARCHIVO
--
-- Un proyecto Supabase trae de fabrica los roles anon, authenticated y
-- service_role. Toda politica RLS y todo GRANT que escribamos va a
-- referenciarlos. Si no existen en el Postgres local, ese mismo SQL falla aqui
-- y tendriamos que mantener dos versiones de cada migracion.
--
-- Creandolos localmente (y solo si faltan), el MISMO archivo .sql corre sin
-- cambios en los dos entornos. Es la pieza que hace portable todo lo demas.
--
-- Los tres son NOLOGIN: nadie se conecta con ellos. En Supabase son los roles
-- a los que PostgREST cambia mediante SET ROLE segun el JWT de la peticion.
-- =============================================================================

do $$
begin
    if not exists (select 1 from pg_roles where rolname = 'anon') then
        create role anon nologin noinherit;
        raise notice 'rol anon creado';
    end if;

    if not exists (select 1 from pg_roles where rolname = 'authenticated') then
        create role authenticated nologin noinherit;
        raise notice 'rol authenticated creado';
    end if;

    if not exists (select 1 from pg_roles where rolname = 'service_role') then
        -- bypassrls reproduce el comportamiento de Supabase: la service key
        -- salta las politicas RLS. Por eso esa clave jamas llega al navegador.
        create role service_role nologin noinherit bypassrls;
        raise notice 'rol service_role creado';
    end if;
end
$$;
