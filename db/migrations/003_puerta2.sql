-- =============================================================================
-- 003 - Puerta 2: trazabilidad del analisis (claims, evidencia, veredictos, audit)
-- =============================================================================
-- Primeras tablas de dominio. Llegan despues de PILOT_GO (DEC-023), como
-- mandaba la Puerta 1. Cinco tablas y ninguna mas: lo que el prototipo de
-- START-HERE §18 necesita para que cada numero del veredicto sea rastreable
-- hasta el texto literal de la fuente (raw_value_span).
--
-- REGLAS (002_rls_baseline):
--   - toda tabla nace con RLS activado y forzado al dueno
--   - veritai_app (la API) solo DML: insert y select; audit_log sin update/delete
--   - los roles de Supabase (anon, authenticated) no reciben nada
--   - los enums se copian como CHECK: el vocabulario es el de docs/GLOSARIO.md
-- =============================================================================

-- ---------------------------------------------------------------- claims ----
create table if not exists veritai.claims (
    claim_id            text primary key
                        check (claim_id ~ '^[A-Za-z0-9_.-]{1,64}$'),
    texto               text        not null check (length(texto) <= 2000),
    fuente_url          text        not null check (length(fuente_url) <= 2048),
    conjunto            text        not null check (conjunto in ('desarrollo', 'evaluacion')),
    tipo                text        not null check (tipo in ('cambio_entre_periodos', 'nivel', 'umbral',
                                                             'extremo_historico', 'crecimiento_compuesto', 'otro')),
    origen_case_id      text        not null default '',
    metrica             jsonb       not null,
    periodo_objetivo    text        not null,
    periodo_base        text,
    valores             jsonb       not null default '{}'::jsonb,
    notas               text        not null default '',
    creado_en           timestamptz not null default now()
);
comment on table veritai.claims is
    'Claim estructurado a mano (Puerta 2). conjunto=evaluacion nunca puede venir del piloto (DEC-025).';

-- ------------------------------------------------------ evidence_bundles ----
create table if not exists veritai.evidence_bundles (
    bundle_hash         text primary key check (bundle_hash ~ '^[0-9a-f]{64}$'),
    claim_id            text        not null references veritai.claims (claim_id),
    completeness        text        not null check (completeness in ('complete', 'partial', 'insufficient')),
    missing_slots       jsonb       not null default '[]'::jsonb,
    creado_en           timestamptz not null default now()
);
comment on table veritai.evidence_bundles is
    'sha256 de (fuente, serie, periodo, raw_value_span, version) de todos los items: mismo hash, misma evidencia.';

-- -------------------------------------------------------- evidence_items ----
create table if not exists veritai.evidence_items (
    id                  bigserial primary key,
    bundle_hash         text        not null references veritai.evidence_bundles (bundle_hash),
    rol                 text        not null check (rol in ('primary', 'historical', 'methodology')),
    etiqueta            text        not null,
    publisher           text        not null,
    url                 text        not null check (length(url) <= 2048),
    source_tier         smallint    not null check (source_tier between 1 and 5),
    retrieved_at        timestamptz not null,
    document_date       date,
    version             text        not null default '',
    format              text        not null check (format in ('api', 'dataset', 'html', 'pdf', 'scan', 'none')),
    extraction_method   text        not null,
    serie_codigo        text        not null,
    serie_nombre        text        not null,
    periodo             text        not null,
    valor               numeric,
    raw_value_span      text        not null check (length(raw_value_span) > 0)
);
create index if not exists evidence_items_bundle_idx on veritai.evidence_items (bundle_hash);
comment on column veritai.evidence_items.raw_value_span is
    'Texto literal de la fuente de donde salio el valor. Obligatorio: ningun numero sin origen.';

-- -------------------------------------------------------------- verdicts ----
create table if not exists veritai.verdicts (
    id                  bigserial primary key,
    claim_id            text        not null references veritai.claims (claim_id),
    bundle_hash         text        not null references veritai.evidence_bundles (bundle_hash),
    truth               text        not null check (truth in ('supported', 'contradicted', 'mixed',
                                                              'insufficient_evidence', 'not_applicable')),
    context             text        not null check (context in ('divergence_detected', 'no_divergence_detected',
                                                                'undetermined', 'not_applicable')),
    clase_primaria      text        not null check (clase_primaria in ('1_ranking_vs_value', '2_baseline_selection',
                                                   '2b_base_revisada', '3_absolute_vs_relative', '4_denominator',
                                                   '5_methodology_change', 'none', 'other_observed')),
    abstain_reasons     jsonb       not null default '[]'::jsonb,
    tests               jsonb       not null default '[]'::jsonb,
    comparaciones       jsonb       not null default '[]'::jsonb,
    numeros_usados      jsonb       not null default '[]'::jsonb,
    explicacion         text        not null,
    creado_en           timestamptz not null default now()
);
create index if not exists verdicts_claim_idx on veritai.verdicts (claim_id);
comment on table veritai.verdicts is
    'Dos ejes independientes (DEC-016). numeros_usados: cada numero de la explicacion con su raw_value_span.';

-- ------------------------------------------------------------- audit_log ----
create table if not exists veritai.audit_log (
    id                  bigserial primary key,
    claim_id            text        not null,
    bundle_hash         text,
    verdict_id          bigint,
    accion              text        not null,
    detalle             jsonb       not null default '{}'::jsonb,
    duracion_ms         integer     not null check (duracion_ms >= 0),
    creado_en           timestamptz not null default now()
);
comment on table veritai.audit_log is 'Append-only: veritai_app no tiene update ni delete.';

-- ------------------------------------------------------------------ RLS ----
alter table veritai.claims           enable row level security;
alter table veritai.evidence_bundles enable row level security;
alter table veritai.evidence_items   enable row level security;
alter table veritai.verdicts         enable row level security;
alter table veritai.audit_log        enable row level security;
alter table veritai.claims           force row level security;
alter table veritai.evidence_bundles force row level security;
alter table veritai.evidence_items   force row level security;
alter table veritai.verdicts         force row level security;
alter table veritai.audit_log        force row level security;

-- La API entra como veritai_app y ve todas las filas: no hay usuarios finales
-- todavia. Los roles de Supabase no tienen politica, luego no ven nada.
do $$
declare t text;
begin
    foreach t in array array['claims', 'evidence_bundles', 'evidence_items', 'verdicts', 'audit_log'] loop
        if not exists (select 1 from pg_policy p join pg_class c on c.oid = p.polrelid
                       join pg_namespace n on n.oid = c.relnamespace
                       where n.nspname = 'veritai' and c.relname = t and p.polname = 'app_todo') then
            execute format('create policy app_todo on veritai.%I for all to veritai_app using (true) with check (true)', t);
        end if;
    end loop;
end $$;

-- ------------------------------------------------------- minimo privilegio ----
grant select, insert, update on veritai.claims            to veritai_app;
grant select, insert         on veritai.evidence_bundles  to veritai_app;
grant select, insert         on veritai.evidence_items    to veritai_app;
grant select, insert         on veritai.verdicts          to veritai_app;
grant select, insert         on veritai.audit_log         to veritai_app;
grant usage, select on sequence veritai.evidence_items_id_seq to veritai_app;
grant usage, select on sequence veritai.verdicts_id_seq       to veritai_app;
grant usage, select on sequence veritai.audit_log_id_seq      to veritai_app;
