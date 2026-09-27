> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 1. Resumen / Abstract

**Propósito.** Una página: problema, método, resultado principal con su
intervalo, limitación principal. Se escribe **al final**, con las cifras de
las secciones 8–10 ya cerradas. Versión en español y en inglés si la
plantilla lo pide (`NEEDS_REVIEW`).

## Material que lo alimenta

| Qué | De dónde | Estado |
|---|---|---|
| Título y pregunta de investigación | `docs/TESIS-ENCUADRE.md` §Título, §Pregunta (DEC-026) | disponible |
| Definición operacional de "divergencia contextual computable" | `docs/TESIS-ENCUADRE.md` §Definición operacional; `CLAUDE.md` §1 | disponible |
| Métrica de la Puerta 1 | `research/PILOT-DECISION.md`: 23/31 = 74,2 % conservadora (DEC-021), 25/31 = 80,6 % leniente, 2026-09-25 | disponible |
| Tamaño y composición del conjunto de evaluación | `research/puerta3/validar_evaluacion.py` (salida del 2026-09-27): 66 casos; A 31, B 7 (+1 excedente), C 2, D 10, E 11, F 3, O 1 | cambia con la jornada 5 |
| Recall de 2b con intervalo | diseño §4g: 7/7 → 100 % [64,6; 100]; 6/7 → 85,7 % [48,7; 97,4] (Wilson, `research/arnes/metricas.py`) | **pendiente**: arnés sobre el conjunto congelado |
| FPR (H3) | arnés, bloque 2; límite superior con 0/40 = 8,8 % | **pendiente**: A debe llegar a 40 |
| Resultado de la predicción P1/P2 | diseño §4h; `research/puerta3/PROGRESO.md` jornada 5 | **pendiente** (30-09 y 23-10) |
| Limitación principal | encuadre §Limitación explícita de H1 (DEC-035); diseño §0 (anotador único) | disponible |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Todo lo que afirme el resumen | secciones 8–10 | los números pendientes (arnés sobre el conjunto congelado, P1/P2, A = 40); ninguna afirmación bibliográfica propia | ninguna: el resumen no abre frentes nuevos |

## No entra

Cifras del piloto como prueba de hipótesis (DEC-025). Nada de intención
("no afirma intención", DEC-026).
