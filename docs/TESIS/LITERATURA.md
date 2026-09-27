# Literatura de la tesis principal — fichas

Fichas de las fuentes leídas para la **tesis principal**. Las del futuro eje
de manipulación (L-01 a L-10) están en `docs/IDEAS.md` I-002; la numeración
L-NN es común a las dos listas. Misma plantilla y misma regla: cada ficha sale
del PDF leído, con página, y nada se rellena de memoria. Los PDF están en
`research/literatura/` con su sha256. La tarea que origina cada ficha está en
`docs/TESIS/README.md` §Tareas de la tesis principal.

---

## L-11 · Powell, Bian & Markman 2020

- **Referencia:** Powell, D., Bian, L., & Markman, E. M. (2020). When intents
  to educate can misinform: Inadvertent paltering through violations of
  communicative norms. *PLOS ONE*, 15(5), e0230360.
- **DOI/URL:** 10.1371/journal.pone.0230360 (impreso en la p. 1). PDF:
  `research/literatura/journal.pone.0230360.pdf` (sha256 `373d40ed…`), descargado de PLOS ONE
  el 2026-09-27; acceso abierto, licencia CC BY impresa en la p. 1. Datos y
  scripts en OSF, `https://osf.io/87b5y/` (p. 1; no consultado).
- **Tipo:** artículo de investigación ("Research article"), con editor
  académico; recibido el 31-07-2019, aceptado el 27-02-2020, publicado el
  29-05-2020 (p. 1). Las páginas son las del artículo, 1 a 16.
- **Cómo llega aquí:** es la ref. 265 de Ecker et al. 2022 (ms p. 28), la
  única de sus primarias con *paltering* en el título. Tarea T-01.
- **Qué estudia:** si las explicaciones de la American Diabetes Association
  (ADA) sobre "mitos" de la diabetes inducen a error por violar las máximas
  de Grice (cantidad, calidad, relevancia y manera), y si reescribirlas para
  respetarlas, sin cambiar su contenido, elimina ese efecto (pp. 1, 4–5).
- **Diseño y dataset:** experimento entre sujetos, 2 (mito frente a pregunta)
  × 3 (sin explicación, explicación de la ADA, explicación revisada)
  (pp. 5, 8). 328 participantes de Amazon Mechanical Turk residentes en
  EE. UU.; 32 excluidos por un control de atención; 296 analizados (p. 8).
  Cinco explicaciones de la ADA con violaciones pragmáticas, analizadas y
  revisadas por los autores (tabla 1, pp. 6–7). Medida: diez ítems
  verdadero/falso sobre diabetes, con escala de 4 puntos (pp. 8–9, tabla 2).
  Análisis: regresión logística jerárquica bayesiana (brms) con prior
  Normal(0,1) (p. 10). Aprobado por el comité de ética de Stanford (p. 5).
- **Resultados relevantes:**
  - Los mitos reducen el conocimiento frente a las preguntas, B = −0,49,
    IC95 [−0,97; −0,04]. Las explicaciones de la ADA lo reducen frente a no
    leer ninguna, B = −0,61 (p. 10).
  - Las explicaciones revisadas mejoran la precisión frente a las de la ADA,
    B = 0,74, IC95 [0,24; 1,22], y corrigen el efecto de los mitos (p. 10).
    No mejoran sobre la línea base de las preguntas, Bdiff = 0,181,
    IC95 [−0,308; 0,675] (p. 11).
  - En el ítem sobre el sistema inmunitario aciertan el 41 % con el material
    de la ADA y el 76 % con la explicación revisada (p. 13).
  - Los mitos con la explicación de la ADA aumentan la confianza en las
    respuestas incorrectas frente a solo las preguntas, B = 1,29,
    IC95 [0,59; 2,00] (p. 12).
- **Limitaciones que declara:** no tiene sección de limitaciones. Declara que
  las condiciones se reclutaron en dos fases, primero las de pregunta y
  después las de mito, y se presentan juntas "for simplicity" (p. 8); que
  las revisiones no educan más allá de la línea base, quizá por el nivel
  básico de los ítems (p. 11); y que sospechan que los casos tan claros de
  *paltering* inadvertido son raros (p. 13).
- **Inconsistencia interna:** dos intervalos se imprimen con los extremos
  invertidos, "CI = [-0.15, -1.08]" y "CI [1.365, .314]" (p. 10). No se
  corrigen.

### Las tres preguntas de Mateo

1. **Qué entienden por *paltering*.** "Paltering is a form of deception
   whereby true statements are used to mislead" (resumen, p. 1). "The act of
   deceiving through truthful statements is known as 'paltering'" (p. 1, con
   la ref. 1, Schauer & Zeckhauser 2009). "Palterers imply rather than assert
   falsehoods, leading listeners to draw false inferences from true
   statements" (p. 1). Su tesis es que se consigue violando las máximas de
   Grice (resumen, p. 1; pp. 2–3): "telling the truth but deftly
   manipulating other communicative principles to effectively mislead or
   deceive" (p. 3). Las técnicas son las descripciones vagas, el énfasis
   desplazado y las omisiones (p. 3, citando a Luscombe, ref. 7).
2. **Qué significa "inadvertent".** Distinguen el *paltering* genuino, "a
   form of deliberate deception", del inadvertido. Siguiendo el modelo de
   intencionalidad de Malle & Knobe (ref. 11), el inadvertido ocurre cuando
   el emisor "(a) does not desire to deceive and (b) is not aware of
   communicating in a misleading way" (pp. 1–2). En la conclusión: "These
   same kinds of violations can occur without an explicit intent to deceive
   which can result in unintentional paltering" (p. 14). "Inadvertent" es,
   por tanto, una afirmación sobre el estado mental del emisor: no desea
   engañar y no sabe que está induciendo a error.
3. **¿Exige su marco atribuir intención al emisor?**
   - **Para identificar el mecanismo y medir su efecto, no.** El mecanismo es
     la violación de normas comunicativas con enunciados verdaderos, y se
     analiza sobre el texto (tabla 1, pp. 6–7). El efecto engañoso se mide en
     los lectores (p. 10), en un caso que los autores consideran no
     intencionado. Sostienen que ocurre con intención y sin ella: "the
     neglect of these norms can be just as detrimental to communication as
     their abuse" (p. 14).
   - **Para calificar un caso, sí.** "Genuine" e "inadvertent" son las dos
     atribuciones posibles, una positiva y otra negativa. Los autores
     atribuyen a la ADA la ausencia de intención como creencia, no como
     medida: "we do not believe that the ADA was trying to be misleading" y
     "an apparently unintentional form of paltering" (p. 4); "we suspect that
     ADA had the additional goals…" (p. 13).

**Compatibilidad con la regla dura** (lectura del agente; decide Mateo). La
cita es compatible si se usa para el mecanismo: enunciados verdaderos que
inducen a error por lo que omiten, enfatizan o dejan vago, con intención o
sin ella (p. 14). Y si **no** se adopta ninguna de las dos etiquetas, ni
"genuine" ni "inadvertent": las dos afirman algo sobre el estado mental del
emisor, y DEC-026 no permite afirmarlo en ningún sentido.

- **Qué afirmación de VeritAI puede respaldar:** que la literatura tiene una
  categoría con nombre, *paltering*, para lo que induce a error diciendo la
  verdad (p. 1); que ese error se puede analizar sobre el texto sin saber qué
  quería el emisor (tabla 1, pp. 6–7; p. 14); que su efecto engañoso está
  medido de forma experimental, aunque en otro dominio (p. 10). La
  correspondencia con el objeto de VeritAI es lectura del agente, porque el
  artículo no trata estadísticas ni comparaciones: un dato verdadero con una
  comparación que omite o desplaza lo que la fuente sostiene sería, en su
  vocabulario, una violación de cantidad y relevancia.
- **Qué NO permite afirmar:** nada sobre estadística, cifras ni
  comparaciones de base o de periodo; nada sobre prensa ni sobre español (el
  material es de salud, de un sitio web, y los participantes son de MTurk en
  EE. UU.); ninguna frecuencia (los autores sospechan que los casos claros
  son raros, p. 13); que VeritAI mida lo que mide el artículo, porque VeritAI
  no mide efectos en lectores; ninguna intención del emisor, ni su ausencia.
- **Falta por leer** (citadas en el artículo; no se describe su contenido):
  Schauer & Zeckhauser 2009, capítulo "Paltering" (ref. 1, p. 1), a quienes
  atribuyen el término; Rogers et al. 2017, "Artful paltering", *Journal of
  Personality and Social Psychology* 112(3) (ref. 2); Powell et al. 2018,
  *Psychological Science* (ref. 12), el estudio previo sobre los mitos de la
  ADA; Malle & Knobe 1997 (ref. 11), el modelo de intencionalidad.
- **Estado candidato:** primaria leída para `05-marco-teorico.md` §D.
  Respaldo directo de que la categoría existe y se estudia sin atribuir
  intención. Respaldo indirecto, por analogía del agente, del objeto de
  VeritAI.
