# 04 — Row Level Security: por qué desde el día uno

## El problema, en concreto

Un proyecto Supabase publica automáticamente su base de datos a través de
PostgREST. El frontend accede con la `anon key`, que **es pública por diseño**:
viaja dentro del JavaScript que se descarga el navegador. Cualquiera puede
leerla.

Lo único que separa esa clave pública de tus datos son las políticas RLS.

```
Tabla CON RLS y sin politica     ->  nadie lee nada. Seguro por defecto.
Tabla SIN RLS                    ->  cualquiera con la anon key lee la tabla
                                     entera. Y la anon key la tiene cualquiera.
```

No es un escenario teórico: es la fuga de datos más frecuente en proyectos
Supabase, y siempre por la misma razón —la tabla se creó antes de acordarse de
RLS y nadie volvió a mirarla.

---

## La regla del proyecto

> **Toda tabla creada en el esquema `veritai` nace con RLS activado.**
> Sin excepciones, y aunque hoy no exista Supabase por ningún lado.

Plantilla obligatoria para cualquier migración que cree una tabla:

```sql
create table veritai.mi_tabla (
    id          uuid primary key default gen_random_uuid(),
    creado_en   timestamptz not null default now()
    -- ...
);

-- Obligatorio, en la MISMA migracion que crea la tabla.
alter table veritai.mi_tabla enable row level security;

-- Sin politicas, la tabla queda cerrada a todo el mundo. Eso es lo correcto
-- por defecto: se abre despues, de forma explicita y justificada.
```

---

## Por qué hacerlo ahora, con cero tablas

Cuesta una línea por tabla hoy. Después de la migración cuesta auditar cada
tabla ya escrita, decidir su política sin recordar el contexto, y hacerlo con
datos reales dentro. Y mientras tanto, la ventana está abierta.

En el PostgreSQL local RLS es prácticamente inerte: la API se conecta con
`veritai_app`, que no es dueño de las tablas y no tiene permisos amplios. Es
decir: **no estorba ahora y evita un agujero después.**

---

## Comprobación automática

`db/migrations/002_rls_baseline.sql` crea esta vista:

```sql
select * from veritai.v_cumplimiento_rls where rls_activado = false;
```

Toda fila que devuelva es un bloqueante para migrar. Se comprueba:

- antes de cada migración a Supabase (`01-CHECKLIST-MIGRACION.md`),
- y como test de integración cuando exista la primera tabla.

---

## Qué NO resuelve RLS

RLS protege el acceso a filas. No sustituye a nada de lo que ya exige el
START-HERE §23–25:

- consultas parametrizadas — RLS no protege de una inyección SQL en el backend;
- usuario de aplicación con mínimo privilegio — ya implementado (`veritai_app`);
- validación de entrada con Pydantic;
- y la regla de que **el contenido externo es DATA, nunca INSTRUCCIÓN**, que es
  de otra capa por completo.
