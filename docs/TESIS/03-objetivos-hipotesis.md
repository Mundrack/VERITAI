> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 3. Objetivos e hipótesis

**Propósito.** Objetivo general, objetivos específicos y las tres hipótesis
con la tasa de H3 fijada antes de evaluar y la limitación explícita de H1.

## Material que lo alimenta

| Qué | De dónde | Nota |
|---|---|---|
| Objetivo general y específicos | `docs/TESIS-ENCUADRE.md` §Objetivo general, §Objetivos específicos | manda sobre `02-1` §Objetivos |
| H1 objeto, H2 computabilidad, H3 falsos positivos | `docs/TESIS-ENCUADRE.md` §Hipótesis | texto literal |
| Tasa de H3 fijada a priori | `research/PUERTA-3-DISENO.md` §1: FPR ≤ 10 % y límite superior Wilson 95 % ≤ 15 %; mínimo 40 controles (DEC-031) | tabla de límites por n y k en §1 |
| Clase principal y secundaria | DEC-034: B = 2b (base revisada); 2a secundaria con 0/43 | |
| Limitación explícita de H1 | DEC-035; encuadre §Limitación explícita de H1; diseño §4g: B declarada con 7, Wilson 7/7 [64,6; 100] | "existencia y computabilidad, no frecuencia" |
| Qué afirma la tesis y qué no | `docs/TESIS-ENCUADRE.md` §Qué afirma la tesis y qué no | incluye "no afirma que 2b sea frecuente" (DEC-035) |
| Hipótesis auxiliar sobre dónde aparece 2b | diseño §4d (fijada por Mateo antes de la jornada 4) y §4h (predicción P1/P2 preinscrita el 2026-09-27, commit `13e03fa`) | resultado **pendiente** |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Un FPR ≤ 10 % con límite superior Wilson ≤ 15 % es una tasa razonable para H3 | diseño §1 ("propuesta", aprobada en DEC-031) | justificación externa del orden de magnitud, o declararlo como convención del proyecto | C7 |
| Wilson al 95 % y la regla de tres son el método adecuado para proporciones con n pequeño | `research/arnes/metricas.py`; diseño §1 | referencia del método | C7 |
| H2: la divergencia se decide con tests determinísticos sobre dos ediciones | encuadre §Hipótesis; DEC-028, DEC-034 | antecedente de verificación numérica contra datos estructurados | C2 |
| H1 se puede sostener como existencia y computabilidad sin afirmar frecuencia | DEC-035; encuadre §Limitación explícita de H1 | precedente de estudios de existencia/mecanismo con n pequeño y su forma de reportarse | C7 |
| La hipótesis §4d (2b aparece donde el redactor calcula la tasa) tiene un mecanismo plausible | diseño §4d, §4e | literatura sobre rutinas de redacción con estadísticas oficiales | C5 |

## No entra

Los objetivos del `02-1` que el encuadre dejó fuera (calibración Brier/ECE,
extensión de navegador, ablación LLM): se citan en 11 como trabajo futuro si
procede.
