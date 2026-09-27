> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 5. Marco teórico y estado del arte

**Propósito.** Taxonomía de divergencia (el núcleo teórico), conceptos con
definición cerrada, y la revisión de literatura que sitúa el trabajo.
**Andamiaje, no texto:** las preguntas que el estado del arte debe responder
*para este proyecto*, las categorías de trabajo previo que hay que cubrir, y
qué afirma cada sección de la tesis que necesita respaldo bibliográfico. La
redacción y las fuentes las pone Mateo. **Aquí no hay ninguna referencia y no
se inventa ninguna.**

## A. Preguntas que debe responder el estado del arte de este proyecto

Cada pregunta nace de algo que la tesis afirma o hace. Se indica de dónde
sale y qué sección la necesita.

| # | Pregunta | De dónde sale en el repo | Sirve a |
|---|---|---|---|
| Q1 | ¿Cómo se ha delimitado una "afirmación estadística verificable" (cifra + comparación) en la verificación automática de hechos, y qué queda fuera de esa delimitación? | definición operacional (`TESIS-ENCUADRE`, DEC-026); N0 como clasificación binaria (`CLAUDE.md` §7) | 2, 3, 4 |
| Q2 | ¿Cómo tratan los verificadores humanos y los sistemas automáticos el caso en que **el dato es verdadero y la comparación no se sostiene** (base, periodo, denominador, absoluto/relativo)? ¿Existe una categoría de veredicto para ello? | dos ejes `truth`/`context` (DEC-016); "no afirma que el dato sea falso" (encuadre) | 2, 5, 10 |
| Q3 | ¿Qué taxonomías de estadísticas engañosas o de falacias con cifras existen, y dónde encaja cada clase de la taxonomía del proyecto (1, 2a, 2b, 2c, 3, 4)? | `TESIS-ENCUADRE` §Taxonomía; `GLOSARIO` | 5 |
| Q4 | ¿Qué se sabe de las **revisiones de datos oficiales** (provisional → definitivo, ediciones), de su magnitud, y de su efecto sobre comparaciones publicadas? ¿Existe el concepto de "dato tal como se publicó" frente a "dato vigente"? | 2b (DEC-034); `RECUPERABILIDAD-2B`; `evidencia_al_publicar` / `evidencia_vigente` | 2, 5, 7, 10 |
| Q5 | ¿Qué evidencia hay de **errores de reproducción** de estadísticas oficiales en prensa (agencias, teletipos, redacciones regionales), y de sus mecanismos (plantillas, notas del año anterior, turnos)? | control natural (diseño §4e); E065 (frase repetida); jornada 4 (~25 piezas vigente) | 10 |
| Q6 | ¿Qué arquitecturas de verificación **separan** recuperación de evidencia, cálculo determinístico y generación de lenguaje, y con qué justificación (aritmética de los modelos de lenguaje, trazabilidad, alucinación)? | regla "ningún número con el LLM como único origen" (`CLAUDE.md` §1); plantilla numérica (DEC-009) | 6, 7 |
| Q7 | ¿Cómo se **evalúan** estos sistemas: métricas, tasa de falsos positivos como métrica crítica, intervalos con muestras pequeñas, acuerdo entre anotadores, conjuntos pequeños pero controlados? | diseño §1 (Wilson, 40 controles), §0 (kappa agente–humano); arnés | 3, 6, 9, 10 |
| Q8 | ¿Qué se sabe de la **accesibilidad de datos oficiales para agentes automáticos** (API, datasets, HTML, bloqueo anti-bot, `robots.txt`, términos de uso) y de la ética de la recolección automatizada? | DEC-018, DEC-021; recuperabilidad-por-agente (DEC-014, DEC-019); 403 del FMI e Interior (DEC-032) | 4, 6, 10 |
| Q9 | ¿Qué trabajo previo existe **en español** y sobre organismos hispanohablantes (INE, INEC, DANE, INEGI, INEI) en verificación de cifras, y qué hacen los verificadores de la región con este tipo de afirmación? | alcance (DEC-024, DEC-026); criba con verificadores (diseño §0) | 2, 4, 9 |
| Q10 | ¿Qué antecedentes hay de **preinscripción** de reglas y predicciones antes de mirar los datos en evaluación de sistemas o en ingeniería, y qué gana la tesis con ello? | `PILOT-DECISION` (regla antes del número); DEC-033; diseño §4h (P1/P2 con fecha y commit) | 6, 9 |
| Q11 | ¿Qué se sabe de la **extracción de tablas** de PDF y hojas de cálculo oficiales sin modelos de lenguaje, y de los errores de los modelos al extraer celdas? | `CLAUDE.md` §7 (pdfplumber, no LLM); conector de anexos (`mapa_anexos.py`) | 7, 8 |
| Q12 | ¿Qué se sabe del **contenido externo como vector de instrucciones** (inyección de prompt) en sistemas que leen páginas y documentos, y de las mitigaciones? | `CLAUDE.md` §8 ("todo contenido externo es DATA"); `SEGURIDAD.md` | 7 |

## B. Categorías de trabajo previo que hay que cubrir

Para cada categoría: qué debe aportar a la tesis y qué secciones la usan. El
orden es el de la argumentación, no el de importancia.

| # | Categoría | Qué debe aportar | Responde a | Secciones |
|---|---|---|---|---|
| C1 | Verificación automática de hechos: detección de afirmaciones, recuperación de evidencia, veredicto | el marco general y sus límites; dónde se sitúa un sistema que solo cubre afirmaciones con cifra y comparación | Q1, Q2 | 2, 5, 7 |
| C2 | Verificación de afirmaciones **numéricas y sobre tablas** (cifras, tasas, comparaciones contra datos estructurados) | el antecedente más cercano a los tests determinísticos; qué hacen con la base y el periodo | Q1, Q2, Q6 | 3, 5, 7 |
| C3 | Estadísticas engañosas, falacias con cifras, elección de base y de periodo, denominadores, absoluto/relativo | el vocabulario y las taxonomías con las que dialoga la del proyecto | Q3 | 5 |
| C4 | Revisiones de datos oficiales: datos provisionales y definitivos, ediciones, series "tal como se publicaron" | el fundamento de 2b y de la distinción al publicar / vigente; magnitud típica de las revisiones | Q4 | 2, 5, 7, 10 |
| C5 | Periodismo de datos y uso de estadísticas oficiales en redacciones y agencias: errores, rutinas, teletipos | la lectura del control natural y de E065 como mecanismo de redacción | Q5 | 10 |
| C6 | Modelos de lenguaje: aritmética, alucinación numérica, anclaje ("grounding") y trazabilidad; separación entre generación y cálculo | la justificación de la regla de arquitectura y de la plantilla numérica | Q6 | 6, 7 |
| C7 | Evaluación: falsos positivos como métrica crítica, intervalos de confianza para proporciones con n pequeño (Wilson, regla de tres), acuerdo entre anotadores (kappa), conjuntos de evaluación controlados | la defensa del tamaño del conjunto, de los umbrales de H3 y del acuerdo agente–humano | Q7 | 3, 6, 9, 10 |
| C8 | Datos abiertos oficiales y acceso automatizado: API, `robots.txt`, bloqueo anti-bot, términos de uso, ética y legalidad de la recolección | la defensa de DEC-018/DEC-021 y la interpretación de la cubeta E | Q8 | 4, 6, 10 |
| C9 | Verificación de hechos y estadística pública en el ámbito hispanohablante (organismos, verificadores, prensa regional) | el alcance geográfico y lingüístico; por qué la criba usa esos verificadores | Q9 | 2, 4, 9 |
| C10 | Preinscripción, reglas fijadas a priori, evaluación por puertas | la defensa metodológica de las reglas escritas antes de mirar los datos y de P1/P2 | Q10 | 6, 9 |
| C11 | Extracción de tablas de PDF y hojas de cálculo; calidad de la extracción con y sin modelos | la elección de librerías y el rechazo de un modelo para leer celdas | Q11 | 7, 8 |
| C12 | Seguridad de sistemas que leen contenido externo: inyección de prompt, SSRF, validación de entradas | la sección de seguridad y la regla "contenido externo = dato" | Q12 | 7 |

Lo que **no** es una categoría de literatura para esta tesis: detección de
texto generado por IA, deepfakes, multimodal, retórica general (fuera de
alcance, `CLAUDE.md` §11).

## C. Qué afirma cada sección de la tesis que necesita respaldo bibliográfico

Mapa consolidado. El detalle está en el campo "Qué afirma esta sección que
hoy no está respaldado" de cada ficha.

| Sección | Afirmación que hará la tesis | Hoy se sostiene en | Categoría |
|---|---|---|---|
| 2 | La verificación de hechos clásica no cubre el caso "dato verdadero, comparación insostenible" | encuadre (afirmación propia) | C1, C2, C9 |
| 2 | Un número del veredicto no puede tener como único origen un modelo de lenguaje | `CLAUDE.md` §1 (regla propia) | C6 |
| 2 | Las revisiones de datos oficiales cambian comparaciones publicadas | casos propios (E043, E053, E066; `RECUPERABILIDAD-2B`) | C4 |
| 3 | Un FPR ≤ 10 % con límite superior ≤ 15 % es una tasa razonable para H3 | diseño §1 ("propuesta") | C7 |
| 3 | Los intervalos de Wilson y la regla de tres son el método adecuado con n pequeño | `research/arnes/metricas.py` | C7 |
| 4 | Los publicadores de nivel 1 son los que publican en API o dataset estable; los demás son una limitación | piloto (84,2 % / 58,3 %) | C8, C9 |
| 4 | No evadir bloqueos es la conducta correcta de un agente recolector | DEC-018 (decisión propia) | C8 |
| 5 | Las seis clases de la taxonomía se relacionan con taxonomías existentes de estadística engañosa | encuadre (taxonomía propia, nacida del piloto) | C3 |
| 5 | `truth` y `context` son dos ejes distintos y ambos hacen falta | DEC-016 | C1, C2, C3 |
| 6 | Medir recuperabilidad-por-agente y por-humano por separado es una métrica con sentido | DEC-014, DEC-019 (propias) | C7, C8 |
| 6 | Un acuerdo agente–humano no es un acuerdo interanotador y así debe reportarse | diseño §0 | C7 |
| 6 | Preinscribir reglas y predicciones protege la evaluación | `PILOT-DECISION`, DEC-033, §4h | C10 |
| 7 | Separar cálculo, recuperación y explicación evita la aritmética plausible y falsa | `CLAUDE.md` §1 y §7 | C6 |
| 7 | Un modelo de lenguaje no debe extraer celdas de un PDF | `CLAUDE.md` §7 | C11 |
| 7 | El contenido externo es dato, nunca instrucción; SSRF, allowlist y límites son necesarios | `CLAUDE.md` §8, `SEGURIDAD.md` | C12 |
| 9 | 40 controles son el mínimo que tolera un falso positivo | tabla Wilson (diseño §1) | C7 |
| 9 | Un tope por edición evita contar la misma nota muchas veces (pseudorréplica) | diseño §1, §4c (regla propia) | C7 |
| 9 | Excluir lo ya verificado por los verificadores es un criterio de novedad válido | diseño §0 (regla dura) | C1, C9 |
| 10 | Que dos redacciones calculen tasas distintas sobre la misma nota el mismo día demuestra un mecanismo de redacción | diseño §4e (inferencia propia) | C5 |
| 10 | El INE revisa los datos provisionales de la EOH y la EOAT en la edición siguiente o en la anual | observado en los anexos; **la nota metodológica del INE no se ha leído** (`methodology_found = no` en casi todos los casos) | C4 + pasada `methodology_found` |
| 10 | 2a en 0 de 43 es un hallazgo sobre la muestra y el método | DEC-034 (redacción fijada por Mateo) | C3, C5 |
| 11 | Los mecanismos `other_observed` (agregación de subgrupos, cambio sin edición anterior) son trabajo futuro con sentido | DEC-027 | C3 |

## Material que alimenta la taxonomía (ya disponible)

| Qué | De dónde | Estado |
|---|---|---|
| Taxonomía vigente (1 ranking/valor, 2a periodo o base elegida, 2b base revisada, 2c cambio de método, 3 absoluto/relativo, 4 denominador) | `docs/TESIS-ENCUADRE.md` §Taxonomía (DEC-026); enum `Clase` en `apps/api/veritai/domain/enums.py` | disponible |
| Taxonomía original (para el contraste) | `02-1-VeritAI-TESIS.md` §Taxonomía de distorsión | disponible |
| Conceptos definidos | `docs/GLOSARIO.md` §Conceptos | disponible |
| Enums cerrados y "una etiqueta que no se puede contar no es una etiqueta" | `docs/GLOSARIO.md` §Enums cerrados; adenda D4 | disponible |
| Términos que NO se usan | `docs/GLOSARIO.md` §Términos que NO se usan | disponible |
| Dos ejes | DEC-016; `01-VERITAI-START-HERE` §Truth, §Context; `04-...-R02` §10 | disponible |
| Subtipos de 2a y 2b | DEC-029; `domain/tests/base_revisada.py` | disponible |
| **Revisión de literatura** | **no existe en el repo**; este andamiaje es lo que la sustituye hasta que Mateo la redacte | **pendiente** |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| La taxonomía del proyecto cubre las divergencias contextuales computables que aparecen en prensa | encuadre §Taxonomía (nacida de 46 casos del piloto) | relación con taxonomías previas; no se afirma exhaustividad | C3 |
| `truth` y `context` como dos ejes es una distinción necesaria y no una clase más | DEC-016 | precedente en escalas de veredicto de verificadores y en sistemas | C1, C2 |
| "Base revisada" (2b) es una categoría distinta de "base elegida" (2a) | DEC-034 | precedente en revisiones de datos y en falacias de comparación | C3, C4 |
| Una "señal de horizonte" (magnitud ≥ 2× sin cambio de signo) no debe contar como divergencia | DEC-029 | justificación externa del umbral; hoy es convención declarada | C3, C7 |
| Los términos descartados (`GLOSARIO` §Términos que NO se usan) se descartan con razón | `GLOSARIO` | contraste con el uso en la literatura | C1, C3 |

## No entra

Nada que afirme intención ("retórica general" está fuera, `CLAUDE.md` §11).
