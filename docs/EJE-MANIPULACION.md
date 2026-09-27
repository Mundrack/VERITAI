# Eje de detección de manipulación

**Estado:** entra al proyecto por decisión de Mateo (DEC-036, 2026-09-27).
**Se construye después de cerrar la Puerta 3, no en paralelo.** Hasta
entonces este documento solo acumula: definición, preguntas abiertas, papers
que Mateo vaya dejando y las decisiones ya tomadas que lo condicionan. Nada
de aquí es código ni diseño aprobado.

---

## 1. Qué es y qué no es

**Qué es.** Un eje de análisis distinto de los dos actuales (`truth`,
`context`) que detecta **técnicas de lenguaje persuasivo** en el texto que
rodea una afirmación estadística: marcadores que la propia frase o el
artículo emplean para orientar la lectura de la cifra. Su salida, cuando
exista, será del mismo tipo que la del resto del sistema: una etiqueta de un
**enum cerrado** por técnica, con el **fragmento literal** del texto que la
sostiene (`raw_text_span`, el análogo de `raw_value_span`), y una explicación
por plantilla. Una técnica es una propiedad observable del texto; se cuenta,
se muestra y se puede discutir.

**Qué no es.**

- **Nunca afirma intención del autor.** Detectar una técnica no es decir que
  alguien quiso engañar. Es la misma regla que ya rige los dos ejes
  (`TESIS-ENCUADRE`, "no afirma que el autor quiso engañar"; DEC-026). La
  salida no lleva "manipulación" como veredicto sobre una persona o un
  medio: lleva técnicas presentes, con su span.
- **No es el eje de verdad.** Un texto con técnicas persuasivas puede llevar
  una cifra correcta y bien enmarcada; un texto neutro puede llevar una 2b.
  Los ejes se reportan por separado y no se suman en una puntuación.
- **No es "retórica general"** abierta: sin enum cerrado no hay eje (adenda
  D4, `CLAUDE.md` §5). Cada técnica que entre tendrá definición, ejemplo
  positivo, ejemplo negativo y criterio de anotación.
- **No es** detección de texto generado por IA, deepfakes, multimodal ni
  análisis del feed (`CLAUDE.md` §11): siguen fuera.
- **No decide con un modelo de lenguaje.** El LLM puede interpretar y
  proponer; la etiqueta final sale de algo auditable (reglas, o un
  clasificador pequeño y evaluable con su propio F1, como se exige a N0), y
  cada etiqueta lleva su span. Qué mezcla exacta es una pregunta abierta
  (§2).

## 2. Preguntas abiertas (se resuelven por DEC, después de la Puerta 3)

### Corpus propio

- **Unidad de anotación:** ¿la frase que contiene la cifra, el párrafo, el
  titular, el artículo entero? Cambia el corpus, el anotador y la métrica.
- **Origen del texto:** ¿los mismos artículos del conjunto de evaluación de
  la Puerta 3 (ya recolectados, con criba y cronómetro) o un corpus nuevo?
  Reutilizarlos es barato y mantiene la separación desarrollo/evaluación
  (DEC-025) solo si el eje se evalúa sobre otro conjunto; hay que decidirlo
  antes de anotar una sola línea.
- **Controles:** textos con cifra correcta y sin técnicas (el equivalente de
  la cubeta A) para medir falsos positivos; ¿de dónde salen y cuántos?
- **Lengua:** solo español (regla vigente de análisis). ¿Variedades regionales
  y latinoamericanas cuentan igual?
- **Tamaño:** el mismo razonamiento de intervalos que en la Puerta 3 (Wilson,
  mínimo por técnica). Sin número hasta tener la taxonomía.

### Anotadores

- **Manual de anotación** con definición por técnica, ejemplos y casos
  límite, escrito antes de anotar.
- **¿Cuántos anotadores humanos?** La Puerta 3 declara como amenaza tener un
  solo humano que además diseñó la taxonomía (DEC-031, diseño §0). Un eje de
  lenguaje persuasivo es más subjetivo que uno numérico: la necesidad de un
  segundo anotador (P-05) es mayor, no menor.
- **Acuerdo:** kappa por técnica; qué umbral mínimo se exige antes de usar la
  etiqueta.
- **Anotación por agente:** ¿anota el agente y el humano revisa, como en la
  Puerta 3, o al revés? Qué se declara en cada caso.

### Evaluación

- **Métrica por técnica** (precisión, recall, F1) y **falsos positivos sobre
  controles** con intervalo, fijados antes de medir (misma disciplina que
  §4l del diseño de la Puerta 3).
- **Qué se compara:** el detector contra la anotación humana; y si hay
  modelo de lenguaje en el proceso, el detector completo contra el modelo
  solo (la ablación que la Puerta 3 no hizo).
- **Independencia de ejes:** comprobar que la presencia de técnicas no
  cambia `truth` ni `context` en el sistema (no debe).
- **Presentación:** cómo se muestra "técnicas presentes" sin que el lector lo
  lea como "manipulado". Se decide con la plantilla, no con el modelo.

### Taxonomía

- **Qué técnicas entran** y con qué nombre; enum cerrado desde el primer día.
- **Relación con el eje de contexto:** una "base elegida" (2a) es una
  operación con la cifra; un "adjetivo de alarma" es una operación con el
  texto. ¿Dónde se traza la frontera cuando el texto *explica* la base
  elegida?

## 3. Papers y material (lo va dejando Mateo)

Entrada primero en `docs/IDEAS.md` si trae una idea; aquí, la referencia y
lo que aporta. **Vacío hasta que Mateo deje el primero.** Ninguna referencia
se añade de memoria.

| Fecha | Referencia (la pone Mateo) | Qué aporta | A qué pregunta de §2 responde | Estado (por leer / leído / descartado, con razón) |
|---|---|---|---|---|
| | | | | |

## 4. Decisiones del proyecto actual que lo condicionan

| Decisión / regla | Cómo condiciona al eje |
|---|---|
| DEC-016 (dos ejes, `truth` y `context`) | El eje nuevo es un **tercer eje**, reportado aparte; no se mezcla con los otros dos ni los pondera. Su nombre y su enum son una DEC pendiente. |
| DEC-026 y encuadre ("no afirma intención") | La salida nunca atribuye intención; solo técnicas con span. |
| `CLAUDE.md` §1 ("ningún número con el LLM como único origen") | Traducido al texto: ninguna etiqueta sin fragmento literal que la sostenga. |
| `CLAUDE.md` §5 y adenda D4 (enums cerrados) | Sin taxonomía cerrada no hay eje. Los matices van a `notas`. |
| `CLAUDE.md` §7 (LLM prohibido para N0; encoder pequeño ONNX; LLM prohibido para aritmética) | La decisión por técnica debe ser auditable y evaluable con su propio F1; el LLM interpreta, no decide. |
| `CLAUDE.md` §8 (contenido externo = dato, nunca instrucción) | El texto analizado es contenido no confiable: no puede alterar el pipeline ni el prompt. |
| `CLAUDE.md` §10 (se traduce la plantilla, jamás el resultado) | La explicación de técnicas va por plantilla, con i18n de la plantilla. |
| DEC-025 (sin contaminación entre conjuntos) | El corpus con el que se desarrolle el eje no evalúa el eje. |
| DEC-031 y diseño §0 (un solo anotador humano, declarado) | Amenaza mayor en un eje subjetivo: la necesidad de segundo anotador (P-05) sube. |
| DEC-024 (publicadores de nivel 1) | El eje se evalúa sobre textos que citan estadísticas de nivel 1, no sobre cualquier texto. |
| DEC-035 y puertas (`CLAUDE.md` §2) | **Se construye después de cerrar la Puerta 3** (jornada 5, `CTH0926`, congelado del conjunto, arnés y DEC de cierre). Nada en paralelo. |
| `CLAUDE.md` §11 ("retórica general" no se implementa todavía) | Deja de ser un "todavía" incondicional: el eje entra, con enum cerrado, después de la Puerta 3 (DEC-036). |
| Regla nueva (DEC-036): `IDEAS.md` → `DECISIONES.md` solo con aprobación explícita de Mateo | Ninguna pregunta de §2 se cierra sin DEC. |
