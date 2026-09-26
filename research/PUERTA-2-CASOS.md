# Puerta 2 — prototipo end-to-end: una clase (2a), un emisor (INE), 10 casos

**Fecha:** 2026-09-25 (noche; los sellos del cronómetro son UTC, 2026-09-26T00:59–01:45Z)
**Rama:** `feat/puerta-2-ine-2a` · **Plan aprobado:** el de una página (sesión del 2026-09-25)
**Conjunto:** los 10 casos son de **desarrollo** (DEC-025). Ninguno evalúa nada.
**Versión:** tras las decisiones de Mateo sobre la primera corrida (DEC-029). La
primera corrida y lo que se decidió a partir de ella están en §6.

> Este documento reporta lo que el prototipo hizo con 10 claims reales, número
> a número. No es una evaluación: es la prueba de que la cadena
> *claim estructurado → evidencia con spans → test 2a → veredicto en dos ejes →
> explicación → auditoría* existe y deja rastro. Los desacuerdos con el corpus
> se reportan; el único que se corrigió en el corpus (C11) lo decidió Mateo.

---

## 1. Qué se construyó

```
POST /analisis
   │  JSON del claim, estructurado A MANO (sin LLM en ningún paso)
   ▼
ClaimEstructurado ──► ProveedorINE (API Tempus, allowlist servicios.ine.es)
                          │  descarga la tabla, casa la serie por nombre exacto
                          ▼
                     EvidenceBundle: objetivo · base_claim · ref:anterior · ref:interanual
                                     · ventana (8 periodos) · metodología
                                     cada número con su raw_value_span literal del JSON
                          │
                          ▼
             hard gates de abstención ──► test 2a (determinístico) ──► verdad (tolerancias)
                          │
                          ▼
              Veredicto {truth, context, clase, abstain_reasons, tests[senales], numeros_usados}
              + explicación por plantilla + fila en audit_log + 5 tablas con RLS
```

| Capa | Archivos | Qué hace |
|---|---|---|
| dominio | `domain/{enums,periodo,claim,evidencia,verdad,abstencion,veredicto,plantilla,puertos}.py`, `domain/tests/comparacion_base.py` | entidades, aritmética de periodos, hard gates, **test 2a**, verdad con tolerancias, plantilla. Sin infraestructura |
| aplicación | `application/analizar_claim.py` | el caso de uso: claim → bundle → gates → test → verdad → veredicto → persistencia |
| infraestructura | `infrastructure/ine/{tempus,extractor,proveedor}.py`, `infrastructure/repositorio.py` | cliente Tempus (allowlist, timeout, tamaño máximo, UA identificado, 401/403/406/418/429 = rechazo, DEC-018/021), extractor con spans literales, repositorio Postgres en una transacción |
| API | `api/routes/analisis.py` | `POST /analisis`, validación pydantic (emisor `INE`, tabla `^\d{1,8}$`, periodos parseados, texto ≤ 2000) |
| base de datos | `db/migrations/003_puerta2.sql` | `veritai.claims`, `evidence_bundles`, `evidence_items`, `verdicts`, `audit_log`; CHECK con los enums; RLS activada **y forzada**; `veritai_app` solo DML, `audit_log` solo insert/select |
| casos | `research/puerta2/casos/*.json`, `generar_casos_piloto.py`, `ejecutar_casos.py` | los 10 claims estructurados; el script que los corre y escribe `resultados/*.json`, `resultados.csv`, `resultados.md` |

**El test 2a, definido antes de correr los casos (DEC-028) y afinado por
decisión después de verlos (DEC-029):**

- Aplica solo a `cambio_entre_periodos` con base declarada.
- **(B) `valor_atribuido_a_otro_periodo`** — dispara: el valor que el claim
  atribuye al periodo objetivo no cuadra ahí, pero sí en otro periodo de la
  ventana de 8.
- **(A) `cambio_de_signo`** — dispara: la base del claim no coincide con
  ninguna referencia del emisor (periodo anterior o interanual) **y**
  recomputar el cambio contra la referencia principal **invierte el signo**.
- **Señal `horizonte_largo`** — no dispara: la base no es referencia del
  emisor y la magnitud recomputada difiere ≥ 2× (o ≤ 0,5×) **sin** cambiar
  de signo. Se registra en `tests[].senales`, en `calculos.senal` y en la
  explicación; no toca `context`. Solo el signo confirma 2a (DEC-029).
- Tolerancias: valores, media unidad del último decimal del claim (mínimo 0,5 %
  relativo); cambios, lo mismo con mínimo 0,15.
- `context`: test aplicable y no dispara, sin motivos de abstención →
  `no_divergence_detected` (una señal no cambia esto); ningún test aplicable →
  `undetermined` (DEC-029, P-22); motivo bloqueante → `insufficient_evidence` /
  `undetermined`.

---

## 2. Los 10 casos

**Composición (aprobada en el plan):** los 7 casos del piloto cuya primaria es
el INE (todos los que hay: DEC-024) más 3 claims crudos nuevos con mecanismo 2a,
recolectados con el método de la TAREA 2 (regla dura, criba de verificadores,
cronómetro, vía registrada). Por qué no "10 de clase 2a": un prototipo de una
clase necesita casos donde **no** deba disparar.

| Caso | Origen | Tipo | Serie INE (tabla) | Para qué está |
|---|---|---|---|---|
| C11 | piloto, crudo | nivel | IPC variación anual (25333) | nivel correcto: el test 2a no aplica |
| C16 | piloto, crudo | cambio | EPA tasa de paro < 25 (65334) | **control negativo** con test aplicable: base = referencia del emisor |
| C17 | piloto, crudo | cambio | EPA tasa de paro < 25 (65334) | claim falso (24,5 % es el valor del trimestre anterior) |
| P11 | piloto, auditado | cambio | sociedades mercantiles (13913) | el único 2a del piloto con primaria INE (`NEEDS_REVIEW`, §4) |
| P04 | piloto, auditado | crecimiento compuesto | condenados delitos sexuales (28724) | fuera del alcance del prototipo: debe abstenerse |
| P16 | piloto, auditado | umbral | EPA horas extra no pagadas, mujeres (65217) | fuera del alcance: debe abstenerse |
| P19 | piloto, auditado | extremo histórico | EPA tasa de paro < 25 (65334) | fuera del alcance: debe abstenerse |
| **N01** | nuevo | cambio | IPV vivienda nueva (80270) | base declarada prepandemia (4T2019) |
| **N03** | nuevo | cambio | EPA asalariados sector público (65183) | base declarada política (2T2018) |
| **N04** | nuevo | cambio | IPC alimentos, media anual (50934) | base declarada previa al episodio inflacionario (2020) |

### 2.1 Recolección de los tres nuevos

Método de la TAREA 2, sin cambios: búsqueda dirigida a organismo, criba contra
Newtral / Maldita / EFE Verifica / Verificat, cronómetro `t0 t1 t2` en
`research/cronometro.log`, vía y consulta registradas en el bloque
`_recoleccion` de cada JSON.

| Id | Medio, fecha | Claim | Criba | Resultado |
|---|---|---|---|---|
| N01 | El Independiente, 2026-04-21 | "Desde 2019 los salarios han crecido un 1% mientras la vivienda se ha disparado un 64%" | sin verificación | **admitido** |
| N02 | Ethic, 2026-06-15 | nacimientos −38 % desde 2008 | Newtral tiene explainers con las mismas cifras (519.779 → 321.164) | **rechazado**, `cobertura_explainer` |
| N03 | The Objective, 2026-06-08 | "Uno de cada seis empleados públicos logró su puesto durante los gobiernos de Sánchez" | ningún verificador cubre las cifras; el explainer de Maldita (2022) es de nivel, no de cambio | **admitido** |
| N04 | economia3, 2026-05-26 | "Hacer la compra cuesta un 37% más" (alimentos +37 % entre 2020 y 2024, IPC) | Newtral 2026-09-22 (Feijóo, frescos de agosto) no cubre la cifra | **admitido** |

Candidatos vistos y **no usados**, con motivo: Libre Mercado (pluriempleo
+53,55 % desde 3T2018) — misma base política que N03 y tema cubierto por el
fact-check de Newtral del 2026-06-12; El Independiente 2026-05-06 (funcionarios
crecen 4× más que el privado con Sánchez) y The Objective 2025-10-25 (142
puestos públicos al día) — hermanos de N03 por serie y base.

**Tope de tiempo del plan (≤ 2 h):** los 7 del piloto corrieron a las
00:59Z; N01 `t0` a las 01:04:36Z; N04 `t2` a las 01:12:48Z. La recolección
entera cupo en **unos 15 minutos** de reloj. El inicio exacto de la búsqueda no
quedó cronometrado (se toma como cota el `t0` de N01); los tres casos salieron
en la primera pasada, lo que es una limitación de diversidad, no un mérito:
son tres bases elegidas de tres tipos (prepandemia, política, pre-inflación),
pero un solo recolector y una sola tarde.

---

## 3. Resultados (corrida final, tras DEC-029)

Tabla generada por `ejecutar_casos.py` (01:43–01:45Z; ningún número se teclea):

| caso | origen | tipo | truth | context | clase | abstención | test 2a | corpus (truth/context/clase) | acuerdo | ms |
|---|---|---|---|---|---|---|---|---|---|---|
| C11 | C11 | nivel | supported | undetermined | none | — | n/a | supported / undetermined / none | true / true | 14043 |
| C16 | C16 | cambio_entre_periodos | supported | no_divergence_detected | none | — | no dispara | supported / no_divergence_detected / none | true / true | 3459 |
| C17 | C17 | cambio_entre_periodos | contradicted | divergence_detected | 2_baseline_selection | — | DISPARA valor_atribuido_a_otro_periodo | contradicted / no_divergence_detected / none | true / false | 26 |
| N01 |  | cambio_entre_periodos | mixed | no_divergence_detected | none | — | no dispara · señal horizonte_largo | — | — | 2515 |
| N03 |  | cambio_entre_periodos | supported | no_divergence_detected | none | — | no dispara · señal horizonte_largo | — | — | 354 |
| N04 |  | cambio_entre_periodos | mixed | no_divergence_detected | none | — | no dispara · señal horizonte_largo | — | — | 353 |
| P04 | P04 | crecimiento_compuesto | insufficient_evidence | undetermined | none | UNSUPPORTED_CLAIM_TYPE | n/a | contradicted / divergence_detected / 3_absolute_vs_relative | false / false | 188 |
| P11 | P11 | cambio_entre_periodos | supported | divergence_detected | 2_baseline_selection | — | DISPARA cambio_de_signo | supported / divergence_detected / 2_baseline_selection | true / true | 6079 |
| P16 | P16 | umbral | insufficient_evidence | undetermined | none | UNSUPPORTED_CLAIM_TYPE | n/a | contradicted / no_divergence_detected / none | false / false | 929 |
| P19 | P19 | extremo_historico | insufficient_evidence | undetermined | none | UNSUPPORTED_CLAIM_TYPE | n/a | mixed / divergence_detected / 3_absolute_vs_relative | false / false | 3697 |

```
truth     supported 4 · mixed 2 · contradicted 1 · insufficient_evidence 3
context   divergence_detected 2 · no_divergence_detected 4 · undetermined 4

test 2a   2a CONFIRMADA 2   (cambio_de_signo: P11 · valor_atribuido_a_otro_periodo: C17)
          señal horizonte_largo 3 (N01 N03 N04: no disparan, quedan registradas)
          no dispara, sin señal 1 (C16)
          no aplicable 4 (C11 nivel · P04 P16 P19 abstención)

FPR sobre controles con test aplicable   0 / 1   (solo C16; n = 1 no mide nada, es humo)
```

**Acuerdo con el corpus (7 casos del piloto):** truth 4/7, context 3/7. Los
tres desacuerdos en `truth` (P04, P16, P19) son abstenciones **por diseño**: el
prototipo no evalúa esos tipos de claim. Sobre los 4 casos dentro del alcance
del prototipo: truth **4/4**, context **3/4**; el desacuerdo que queda (C17)
está registrado en el corpus y se resuelve en el conjunto de evaluación
(DEC-029). C11 coincide porque **se corrigió el corpus**, no el sistema (§4).

**Latencia:** mediana ≈ 1,7 s; máximo 14,0 s (C11: la tabla 25333 del IPC es
grande); 26 ms cuando la tabla ya está en caché (C17 tras C16). Las descargas
son de tablas enteras con `nult` calculado para cubrir el periodo más antiguo
que el claim necesita.

---

## 4. Trazabilidad caso a caso

Cada caso tiene su respuesta completa en `research/puerta2/resultados/<id>.json`
(veredicto, tests con `calculos` y `senales`, `numeros_usados`, evidencia con
`raw_value_span` de cada número). Aquí, lo que importa de cada uno.

**C16 · control negativo.** Claim: cae al 23,77 % (−0,77 pp del 1T al 2T).
Fuente: 2T2026 = 23,77; base 1T2026 = 24,54; cambio −0,77 pp: cuadra. La base
del claim **es** la referencia del emisor (trimestre anterior): el test no
dispara y no hay señal. `supported / no_divergence_detected`. Coincide con el
corpus.

**C17 · claim falso.** Claim: "escala hasta el 24,5 % en el segundo trimestre".
Fuente: 2T2026 = 23,77 (no cuadra), y baja, no sube (no cuadra):
`contradicted`. El test dispara por **(B)**: 24,5 es el valor de 1T2026
(24,54). El corpus lo tiene como `no_divergence_detected` (claim falso sin
más). Es el mismo mecanismo con el que DEC-027 pasó P05 a 2a ("valor real
atribuido al periodo equivocado"). **Decisión (DEC-029): no se reetiqueta.**
La discrepancia queda anotada en las `notas` de C17 y se resuelve en el
conjunto de evaluación, no caso a caso. Dato verificado contra el INE: 2025-T2
y 2026-T1 valen exactamente 24,54; el test atribuye al más cercano en la
ventana.

**C11 · nivel.** Claim: IPC de agosto 4,3 %. Fuente: 4,3: cuadra. Ningún test
aplica a un nivel y el prototipo devuelve `undetermined`. El corpus decía
`no_divergence_detected`. **Decisión (DEC-029, P-22): el sistema tiene razón
y el corpus estaba mal**: sin test aplicable no se puede afirmar ausencia de
divergencia. Se corrigió la etiqueta del corpus (`lote_crudo.py`, los CSV y
`PILOT-40.csv`), la cubeta `control_negativo` se conserva, y el FPR se mide
sobre controles con test aplicable. Queda como **hallazgo**: la anotación
humana afirmaba algo que el método no puede afirmar.

**P11 · el 2a por signo.** Claim: creación de empresas −23 % (mayo → diciembre
de 2018). Fuente: 8.830 → 6.809 = −22,89 %: cuadra. Referencia interanual
(diciembre de 2017 = 6.735): **+1,10 %**. Cambia de signo → dispara (A),
subtipo `cambio_de_signo`. `supported / divergence_detected / 2a`. Coincide
con el corpus en los tres campos. **`NEEDS_REVIEW` — no se cita (DEC-029):**
el PDF de febrero de 2019 usado en el piloto daba 8.908 (total) / 8.830 (S.L.)
y 6.811; la API de hoy da 8.830 y 6.809 para "Mercantiles". O la serie fue
revisada, o la serie de la API no es el mismo total que usó el PDF. Se coteja
contra `research/evidencia/` antes de usarlo en cualquier texto.

**N01 · base prepandemia.** Claim: vivienda +64 % desde 2019. Serie: IPV
vivienda nueva (la que el propio artículo cita para el 64 %). Fuente: 4T2019
62,739 → 4T2025 102,559 = **+63,47 %**; el claim dice 64 → fuera de la
tolerancia (0,5) pero con la dirección correcta: `mixed`. Referencia
interanual (4T2024 = 92,211): **+11,22 %**; ratio 5,7, mismo signo → **señal
de horizonte**, no dispara: `no_divergence_detected`, clase `none`. Tres
observaciones: (1) el artículo escribe 63,7 % y la API da 63,5 %: el IPV se
revisa (el span lleva `T3_TipoDato: Definitivo`; la nota de prensa de marzo
pudo ser provisional); (2) el titular llama "la vivienda" a un subgrupo: el
índice general dio +49,0 % en el mismo tramo — **reaparece el mecanismo
candidato P17** (agregación con subgrupos), segunda aparición, en conjunto de
desarrollo, así que no cuenta para el criterio de DEC-027 pero se anota; (3)
el 1 % de salarios queda fuera: una métrica por claim.

**N03 · base política.** Claim: 3.662.500 (1T2026) frente a 3.117.800
(2T2018), +544.700, +17,5 %. Fuente: los cuatro números cuadran (17,47 %).
Referencia interanual (1T2025 = 3.499,1): **+4,67 %**; ratio 3,7, mismo signo
→ señal de horizonte: `supported / no_divergence_detected`. "Uno de cada
seis" es 544,7 / 3.662,5 = 14,9 %, no 16,7 %: redondeo del titular, no del
dato.

**N04 · base previa a la inflación.** Claim: alimentos +37 % entre 2020 y 2024.
Fuente: medias anuales 98,187 → 129,105 = **+31,49 %**: no cuadra, dirección
sí: `mixed`. Referencia (2023 = 124,659): +3,57 %; ratio 8,8, mismo signo →
señal de horizonte: `no_divergence_detected`. Observación registrada, no
corregida: el 37 % coincide con el informe Idra citado por Infobae (productos
más baratos +37 % 2021–2024). El artículo lo atribuye al IPC del INE; el
prototipo evalúa el claim tal como se afirma.

**P04, P16, P19 · fuera del alcance.** Abstención con
`UNSUPPORTED_CLAIM_TYPE` (crecimiento compuesto, umbral con denominador,
extremo histórico). El bundle se construye igual: P04 queda `partial` con
`base_claim` ausente (la tabla 28724 empieza en 2017; 1998 no existe), pero el
motivo `PREVIOUS_EDITION_NOT_FOUND` solo se evalúa para cambios entre periodos,
así que no aparece. P19 descarga la ventana completa de la tasa (10 items) y
aun así se abstiene: correcto. **P04 encontró un bug**: la primera corrida
devolvió `EXTRACTION_FAILED | PRIMARY_SOURCE_NOT_FOUND` porque las tablas
anuales del INE traen `T3_Periodo: "A"` y el parser esperaba dígitos. Corregido
en `Periodo.desde_ine`, con test, y reconstruida la imagen de la API.

---

## 5. Persistencia y trazabilidad, comprobadas en Postgres

```
veritai.claims             10        (upsert por claim_id)
veritai.evidence_bundles   10        (una fila por bundle_hash; sin cambios entre corridas 2 y 3)
veritai.evidence_items     96        0 sin raw_value_span
veritai.verdicts           27        7 (00:59Z) + 10 (01:13Z) + 10 (01:44Z, tras DEC-029)
veritai.audit_log          27        una fila por análisis
RLS                        activada y forzada en las 5 tablas
```

- **`bundle_hash` estable entre corridas** para todos los casos desde la
  segunda corrida; C16 y C17 comparten hash (mismos items). Entre la primera y
  la segunda, **P04 cambió** (`4f53cda1…` → `52338f45…`): la corrección del
  periodo anual cambió lo extraído, y el hash lo delata. Es exactamente para
  lo que existe.
- La señal de horizonte queda en `verdicts.tests` (`senales`) y en
  `calculos.senal`: la tercera corrida guarda los mismos bundles con veredictos
  distintos, y la auditoría lo muestra.
- `test_trazabilidad.py` comprueba en cada respuesta que **todo número del
  veredicto tiene su `raw_value_span`** en la evidencia.
- La explicación es una plantilla numérica; no hay LLM en ninguna etapa.

---

## 6. Lo que la Puerta 2 enseñó y lo que se decidió (DEC-029)

La primera corrida marcó `divergence_detected` en N01, N03 y N04 por el
criterio de magnitud (ratio 5,7 / 3,7 / 8,8) y C11 salió `undetermined` contra
un corpus que decía `no_divergence_detected`. Se reportó sin retocar nada y
Mateo decidió:

1. **Magnitud ≥ 2× no es evidencia de divergencia por sí sola** (P-21). Toda
   base declarada de horizonte largo la produce contra una referencia
   interanual. Se separa como **señal de horizonte**; **solo el cambio de signo
   confirma 2a**. El umbral no cambia; cambia lo que significa. Endurecer
   (disparar solo por signo y descartar la señal) se descartó: la señal se
   registra para poder estudiarla en la evaluación.
2. **Sin test aplicable, `undetermined`** (P-22). C11 se queda así; **el
   sistema tiene razón y el corpus estaba mal**. Se corrige la etiqueta del
   corpus, no el sistema; queda como hallazgo sobre la anotación humana.
3. **C17 no se reetiqueta.** Discrepancia anotada; se resuelve en el conjunto
   de evaluación.
4. **P11 no se cita** hasta cotejarlo contra `research/evidencia/`.
5. **La API Tempus sirve solo la edición vigente.** Las revisiones (P11, N01)
   se ven comparando con el PDF antiguo, no desde la API. **2b queda fuera del
   prototipo** como limitación del conector (`ARQUITECTURA.md` §8,
   `TESIS-ENCUADRE.md`).

Lo que sigue abierto o anotado, sin decisión nueva:

- **Caso canónico de la familia B (cinco requisitos, DEC-026): sigue sin
  haberlo.** Los 10 son 2a y el conector no ve revisiones. Queda para el
  conjunto de evaluación, con ediciones anteriores documentales.
- **Deuda técnica:** la caché de tablas del proveedor vive en la instancia de
  la API y solo se invalida al pedir un periodo más antiguo (hace falta TTL o
  descarga por petición). El item de metodología usa el año centinela 1900.
- **Mecanismo candidato P17, segunda aparición** (N01). Conjunto de
  desarrollo: no cuenta para el criterio de reaparición de DEC-027. Se anota.
- **Otros niveles del corpus:** la regla de P-22 se aplicó a C11 porque fue el
  caso que la hizo visible. Al anotar el conjunto de evaluación, todo claim
  sin test aplicable se etiqueta `undetermined` desde el principio.

---

## 7. Qué NO se hizo (a propósito)

N0 y N1; extensión de navegador; otros emisores (FMI, Interior) u otras
clases; ningún LLM; ningún conjunto de evaluación; el panel web no muestra
veredictos; `pgvector` sigue sin activar; 2b fuera (DEC-029). Ninguno de estos
10 casos entrará en la evaluación (DEC-025).

---

## 8. Verificación

| Comprobación | Resultado |
|---|---|
| `pytest` en `apps/api` | **46 passed** (`-p no:warnings`), 2026-09-25, con el test de la señal de horizonte |
| `ruff check .` | limpio |
| `validar_lote_crudo.py`, `pilot40.py` tras corregir C11 | salen 0; el validador acepta `undetermined` para controles de nivel |
| 10 casos por `POST /analisis`, HTTP 200 los 10, tres corridas | ✅ |
| Todo número del veredicto con `raw_value_span` | ✅ (96 items, 0 sin span; test automático) |
| `docker compose up -d --build api`; migración 003 aplicada e idempotente | ✅ `sin migraciones pendientes (4 ya aplicadas)` |
| `veritai_app` sin DDL; RLS forzada en las 5 tablas | ✅ |
| Ninguna contraseña ni clave en el diff | ✅ `git grep` vacío |

## 9. Cómo reproducir

```bash
docker compose up -d
python research/scripts/validar_lote_crudo.py     # CSV del corpus (C11 con undetermined)
python research/scripts/pilot40.py                # PILOT-40.csv
python research/puerta2/generar_casos_piloto.py   # reescribe los 7 JSON del piloto desde PILOT-40.csv
python research/puerta2/ejecutar_casos.py         # corre los 10 y escribe resultados/, resultados.csv, resultados.md
python research/puerta2/ejecutar_casos.py --solo N03
```

Los tres JSON nuevos (`N01`, `N03`, `N04`) están escritos a mano, con su bloque
`_recoleccion`; el script los envía sin ese bloque.
