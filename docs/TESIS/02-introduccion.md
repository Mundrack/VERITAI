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

## No entra

Revisión de literatura (va en 5). Objetivos e hipótesis (van en 3).
