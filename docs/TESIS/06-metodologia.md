> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 6. Metodología

**Propósito.** Cómo se trabajó: puertas en lugar de calendario, reglas
fijadas antes de mirar los datos, dos métricas, cronómetro, separación de
conjuntos, anotación, y la prueba de predicción.

## Material que lo alimenta

| Qué | De dónde | Nota |
|---|---|---|
| Puertas 1–4 y sus criterios | `00b-DECISIONES-MATEO.md`; `CLAUDE.md` §2; `docs/ESTADO.md` | |
| La métrica que decidió la Puerta 1, escrita antes del número | `research/PILOT-DECISION.md` §La regla; DEC-019 (dos métricas), DEC-020 (denominador: todos los admitidos), DEC-021 (primer rechazo cierra) | 23/31 = 74,2 % |
| Regla dura anti-bot | DEC-018 ("si bloquea, ese es el resultado") | |
| Cronómetro y recuperabilidad-por-agente | DEC-014; `research/cronometro.log`; `research/scripts/cronometro.py` | tiempos de agente, no esfuerzo humano (`PILOT-FINDINGS` §3.4) |
| Separación de conjuntos | DEC-025 (piloto y Puerta 2 = desarrollo; evaluación aparte) | guardia del arnés |
| Dos vías de descubrimiento, registradas por caso | DEC-032; diseño §1b | busqueda_a_organismo 32 / titular_prensa 34 (2026-09-27) |
| Criba (regla dura: sin artículo de verificación previo) | diseño §0; campos `criba_query_a/b` en `research/puerta3/lote_evaluacion.py` | |
| Anotación con un solo humano, declarada | DEC-031; diseño §0 (muestra 25 % a ciegas, semilla 20260925, kappa agente–humano, revisión del 100 % si desacuerdo > 20 %) | **pendiente**: P-20 (5 casos de Mateo), muestra al congelar |
| Jornadas como medición con regla previa | DEC-033 (jornada 2), diseño §4b (jornada 3), §4h (jornada 5 como predicción preinscrita) | |
| Tope de tres por edición (controles y B) | diseño §1, §4c | |
| Congelado del conjunto | diseño §0: sha256 del CSV en una DEC antes de correr el arnés | **pendiente** |
| Método de la Puerta 2 (prototipo de una clase y un emisor) | DEC-028; `research/PUERTA-2-CASOS.md` §1 | |
| Método original planificado (para contraste) | `02-1` §Metodología (revisión sistemática, doble anotación 20 %, ablación) | lo que no se hizo se declara en 10 |

## No entra

Resultados (van en 10). Detalles del código (van en 7 y 8).
