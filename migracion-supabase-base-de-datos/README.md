# Migración de la base de datos a Supabase

Esta carpeta contiene **todo lo necesario para mover la base de datos de VERITAI
desde el contenedor PostgreSQL local a un proyecto Supabase**, sin reescribir el
código de la aplicación.

Hoy no se usa. Existe porque las decisiones que hacen posible esa migración hay
que tomarlas **ahora**, mientras no hay tablas, no después, cuando haya treinta.

---

## Estado actual

| | |
|---|---|
| Base de datos en uso | PostgreSQL 17 en Docker (`pgvector/pgvector:pg17`) |
| Supabase | **No se usa todavía** — la cuenta del proyecto sigue en configuración |
| Cuándo se migra | Cuando la cuenta esté lista. No hay nada que bloquee el desarrollo mientras tanto |

---

## La idea en una frase

> La aplicación conoce **una sola** forma de llegar a la base de datos: la
> variable `DATABASE_URL`. Migrar consiste en cambiar su valor.

Supabase no es "otra base de datos": **es PostgreSQL**. Da una cadena de
conexión estándar. Si el código habla SQL, la migración es un cambio de
configuración. Si el código habla PostgREST a través del cliente `supabase-js` o
`supabase-py`, la migración es una reescritura de la capa de datos, y la vuelta
atrás es imposible.

De ahí la única regla dura de esta carpeta:

```
PROHIBIDO importar supabase-py o supabase-js en el codigo de dominio.
Se habla SQL. Siempre.
```

---

## Qué hay aquí

| Archivo | Para qué |
|---|---|
| `00-ESTRATEGIA-MIGRACION.md` | El contrato de portabilidad: qué está permitido escribir y qué no |
| `01-CHECKLIST-MIGRACION.md` | Runbook del día de la migración, paso a paso |
| `02-DIFERENCIAS-LOCAL-VS-SUPABASE.md` | Roles, extensiones, esquemas, pooler, límites |
| `03-VARIABLES-DE-ENTORNO.md` | Tabla de mapeo local ↔ Supabase, variable por variable |
| `04-RLS-Y-SEGURIDAD.md` | Row Level Security: por qué desde el día uno |
| `05-ROLLBACK.md` | Cómo volver a local si la migración falla |
| `config/supabase-config.toml.example` | Plantilla de configuración del CLI de Supabase |
| `scripts/verificar-compatibilidad.sql` | Detecta SQL que rompería en Supabase. Correr **antes** de migrar |
| `scripts/exportar-a-supabase.sh` | Volcado del esquema y los datos locales |

---

## Dónde viven las migraciones SQL

En **`db/migrations/`**, en la raíz del repositorio. No aquí.

Son la única fuente de verdad y ya están escritas para correr sin cambios en los
dos entornos. Duplicarlas en esta carpeta garantizaría que las dos copias se
separaran en unas semanas.

Esta carpeta contiene la **estrategia y el pegamento**; `db/migrations/` contiene
el **esquema**.
