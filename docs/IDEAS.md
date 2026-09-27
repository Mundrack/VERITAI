# Ideas — bitácora de lo que todavía no es decisión

Aquí entra **primero** todo lo que Mateo traiga de otra IA, de un paper o de
una conversación, y cualquier idea del agente que no sea una decisión.
Cada entrada lleva fecha, de dónde salió y estado.

**Regla (DEC-036): nada pasa de `IDEAS.md` a `DECISIONES.md` sin que Mateo
lo apruebe explícitamente.** El agente puede proponer, estudiar y preparar;
no decide.

Estados: `idea` (anotada, sin trabajar) · `en estudio` (se está preparando o
midiendo) · `decidida` (tiene DEC; se enlaza) · `descartada` (con la razón,
que se conserva).

| # | Fecha | Idea | De dónde salió | Estado | Enlace |
|---|---|---|---|---|---|
| I-001 | 2026-09-27 | Contraste con búsqueda web: baseline B0 medido sobre los 7 casos B | Mateo | en estudio | [abajo](#i-001--contraste-con-búsqueda-web-baseline-b0) |
| I-002 | 2026-09-27 | Literatura para el futuro eje de manipulación, pasada 1: 9 fichas, SemEval como base, matriz de tres niveles, brechas | Mateo (PDF) | en estudio; la regla de §3, decidida en DEC-037 | [abajo](#i-002--literatura-para-el-futuro-eje-de-manipulación--pasada-1) |

---

## I-001 · Contraste con búsqueda web (baseline B0)

**Fecha:** 2026-09-27 · **De dónde salió:** Mateo · **Estado:** en estudio

**Qué es.** Buscar en Google los 7 casos B (E031, E042, E043, E047, E053,
E055, E066), en español y en inglés, y anotar si alguno de los 10 primeros
resultados **llega al dato corregido del INE** (la cifra vigente, definitiva,
del periodo base). Es el baseline B0 **medido de verdad**: lo que encontraría
una persona que buscara antes de creerse la cifra publicada. Se compara con
el sistema, que llega a las dos ediciones en los 7 (recall 7/7 en tests,
arnés pendiente).

**Qué hay que fijar antes de medir** (para que sea una medición y no una
anécdota):

- **Consulta.** Qué se escribe en el buscador por caso: propuesta, el titular
  o la frase del claim tal cual (español) y su traducción literal (inglés);
  una segunda variante con "INE" + comunidad + mes + variable. Las consultas
  se escriben antes y se registran.
- **Qué cuenta como "llega".** Propuesta: el resultado muestra la cifra
  vigente del periodo base o enlaza a la nota, el anexo o INEbase donde está;
  se anota el rango (1–10) del primer resultado que llega y cuántos llegan.
  Un resultado que repite la cifra provisional no llega.
- **Quién y cómo.** A mano, sesión limpia (sin cuenta, sin historial),
  fecha y hora registradas, captura de la página de resultados por caso. Si
  lo hace el agente, respeta DEC-018 (nada de evadir ni de automatizar
  contra los términos del buscador) y se declara qué buscador usó; el
  buscador del agente no es Google.
- **Dos idiomas.** El inglés mide si el hueco es del idioma o del dato.
- **Fecha.** Los resultados cambian; B0 vale para la fecha en que se mide y
  así se reporta. Conviene medirlo antes de que la tesis se publique, no
  después.
- **Relación con las amenazas ya declaradas.** `PILOT-FINDINGS` §3.3 ("un
  buscador, una sesión, un modelo, un anotador"): B0 hereda la misma
  limitación y se declara.

**Salida esperada.** Una tabla de 7 filas × 2 idiomas: consulta, fecha,
rango del primer resultado que llega, cuántos de 10 llegan, URL del que
llega, y la lectura: en cuántos de los 7 la búsqueda deja al lector con la
cifra provisional.

**Por qué importa para la tesis.** Si B0 es bajo, el sistema aporta algo que
la búsqueda no da; si B0 es alto, la aportación es la trazabilidad y el test,
no el acceso al dato. Cualquiera de los dos resultados se escribe.

---

## I-002 · Literatura para el futuro eje de manipulación — pasada 1

**Fecha:** 2026-09-27 · **De dónde salió:** Mateo (PDF en Descargas) · **Estado:** en estudio (la regla de §3, decidida: DEC-037)

**Alcance de la pasada, fijado por Mateo:** fichas por paper, evaluación de
SemEval 2020/2023 como base metodológica, matriz de tres niveles e informe de
brechas. **Nada de esto es decisión del proyecto, no toca la Puerta 3, no abre
implementación y no modifica `docs/EJE-MANIPULACION.md`.** El diseño de
B0/B1/B2 no se hace todavía.

**Actualización tras la pasada (Mateo, 2026-09-27; DEC-037).** Mateo
aprueba la regla de §3; retira como respaldo la guía árabe de L-10; mueve
el pasaje de Ecker sobre el engaño que dice técnicamente la verdad y la
selección interesada de datos a la tesis principal; y pide rellenar la
tabla de `EJE-MANIPULACION.md` §3 con estas fichas como evidencia
candidata, lo que no convierte nada en decisión. Qué técnicas adoptar
sigue sin decidirse (§2).

**Regla de lectura.** Cada ficha sale del PDF leído, con página. Nada se
rellena de memoria. Los PDF están versionados con su sha256 en
`research/literatura/` (`README.md`, `SHA256SUMS`). Convención de páginas: la
página impresa de la revista o de las actas; entre paréntesis, la del PDF
cuando difieren. En Ecker (manuscrito aceptado) se cita la página del
manuscrito ("ms"). Los DOI de ACL no vienen impresos en los PDF: se
comprobaron en la página de la Antología ACL de cada artículo el 2026-09-27.

**Qué había en la carpeta y qué no:**

| Pedido por Mateo | En la carpeta | Resultado |
|---|---|---|
| SemEval 2020 Task 11 | `2020.semeval-1.186.pdf` | ficha L-01 |
| SemEval 2023 Task 3 | `2023.semeval-1.317.pdf` | ficha L-02 |
| (no pedido) | `2023.semeval-1.0.pdf` | front matter de las actas, no es un artículo: sin ficha; solo confirma que L-02 empieza en la p. 2343 |
| Ecker | `Ecker_v4_TSshorten_UE_clean.pdf` (manuscrito aceptado) y `ecker.2022.nrp_preprint.pdf` | una ficha, L-03, sobre el manuscrito aceptado; el preprint coincide en los seis pasajes comprobados |
| Hauch | ninguno | **no disponible**; sin ficha (L-04 queda reservado) |
| Witte & Allen | `HEB2000WitteFearMeta.pdf` | ficha L-05 |
| (no pedido) | `nihms715564.pdf` | **es Tannenbaum et al. 2015, no Hauch**; ficha L-06 porque está en la carpeta y se leyó entero |
| Brady | `pnas.201618923.pdf` | ficha L-07 |
| Los tres de 2024 | `2024.eacl-long.87.pdf`, `2024.findings-emnlp.850.pdf`, `2024.lrec-main.244.pdf` | fichas L-08, L-09, L-10 |

### 1. Fichas

#### L-01 · SemEval-2020 Task 11

- **Referencia:** Da San Martino, G., Barrón-Cedeño, A., Wachsmuth, H.,
  Petrov, R., & Nakov, P. (2020). SemEval-2020 Task 11: Detection of
  Propaganda Techniques in News Articles. En *Proceedings of the Fourteenth
  Workshop on Semantic Evaluation* (pp. 1377–1414). International Committee
  for Computational Linguistics.
- **DOI/URL:** 10.18653/v1/2020.semeval-1.186 (Antología ACL; el PDF no lo
  imprime).
- **Tipo:** artículo de descripción de tarea compartida (SemEval), revisado
  (agradece a revisores anónimos, p. 1394).
- **Qué estudia:** dos subtareas: SI, identificar los fragmentos (spans) con
  al menos una técnica, "a binary sequence tagging task"; TC, dado un span,
  clasificar la técnica entre 14, "a multi-class classification problem"
  (p. 1377).
- **Diseño y dataset:** PTC-SemEval20, 536 artículos en inglés de mediados de
  2017 a inicios de 2019, de 13 medios "de propaganda" y 36 "no propaganda"
  según Media Bias/Fact Check; 8.981 fragmentos (train 371 art. / 6.128; dev
  75 / 1.063; test 90 / 1.790) (pp. 1380–1381). Dos anotadores
  independientes y consolidación con un consolidador; seis anotadores
  profesionales; test con una consolidación adicional por al menos tres
  expertos (pp. 1380–1381). Taxonomía: de 18 técnicas a 14, fusionando las
  raras y eliminando "Obfuscation, Intentional vagueness, Confusion"
  (p. 1380). SI se evalúa con F1 que da crédito parcial a nivel de carácter
  (pp. 1382–1383); TC con micro-F1; el 1,8 % de los spans idénticos llevan
  varias técnicas y se tratan como tarea de una etiqueta (p. 1383).
- **Resultados relevantes:**
  - Criterio de inclusión de técnicas: "We only include techniques that can be
    found in journalistic articles and can be judged intrinsically, without
    the need to retrieve supporting information from external resources"; se
    excluye *card stacking* porque exigiría comparar varias fuentes (p. 1378).
    El diagrama que guía a los anotadores termina en "stop judging this
    fragment" si hace falta información externa para juzgar (p. 1407, fig. 8).
  - Instrucción a los anotadores: "Your emotions have nothing to do with the
    articles, as you are requested to spot propagandistic techniques, not
    their message" (p. 1406, fig. 7).
  - Resultados con el evaluador corregido (anexo B): SI, mejor F1 = 51,74
    (P 55,76; R 48,27), baseline aleatorio 0,32 (p. 1404, tabla 8); TC, mejor
    micro-F1 = 63,74, baseline por longitud 25,20 (p. 1405, tabla 9).
  - *Loaded Language* es la técnica más frecuente, casi el doble que *Name
    Calling* (p. 1381); *Doubt* es la clase más difícil de reconocer
    (p. 1389).
  - La definición de propaganda que usan incluye intención: "deliberately
    designed to influence opinions or actions" (Institute for Propaganda
    Analysis, 1938) y, según Bolsover y Howard, "(ii) doing so on purpose"
    (p. 1378).
  - Agreement γ entre cada anotador y el gold: 0,6 de media (p. 1381).
- **Limitaciones que declara:** error en el script de evaluación descubierto
  tras la competición (anexo B, p. 1404); posible sobreajuste de sistemas al
  desarrollo (pp. 1387–1388); el conjunto de técnicas y sus definiciones
  "differ between different scholars" (p. 1378); trabajo futuro: más técnicas
  y otros idiomas (p. 1394).
- **Qué afirmación de VeritAI puede respaldar:** que un eje de técnicas se
  puede definir como spans con etiqueta de un conjunto cerrado y evaluar con
  F1 de spans; que la detección de técnicas se hace **sobre el propio texto,
  sin fuentes externas**, lo que la separa por construcción de `truth` y
  `context`; que la tarea es difícil incluso en inglés (≈ 52 % de F1 en spans
  con el mejor sistema); precedente de reducir la taxonomía por escasez de
  datos (18 → 14).
- **Qué NO permite afirmar:** nada sobre español ni sobre prensa estadística;
  nada sobre el efecto en el lector; su noción de propaganda incluye
  intención, así que no respalda ninguna salida que la atribuya; no trata si
  la exageración de una **cifra** puede juzgarse sin la fuente.
- **Ambigüedad registrada:** el pie de la tabla 9 (p. 1405) dice que las
  columnas siguen el orden de la sección 2, pero el texto (p. 1388) dice que
  *Loaded Language* y *Name Calling* rinden razonablemente bien, lo que solo
  cuadra con un orden alfabético de columnas. No se cita ninguna cifra por
  técnica de esa tabla (NEEDS_REVIEW).
- **Estado candidato:** base metodológica candidata (formato de anotación,
  métricas, criterio intrínseco). Taxonomía no adoptable tal cual.

#### L-02 · SemEval-2023 Task 3

- **Referencia:** Piskorski, J., Stefanovitch, N., Da San Martino, G., &
  Nakov, P. (2023). SemEval-2023 Task 3: Detecting the Category, the Framing,
  and the Persuasion Techniques in Online News in a Multi-lingual Setup. En
  *Proceedings of the 17th International Workshop on Semantic Evaluation
  (SemEval-2023)* (pp. 2343–2361). Association for Computational Linguistics.
- **DOI/URL:** 10.18653/v1/2023.semeval-1.317 (Antología ACL). El PDF no
  imprime páginas; el inicio en la p. 2343 consta en el índice de las actas
  (`2023.semeval-1.0.pdf`).
- **Tipo:** artículo de descripción de tarea compartida, con sección de
  limitaciones.
- **Qué estudia:** tres subtareas sobre noticias en nueve idiomas: género
  (opinión, información, sátira), *framing* (14 marcos) y técnicas de
  persuasión (23 técnicas en seis categorías); español, griego y georgiano
  solo en el test, "surprise languages" (pp. 2343–2344, 2347).
- **Diseño y dataset:** artículos de 2020 a mediados de 2022, de medios
  generalistas y "alternativos" (identificados con Media Bias/Fact Check y
  NewsGuard) (p. 2346). Unos 40 anotadores (analistas de medios,
  especialistas en desinformación, expertos en PLN), nativos o casi nativos;
  al menos dos por documento y un curador que consolida (pp. 2346–2347).
  2.049 documentos (p. 2347). Las técnicas se anotan a nivel de span, pero la
  subtarea 3 se evalúa como clasificación multietiqueta **por párrafo**, con
  micro-F1 oficial (pp. 2346–2347). **Español:** 30 documentos, 546 spans,
  330 párrafos no vacíos (tabla 1, p. 2346); 14 de opinión, 9 informativos,
  7 sátira (tabla 2, p. 2346); sin datos de entrenamiento.
- **Resultados relevantes:**
  - Acuerdo entre anotadores, Krippendorff α = 0,342 **antes** de la
    consolidación, frente a un umbral recomendado de 0,667; 0,415 y 0,250 en
    los grupos de mejores y peores anotadores; 0,588 en el italiano, con dos
    curadores (p. 2347).
  - Subtarea 3: mejor micro-F1 en inglés 0,376 (baseline 0,195) (tabla 9,
    p. 2351); en español 0,381 (baseline 0,248) (tabla 10, p. 2351).
  - Definiciones (fig. 1, p. 2344), entre ellas: *Loaded Language* "use of
    specific words and phrases with strong emotional implications (either
    positive or negative) to influence and convince the audience that an
    argument is valid"; *Exaggeration or Minimisation* "either representing
    something in an excessive manner or making something seem less important
    or smaller than it really is"; *Obfuscation* "words that are deliberately
    not clear"; *Repetition* "with the hope that the repetition will lead to
    persuade the audience"; la categoría *Manipulative wording* usa lenguaje
    no neutral "in order to impact the reader emotionally".
  - En español, las técnicas más anotadas son *Loaded Language* (134),
    *Questioning the Reputation* (66), *Name Calling* (42), *Appeal to
    Fear-Prejudice* (41), *Doubt* (37) y *Exaggeration-Minimisation* (35) de
    546 (tabla 17, p. 2358).
- **Limitaciones que declara (§8, pp. 2351–2352):** el conjunto "should not be
  seen as representative of the media in any country, nor should it be seen
  as perfectly balanced"; la anotación implica subjetividad, mitigada con una
  guía de 60 páginas, control de calidad y exclusión de anotadores de bajo
  rendimiento, pero "some degree of intrinsic subjectivity will inevitably be
  present in the dataset and will eventually be learned by models". Trabajo
  futuro: evaluar a nivel de frase y de span (p. 2351).
- **Qué afirmación de VeritAI puede respaldar:** precedente de enum cerrado
  en dos niveles (6 categorías, 23 técnicas); que existe un conjunto
  anotado con español, aunque solo de test y pequeño; que el acuerdo previo a
  consolidar es bajo, lo que refuerza la pregunta del segundo anotador en
  `EJE-MANIPULACION.md` §2; que evaluar por párrafo es una opción declarada.
- **Qué NO permite afirmar:** rendimiento en español con entrenamiento (no lo
  hubo); nada sobre prensa estadística (los temas son COVID-19, aborto,
  migración, la guerra ruso-ucraniana y elecciones, p. 2351); usar sus
  definiciones sin arrastrar intención (varias la incluyen); comparación
  directa con L-01 (cambian taxonomía y unidad de evaluación).
- **Inconsistencia interna:** el texto (p. 2356) atribuye 18,5 % a *Loaded
  Language* y 23,7 % a *Name Calling*; recalculado sobre la tabla 17 es al
  revés (11.731 / 49.444 = 23,7 %; 9.131 / 49.444 = 18,5 %). Las seis clases
  más frecuentes suman el 71,8 %, como dice el texto.
- **Estado candidato:** taxonomía de referencia para mapear, no para adoptar;
  única fuente leída con datos en español.

#### L-03 · Ecker et al. 2022

- **Referencia:** Ecker, U. K. H., Lewandowsky, S., Cook, J., Schmid, P.,
  Fazio, L. K., Brashier, N., Kendeou, P., Vraga, E. K., & Amazeen, M. A.
  (2022). The psychological drivers of misinformation belief and its
  resistance to correction. *Nature Reviews Psychology*, 1, 13–29.
- **DOI/URL:** 10.1038/s44159-021-00006-y (impreso en la portada del
  manuscrito aceptado).
- **Tipo:** revisión narrativa (*Review*); se cita el manuscrito aceptado del
  repositorio de Bristol. No declara protocolo de búsqueda.
- **Qué estudia:** factores cognitivos, sociales y afectivos que llevan a
  creer desinformación, el efecto de influencia continuada tras la
  corrección, y las intervenciones previas (*prebunking*) y posteriores
  (*debunking*) (ms p. 3).
- **Diseño y dataset:** revisión de literatura; sin datos propios.
- **Resultados relevantes:**
  - Definiciones: *misinformation* es "any information that turns out to be
    false"; *disinformation* la que se difunde "with intention to harm or
    deceive"; no distinguen tajantemente porque "More research is needed …
    to establish the extent to which people infer intentionality" (ms
    pp. 5–6).
  - Repetición: "simply repeating a claim makes it more believable than
    presenting it only once"; "repetition increases belief in both
    misinformation and facts"; persiste meses y con independencia de la
    capacidad cognitiva (ms pp. 6–7).
  - Fuente: "messages are more persuasive and seem more true when they come
    from sources perceived to be credible" (ms p. 8).
  - Emoción: los contenidos engañosos virales "often contains appeals to
    emotion, which can increase persuasion"; los mensajes de miedo
    "can successfully change attitudes, intentions, and behaviours under
    certain conditions if recipients feel they can act effectively to avoid
    the harm" (cita a Tannenbaum et al. 2015, ref. 70); "People seem to
    understand the association between emotion and persuasion and naturally
    shift towards more emotional language when attempting to convince others"
    (ref. 72, Rocklage et al. 2018) (ms p. 9).
  - Técnicas: la inoculación enseña técnicas engañosas como "selective use
    ('cherry-picking') of data" y los falsos expertos (ms p. 18). Un
    preprint no revisado sugiere que fijarse en pistas léxicas, simplicidad y
    "blatant use of emotion" ayuda a identificar noticias falsas (ref. 169;
    los propios autores lo marcan como no revisado, ms p. 19).
  - Cuadro 1: añadir una palabra moral-emocional a tuits políticos aumenta
    los retuits un 20 % (cita a Brady et al. 2017, ref. 277) (ms p. 32).
- **Limitaciones que declara (ms pp. 27–29):** dependencia de estudios
  pequeños de laboratorio o de pocas plataformas, con participantes no
  representativos "(and primarily U.S.-based)"; medidas de un ítem; "most
  existing work has focused on explicit misinformation and text-based
  materials", y lo más sutil, como el *paltering* "(misleading while
  technically saying the truth)", "not well understood"; falta investigación
  causal y de largo plazo; el papel de la emoción está poco comprendido.
- **Qué afirmación de VeritAI puede respaldar:** que la intención es una
  categoría distinta (desinformación frente a desinformación intencionada) y
  poco estudiada desde el lado del lector, lo que respalda mantenerla fuera
  de la salida; el mecanismo de la repetición; que la emoción puede aumentar
  la persuasión (respaldo de revisión, secundario). **Movido fuera de este
  eje (Mateo, 2026-09-27):** el pasaje sobre el engaño que dice técnicamente
  la verdad (ms p. 28) y la selección interesada de datos (ms p. 18) no es
  del eje de manipulación sino de la tesis principal. Está en
  `docs/TESIS/05-marco-teorico.md` §D como respaldo del objeto de estudio.
- **Qué NO permite afirmar:** tamaños de efecto (es narrativa); efectos en
  prensa en español; que un texto concreto cause creencia; usar el preprint
  de la ref. 169 como evidencia.
- **Estado candidato:** marco psicológico de referencia; fuente secundaria.
  Para cada mecanismo que se use hay que leer la primaria que cita.

#### L-04 · Hauch — no disponible

No hay PDF en la carpeta. Sin ficha. No se escribe nada sobre su contenido.

#### L-05 · Witte & Allen 2000

- **Referencia:** Witte, K., & Allen, M. (2000). A meta-analysis of fear
  appeals: Implications for effective public health campaigns. *Health
  Education & Behavior*, 27(5), 591–615.
- **DOI/URL:** 10.1177/109019810002700506 (impreso).
- **Tipo:** metaanálisis.
- **Qué estudia:** el efecto de las apelaciones al miedo ("persuasive
  messages that arouse fear") sobre percepciones, actitudes, intenciones,
  conductas y respuestas defensivas, y qué modelo teórico ajusta mejor
  (pp. 591–595).
- **Diseño y dataset:** 98 estudios experimentales o cuasiexperimentales con
  al menos dos niveles de miedo; 93 para efectos principales, 23 para
  interacciones, 13 para respuestas de control del miedo; se excluyen
  encuestas transversales (p. 596); efectos corregidos por artefactos
  (p. 597).
- **Resultados relevantes:** la manipulación produce miedo r = .297 (k = 51),
  severidad percibida .439 y susceptibilidad .301 (tabla 1, p. 598); sobre
  actitudes, intenciones y conductas, r = .147, .126 y .158 para el miedo
  (tabla 2, p. 599), "a relatively weak but reliable effect" (p. 602); forma
  lineal positiva, sin curvas (p. 598); las respuestas defensivas crecen con
  la fuerza del miedo (r = .195, k = 13) y con mensajes de eficacia débiles
  (r = −.105) (p. 601). Recomendación: "Strong fear appeals work only when
  accompanied by equally strong efficacy messages" (p. 606), con riesgo de
  "backfiring" sin eficacia (pp. 606–607).
- **Limitaciones que declara:** heterogeneidad significativa en casi todos los
  resultados (p. 602); poca potencia para las interacciones (p. 604); "Most of
  our fear appeal results come from contrived, artificial settings", con
  exposición forzada (p. 605).
- **Qué afirmación de VeritAI puede respaldar:** que "apelación al miedo"
  tiene un mecanismo con literatura experimental sustantiva, con efectos
  pequeños y heterogéneos.
- **Qué NO permite afirmar:** nada sobre noticias ni lectura natural (lo
  declaran); que un texto concreto asuste o persuada; intención; nada en
  español.
- **Estado candidato:** respaldo de mecanismo para la fila B de la matriz
  (dominio salud). En tensión con L-06 (§5).

#### L-06 · Tannenbaum et al. 2015 (no estaba en la lista; está en la carpeta)

- **Referencia:** Tannenbaum, M. B., Hepler, J., Zimmerman, R. S., Saul, L.,
  Jacobs, S., Wilson, K., & Albarracín, D. (2015). Appealing to fear: A
  meta-analysis of fear appeal effectiveness and theories. *Psychological
  Bulletin*, 141(6), 1178–1204. Se cita el manuscrito de autor (PMC); las
  páginas son las del manuscrito.
- **DOI/URL:** 10.1037/a0039729 (impreso).
- **Tipo:** metaanálisis.
- **Qué estudia:** la eficacia de las apelaciones al miedo sobre actitudes,
  intenciones y conductas, y 16 hipótesis teóricas sobre mensaje, conducta
  recomendada y audiencia (pp. 1–8).
- **Diseño y dataset:** 127 artículos (9 % no publicados), 248 muestras
  independientes, N = 27.372; solo diseños experimentales con grupo de
  comparación; búsqueda hasta febrero de 2015 (pp. 1, 8–10); acuerdo de
  codificación κ = .93 en el 20 % (p. 11); efectos aleatorios (p. 15).
- **Resultados relevantes:**
  - Efecto medio d = 0,29 [0,22; 0,35], heterogeneidad I² = 85,11
    (pp. 15–16); sin sesgo de recuperación (Begg, r = −.02) (p. 15).
  - **Miedo representado frente a miedo experimentado:** "depicted fear …
    reflects a property of the message's content, rather than the subjective
    state of fear that message recipients experience"; solo 71 de 248
    estudios midieron el miedo (p. 3, nota 2).
  - Miedo alto frente a moderado: d = −0,05 [−0,34; 0,24], con solo 21
    muestras (p. 17).
  - Con mensaje de eficacia son más eficaces, pero "fear appeals are effective
    with or without efficacy statements"; se descarta la hipótesis fuerte de
    que sin eficacia produzcan efectos negativos (p. 17); "no identified
    circumstances under which they backfire" (pp. 2, 20).
- **Limitaciones que declara (pp. 20–22):** mide apelaciones al miedo, no
  miedo; el 71 % de las muestras no mide miedo subjetivo; solo experimentos,
  de modo que la generalización a campañas reales está por probar; los
  análisis de moderadores son correlacionales.
- **Qué afirmación de VeritAI puede respaldar:** la separación entre una
  **propiedad del texto** y un **estado del lector**, que es exactamente la
  frontera entre el nivel 1 y el nivel 2 de la matriz (§4).
- **Qué NO permite afirmar:** que el lector de un texto concreto sienta miedo
  (lo excluye su propia distinción); nada sobre noticias ni español;
  intención.
- **Estado candidato:** respaldo fuerte para distinguir texto y lector;
  mecanismo del miedo en dominio salud. En tensión con L-05 (§5).

#### L-07 · Brady et al. 2017

- **Referencia:** Brady, W. J., Wills, J. A., Jost, J. T., Tucker, J. A., &
  Van Bavel, J. J. (2017). Emotion shapes the diffusion of moralized content
  in social networks. *Proceedings of the National Academy of Sciences*,
  114(28), 7313–7318.
- **DOI/URL:** 10.1073/pnas.1618923114 (impreso).
- **Tipo:** estudio empírico observacional.
- **Qué estudia:** si el lenguaje moral-emocional predice la difusión
  (retuits) de mensajes sobre temas políticos polarizantes (p. 7313).
- **Diseño y dataset:** 563.312 tuits sobre control de armas (102.328),
  matrimonio igualitario (47.373) y cambio climático (413.611); palabras
  morales, emocionales y moral-emocionales contadas con diccionarios
  validados y un piloto de validez discriminante; regresión binomial negativa
  con covariables (pp. 7314, 7317–7318).
- **Resultados relevantes:** IRR de las palabras moral-emocionales 1,19; 1,17
  y 1,24 por tema, "a 20% increase in retweet rate per moral-emotional word
  added" de media (pp. 7314–7315); la valencia depende del tema y la tristeza
  se asocia a menos difusión (IRR medio 0,73) (p. 7315); más difusión dentro
  del grupo ideológico que fuera (IRR 1,20 y 1,34; no significativo en
  matrimonio) (p. 7316). Los autores especulan con la intención de los
  emisores: "It seems likely that politicians … express moral emotions … in
  an effort to increase message exposure" (p. 7316).
- **Limitaciones que declara (p. 7317):** dificultad para medir constructos
  psicológicos en datos de redes; variabilidad del efecto en matrimonio
  igualitario; "Future work should seek to corroborate our conclusions with
  more carefully controlled laboratory experiments. In particular, it is
  important to test the causal influence of exposure to moral-emotional
  language on attitudes and behavior."
- **Qué afirmación de VeritAI puede respaldar:** que un rasgo léxico contable
  (palabras moral-emocionales de un diccionario validado) se asocia con la
  difusión en un entorno natural; que la carga emocional se puede
  operacionalizar con lexicones auditables.
- **Qué NO permite afirmar:** efectos sobre creencias o actitudes (los autores
  lo dejan como pregunta causal abierta); nada sobre prensa ni español;
  intención (la especulación de p. 7316 es justo lo que VeritAI no puede
  emitir); que difusión implique engaño.
- **Estado candidato:** respaldo parcial (difusión, no persuasión) para la
  fila A de la matriz.

#### L-08 · Chernyavskiy, Ilvovsky & Nakov 2024

- **Referencia:** Chernyavskiy, A., Ilvovsky, D., & Nakov, P. (2024).
  Unleashing the Power of Discourse-Enhanced Transformers for Propaganda
  Detection. En *Proceedings of the 18th Conference of the European Chapter of
  the Association for Computational Linguistics (Volume 1: Long Papers)*
  (pp. 1452–1462). Association for Computational Linguistics.
- **DOI/URL:** 10.18653/v1/2024.eacl-long.87 (Antología ACL).
- **Tipo:** artículo largo de conferencia, con sección de limitaciones.
- **Qué estudia:** si añadir rasgos de estructura del discurso (Rhetorical
  Structure Theory) a un transformer mejora la detección de técnicas, a
  nivel de párrafo y de token (p. 1452).
- **Diseño y dataset:** datos de la subtarea 3 de L-02 en inglés y ruso;
  DeBERTa-v2 base e XLM-RoBERTa base; parsers RST públicos para esos dos
  idiomas; "The only preprocessing was to remove all non-ascii characters from
  the articles" (pp. 1454, 1456).
- **Resultados relevantes:** en inglés, párrafo, micro-F1 de 0,3287 a 0,3751
  con relaciones de discurso (tabla 1, p. 1456); en ruso, de 0,2411 a 0,3120
  (tabla 3, p. 1457); en las clases raras la eficacia "still remains
  negligible or close to zero" (p. 1457); en 9 de 19 clases la intersección
  entre span y unidad de discurso supera el 80 % (p. 1458); correlaciones
  textuales: *Appeal to Authority* con Attribution, *False Dilemma* con
  Condition, *Exaggeration-Minimisation* "primarily associated with the
  Comparison relation", *Appeal to Fear* con Condition (p. 1459).
- **Limitaciones que declara (p. 1460):** necesita datos anotados o un parser
  RST; depende de una arquitectura *encoder*; posibles errores de los parsers
  (p. 1456).
- **Qué afirmación de VeritAI puede respaldar:** que las técnicas tienen
  correlatos estructurales medibles, lo que apoya una detección auditable y
  no solo léxica; indicio, relevante para prensa estadística, de que la
  exageración o minimización se asocia a relaciones de comparación.
- **Qué NO permite afirmar:** nada para español (no hay parser español en el
  estudio y el preprocesado elimina lo no-ASCII); ningún mecanismo
  psicológico (son correlaciones textuales); detección de clases raras.
- **Discrepancia con L-02:** habla de "a set of 19 labels" (p. 1456; su tabla 6
  lista 19) frente a las 23 técnicas de L-02, que da recuentos en inglés
  para las 23 (tabla 17). Registrada, no resuelta.
- **Estado candidato:** indicio técnico; ningún respaldo psicológico.

#### L-09 · Hasanain, Ahmad & Alam 2024 (Findings EMNLP)

- **Referencia:** Hasanain, M., Ahmad, F., & Alam, F. (2024). Large Language
  Models for Propaganda Span Annotation. En *Findings of the Association for
  Computational Linguistics: EMNLP 2024* (pp. 14522–14532). Association for
  Computational Linguistics.
- **DOI/URL:** 10.18653/v1/2024.findings-emnlp.850 (Antología ACL).
- **Tipo:** artículo de conferencia (Findings), con limitaciones.
- **Qué estudia:** si GPT-4 puede anotar spans de técnicas en tres papeles
  (anotador, selector entre etiquetas dadas, consolidador de anotaciones
  humanas) y si sus etiquetas sirven para entrenar modelos (pp. 14522–14523).
- **Diseño y dataset:** ArPro, en árabe: 8.000 párrafos (63 % con algún span)
  de 2,8K artículos de más de 300 medios; 23 técnicas de la taxonomía de
  L-02; tres anotadores y dos consolidadores; γ = 0,546 (p. 14524); GPT-4
  (versión 0314, temperatura 0, *zero-shot*) y AraBERT ajustado (p. 14526).
- **Resultados relevantes:** micro-F1 de GPT-4 como anotador 0,050, selector
  0,137, consolidador 0,671 (tabla 3, p. 14527); GPT-4 "frequently generated
  indices not matching the corresponding spans" y corregirlos duplica el F1
  de los dos primeros papeles, a 0,117 y 0,297 (pp. 14527–14528, tabla 4);
  como consolidador mejora un 38 % el acuerdo con los consolidadores
  respecto de los anotadores iniciales (p. 14528); un modelo especializado
  entrenado con las etiquetas gold llega a 0,387 frente a 0,117 de GPT-4
  directo (tabla 6, p. 14529).
- **Limitaciones que declara (p. 14530):** solo árabe; solo un LLM cerrado;
  los modelos abiertos probados "are either unable to understand the task or
  showed more inferior performance".
- **Qué afirmación de VeritAI puede respaldar:** que un LLM no debe decidir
  los spans por sí solo (F1 0,05 sin ayuda e índices que no corresponden al
  texto), lo que es coherente con `CLAUDE.md` §7 y con exigir que cada span
  se compruebe por código contra el texto; que un modelo pequeño ajustado
  rinde más.
- **Qué NO permite afirmar:** nada en español; usar GPT-4 como dependencia
  (API de pago, prohibida como obligatoria en `CLAUDE.md` §7); generalizar a
  otros LLM; el papel de consolidador presupone anotaciones humanas previas,
  así que no sustituye anotadores.
- **Estado candidato:** respaldo parcial para "el LLM no decide" y "el span se
  verifica por código".

#### L-10 · Hasanain, Ahmed & Alam 2024 (LREC-COLING)

- **Referencia:** Hasanain, M., Ahmed, F., & Alam, F. (2024). Can GPT-4
  Identify Propaganda? Annotation and Detection of Propaganda Spans in News
  Articles. En *Proceedings of the 2024 Joint International Conference on
  Computational Linguistics, Language Resources and Evaluation (LREC-COLING
  2024)* (pp. 2724–2744). ELRA and ICCL.
- **DOI/URL:** la página de la Antología ACL (2024.lrec-main.244) no muestra
  DOI (consultada el 2026-09-27). El PDF imprime "Fatema Ahmed" y la
  Antología "Fatema Ahmad" (NEEDS_REVIEW).
- **Tipo:** artículo de conferencia (recurso y evaluación).
- **Qué estudia:** la construcción de ArPro y el rendimiento de GPT-4 frente a
  modelos ajustados en cuatro granularidades: binaria, categorías gruesas,
  multietiqueta y span (pp. 2724, 2728–2729).
- **Diseño y dataset:** 8.000 párrafos, 2.810 artículos, 300 dominios; 23
  técnicas en seis categorías; guía en árabe; siete anotadores y equipos de
  consolidación (pp. 2725–2726).
- **Resultados relevantes:**
  - Acuerdo (tabla 1, p. 2727): α multietiqueta 0,375 de media en la tabla
    (el texto dice 0,335), binario 0,622, γ de span 0,546; en la fase inicial,
    α 0,243 y 0,296.
  - *Loaded Language* es la mitad de los spans (10.388 de 20.487);
    *Exaggeration-Minimisation*, 1.290 (tabla 4, p. 2728). Usan propaganda y
    persuasión "interchangeably" (p. 2728).
  - Binario: AraBERT ajustado 0,767 de micro-F1 frente a GPT-4 *zero-shot*
    0,526, con azar en 0,510 (tabla 8, p. 2730). Spans, GPT-4 *zero-shot*,
    micro-F1: árabe 0,117, inglés 0,111, francés 0,138, alemán 0,057,
    italiano 0,115, polaco 0,071, ruso 0,073 (tabla 9, p. 2730). Español no
    evaluado.
  - Anexo D (p. 2744): guía de anotación en árabe. **No se usa como
    respaldo** (Mateo, 2026-09-27; DEC-037): leerla depende de una
    traducción propia sin revisar, y una cita así no entra en la tesis. Si
    alguien la verifica, se añade. Aquí no se reproduce su contenido.
- **Limitaciones que declara:** "annotations are subjective, inevitably
  introducing biases into our dataset" (p. 2732); la distribución sesgada de
  técnicas "requires further studies to understand whether such techniques
  are inherently scarcely used in news reporting" (p. 2725).
- **Qué afirmación de VeritAI puede respaldar:** que el acuerdo de la fase 1,
  entre tres anotadores, es bajo (α 0,243 multietiqueta y 0,296 binario) y
  que los autores lo leen como prueba de que hace falta la segunda fase, con
  consolidadores expertos (p. 2727); que un LLM *zero-shot* no localiza
  spans de forma fiable en siete idiomas (p. 2730).
- **Qué NO permite afirmar:** nada en español ni en prensa estadística;
  prevalencia de técnicas en las noticias (lo dejan como pregunta).
- **Estado candidato:** respaldo para "el LLM no decide" y para consolidar
  la anotación; el recurso árabe no es reutilizable aquí. La independencia
  de ejes se apoya solo en L-01.

### 2. SemEval 2020 y 2023 como taxonomía y metodología base

| Criterio | 2020 (L-01) | 2023 (L-02) | Lectura para prensa estadística en español |
|---|---|---|---|
| **Identificación de spans** | tarea propia (SI), F1 con crédito parcial por carácter; mejor 51,74 (p. 1404) | anotado por span pero evaluado por párrafo; la evaluación por span queda como trabajo futuro (pp. 2346–2347, 2351) | el formato span + etiqueta encaja con `raw_text_span` de `EJE-MANIPULACION.md` §1; las cifras muestran que la localización exacta es lo más difícil |
| **Multietiqueta** | el 1,8 % de spans idénticos con varias técnicas se trata como una etiqueta (p. 1383) | multietiqueta por párrafo, micro-F1 oficial (p. 2347) | la coaparición de técnicas es frecuente en árabe (L-10, tabla 5, p. 2728) y los spans pueden solaparse (L-10, fig. 1, p. 2724); la unidad de evaluación hay que decidirla |
| **Taxonomía cerrada** | 14 técnicas, reducidas desde 18 por escasez (p. 1380) | 23 técnicas en 6 categorías (p. 2344) | ambas son enums cerrados; varias definiciones de 2023 incluyen intención (§3) |
| **Resultados en español** | ninguno | solo test: 30 documentos, 546 spans; mejor micro-F1 0,381 sin datos de entrenamiento en español (pp. 2346, 2351) | la evidencia en español es mínima y de otro dominio (política, COVID, guerra) |
| **Acuerdo entre anotadores** | γ ≈ 0,6 anotador–gold (p. 1381) | α = 0,342 antes de consolidar (p. 2347) | la subjetividad es la amenaza principal; mayor que en el eje numérico |
| **Criterio intrínseco** | explícito: sin fuentes externas (p. 1378; fig. 8, p. 1407) | no lo repite en el overview | separa el eje de `truth` y `context`, que sí usan fuente; respaldo solo en SemEval 2020 |

**Qué aportaría cada opción** (análisis, no decisión):

- **Adoptar las 23.** Aporta comparabilidad directa con el único conjunto
  multilingüe que incluye español y con los sistemas publicados, y una guía de
  60 páginas (L-02, p. 2351; no leída). Cuesta: muchas técnicas son de debate
  político (*Whataboutism*, *Straw Man*, *Red Herring*, *Guilt by
  Association*, *Appeal to Hypocrisy*, *Flag Waving*) y su pertinencia en
  prensa estadística no está respaldada por nada de lo leído; las clases
  raras se detectan con eficacia "close to zero" (L-08, p. 1457); varias
  definiciones incluyen intención; y el acuerdo previo a consolidar es bajo.
- **Adaptar.** Conservar el formato (span + etiqueta de un enum cerrado), las
  métricas y el criterio intrínseco, pero reescribir las definiciones en
  términos observables, sin intención, con ejemplos de prensa estadística en
  español. Aporta coherencia con la regla dura y con `CLAUDE.md` §5. Cuesta
  comparabilidad: los resultados ya no se miden contra SemEval, y obliga a un
  manual propio con acuerdo medido.
- **Reducir.** Quedarse con un subconjunto. Precedente: el propio 2020 redujo
  de 18 a 14 por escasez (p. 1380). Lo leído solo muestra qué técnicas son
  **frecuentes** en noticias de otros dominios: *Loaded Language* y *Name
  Calling* dominan en 2020, 2023 y ArPro; *Exaggeration-Minimisation*,
  *Doubt* y *Appeal to Fear* aparecen en el grupo siguiente. Qué técnicas son
  pertinentes en prensa estadística **no está respaldado**: se tendría que
  medir. Conservar el mapeo a las seis categorías de 2023 permitiría comparar
  a nivel grueso.

Las tres opciones son compatibles con conservar las métricas y el formato;
lo que cambia es el enum y sus definiciones. Nada de esto se decide aquí.

**Qué técnicas de SemEval adoptar no se decide ahora** (Mateo, 2026-09-27):
queda en esta entrada hasta después de cerrar la Puerta 3.

**Pendiente para el diseño de la taxonomía: definiciones con intención.**
Varias definiciones de SemEval 2023 incorporan intención: *Obfuscation*,
"words that are deliberately not clear"; *Repetition*, "with the hope that
the repetition will lead to persuade the audience"; *Loaded Language*, "to
influence and convince the audience that an argument is valid"; la categoría
*Manipulative wording*, "in order to impact the reader emotionally" (L-02,
fig. 1, p. 2344). Adoptarlas tal cual contradiría la regla dura (§3). Es el
punto que habrá que resolver al diseñar la taxonomía.

### 3. Regla dura

> **El sistema nunca emite intención del autor.**

Motivo documental, no solo de principio: las propias fuentes meten la
intención en las definiciones. La definición de propaganda de L-01 incluye
"deliberately designed" y "doing so on purpose" (p. 1378); en L-02, *Obfuscation*
son palabras "deliberately not clear", la *Repetition* se usa "with the hope
that…" y el *Manipulative wording* busca "impact the reader emotionally"
(p. 2344); L-07 especula con la intención de los políticos (p. 7316). Adoptar
esas definiciones tal cual metería la intención en la salida por la puerta de
atrás.

**Aprobado por Mateo (2026-09-27; DEC-037):** el sistema tampoco emite
**estados del lector** (miedo, creencia, persuasión) ni **efectos de
difusión**. Razón anotada: L-06 distingue el miedo representado en el mensaje
del experimentado por el receptor y solo 71 de 248 estudios midieron lo
segundo (p. 3, nota 2); L-07 pide experimentos para establecer efectos sobre
actitudes (p. 7317). Los mecanismos de la columna 2 son resultados
poblacionales, casi todos experimentales y de otros dominios: no licencian
una afirmación sobre un texto concreto ni sobre un lector concreto.

### 4. Matriz de tres niveles

Columna 1: lo único que el sistema podría emitir (técnica del enum y span
literal). Columna 2: qué mecanismo tiene respaldo en lo leído y cuán fuerte.
Columna 3: lo que el sistema no puede emitir nunca. Los ejemplos de prensa
estadística son del agente, no de las fuentes.

| # | Fenómeno observable en el texto (definición de la fuente) | Mecanismo psicológico con respaldo (fuente, página, fuerza) | Inferencia prohibida |
|---|---|---|---|
| A | **Lenguaje cargado:** palabras o frases con fuerte carga emocional, positiva o negativa (L-01 p. 1378; L-02 p. 2344, que añade una finalidad: ver §3). Operacionalizable con lexicones validados (L-07 pp. 7314, 7317) | Palabras moral-emocionales asociadas a +≈20 % de retuits por palabra (L-07 pp. 7313–7315): **parcial**, observacional, Twitter, inglés, difusión y no creencia. La emoción "can increase persuasion" (L-03 ms p. 9): **secundario** | "El autor quiso emocionar o manipular"; "el texto persuade al lector"; "se difundirá más"; "el medio hace propaganda" |
| B | **Apelación al miedo:** en términos observables, el fragmento representa un daño o amenaza ("depicted fear", L-06 p. 3). La definición de L-01 ("Seeking to build support … by instilling anxiety", p. 1379) incluye finalidad y habría que reescribirla | Miedo representado aumenta actitudes, intenciones y conductas en experimentos: d = 0,29 (L-06 p. 15); r = .147, .126 y .158 sobre actitudes, intenciones y conductas (L-05 tabla 2, p. 599). **Sólido en su dominio** (salud, laboratorio); **traslado a noticias no respaldado** (L-05 p. 605; L-06 p. 21). Papel de la eficacia en contradicción (§5) | "El lector siente miedo" (L-06 lo excluye, p. 3); "el autor busca asustar"; "el texto cambiará conductas" |
| C | **Exageración o minimización:** representar algo de forma excesiva o hacerlo parecer menos importante de lo que es (L-01 p. 1379; L-02 p. 2344). En prensa estadística, por ejemplo, adjetivos de magnitud sobre una cifra | **Ninguno en lo leído.** Solo un correlato textual: asociación con la relación discursiva de comparación (L-08 p. 1459), que no es mecanismo psicológico | Intención; "la cifra es falsa o exagerada" (eso lo decide `truth`/`context` con fuente). Pregunta abierta: si juzgar la exageración de una cifra exige la fuente, choca con el criterio intrínseco de L-01 (p. 1378) |
| D | **Repetición:** repetir el mismo mensaje (L-01 p. 1379); L-02 añade "with the hope that" (p. 2344): ver §3 | Efecto de verdad ilusoria: repetir aumenta la credibilidad, también de hechos (L-03 ms pp. 6–7): **sólido según la revisión**, pero se refiere a exposiciones repetidas, no a repetición dentro de un texto: **traslado parcial** | "El autor repite para que se crea"; "el lector lo creerá" |
| E | **Duda:** cuestionar la credibilidad de alguien o algo (L-01 p. 1379) | La credibilidad percibida de la fuente influye en la creencia (L-03 ms pp. 8, 13–14): **parcial**. Es la clase más difícil para los sistemas (L-01 p. 1389) | "El autor quiere desacreditar a X" |
| F | **Apelación a la autoridad:** afirmar que algo es cierto solo porque una autoridad lo respalda, sin otra evidencia (L-01 p. 1379) | Los mensajes de fuentes percibidas como creíbles persuaden más (L-03 ms p. 8): **parcial**. Riesgo propio del dominio (observación del agente): en prensa estadística citar al emisor oficial es la norma, así que el criterio "sin otra evidencia" es la frontera y hay que definirla | "Falacia de autoridad" como juicio sobre el autor |
| G | **Simplificación causal:** asumir una causa única cuando hay varias (L-01 p. 1379) | **Ninguno en lo leído** para persuasión (L-03 trata explicaciones causales solo en la corrección, ms p. 13) | Intención |
| H | **Eslóganes, clichés que cortan el pensamiento** (L-01 pp. 1379–1380) | **Ninguno en lo leído** | Intención |
| I | **Técnicas argumentativas de debate** (whataboutism, straw man, red herring, culpa por asociación, hipocresía, bandera) (L-01 pp. 1379–1380; L-02 p. 2344) | **Ninguno en lo leído**; pertinencia en prensa estadística sin respaldo | Intención |

### 5. Informe de brechas

**Sólidamente respaldado por lo leído:**

- Que las técnicas de persuasión se anotan como spans con una taxonomía
  cerrada y se evalúan con métricas de span (L-01, L-02), con acuerdo
  moderado y subjetividad declarada.
- Que la detección de técnicas es **intrínseca al texto** y distinta de
  verificar su veracidad (L-01 p. 1378 y fig. 8 p. 1407). Esto respalda que
  el eje sea un tercer eje independiente de `truth` y `context`. Apoyo solo
  en SemEval 2020; la guía árabe de L-10 está retirada como respaldo.
- Que conviene separar la propiedad del mensaje del estado del receptor (L-06
  p. 3).
- Que la repetición aumenta la credibilidad (L-03), como hallazgo de revisión.
- Que las apelaciones al miedo tienen efecto pequeño y positivo en
  experimentos de salud (L-05, L-06).
- Que un LLM *zero-shot* no localiza spans de forma fiable y que un modelo
  ajustado lo hace mejor (L-09, L-10), en árabe y seis idiomas europeos.

**Respaldado solo en parte:**

- Lenguaje cargado → difusión (L-07): observacional, inglés, Twitter,
  retuits y no creencia.
- Emoción → persuasión y fuente creíble → creencia (L-03): nivel de revisión,
  hay que leer las primarias.
- Cualquier traslado a **prensa estadística en español**: el único dato en
  español son 30 documentos de test de otro dominio (L-02).
- Que la exageración o minimización tenga un correlato medible (L-08):
  correlación textual en inglés, sin mecanismo.

**Sigue siendo convención nuestra:**

- La regla "nunca intención del autor". Las fuentes no la respaldan como
  práctica, porque varias definiciones la incluyen; la sostienen de forma
  indirecta L-03 (la inferencia de intencionalidad está poco estudiada, ms
  p. 6) y L-06 (texto frente a lector, p. 3). Es una decisión de diseño.
- No emitir estados del lector ni efectos de difusión: aprobado por Mateo
  (DEC-037), con la razón anotada en §3.
- Qué técnicas son pertinentes en prensa estadística y cuáles no.
- La unidad de anotación y de evaluación (span, frase, párrafo, titular).
- Cualquier umbral de acuerdo o de falsos positivos para este eje.

**Falta por leer** (referencias citadas en los PDF leídos, con la página
donde se citan; no se describe su contenido):

- Hauch: no disponible.
- Piskorski et al. 2023, guía de anotación, informe técnico JRC-132862 (L-02,
  pp. 2345, 2355): la guía de 60 páginas.
- Da San Martino et al. 2019, EMNLP, las 18 técnicas y el acuerdo (L-01,
  pp. 1380–1381).
- Stefanovitch & Piskorski 2023, acuerdo entre anotadores en la campaña
  multilingüe (citado en L-09, p. 14528).
- Rocklage, Rucker & Nordgren 2018, intención de persuadir y lenguaje
  emocional (L-03, ms p. 9, ref. 72).
- Baum & Abdel Rahman 2021, titulares emocionales y juicios sociales (L-03, ms
  p. 9, ref. 74).
- Brady, Gantman & Van Bavel 2020, captura atencional (L-03, ref. 276).
- Card et al. 2015, Media Frames Corpus (L-02, p. 2344).
- Sprenkamp et al. 2023, LLM y SemEval-2020 (L-09, p. 14523).
- Bolsover & Howard 2017, definición de propaganda con "on purpose" (L-01,
  p. 1378).
- Recursos en español sobre técnicas de persuasión en prensa: **ninguno
  aparece citado en lo leído**; hay que buscarlos.
- Literatura específica sobre exageración de cifras en noticias: **ninguna en
  lo leído**.

**Contradicciones entre papers (registradas, sin resolver):**

- **C-1, eficacia en las apelaciones al miedo.** L-05: "Strong fear appeals
  work only when accompanied by equally strong efficacy messages" y riesgo de
  "backfiring" sin eficacia (pp. 606–607). L-06: "effective with or without
  efficacy statements" (p. 17) y "no identified circumstances under which
  they backfire" (pp. 2, 20). Diferencia de operacionalización, anotada sin
  juzgarla: L-05 mide también respuestas defensivas (p. 601); L-06 mide solo
  actitudes, intenciones y conductas (pp. 9–10).
- **C-2, forma de la relación.** L-05: función lineal positiva (p. 598). L-06:
  miedo alto y moderado no difieren, d = −0,05, con 21 muestras (p. 17).
- **C-3, cita secundaria frente a primaria.** L-03 resume L-06 diciendo que
  los mensajes de miedo funcionan "under certain conditions if recipients
  feel they can act effectively" (ms p. 9, ref. 70); L-06 dice que funcionan
  con o sin mensaje de eficacia (p. 17).
- **C-4, número de técnicas del conjunto 2023.** L-02: 23 técnicas, con
  recuentos en inglés para las 23 (p. 2344, tabla 17). L-08: "a set of 19
  labels" (p. 1456).
- **C-5, dificultad de *Doubt*.** L-01: la clase más difícil para los
  sistemas (p. 1389). L-09: GPT-4 logra alto acuerdo en *Doubt*, lo que los
  propios autores señalan que contradice un ranking de dificultad derivado de
  anotadores humanos (p. 14528).

**Inconsistencias internas detectadas** (no son contradicciones entre
papers): L-01, orden de columnas de la tabla 9 (p. 1405 frente a p. 1388);
L-02, porcentajes intercambiados en p. 2356; L-10, α 0,335 en el texto frente
a 0,375 en la tabla 1 (p. 2727).

**Hecho (Mateo, 2026-09-27):** la tabla de papers de `EJE-MANIPULACION.md`
§3 lleva las nueve fichas marcadas como evidencia candidata. Eso no convierte
nada en decisión.
