> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 7. Diseño del sistema

**Propósito.** Arquitectura, contratos, tests determinísticos, plantilla
numérica, trazabilidad y seguridad. Lo que existe, no lo planeado.

## Material que lo alimenta

| Qué | De dónde | Nota |
|---|---|---|
| Ecuación de responsabilidades (LLM interpreta, fuente = hechos, Python calcula, reglas = pruebas, plantilla explica, base de datos = trazabilidad) | `CLAUDE.md` §1 | |
| Arquitectura construida | `docs/ARQUITECTURA.md` §1–§8 (incluida la sección "El test 2b y el conector") | |
| Dirección de dependencias (api → application → domain; infraestructura implementa puertos) | `docs/ARQUITECTURA.md` §3; `CLAUDE.md` §4 | |
| Entidades: claim estructurado, `EvidenceItem` con `raw_value_span`, `EvidenceBundle` con `bundle_hash`, `Veredicto` con `evidencia_al_publicar` / `evidencia_vigente` | `apps/api/veritai/domain/` (`claim.py`, `evidencia.py`, `veredicto.py`) | |
| Tests 2a y 2b | `domain/tests/comparacion_base.py`, `domain/tests/base_revisada.py`; DEC-029, DEC-034 | tolerancia mínima 0,15; orden verdad → 2a → 2b |
| Reglas de `context` | `application/analizar_claim.py` docstring (DEC-016, R02 §10, DEC-029: sin test aplicable → `undetermined`) | |
| Abstención | enum `AbstainReason` (incl. `PREVIOUS_EDITION_OUT_OF_MAP`, no bloqueante); `domain/abstencion.py` | |
| Conector de edición anterior y mapa cerrado | `infrastructure/ine/edicion_anterior.py`, `mapa_anexos.py`; `docs/PROPUESTA-2B.md` | 8 operaciones; patrón `<PREFIJO><MM><YY>` |
| Amenaza a la validez del conector (patrón no documentado por el INE) | `docs/TESIS-ENCUADRE.md` §Amenaza a la validez de 2b | |
| Plantilla numérica, i18n (se traduce la plantilla, jamás el resultado) | `domain/plantilla.py`; DEC-009; `CLAUDE.md` §10 | |
| Base de datos y trazabilidad | DEC-001–DEC-007; `db/migrations/`; `docs/ARQUITECTURA.md` §5 (esquema `veritai`, RLS, `veritai_app` sin DDL) | |
| Seguridad implementada | `docs/SEGURIDAD.md` §Implementado y verificado (allowlist, timeout, tope de bytes, bytes mágicos, contenido externo = dato) | |
| Modelo de amenazas | `01-VERITAI-START-HERE` §23–25; `docs/SEGURIDAD.md` | |
| Librerías prohibidas y por qué | `CLAUDE.md` §7 | |
| Lo que la arquitectura no responde todavía | `docs/ARQUITECTURA.md` §8 | |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Separar cálculo (Python), recuperación (fuente) y explicación (plantilla) elimina la aritmética plausible y falsa | `CLAUDE.md` §1, §7 | evidencia sobre aritmética de los modelos y sobre arquitecturas que la delegan | C6 |
| Una plantilla numérica es preferible a una explicación generada libremente | DEC-009; `domain/plantilla.py` | literatura sobre generación controlada y trazabilidad de explicaciones | C6 |
| Un modelo de lenguaje no debe extraer celdas de un PDF; `pdfplumber`/`camelot` sí | `CLAUDE.md` §7 | evidencia sobre errores de extracción de tablas con modelos y sin ellos | C11 |
| Todo contenido externo es dato, nunca instrucción | `CLAUDE.md` §8; `SEGURIDAD.md` | literatura sobre inyección de prompt y mitigaciones | C12 |
| Allowlist, timeout, tope de bytes, bytes mágicos, bloqueo de rangos privados son los controles necesarios | `SEGURIDAD.md`; `01-START-HERE` §23–25 | referencia a estándares de seguridad de aplicaciones | C12 |
| Dos ejes (`truth`, `context`) en la salida en lugar de un único veredicto | DEC-016 | precedente en escalas de veredicto | C1, C2 |
| `raw_value_span` por número convierte la regla de arquitectura en un test automatizable | `CLAUDE.md` §1 | precedente de trazabilidad a nivel de celda/fragmento en verificación | C2, C6 |
| Traducir la plantilla y nunca el resultado renderizado evita reintroducir el riesgo | DEC-009; `CLAUDE.md` §10 | menor: práctica de i18n; puede quedar como decisión de diseño | C6 |

## No entra

N0/N1, extensión de navegador, modelo local: no existen (`docs/ESTADO.md`).
