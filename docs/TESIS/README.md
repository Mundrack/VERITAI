# Documento de tesis — esqueleto (formato UDLA, 11 secciones)

**Estado:** solo estructura (decisión de Mateo, 2026-09-27). **No se redacta**
hasta que lo diga. Nombre y orden de las secciones son provisionales:
`NEEDS_REVIEW` hasta cotejarlos con la plantilla de titulación de la UDLA
(P-06: existe, pendiente de entregar; no está en el repo). El mapeo de
material es por contenido, así que sobrevive a un cambio de nombres.

## Las 11 secciones

| # | Fichero | Sección (provisional) | Qué la sostiene hoy | Estado del material |
|---|---|---|---|---|
| 1 | [`01-resumen.md`](01-resumen.md) | Resumen / Abstract | los números finales de 8–10 | pendiente (se escribe al final) |
| 2 | [`02-introduccion.md`](02-introduccion.md) | Introducción: antecedentes, problema, pregunta | `TESIS-ENCUADRE`, `02-1`, DEC-026 | disponible |
| 3 | [`03-objetivos-hipotesis.md`](03-objetivos-hipotesis.md) | Objetivos e hipótesis | `TESIS-ENCUADRE` (H1–H3), DEC-031, DEC-034, DEC-035 | disponible |
| 4 | [`04-alcance-justificacion.md`](04-alcance-justificacion.md) | Alcance declarado y justificación | DEC-024, DEC-013, `PILOT-FINDINGS` §4, `CLAUDE.md` §11 | disponible |
| 5 | [`05-marco-teorico.md`](05-marco-teorico.md) | Marco teórico y estado del arte | taxonomía (`TESIS-ENCUADRE`, `GLOSARIO`), `02-1`; andamiaje Q1–Q12 / C1–C12 | taxonomía disponible; **literatura no existe en el repo**; andamiaje listo; primera referencia leída para el objeto de estudio (§D, Ecker et al. 2022) |
| 6 | [`06-metodologia.md`](06-metodologia.md) | Metodología | puertas (`00b`), DEC-014/018/019/020/021/025/031/032/033/035 | disponible |
| 7 | [`07-diseno-sistema.md`](07-diseno-sistema.md) | Diseño del sistema | `ARQUITECTURA`, `SEGURIDAD`, `GLOSARIO` enums, DEC-016, `PROPUESTA-2B` | disponible |
| 8 | [`08-implementacion.md`](08-implementacion.md) | Implementación y verificación del prototipo | `PUERTA-2-CASOS`, `RECUPERABILIDAD-2B`, tests, arnés | disponible; humo, no evaluación |
| 9 | [`09-evaluacion-diseno-corpus.md`](09-evaluacion-diseno-corpus.md) | Evaluación: diseño experimental y corpus | `PUERTA-3-DISENO`, `PILOT-DECISION`, lote de 66 | corpus en curso (jornada 5) |
| 10 | [`10-resultados-discusion.md`](10-resultados-discusion.md) | Resultados y discusión | arnés sobre el conjunto congelado, P1/P2, control natural, amenazas | **pendiente** en su mayor parte |
| 11 | [`11-conclusiones-futuro.md`](11-conclusiones-futuro.md) | Conclusiones y trabajo futuro (+ referencias y anexos como materia final) | DEC-027, `PREGUNTAS-ABIERTAS`, `CLAUDE.md` §11, anexos del repo | estructura lista; contenido depende de 10 |

## Campo común a las once fichas

**"Qué afirma esta sección que hoy no está respaldado"**: una tabla por
ficha con la afirmación, dónde la hace el repo, qué falta (bibliográfico o
empírico pendiente) y en qué categoría de la sección 5 (C1–C12) buscar
literatura. Es el índice de dónde buscar. La sección 5 lleva además el
andamiaje del estado del arte: preguntas Q1–Q12, categorías C1–C12 y el mapa
consolidado sección → afirmación → categoría. **Sin fuentes: las pone Mateo.**

## Reglas del esqueleto

- **Un número, una fuente.** Cada cifra del documento sale de un fichero del
  repo con fecha (validador, arnés, CSV, DEC). Ninguna cifra se redacta de
  memoria. Los que cambian con la jornada 5 llevan **pendiente**.
- **Las decisiones se citan por número** (DEC-NNN) y las amenazas a la validez
  se declaran donde nacieron (`PILOT-FINDINGS` §3, diseño §0/§4, encuadre).
- **No se traduce ningún resultado**: las tablas se generan desde el arnés
  (`research/arnes/arnes.py`) y se pegan; el texto explica, no recalcula.
- **Lo que no entra**: el piloto no prueba H1–H3 (DEC-025); el lote crudo y
  los 10 casos de la Puerta 2 son desarrollo; `other_observed` (P08, P09,
  P17, C10) va a trabajo futuro.

## Materia final (fuera de las 11 o dentro, según la plantilla)

- **Referencias**: no hay bibliografía en el repo. Se construye en 5.
- **Anexos**: `research/puerta3/casos/*.json` (un JSON por caso, con spans),
  `research/puerta3/evaluacion-anotacion.csv` (congelado con sha256 en una
  DEC), `research/evidencia/D2B_*` (ediciones anteriores con sha256),
  `research/cronometro.log`, `docs/DECISIONES.md` completo, `docs/GLOSARIO.md`
  (enums cerrados).
