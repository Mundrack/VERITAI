# Estado del proyecto

> **Este documento se sobrescribe entero en cada actualización.** Es una foto,
> no un historial. El historial está en [`BITACORA.md`](BITACORA.md).

**Última actualización:** 2026-09-25 (tarde)

---

## Dónde estamos

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO        SUPERADA 2026-09-25
           TAREA 1 · TAREA 2 · TAREA 3 hechas                  (DEC-023, alcance nivel 1
                                                               por DEC-024)

PUERTA 2   prototipo end-to-end, UNA clase y UN emisor,      <-- AQUI, sin arrancar:
           10 casos con trazabilidad completa                 BLOQUEADA hasta que Mateo
                                                               cierre P-15 (la clase)

PUERTA 3   corpus completo anotado + arnes de evaluacion

PUERTA 4   evaluacion completa: metricas, ablacion,
           sondas contrafactuales
```

**La métrica que decide, en dos partes** *(DEC-019, 2026-09-25)*:

> Porcentaje de los candidatos **admitidos por la regla dura** (sin artículo de
> verificación previo) —todos los trabajados, no solo el lote por cubetas
> (DEC-020)— donde se localiza la **edición anterior** del dato, medido dos veces:
>
> ```
> recuperable-por-humano   una persona con navegador la localiza
> recuperable-por-agente   el sistema la localiza SIN evadir nada   <- DECIDE
> ```
>
> `>60%` verde → PILOT_GO · `30–60%` ámbar → alcance reducido · `<30%` rojo → PILOT_PIVOT
> — aplicado a la del **agente**. La humana se reporta como contexto.

**Valor medido el 2026-09-25** (`research/COLECCION-LOTE-CRUDO.md` §3), sobre
los 31 admitidos y trabajados:

```
recuperable-por-agente, conservadora   23/31   74,2%   <- DECIDE  (DEC-021: un 403/406/418 cierra)
recuperable-por-agente, leniente       25/31   80,6%      se reporta al lado
alcanzable_por_humano (si|probable)    29/31   93,5%
```

**Con su límite (DEC-020):** 19 de 31 son estadística oficial de nivel 1 —lo
que el buscador entrega con más facilidad— y ahí sale 84,2%; en el resto,
58,3%. El número no cambia; se declara. La humana real llega con los 5 casos
manuales de Mateo. **Esto no es la decisión**: la decisión es la TAREA 3.

---

## Qué funciona hoy

Entorno de desarrollo local completo en Docker (rama `feat/entorno-docker-local`,
sin fusionar). Se levanta con un comando y no requiere nada instalado en la
máquina aparte de Docker.

```bash
docker compose up -d
```

| Servicio | Dirección | Estado |
|---|---|---|
| Web (Vite + TypeScript) | http://127.0.0.1:5173 | funcionando |
| API (FastAPI) | http://127.0.0.1:8000 | funcionando, healthy |
| API · OpenAPI | http://127.0.0.1:8000/docs | solo en local |
| PostgreSQL 17 | `127.0.0.1:55432` | funcionando, healthy |

Verificación de la cadena completa:

```
$ curl http://127.0.0.1:8000/health
{"servicio":"veritai-api","version":"0.1.0","entorno":"local","base_de_datos":"conectada"}
```

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
| Tests de la API | ✅ 5 passed | 2026-09-08 |
| `ruff check` | ✅ sin avisos | 2026-09-08 |
| `tsc --noEmit` | ✅ sin errores | 2026-09-08 |
| Ninguna contraseña real en el repositorio | ✅ `git grep` vacío | 2026-09-08 |
| `normalizar_a_enums.py` sale 0 (TAREA 1) | ✅ | 2026-09-25 |
| `validar_lote_crudo.py` sale 0: 38 candidatos, cero fuera de enum, cubetas dentro de objetivo, 3 hitos por caso | ✅ | 2026-09-25 |

---

## Qué NO existe todavía, a propósito

| | Por qué |
|---|---|
| Tablas de dominio en la base de datos | Puerta 1. Llegan después de `PILOT_GO` |
| Endpoints que no sean de salud | Ídem |
| Cualquier LLM, local o remoto | R02 §15: no elegir modelo antes del piloto |
| Conectores a fuentes primarias | Se eligen con los datos del piloto, no antes |
| La extensión MV3 | El panel web es el mismo código; se empaqueta más tarde |
| pgvector activado | La imagen lo trae; la extensión no hace falta hasta *embeddings* |
| El aparato completo de `/docs` y los ADR formales | Adenda D6: después de `PILOT_GO` |
| Ratificación de `PILOT-DECISION.md` | Es de Mateo; y FINDINGS §7 (humano vs agente) espera sus 5 casos |

---

## Base de datos

PostgreSQL 17 en Docker, volumen persistente `veritai_pgdata`. Los datos
sobreviven a `docker compose down`; solo se borran con `down -v`.

```
esquema veritai        vacio a proposito. Las tablas llegan tras PILOT_GO
esquema veritai_meta   schema_migrations: 3 migraciones aplicadas
roles                  veritai_migrator (DDL) · veritai_app (solo DML)
                       anon · authenticated · service_role (compatibilidad Supabase)
```

**Supabase no se usa todavía.** La cuenta del proyecto sigue en configuración.
La arquitectura está preparada para migrar cambiando `DATABASE_URL`: ver
[`../migracion-supabase-base-de-datos/`](../migracion-supabase-base-de-datos/README.md).

---

## Estado de git

```
main                          paquete + registro vivo + TAREA 1 + TAREA 2 + entorno Docker
│                             (todo fusionado con --no-ff; ultimo merge 26d42da)
├─ docs/registro-vivo         FUSIONADO
├─ feat/auditoria-piloto-20   FUSIONADO (a946ff9)
├─ feat/lote-crudo-20         FUSIONADO (84303a8)
├─ feat/entorno-docker-local  FUSIONADO (26d42da)
│
├─ feat/via-descubrimiento    FUSIONADO (e6768e4)
│
└─ feat/tarea-3-decision      FUSIONADA: TAREA 3 + DEC-023, DEC-024

Sin rama de trabajo abierta: la siguiente (Puerta 2) se crea cuando Mateo
cierre P-15.
```

Con el entorno Docker en `main`, los enlaces a
`migracion-supabase-base-de-datos/` y a `CLAUDE.md` ya resuelven. `CLAUDE.md`
sigue siendo **propuesta** (P-02); lleva las reglas de DEC-017, DEC-018,
DEC-020 y DEC-021 añadidas como propuesta también.

`ATENCIÓN` No hay remoto configurado y `gh` no está instalado: las ramas
existen pero **no hay pull requests** (P-01). Nada se ha subido a ningún
servidor.

---

## Lo siguiente

En orden, y sin saltarse pasos:

1. ~~TAREA 1~~ **Hecha y fusionada** (2026-09-24/25).
2. ~~TAREA 2 — recolectar el lote crudo~~ **Hecha y commiteada el 2026-09-25**
   en `feat/lote-crudo-20` (pendiente de fusionar a `main`). Entregables en
   [`../research/COLECCION-LOTE-CRUDO.md`](../research/COLECCION-LOTE-CRUDO.md):
   38 candidatos, 31 trabajados, cubetas 7/7 · 6/6 · 3/3 · 2/2 · **0/2 formato
   hostil** (aceptado como hallazgo, DEC-022), lote de 23, 8 excedentes.
3. ~~P-16, P-17, P-18~~ **Decididas el 2026-09-25** (DEC-020 a DEC-022):
   decide la tasa natural sobre los 31; un 403/406/418 al primer cliente cierra
   el caso (C30 y C31 pasan a bloqueados, 74,2% conservadora); el déficit de
   formato hostil se acepta.
4. **Mateo:** los 5 casos manuales — **C04, C05, C11, C14, C22** (semilla
   `20260925`), solo con claim y URL, sin ver los resultados del agente. Están
   en `COLECCION-LOTE-CRUDO.md` §8. El agente no toca ese CSV.
5. ~~Reconstruir la vía de descubrimiento~~ **Hecha el 2026-09-25**: 38 de 38
   candidatos localizados en el transcript (35 por URL exacta, 3 por pista;
   23 consultas). `research/pilot-crudo-descubrimiento.csv` y columnas
   `descubrimiento_via/query` en screening y lote. Resultado: consultas que
   nombran un organismo → 92,3%; ranking/encuesta/tema → 50%; y **6 de 31
   casos salieron de la búsqueda negativa de otro candidato** (no son
   independientes). Ver `COLECCION-LOTE-CRUDO.md` §3.
6. ~~TAREA 3 — decidir~~ **Hecha el 2026-09-25** en `feat/tarea-3-decision`:
   [`../research/PILOT-DECISION.md`](../research/PILOT-DECISION.md) dice
   **`PILOT_GO` con alcance declarado a nivel 1** (conservadora 23/31 =
   74,2%; nivel 1 84,2%, resto 58,3%; sin hermanos 18/25 = 72,0%).
   [`PILOT-FINDINGS.md`](../research/PILOT-FINDINGS.md) lleva la sección de
   amenazas a la validez, el alcance honesto (P-19), P-15 con cinco opciones y
   recomendación (E objeto / B primera clase / A ilustrativa), y Perú/bloqueo
   ("no alcanza"). [`PILOT-FAILURES.md`](../research/PILOT-FAILURES.md), el
   catálogo de fallos.
7. ~~Ratificar `PILOT_GO`; decidir P-19~~ **Hecho el 2026-09-25**: GO
   ratificado (DEC-023); alcance de nivel 1 con INE, FMI e Interior (DEC-024).
8. **Mateo cierra P-15.** Va con la recomendación (E objeto, B primera clase,
   A ilustrativa, C subtipo de B) y pidió ver antes qué implica para el
   título y la hipótesis: la redacción propuesta está en
   [`PREGUNTAS-ABIERTAS.md`](PREGUNTAS-ABIERTAS.md), P-15. **Hasta que la
   apruebe o corrija, no se toca nada de la Puerta 2.**
9. **P-20:** los 5 casos manuales de Mateo, en tabla, cierran FINDINGS §7. Si
   contradicen la lectura del agente, la decisión se reabre.
10. **Puerta 2, después de 8:** prototipo de START-HERE §18 con INE como
    primer conector, la clase que salga de P-15, 10 casos de `PILOT-40.csv`,
    sin LLM.
7. ~~Fusionar `feat/entorno-docker-local`~~ **Hecho (26d42da).** Las reglas de
   DEC-017, DEC-018, DEC-020 y DEC-021 están en `CLAUDE.md` §3, como parte de
   la propuesta que Mateo revisa (P-02).

No se avanza a la Puerta 2 hasta entregar `PILOT-DECISION.md`.
