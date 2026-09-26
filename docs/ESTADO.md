# Estado del proyecto

> **Este documento se sobrescribe entero en cada actualización.** Es una foto,
> no un historial. El historial está en [`BITACORA.md`](BITACORA.md).

**Última actualización:** 2026-09-25 (noche)

---

## Dónde estamos

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO        SUPERADA 2026-09-25
           TAREA 1 · TAREA 2 · TAREA 3 hechas                  (DEC-023, alcance nivel 1
                                                               por DEC-024)

PUERTA 2   prototipo end-to-end, UNA clase y UN emisor,      <-- AQUI, EJECUTADA:
           10 casos con trazabilidad completa                 10/10 corren por POST /analisis
           clase: 2a periodo o base elegida (DEC-026, P-12)    en feat/puerta-2-ine-2a,
           emisor: INE, API Tempus (DEC-024)                   SIN commitear. Cierre
           sin LLM en ningun paso (DEC-028)                    pendiente de que Mateo
           nada del piloto evalua (DEC-025)                    lea PUERTA-2-CASOS.md y
                                                               decida P-21, P-22 y C17

PUERTA 3   corpus completo anotado + arnes de evaluacion
           (conjunto de evaluacion recolectado aparte, DEC-025)

PUERTA 4   evaluacion completa: metricas, ablacion,
           sondas contrafactuales
```

**La métrica que decidió la Puerta 1** *(DEC-019, DEC-020, DEC-021)*: recuperable-por-agente
conservadora **23/31 = 74,2 %** (leniente 80,6 %; nivel 1 84,2 %, resto 58,3 %;
sin hermanos 72,0 %). Detalle en `research/PILOT-DECISION.md`. La humana real
sigue esperando los 5 casos de Mateo (P-20).

**Lo que salió de la Puerta 2** (`research/PUERTA-2-CASOS.md`, casos de desarrollo,
no evalúan):

```
test 2a   dispara 5 (signo 1: P11 · magnitud 3: N01 N03 N04 · valor de otro periodo 1: C17)
          no dispara 1 (C16, control) · no aplica 4 (C11 nivel; P04 P16 P19 abstencion por diseno)
truth     supported 4 · mixed 2 · contradicted 1 · insufficient_evidence 3
acuerdo con el corpus, dentro del alcance del prototipo   truth 4/4 · context 2/4
Postgres  claims 10 · bundles 10 · items 96 (0 sin raw_value_span) · verdicts 17 · audit 17
```

Los dos desacuerdos de contexto son decisiones de regla, no de cálculo:
**P-21** (la magnitud dispara con toda base declarada de horizonte largo) y
**P-22** (`undetermined` cuando ningún test aplica). C17 es un desacuerdo de
etiqueta que decide Mateo.

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
sin `-v`: los 10 claims y sus 17 veredictos siguen en el volumen).

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
| `validar_lote_crudo.py` sale 0: 38 candidatos, cero fuera de enum, 3 hitos por caso (avisa por C03) | ✅ | 2026-09-25 |
| Migración `003_puerta2.sql` aplicada al reconstruir la API | ✅ `listo: 1 migraciones aplicadas` | 2026-09-25 |
| Tests de la API (dominio, INE con fixture real, endpoint, trazabilidad) | ✅ **45 passed** | 2026-09-25 |
| `ruff check .` | ✅ `All checks passed!` | 2026-09-25 |
| 10 casos por `POST /analisis`, HTTP 200 los 10 | ✅ `research/puerta2/resultados.csv` | 2026-09-25 |
| Todo número del veredicto con `raw_value_span` | ✅ 96 items, 0 sin span (SQL) + test automático | 2026-09-25 |
| RLS activada y forzada en `claims`, `evidence_bundles`, `evidence_items`, `verdicts`, `audit_log` | ✅ `pg_class` | 2026-09-25 |
| Valores INE de C16/C17 (24,54 en 2025-T2 y 2026-T1) contrastados a mano con la API | ✅ coincidencia real | 2026-09-25 |
| Ninguna contraseña real en el repositorio ni en archivos sin seguimiento | ✅ `git grep` vacío | 2026-09-25 |

---

## Qué NO existe todavía, a propósito

| | Por qué |
|---|---|
| Cualquier LLM, local o remoto | DEC-028: el prototipo demuestra que la decisión no depende de un modelo; el claim se estructura a mano |
| Conectores de FMI e Interior (los otros dos emisores de DEC-024) | Puerta 2 = un emisor. Llegan con el conjunto de evaluación |
| Otras clases (1, 3, 4, 2b, 2c) como tests | Puerta 2 = una clase. 2b no es computable con Tempus solo (sirve la edición vigente) |
| N0 (regex + encoder) y N1 | Después del prototipo |
| Panel web que muestre veredictos | Solo si sobra tiempo; hoy pinta `/health` |
| La extensión MV3 | El panel web es el mismo código; se empaqueta más tarde |
| pgvector activado | La imagen lo trae; la extensión no hace falta hasta *embeddings* |
| Conjunto de evaluación | Se recolecta aparte, con el método de la TAREA 2, cuando P-21 y P-22 estén decididas (DEC-025) |
| Ratificación del cierre de la Puerta 2 | Es de Mateo, al leer `PUERTA-2-CASOS.md` |
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
main                          paquete + registro vivo + TAREAS 1-3 + entorno Docker + encuadre + P-12
│                             (todo fusionado con --no-ff; ultimo merge 11b9a00)
├─ docs/registro-vivo         FUSIONADO
├─ feat/auditoria-piloto-20   FUSIONADO (a946ff9)
├─ feat/lote-crudo-20         FUSIONADO (84303a8)
├─ feat/entorno-docker-local  FUSIONADO (26d42da)
├─ feat/via-descubrimiento    FUSIONADO (e6768e4)
├─ feat/tarea-3-decision      FUSIONADA (588fee6): TAREA 3 + DEC-023, DEC-024
├─ docs/p15-encuadre          FUSIONADA (c6c47e2): DEC-025, DEC-026, TESIS-ENCUADRE.md
├─ docs/p12-other-observed    FUSIONADA (3798414): desglose de other_observed
├─ docs/p12-cierre            FUSIONADA (11b9a00): DEC-027
│
└─ feat/puerta-2-ine-2a       Puerta 2: dominio + INE + POST /analisis + migracion 003   <- rama actual,
                              + 10 casos + PUERTA-2-CASOS.md + DEC-028 + P-21/P-22       SIN COMMITEAR
```

`CLAUDE.md` sigue siendo **propuesta** (P-02). Un archivo `AGENTS.md` apareció
sin seguimiento en la raíz (copia de las reglas de `CLAUDE.md`; no lo creó el
agente): queda sin tocar y sin commitear hasta que Mateo diga qué es.

`ATENCIÓN` No hay remoto configurado y `gh` no está instalado: las ramas
existen pero **no hay pull requests** (P-01). Nada se ha subido a ningún
servidor.

---

## Lo siguiente

En orden, y sin saltarse pasos:

1. ~~TAREA 1, TAREA 2, vía de descubrimiento, TAREA 3, ratificación del GO,
   P-15, P-12~~ **Hechas y fusionadas** (2026-09-24/25; DEC-013 a DEC-027).
2. ~~Puerta 2: plan de una página~~ **Aprobado y ejecutado el 2026-09-25**:
   dominio, conector INE, `POST /analisis`, migración 003, 10 casos de
   desarrollo (7 del piloto + N01, N03, N04) con trazabilidad completa.
   Informe: [`../research/PUERTA-2-CASOS.md`](../research/PUERTA-2-CASOS.md).
   Decisión registrada: DEC-028.
3. **Mateo:** leer el informe y decidir **P-21** (magnitud del 2a en horizontes
   largos declarados: mantener / subtipo / endurecer), **P-22** (`undetermined`
   sin test aplicable) y la etiqueta de **C17** (claim falso o 2a por valor
   atribuido a otro periodo). Con eso, ratificar o no el cierre de la Puerta 2.
4. **Commit** en `feat/puerta-2-ine-2a` cuando Mateo lo diga; **merge `--no-ff`**
   a `main` cuando lo diga.
5. **Mateo:** los 5 casos manuales (**C04, C05, C11, C14, C22**, semilla
   `20260925`), en tabla, cierran FINDINGS §7 (P-20). Si contradicen la
   lectura del agente, `PILOT-DECISION` se reabre.
6. `NEEDS_REVIEW` antes de citar P11 en texto: el 8.830 de la API coincide con
   la cifra de S.L. del PDF de 2019 (revisión o serie distinta); cotejar contra
   `research/evidencia/`.
7. Puerta 3, solo después de 3 y 4: recolectar el **conjunto de evaluación**
   con el método de la TAREA 2 (criba, cronómetro, vía), sin nada del piloto
   ni de la Puerta 2 (DEC-025); conectores de FMI e Interior; criterio de
   reaparición de P17/C10 aplicado una sola vez (DEC-027).

No se toca el test 2a a la vista de estos resultados: lo que cambie sale de
P-21, por escrito, antes del conjunto de evaluación.
