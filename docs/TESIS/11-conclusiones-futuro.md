> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 11. Conclusiones y trabajo futuro (materia final: referencias y anexos)

**Propósito.** Qué se sostiene y con qué intervalo, qué no, qué queda como
trabajo futuro; y la materia final que pida la plantilla (`NEEDS_REVIEW`: si
referencias y anexos son secciones propias, esta pasa a ser la 9 u otra
numeración).

## Material que lo alimenta

| Qué | De dónde | Estado |
|---|---|---|
| Conclusión por hipótesis | sección 10 | **pendiente** |
| Resultado negativo documentado si 2b no funciona | DEC-034 punto 5 | se escribe según 10 |
| Trabajo futuro: `other_observed` (P08, P09, P17, C10) | DEC-013, DEC-027; criterio de reaparición (diseño §2) | disponible |
| Trabajo futuro: lo no implementado | `CLAUDE.md` §11; `docs/ARQUITECTURA.md` §8 | disponible |
| Trabajo futuro: segundo anotador, ablación, baseline LLM, calibración | diseño §0; `02-1` §Evaluación | disponible como lista |
| Trabajo futuro: BdE como segunda operación con revisión (cuadro del PDF no extraíble) | `PROGRESO.md` §Jornada 4 | disponible |
| Preguntas abiertas | `docs/PREGUNTAS-ABIERTAS.md` (P-05, P-06, P-08, P-20, P-23, entre otras) | disponible |
| Referencias | **no existen en el repo** (ver sección 5) | **pendiente** |
| Anexo A: casos del conjunto | `research/puerta3/casos/*.json`; `evaluacion-anotacion.csv` | congelar antes |
| Anexo B: ediciones anteriores conservadas | `research/evidencia/D2B_*` con sha256 | disponible |
| Anexo C: cronómetro | `research/cronometro.log` | disponible |
| Anexo D: decisiones | `docs/DECISIONES.md` (DEC-001–DEC-035) | disponible |
| Anexo E: glosario y enums | `docs/GLOSARIO.md` | disponible |
| Anexo F: salida del arnés | `<salida>.md` y `<salida>.json` del arnés sobre el conjunto congelado | **pendiente** |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Lo que se concluya por hipótesis | sección 10 | los resultados del arnés y de P1/P2 (**pendiente**) | — |
| Los mecanismos `other_observed` (agregación de subgrupos P17, cambio sin edición anterior C10) merecen trabajo futuro | DEC-027 | relación con falacias de agregación conocidas | C3 |
| Un segundo anotador humano, la ablación y el baseline con modelo son el trabajo futuro correcto | diseño §0; `02-1` | precedente de qué añade cada uno | C6, C7 |
| El avance mensual del Banco de España es una segunda operación con revisión (2b posible) | `PROGRESO.md` §Jornada 4 | nada bibliográfico; empírico pendiente (cuadro del PDF no extraíble) | C4, C11 |

## No entra

Promesas sobre niveles 3–5 ("el 58,3 % es una limitación, no una promesa").
