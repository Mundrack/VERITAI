# Estado del proyecto

> **Este documento se sobrescribe entero en cada actualización.** Es una foto,
> no un historial. El historial está en [`BITACORA.md`](BITACORA.md).

**Última actualización:** 2026-09-25 (noche, tras DEC-030)

---

## Dónde estamos

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO        SUPERADA 2026-09-25
           TAREA 1 · TAREA 2 · TAREA 3 hechas                  (DEC-023, alcance nivel 1
                                                               por DEC-024)

PUERTA 2   prototipo end-to-end, UNA clase y UN emisor,      CERRADA 2026-09-25 (DEC-030)
           10 casos con trazabilidad completa                 fusionada a main (4403971);
           clase: 2a periodo o base elegida (DEC-026, P-12)    DEC-028, DEC-029 aplicadas.
           emisor: INE, API Tempus (DEC-024)                   Condicion pendiente anotada:
           sin LLM en ningun paso (DEC-028)                    P11 en NEEDS_REVIEW (P-23),
           nada del piloto evalua (DEC-025)                    no se cita hasta cotejarlo

PUERTA 3   corpus completo anotado + arnes de evaluacion     <-- AQUI, sin recolectar:
           conjunto de evaluacion recolectado aparte (DEC-025)  diseno del conjunto PROPUESTO
           diseno: research/PUERTA-3-DISENO.md                 (pendiente de aprobar);
           arnes: rama feat/arnes-evaluacion                   arnes en paralelo;
                                                               conectores FMI/Interior despues

PUERTA 4   evaluacion completa: metricas, ablacion,
           sondas contrafactuales
```

**La métrica que decidió la Puerta 1** *(DEC-019, DEC-020, DEC-021)*: recuperable-por-agente
conservadora **23/31 = 74,2 %** (leniente 80,6 %; nivel 1 84,2 %, resto 58,3 %;
sin hermanos 72,0 %). Detalle en `research/PILOT-DECISION.md`. La humana real
sigue esperando los 5 casos de Mateo (P-20).

**Lo que salió de la Puerta 2** (`research/PUERTA-2-CASOS.md`, casos de desarrollo,
no evalúan; corrida final tras DEC-029):

```
test 2a   confirmada 2 (P11 cambio de signo · C17 valor de otro periodo)
          senal de horizonte 3 (N01 N03 N04: se registran, no disparan)
          no dispara sin senal 1 (C16, control) · no aplica 4 (C11 nivel; P04 P16 P19 abstencion)
truth     supported 4 · mixed 2 · contradicted 1 · insufficient_evidence 3
context   divergence 2 · no_divergence 4 · undetermined 4
acuerdo con el corpus, dentro del alcance del prototipo   truth 4/4 · context 3/4 (C17, registrado)
Postgres  claims 10 · bundles 10 · items 96 (0 sin raw_value_span) · verdicts 27 · audit 27
```

Reglas que salieron de ahí y ya gobiernan (DEC-029): **solo el cambio de signo
confirma 2a**; la magnitud ≥ 2× en una base de horizonte largo es una *señal*,
registrada y explicada, que no cuenta; **sin test aplicable, `undetermined`**
(C11 se corrigió en el corpus, no en el sistema). C17 queda como discrepancia
para la evaluación. **P11 no se cita** hasta cotejarlo (`NEEDS_REVIEW`). 2b
fuera del prototipo: la API Tempus sirve solo la edición vigente.

---

## Qué funciona hoy

Entorno local en Docker más el primer flujo de dominio. Se levanta con un
comando y no requiere nada instalado aparte de Docker.

```bash
docker compose up -d
python research/puerta2/ejecutar_casos.py            # los 10 casos, resultados en research/puerta2/
python research/puerta2/ejecutar_casos.py --solo C16 # uno
```

| Servicio | Dirección | Estado |
|---|---|---|
| Web (Vite + TypeScript) | http://127.0.0.1:5173 | funcionando (solo `/health`; no muestra veredictos) |
| API (FastAPI) | http://127.0.0.1:8000 | funcionando, healthy; `POST /analisis` |
| API · OpenAPI | http://127.0.0.1:8000/docs | solo en local |
| PostgreSQL 17 | `127.0.0.1:55432` | funcionando, healthy; 5 tablas de dominio con RLS forzada |

Los contenedores quedaron **apagados** al cerrar la sesión (`docker compose down`,
sin `-v`: los 10 claims y sus 27 veredictos siguen en el volumen).

### Comprobado, no supuesto

| Comprobación | Resultado | Fecha |
|---|---|---|
| `docker compose up -d` levanta los 4 servicios | ✅ | 2026-09-08 |
| Cadena web → API → PostgreSQL | ✅ `base_de_datos: conectada` | 2026-09-08 |
| Migraciones idempotentes en la segunda pasada | ✅ `sin migraciones pendientes` | 2026-09-08 |
| `veritai_app` no puede hacer DDL | ✅ `permission denied for schema veritai` | 2026-09-08 |
| Los datos sobreviven a `down` y `up` | ✅ | 2026-09-08 |
| Roles de Supabase presentes en local | ✅ `anon`, `authenticated`, `service_role` | 2026-09-08 |
| `verificar-compatibilidad.sql` | ✅ 0 filas en los 3 bloques bloqueantes | 2026-09-08 |
| `tsc --noEmit` | ✅ sin errores | 2026-09-08 |
| `normalizar_a_enums.py` sale 0 (TAREA 1) | ✅ | 2026-09-25 |
| `validar_lote_crudo.py` sale 0: 38 candidatos, cero fuera de enum, 3 hitos por caso (avisa por C03; acepta `undetermined` en C11) | ✅ | 2026-09-25 |
| Migración `003_puerta2.sql` aplicada; segunda pasada idempotente | ✅ `sin migraciones pendientes (4 ya aplicadas)` | 2026-09-25 |
| Tests de la API (dominio, INE con fixture real, endpoint, trazabilidad, señal de horizonte) | ✅ **46 passed** | 2026-09-25 |
| `ruff check .` | ✅ `All checks passed!` | 2026-09-25 |
| 10 casos por `POST /analisis`, HTTP 200 los 10, tres corridas | ✅ `research/puerta2/resultados.csv` | 2026-09-25 |
| Todo número del veredicto con `raw_value_span` | ✅ 96 items, 0 sin span (SQL) + test automático | 2026-09-25 |
| RLS activada y forzada en `claims`, `evidence_bundles`, `evidence_items`, `verdicts`, `audit_log` | ✅ `pg_class` | 2026-09-25 |
| La señal de horizonte queda persistida en `verdicts.tests` | ✅ `["horizonte_largo"]` en N01, N03, N04 | 2026-09-25 |
| Valores INE de C16/C17 (24,54 en 2025-T2 y 2026-T1) contrastados a mano con la API | ✅ coincidencia real | 2026-09-25 |
| Ninguna contraseña real en el repositorio ni en archivos sin seguimiento | ✅ `git grep` vacío | 2026-09-25 |

---

## Qué NO existe todavía, a propósito

| | Por qué |
|---|---|
| Cualquier LLM, local o remoto | DEC-028: el prototipo demuestra que la decisión no depende de un modelo; el claim se estructura a mano |
| Conectores de FMI e Interior (los otros dos emisores de DEC-024) | Puerta 2 = un emisor. Llegan con el conjunto de evaluación |
| Otras clases (1, 3, 4, 2c) como tests; **2b fuera** | Puerta 2 = una clase. 2b no es computable con Tempus (solo edición vigente, DEC-029) |
| N0 (regex + encoder) y N1 | Después del prototipo |
| Panel web que muestre veredictos | Solo si sobra tiempo; hoy pinta `/health` |
| La extensión MV3 | El panel web es el mismo código; se empaqueta más tarde |
| pgvector activado | La imagen lo trae; la extensión no hace falta hasta *embeddings* |
| Conjunto de evaluación | Se recolecta aparte, con el método de la TAREA 2 (DEC-025). Es la Puerta 3 |
| El aparato completo de `/docs` y los ADR formales | Adenda D6: después de `PILOT_GO`; sigue pendiente |

---

## Base de datos

PostgreSQL 17 en Docker, volumen persistente `veritai_pgdata`. Los datos
sobreviven a `docker compose down`; solo se borran con `down -v`.

```
esquema veritai        claims · evidence_bundles · evidence_items · verdicts · audit_log
                       (003_puerta2; CHECK con los enums; RLS forzada; audit_log solo insert/select)
esquema veritai_meta   schema_migrations: 4 migraciones aplicadas
roles                  veritai_migrator (DDL) · veritai_app (solo DML)
                       anon · authenticated · service_role (compatibilidad Supabase)
```

**Supabase no se usa todavía.** La cuenta del proyecto sigue en configuración
y la contraseña sigue sin rotar (P-09: rotar antes de cargar datos reales). La
arquitectura está preparada para migrar cambiando `DATABASE_URL`: ver
[`../migracion-supabase-base-de-datos/`](../migracion-supabase-base-de-datos/README.md).

---

## Estado de git

```
main                          paquete + registro vivo + TAREAS 1-3 + Docker + encuadre + P-12 + PUERTA 2
│                             (todo fusionado con --no-ff)
├─ docs/registro-vivo         FUSIONADO
├─ feat/auditoria-piloto-20   FUSIONADO (a946ff9)
├─ feat/lote-crudo-20         FUSIONADO (84303a8)
├─ feat/entorno-docker-local  FUSIONADO (26d42da)
├─ feat/via-descubrimiento    FUSIONADO (e6768e4)
├─ feat/tarea-3-decision      FUSIONADA (588fee6): TAREA 3 + DEC-023, DEC-024
├─ docs/p15-encuadre          FUSIONADA (c6c47e2): DEC-025, DEC-026, TESIS-ENCUADRE.md
├─ docs/p12-other-observed    FUSIONADA (3798414): desglose de other_observed
├─ docs/p12-cierre            FUSIONADA (11b9a00): DEC-027
├─ feat/puerta-2-ine-2a       FUSIONADA (4403971): 104cf22 Puerta 2 tal como se reviso
│                             + a6c7d91 DEC-029 aplicada
│
├─ docs/cierre-puerta-2       DEC-030 (Puerta 2 cerrada), P-23, PUERTA-3-DISENO.md   <- SIN fusionar
└─ feat/arnes-evaluacion      arnes: cinco metricas de R02 §7 + FPR con intervalos    <- SIN fusionar
```

Las dos ramas nuevas se fusionan cuando Mateo lo diga; el diseño de la
Puerta 3 es propuesta hasta que lo apruebe.

`CLAUDE.md` sigue siendo **propuesta** (P-02); ahora lleva el estado de las
puertas y las reglas de DEC-025 y DEC-029. Un archivo `AGENTS.md` sigue sin
seguimiento en la raíz: **ni leído, ni aplicado, ni commiteado**, por
instrucción de Mateo, que lo revisa él.

`ATENCIÓN` No hay remoto configurado y `gh` no está instalado: las ramas
existen pero **no hay pull requests** (P-01). Nada se ha subido a ningún
servidor.

---

## Lo siguiente

En orden, y sin saltarse pasos:

1. ~~TAREA 1, TAREA 2, vía de descubrimiento, TAREA 3, ratificación del GO,
   P-15, P-12~~ **Hechas y fusionadas** (2026-09-24/25; DEC-013 a DEC-027).
2. ~~Puerta 2: plan, ejecución, decisiones sobre la primera corrida~~ **Hecho
   y fusionado el 2026-09-25** (DEC-028, DEC-029). Informe:
   [`../research/PUERTA-2-CASOS.md`](../research/PUERTA-2-CASOS.md).
3. ~~Cerrar la Puerta 2~~ **Cerrada el 2026-09-25 (DEC-030)**, con P11 en
   `NEEDS_REVIEW` como condición anotada (P-23).
4. **Mateo:** aprobar (o corregir) el **diseño del conjunto de evaluación**:
   [`../research/PUERTA-3-DISENO.md`](../research/PUERTA-3-DISENO.md). Lo que
   decide: tasa de H3 (10 % / límite superior 15 %), **50 controles con test
   aplicable (mínimo 40)**, resto de cubetas (total 110 / 78), tope de cuatro
   jornadas con revisión a la mitad, 25 % de doble anotación. **No se
   recolecta nada antes.**
5. En paralelo, sin depender del corpus: el **arnés** (rama
   `feat/arnes-evaluacion`): cinco métricas de R02 §7 + FPR con intervalos de
   Wilson; se prueba en humo sobre los 10 casos de desarrollo, marcados como
   tales.
6. Después del diseño aprobado: conectores de **FMI e Interior**; después,
   recolección y anotación; anotación congelada (sha256 en DEC) antes de
   correr el arnés; criterio de reaparición de P17/C10 aplicado una sola vez.
7. **Mateo:** los 5 casos manuales (**C04, C05, C11, C14, C22**, semilla
   `20260925`), en tabla, cierran FINDINGS §7 (P-20).
8. P-23: cotejar P11 contra `research/evidencia/` antes de citarlo.

No se toca el test 2a a la vista de resultados: lo que cambie sale de una DEC,
por escrito, y aplica al siguiente conjunto.
