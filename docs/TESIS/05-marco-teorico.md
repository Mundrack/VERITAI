> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 5. Marco teórico y estado del arte

**Propósito.** Taxonomía de divergencia (el núcleo teórico), conceptos con
definición cerrada, y la revisión de literatura que sitúa el trabajo.

## Material que lo alimenta

| Qué | De dónde | Estado |
|---|---|---|
| Taxonomía vigente (familias y clases: 1 ranking/valor, 2a periodo o base elegida, 2b base revisada, 2c cambio de método, 3 absoluto/relativo, 4 denominador) | `docs/TESIS-ENCUADRE.md` §Taxonomía (DEC-026); enum `Clase` en `apps/api/veritai/domain/enums.py` | disponible |
| Taxonomía original (para el contraste) | `02-1-VeritAI-TESIS.md` §Taxonomía de distorsión | disponible |
| Conceptos definidos | `docs/GLOSARIO.md` §Conceptos (edición al publicar / vigente, señal de horizonte, control natural, fallo de cobertura, hermano por criba, etc.) | disponible |
| Enums cerrados | `docs/GLOSARIO.md` §Enums cerrados; regla "una etiqueta que no se puede contar no es una etiqueta" (adenda D4) | disponible |
| Términos que NO se usan | `docs/GLOSARIO.md` §Términos que NO se usan | disponible |
| Truth y context como dos ejes | DEC-016; `01-VERITAI-START-HERE` §Truth, §Context; `04-...-R02` §10 | disponible |
| Subtipos de 2a y 2b | DEC-029 (signo, valor atribuido a otro periodo, señal de horizonte); `domain/tests/base_revisada.py` (signo, magnitud) | disponible |
| **Revisión de literatura** | **no existe en el repo.** El `02-1` la planificaba (semanas 1–2) y no se hizo | **pendiente, NEEDS_REVIEW**: verificación de hechos automatizada, claims numéricos, revisiones de datos oficiales, detección de comparaciones engañosas |

## No entra

Nada que afirme intención ("retórica general" está fuera, `CLAUDE.md` §11).
