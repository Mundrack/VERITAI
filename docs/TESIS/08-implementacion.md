> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 8. Implementación y verificación del prototipo

**Propósito.** Qué se construyó en cada puerta, cómo se verificó, y qué
enseñó (sin evaluar nada: todo es desarrollo hasta la sección 9).

## Material que lo alimenta

| Qué | De dónde | Número |
|---|---|---|
| Puerta 2: prototipo end-to-end, una clase (2a), un emisor (INE), 10 casos | `research/PUERTA-2-CASOS.md` §1–§9; DEC-028, DEC-029, DEC-030 | 10 casos por `POST /analisis`, HTTP 200, tres corridas; persistencia comprobada en Postgres (§5) |
| Lo que la Puerta 2 enseñó | `research/PUERTA-2-CASOS.md` §6; DEC-029 (señal de horizonte, `undetermined`, C17, P11 en `NEEDS_REVIEW`, 2b fuera) | P-23 sigue abierta |
| Recuperabilidad de la edición anterior fuera de Tempus (condición bloqueante de DEC-034) | `research/puerta3/RECUPERABILIDAD-2B.md` | 5 ediciones de 4 operaciones, todas 200; en las cinco el valor publicado difiere del vigente |
| Test 2b y conector, implementados | commit `2f151ef` (2026-09-26); `docs/ARQUITECTURA.md`, `docs/SEGURIDAD.md` | 114 tests; `ruff` limpio; los 7 B del conjunto disparan 2b con sus dos evidencias fechadas (`apps/api/tests/test_analisis_2b.py`) |
| Fixture de columnas verificadas contra los anexos | `apps/api/tests/fixtures/d2b/filas_absolutas.json` | 19 series, 9 ediciones |
| Arnés de evaluación | `research/arnes/README.md`, `arnes.py`, `metricas.py`, `test_metricas.py` | cinco métricas de R02 §7 + FPR + acuerdo; Wilson 95 % |
| Humo del arnés sobre desarrollo (no evalúa) | `research/arnes/humo-puerta2.md` (2026-09-26) | se cita solo como prueba de que el arnés corre |
| Cómo reproducir | `research/PUERTA-2-CASOS.md` §9; `CLAUDE.md` §6 (docker, pytest); `research/puerta2/ejecutar_casos.py` | |
| Herramientas de investigación | `research/puerta3/edicion_anterior.py`, `ine_buscar.py`, `validar_evaluacion.py`, `research/scripts/cronometro.py` | |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| El patrón de código de las notas del INE no está documentado y es una amenaza a la validez del conector | encuadre §Amenaza a la validez de 2b; `RECUPERABILIDAD-2B` | comprobación con el INE (documentación o consulta); hoy es observación propia | C8 |
| La edición anterior es recuperable por el agente en las operaciones del mapa | `RECUPERABILIDAD-2B` (5 ediciones, 200) | nada bibliográfico; empírico y disponible | — |
| La extracción por columna absoluta contra el anexo es robusta | `mapa_anexos.py`; fixture de 19 series | nada bibliográfico; queda la amenaza de cambio de formato del anexo (declarar) | C11 |
| Los 10 casos de la Puerta 2 no evalúan nada | DEC-025 | nada bibliográfico; regla propia con antecedente en separación de conjuntos | C7 |

## No entra

Ninguna métrica de los 10 casos como resultado (DEC-025). El `requirements.lock.txt`
se regenera desde el contenedor (pendiente, `docs/BITACORA.md`).
