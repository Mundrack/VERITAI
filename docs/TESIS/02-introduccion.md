> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 2. Introducción: antecedentes, problema y pregunta

**Propósito.** Por qué existe el problema (afirmaciones estadísticas con dato
verdadero y comparación que no se sostiene), qué no resuelve la verificación
de hechos clásica, y la pregunta de investigación tal como quedó tras el
piloto.

## Material que lo alimenta

| Qué | De dónde | Nota |
|---|---|---|
| El problema en una frase | `02-1-VeritAI-TESIS.md` §"El problema, en una frase"; `03-2-VeritAI-PROYECTO-TOTAL.md` | el `02-1` es la propuesta original; **manda el encuadre** (`docs/README.md`) |
| Pregunta de investigación vigente | `docs/TESIS-ENCUADRE.md` §Pregunta de investigación (DEC-026) | |
| Definición operacional | `docs/TESIS-ENCUADRE.md` §Definición operacional; `CLAUDE.md` §1 | tres condiciones: verificable con `raw_value_span`, comparación distinta de la del emisor, test determinístico |
| La regla que define la arquitectura | `CLAUDE.md` §1: "ningún número del veredicto puede tener como único origen el LLM" | |
| Dos ejes, no una clase más | DEC-016 (`truth` y `context`) | |
| Antecedente empírico: el piloto | `research/PILOT-FINDINGS.md` §0–§2; `research/AUDIT-PILOT-20.md` | solo como descubrimiento y refinamiento (DEC-025) |
| Caso ilustrativo del fenómeno | E043 (Baleares, +3,8 % publicado frente a −2,3 % con la edición vigente) y E053 (Galicia, +0,68 % frente a −0,35 %): `research/puerta3/casos/E043.json`, `E053.json` | son casos de **evaluación**: se citan como ilustración sin adelantar resultados |
| Por qué no hay caso canónico todavía | `docs/TESIS-ENCUADRE.md` §Caso canónico | |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Existe un tipo de afirmación con dato verdadero y comparación insostenible, y es relevante para la verificación | encuadre §Definición operacional; `PILOT-FINDINGS` §0–§2 (46 casos) | relevancia más allá del piloto; cómo lo nombran y tratan los verificadores; **no** se afirma frecuencia (DEC-035) | C1, C2, C9 |
| La verificación de hechos clásica (¿es verdadero el dato?) no cubre ese caso | encuadre (afirmación propia); respaldo parcial leído en 05 §D (Ecker et al. 2022, ms p. 28), de revisión | descripción de los pipelines y escalas de veredicto existentes y de su hueco | C1, C2 |
| Un número del veredicto no puede tener como único origen un modelo de lenguaje | `CLAUDE.md` §1 | evidencia sobre aritmética y alucinación numérica de los modelos | C6 |
| Las revisiones de datos oficiales cambian comparaciones ya publicadas | E043, E053, E066; `RECUPERABILIDAD-2B` (5 ediciones) | la política del INE ya está leída y citada (IME §14.1 y §17 de EOH, EOAP y EOAC; Política de revisión 2015; `research/puerta3/METODOLOGIA-REVISION-INE.md`); falta la literatura general sobre revisiones de datos oficiales y su magnitud | C4 |
| El caso canónico de base revisada con los cinco requisitos todavía no existe | encuadre §Caso canónico | nada bibliográfico; se resuelve o no con el conjunto de evaluación | — |

## No entra

Revisión de literatura (va en 5). Objetivos e hipótesis (van en 3).
