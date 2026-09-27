# Puerta 3 — diseño del conjunto de evaluación (APROBADO, DEC-031)

**Fecha:** 2026-09-25 · **Estado:** **aprobado por Mateo el 2026-09-25 (DEC-031)**; la recolección arranca con tope de cuatro jornadas y revisión a la mitad · **Aplica:** DEC-018, DEC-020, DEC-021, DEC-025, DEC-027, DEC-029

> El número que manda es el de **controles con test aplicable**: sin él, H3 no
> es medible (hoy n = 1). Todo lo demás se dimensiona después de ese número.

## 0. Reglas previas, ya decididas

Nada del piloto ni de la Puerta 2 entra, ni sus hermanos por criba (misma
primaria y misma consulta) (DEC-025). Regla dura: sin artículo de verificación
previo (DEC-018); el primer rechazo del publicador cierra el caso (DEC-021).
Enums cerrados; `undetermined` cuando ningún test aplica; la señal de horizonte
se anota aparte y no es divergencia (DEC-029). Cada caso registra vía de
descubrimiento y consulta (DEC-020). **La anotación se congela antes de correr
el arnés**: sha256 del CSV en una DEC; después, ningún test se toca para este
conjunto (un cambio de test es una DEC y aplica al siguiente conjunto).

**Anotación, y lo que se declara si no hay segundo anotador (DEC-031).** Anota
el agente todos los casos, con cronómetro. **Mateo anota a ciegas una muestra
estratificada del 25 %** (por cubeta, semilla `20260925`, extraída al cerrar la
recolección y antes de congelar; recibe solo claim y URL, como en P-20). Eso da
el **acuerdo agente–humano** (kappa sobre `truth`, `context`, `clase`), que
mide la consistencia del método, **no la fiabilidad entre humanos**. Hoy no
hay segundo anotador humano (P-05). Si sigue sin haberlo al congelar:

- la tesis **no afirma kappa interanotador**; reporta el acuerdo agente–humano
  con su intervalo y lo nombra así;
- se declara como **amenaza a la validez**: un solo anotador humano, que
  además diseñó la taxonomía; las etiquetas pueden reflejar su lectura;
- en la muestra del 25 %, ante desacuerdo **manda la etiqueta de Mateo**, cada
  desacuerdo queda registrado con su motivo, y **si el desacuerdo en `context`
  supera el 20 % de la muestra, Mateo revisa el 100 % antes de congelar**
  (la consecuencia se fija ahora para que no sea una decisión a posteriori);
- si aparece un segundo anotador antes de congelar, anota el mismo 25 % a
  ciegas y se reporta el kappa entre humanos además del agente–humano; si
  aparece después, se reporta como trabajo posterior sin tocar el congelado.

## 1. Tamaño y cubetas

**H3 necesita una tasa fijada antes de evaluar** (`TESIS-ENCUADRE`). Propuesta:
**FPR ≤ 10 %** sobre controles con test aplicable, y H3 se sostiene solo si el
**límite superior del IC 95 % (Wilson) es ≤ 15 %**. Sin la segunda condición,
un 0/10 "pasa" con un intervalo que llega al 28 %.

Límite superior Wilson 95 % del FPR (%), por n controles y k falsos positivos:

| n | k=0 | k=1 | k=2 | k=3 |
|---|---|---|---|---|
| 20 | 16,1 | 23,6 | 30,1 | 36,0 |
| 30 | 11,4 | 16,7 | 21,3 | 25,6 |
| 40 | 8,8 | 12,9 | 16,5 | 19,9 |
| **50** | **7,1** | **10,5** | **13,5** | 16,2 |
| 60 | 6,0 | 8,9 | 11,4 | 13,7 |

Con 20 controles H3 no es evaluable ni con cero errores. Con 30 solo pasa si
el sistema no falla nunca. **40 es el mínimo** que tolera un falso positivo;
**50 tolera dos**. Objetivo: **50 controles con test aplicable, mínimo 40.**

| Cubeta | Qué es | Objetivo (mín.) | Para qué |
|---|---|---|---|
| **A · Controles con test aplicable** | cambio entre periodos correctamente enmarcado: base = referencia del emisor, `truth` supported, `context` no_divergence | **50 (40)** | **FPR, H3** |
| B · **2b esperada** (DEC-034; antes 2a) | base revisada: la tasa del claim usa la edición **al publicar** del periodo base y la edición **vigente** la contradice, con o sin cambio de signo | **7 (7)** desde DEC-035 (§4g; antes 20 (15)) — 7/7 detectados da 100 % [64,6; 100]; 6/7, 85,7 % [48,7; 97,4] | H1, H2 |
| C · Otras clases | 2a periodo o base elegida (secundaria desde DEC-034, 0/43), 3 absoluto/relativo, 4 denominador, 2c método; 1 ilustrativa | 15 (10) | el test principal no debe disparar; H1 |
| D · Sin test aplicable | niveles, extremos, umbrales, compuestos, correctos | 10 (5) | `undetermined` y abstención correctos |
| E · Fallo de recuperación | primaria o edición anterior no localizable; bloqueado | 10 (5) | las cinco de R02 §7, sin maquillar |
| F · Claims falsos | `contradicted` sin divergencia | 5 (3) | resuelve la discrepancia C17 |
| | **Total** | **97 (70)** desde DEC-035 (antes 110 (78)) | |

Reglas de composición: los hermanos por criba cuentan **una vez** y quedan
marcados; A y B con **≥ 2 emisores** cada una; **≤ 3 controles por nota de
prensa** del INE (50 controles de la misma nota no son 50 casos); INE **≤ 70 %**
del conjunto, los otros emisores ≥ 30 % como objetivo (se declara si no se
alcanza; sus conectores llegan después del diseño y los casos se anotan
igual); España / Latinoamérica sin cuota, desequilibrio declarado (DEC-026).
Esfuerzo previsto al ritmo de la TAREA 2 (31 casos en una jornada de agente,
unos 15 min por caso con criba): **cuatro jornadas** de recolección y
anotación.

**Emisores tras la jornada 1 (DEC-032, cierra P-24).** `imf.org` e
`interior.gob.es` devolvieron **403** al agente identificado en la primera
petición (API, HTML y PDF en el FMI; PDF del Balance en Interior). Por DEC-018
y DEC-021 eso cierra esos casos y **no se evade**; queda como hallazgo escrito
y los nueve casos bloqueados se quedan en la cubeta E. Sustitución, probada
con una petición identificada por URL el 2026-09-26: el **Portal Estadístico
de Criminalidad** (`estadisticasdecriminalidad.ses.mir.es`, CSV y HTML, 200)
sustituye a `interior.gob.es` como vía de Interior; **SEPE** (HTML, 200) entra
como tercer emisor en lugar del FMI; el **Banco de España** (HTML y CSV del
Boletín Estadístico, 200) queda como reserva para claims financieros. Nada de
acceso formal: no cabe en el calendario.

## 1b. Dos vías de descubrimiento, registradas por caso (DEC-032)

La jornada 1 lo dejó claro: 26 casos, **B = 0**. La recolección iba del
organismo hacia fuera (nota del INE → prensa que la relaya) y esa vía solo
produce controles: la prensa que relaya una nota reproduce la comparación del
emisor. Las divergencias están en la prensa que **interpreta** el dato con su
propia base, su propio periodo o su propio denominador. Por eso hay dos vías,
separadas y registradas:

| Vía | Para | Cómo | `descubrimiento_via` |
|---|---|---|---|
| **Control** (A, D) | controles con test aplicable, niveles, extremos | desde el organismo: nota o tabla → prensa que la relaya, ≤ 3 por edición. **Funciona; no se toca** | `busqueda_a_organismo` |
| **Divergencia** (B, C, F) | 2a por signo o por valor de otro periodo, otras clases, claims falsos | desde la prensa, como en la TAREA 2: titulares con cifra y una **comparación propia** ("desde 2019", "frente a <periodo no estándar>", "se dispara / se hunde", "por primera vez desde", "uno de cada", "el doble que", rankings, encuestas), y **después** la primaria y su edición anterior | `titular_prensa` (patrón de comparación), `busqueda_de_rankings`, `busqueda_de_encuestas`, `busqueda_por_tema`, `criba_negativa` |

Reglas: cada caso lleva su `descubrimiento_via` y su `descubrimiento_query`
(DEC-020) **para que el sesgo de la vía quede medido, no inferido**; el
validador imprime la tabla cubeta × vía; la vía no cambia la anotación (un
titular de prensa que resulta correcto es un control A aunque venga de la vía
divergencia, y se cuenta como tal); la criba y el cronómetro son los mismos
en las dos vías.

**Tasas de referencia para proyectar B**, del lote crudo del piloto (31 casos
recolectados desde la prensa, etiquetas del corpus): B (2a) 3 de 31 = 9,7 %,
C 5 de 31 = 16 %, F 2 de 31 = 6,5 %, controles 13 de 31. De los 3 B, 2
salieron de la vía organismo y 1 de la criba negativa; bajo la regla de
DEC-029 (solo signo o valor de otro periodo confirman) la tasa de B es menor
o igual que esa. La proyección por jornada se reporta a Mateo antes de gastar
más jornadas; si B no puede llegar a 15 con el tope, el conjunto no sirve para
H1 y se replantea (§3).

## 2. Criterio de reaparición de P17 y C10, escrito antes de ver los datos

Al anotar, todo `other_observed` lleva `mecanismo_candidato` ∈
{`P17_agregacion_subgrupos`, `C10_cambio_sin_edicion_anterior`, `otro`} y una
línea con el mecanismo. Una candidata pasa a clase o subtipo **solo si**, con
la anotación congelada: **≥ 3 casos independientes** (sin hermanos), de
**≥ 2 emisores**, recuperabilidad **A o B** cada uno, y un **test computable
sin juicio humano** escrito como pseudocódigo. Se cuenta **una sola vez**, al
congelar, antes de correr el arnés, y queda como DEC (DEC-027). Con 1–2 sigue
como `other_observed` anotada; con 0 se archiva. **Si pasa:** se crea el código
y se escribe el test, pero su evaluación sobre este conjunto es
**exploratoria** y se reporta aparte: el test se diseñó viendo estos casos, y
la confirmación exige datos nuevos. N01 (segunda aparición de P17) es
desarrollo y no cuenta.

## 3. Regla de parada y qué se declara como limitación

**Tope:** cuatro jornadas de recolección cronometradas, con **revisión a la
mitad** (fin de la jornada 2): proyección por cubeta con el ritmo real.

- **A la mitad, si A proyecta < 40:** pivote de **recolección**, no de tesis:
  descubrimiento dirigido a organismo (nota de prensa → prensa que la relaya),
  que en el piloto dio 92,3 % de recuperabilidad frente a 50 % del resto de
  vías. Si el pivote no levanta A, se sigue hasta el tope y se reporta.
- **Al tope, cubeta A:** ≥ 40 → H3 evaluable. **20–39** → H3 "evaluable con
  intervalo ancho": se reporta el límite superior real, **sin afirmar
  FPR < 10 %**, y se declara como limitación. **< 20** → H3 **no evaluable**;
  la Puerta 3 no se cierra y se decide por DEC (más tiempo o rediseño).
- **Otras cubetas bajo mínimo:** se reporta con su intervalo y se declara la
  limitación por hipótesis (B < 7 desde DEC-035, antes 15: recall sin afirmación sobre H2; E < 5:
  métricas de recuperabilidad marcadas como posiblemente optimistas; F < 3: la
  discrepancia C17 queda sin resolver). Ninguna cubeta se rellena con
  hermanos, con casos del piloto ni relajando la regla dura.
- **Siempre se declara:** un solo recolector (el agente) con cronómetro, un
  anotador humano sobre muestra, vía de descubrimiento por caso, y el
  desequilibrio geográfico y por emisor que salga.

**Qué aprueba Mateo:** la tasa de H3 (10 % / límite 15 %), el objetivo y
mínimo de A (50 / 40), el resto de cubetas, el tope de cuatro jornadas con
revisión a la mitad, y el 25 % de doble anotación. Con eso se abre la
recolección; sin eso, no.

### 3b. Regla de la jornada 2, fijada antes de recolectarla (DEC-033)

La jornada 2 (4 h de reloj, pausas descontadas) se hace **entera por la vía
divergencia dirigida** y se trata como **medición**. Al cerrarla se cuenta
**B** = casos anotados en la cubeta B (2a esperada **por cambio de signo o por
valor atribuido a otro periodo**, DEC-029), con criba hecha, trabajados, y
contando los hermanos por criba una sola vez. **La señal de horizonte no
cuenta como B en ningún escenario.** La asignación es completa y previa:

| B al cerrar la jornada 2 | Qué se hace | Por qué esa salida |
|---|---|---|
| **≥ 4** | **Sigue.** Jornadas 3 y 4 por la vía divergencia; los controles A que aparezcan por esa vía se cuentan igual. | 4 por jornada × 2 jornadas ≥ 8 más: 12–15 al tope; si al final B < 15, aplica la limitación de §3 (recall con intervalo, sin afirmación sobre H1/H2). |
| **= 3** | **Replanteo 1: ampliar el tope en dos jornadas** (seis en total). El mínimo de B sigue en 15. | 3 por jornada × 4 jornadas restantes = 12, más 3 = 15: alcanzable justo, sin tocar el mínimo. |
| **= 1 o 2** | **Replanteo 3: ambas.** Ampliar el tope en dos jornadas **y** bajar el mínimo de B a 10 con intervalo declarado (10 positivos, 9 detectados → 90 % [59,6; 98,2]). | Con 1–2 por jornada no se llega a 15 ni con seis jornadas; con 10 y seis jornadas, sí. La tesis dice que H1/H2 se evalúan con poca potencia y da el intervalo. |
| **= 0** | **Ninguna de las tres basta: no se gasta la jornada 3.** Se abre una DEC de replanteo con Mateo: si la definición de B (2a por signo) es demasiado estrecha para lo que la prensa produce, si hay que cambiar la vía o los emisores, o si la tesis evalúa H1 con B < 10 como limitación. | Ampliar jornadas a tasa cero no produce casos; bajar el mínimo a 10 con tasa cero tampoco. Decidirlo después de ver un número distinto de cero sería ajustar el umbral a posteriori. |

Lo que no cambia en ningún escenario: la regla dura, DEC-021, DEC-025,
DEC-029, los hermanos cuentan una vez, y los casos de la vía divergencia que
resulten controles se anotan como A y cuentan para el FPR.

## 4. Replanteo tras la jornada 2 (DEC-034): la cubeta B es 2b

La jornada 2 cerró con **B = 0**: 2a no apareció en 43 casos recolectados con
este método (`puerta3/PROGRESO.md`). Por DEC-034 la cubeta B pasa a ser
**`2b_base_revisada`**: la tasa del claim se calculó con la edición **al
publicar** del periodo base y la edición **vigente** la contradice, con o sin
cambio de signo. 2a pasa a la cubeta C como clase secundaria y conserva su
0/43. Los objetivos numéricos de §1 no cambian (B 20, mínimo 15: los
intervalos valen para cualquier clase).

Condición bloqueante, cumplida antes de recolectar nada más: la edición
anterior del INE es recuperable por el agente fuera de Tempus
([`puerta3/RECUPERABILIDAD-2B.md`](puerta3/RECUPERABILIDAD-2B.md): cinco
ediciones de cuatro operaciones, nota HTML, nota PDF y anexo XLSX con 200, y el
valor publicado difiere del vigente en las cinco).

Anotación de un caso B: `estructura.evidencia_al_publicar` y
`estructura.evidencia_vigente`, cada una con valor, edición, **fecha**
(publicación / consulta), URL y `raw_value_span` (E031, E042, E043). Tasa
observada de 2b en la jornada 2: 3 de 17 casos de prensa, pero salió de un lote
que buscaba otra cosa. Q048 sigue vetado por DEC-025.

**Amenaza a la validez de 2b (no una nota al pie).** La edición anterior se
recupera por el patrón de código de las notas del INE, que el INE no
documenta; INEbase no enlaza notas anteriores. **Si el INE cambia el patrón,
el conector se rompe y 2b deja de ser computable por el agente.** Mitigación
solo para que la rotura sea visible: abstención `PREVIOUS_EDITION_NOT_FOUND`,
nunca un valor inventado, y ediciones ya descargadas conservadas con sha256.
Se declara en la tesis como límite de validez externa del conector. El
conector cubre un mapa cerrado de 8 operaciones del INE
(`docs/PROPUESTA-2B.md` §4).

### 4b. Regla de la jornada 3, fijada por Mateo antes de recolectarla

La jornada 3 se hace por la vía divergencia con **B = 2b** y se trata también
como **medición**, porque los 3 de 17 de la jornada 2 vienen de un lote que
buscaba otra cosa. Regla previa: **B por jornada ≥ 4 → la proyección sostiene
los 15 y se sigue; B ≤ 3 → se para y se replantea el mínimo con intervalo
declarado.** Cuentan los casos anotados en B (2b) con criba hecha y
trabajados; los hermanos por criba una sola vez. Se avisa al cerrar la
jornada con el número de B.

Resultado (2026-09-26): B = 4 en 0,48 h de reloj → sigue. Los cuatro salieron
de dos ediciones de la EOH (CTH0726 y CTH0826), y con los tres de la jornada 2
los siete B del conjunto venían de la misma operación: de ahí el tope de §4c.

### 4c. Tope de tres B por edición (aprobado por Mateo antes de la jornada 4)

Ninguna edición de una primaria aporta más de **tres** casos a la cubeta B,
igual que el tope de tres controles por edición. El cuarto y siguientes se
anotan igual, con `excedente="si"`, y **no cuentan** para la cubeta ni para la
regla de parada; el validador lo comprueba. Aplicado al lote al aprobarse:
CTH0726 tenía cuatro (E042, E043, E053, E056) y **E056 pasa a excedente**;
CTH0826 tiene tres (E031, E047, E055). B cuenta 6.

Por qué: sin tope, la jornada 4 llena B con la EOH y H1 quedaría evaluada
sobre una sola operación y dos meses. Con tope, quince B exigen al menos cinco
ediciones distintas.

### 4d. Límite del fenómeno: 2b aparece donde el redactor calcula la tasa

Hipótesis fijada por Mateo antes de la jornada 4: 2b aparece donde el redactor
tiene que calcular la tasa interanual, y no aparece donde el anexo (o la nota)
ya la trae hecha. Comprobación sobre los anexos descargados de las ocho
operaciones del mapa (`research/evidencia/D2B_*.json`):

| operación | tabla por CCAA en el anexo | ¿tasa de variación por CCAA? | casos regionales vistos | 2b observados |
|---|---|---|---|---|
| CTH (EOH) | `EOH_Hoja3` viajeros y pernoctaciones | **no** (solo niveles; la tasa está solo para precios, IPH/IRSH) | 22 (jornadas 2–3) | **7** |
| EOAT | `EOAP_Hoja1`, `EOAC_Hoja1`, `EOTR_Hoja1`, `EOAL_Hoja2` | **no** (solo niveles) | 3 (E049, E050, E054) | 0 (dos con base vigente, uno claim falso) |
| ETDP | `Hoja9` (ETDP.11) | sí, "% Variación anual" | 3 (E029, E040, Cataluña/Navarra en prensa) | 0 |
| Hipotecas | `Hoja1`/`Hoja6` (niveles) | sí, en la nota HTML: gráfico "Variación anual (%)" por CCAA | 1 (Galicia abril, no registrado) | 0 |
| Sociedades | `Hoja 1` (niveles) | sí, en la nota HTML: gráfico "Variación anual (%)" por CCAA | 0 | 0 |
| IPI | `Tabla 5` | sí, "Tasa anual" por CCAA | 0 | 0 |
| FRONTUR | `Hoja1` por CCAA de destino | sí, "Variación" mensual y acumulada | 0 regionales (E017 nacional) | 0 |
| EGATUR | hoja mensual por CCAA | sí, "Variación" | 0 regionales (E018 nacional) | 0 |

**El patrón se confirma:** los siete 2b (más E050, el claim falso con base
inexistente) están en la única operación sin tasa por CCAA en la que se han
trabajado casos regionales; en las seis operaciones con la tasa hecha no
apareció ninguno. EOAT, la otra sin tasa, tiene tres casos y ningún 2b: la
condición es necesaria, no suficiente (el redactor puede calcular con la
vigente, como hizo Europa Press en E049 y E054).

**Consecuencia declarada como límite del fenómeno (alcance):** 2b, tal como
lo captura este conjunto, es un mecanismo de *redacción* que solo puede
aparecer donde el emisor publica niveles sin tasa por comunidad. La jornada 4
va dirigida a las operaciones que NO traen la tasa (EOH en otros meses y EOAT)
y a los emisores con cuota pendiente (§4f). Lo que la evaluación diga de 2b
vale para ese ámbito, no para "las estadísticas del INE" en general.

### 4e. Control natural: misma edición, mismo día, dos cálculos distintos

Hallazgo de las jornadas 2 y 3, que Mateo pide como apartado propio: en la
misma edición y la misma mañana, unas redacciones calculan la tasa contra la
edición provisional del año anterior y otras contra la vigente. Es un control
natural: el dato es el mismo, la fecha es la misma, y solo cambia la base que
cada redacción tomó.

Edición **CTH0726** (EOH julio 2026, publicada el 21/08/2026):

| base | redacción (caso) | tasa publicada | tasa con la otra base |
|---|---|---|---|
| provisional | Galicia Press / Europa Press (E053) | Galicia +0,68 % | vigente −0,35 % (cambia el signo) |
| provisional | MurciaEconomía y teletipo regional (E056) | Murcia +4,09 % | vigente +3,32 % |
| provisional | El Diario de Madrid (E042) | Madrid −1,43 % | vigente −1,05 % |
| provisional | Economía de Mallorca (E043) | Baleares residentes +3,8 % | vigente −2,3 % (cambia el signo) |
| vigente | RTVC / Europa Press Canarias (E035) | Canarias +2,39 % | provisional +3,49 % |
| vigente | Andalucía Información (E048) | Málaga ciudad +15,57 % | (serie de punto turístico) |
| vigente | Lanza / La Cerca (E057) | Castilla-La Mancha −6,7 % | provisional −5,84 % |
| vigente | atlantico.net, 22/08/2026 (no registrado) | Galicia −0,4 % | provisional +0,68 % |
| vigente | teletipo CyL, 21/08/2026 (no registrado) | Castilla y León −7,1 % | provisional −7,66 % |

Edición **CTH0826** (EOH agosto 2026, publicada el 22/09/2026):

| base | redacción (caso) | tasa publicada | tasa con la otra base |
|---|---|---|---|
| provisional | Europa Press Madrid / Última Hora (E031) | Madrid +2,36 % | vigente +3,55 % |
| provisional | EFE Palma / Última Hora (E047) | Baleares −0,2 % y +3,8 % | vigente −0,44 % y +3,54 % |
| provisional | El Debate / El Correo de Burgos / CyL Digital (E055) | Castilla y León −4,5 % | vigente −3,19 % |
| vigente | Libertad Digital Canarias (E051) | Canarias +2,5 % | provisional +1,97 % |
| vigente | Europa Press Andalucía / Última Hora (E052) | Andalucía +2 % | provisional +1,73 % |
| vigente | Europa Press Valencia / Última Hora (no registrado) | C. Valenciana +1,4 % | provisional +1,43 % (indistinguible) |
| vigente | Galicia Press (no registrado) | Galicia +1 %, "16.452 más" | provisional +1,24 % |
| vigente | Heraldo de León (no registrado) | León −2,08 % | provisional −4,39 % |
| vigente | CLM24 (no registrado) | Castilla-La Mancha −5,6 % | (sin fila provisional comparable en la tabla usada) |
| vigente | empresas.de Murcia (no registrado) | Murcia −0,2 % | provisional +0,25 % (cambia el signo) |
| vigente | ifomo / eldiario.es Cantabria (no registrado) | Cantabria +2,3 % | provisional +2,05 % |
| vigente | Región Digital / Onda Cero Extremadura (no registrado) | Extremadura +5,2 % | provisional +5,76 % |

Lo que sostiene el control: **7 casos registrados con base provisional** frente
a **6 registrados y 9 observados con URL con base vigente**, en dos ediciones y
dos días. La misma agencia usa una base en una delegación y otra en otra
(Europa Press: provisional en Madrid y Galicia, vigente en Canarias, Andalucía
y Valencia). Galicia Press usó la provisional en julio y la vigente en agosto.
El mecanismo es del redactor, no de la edición ni del medio. Para la tesis es
la prueba de que 2b no es un artefacto del conector: dos tasas de signo
opuesto para el mismo dato, publicadas la misma semana (Galicia julio).

**Ampliación en la jornada 4 (2026-09-27).** Se comprobaron unas 25 piezas
regionales de las ediciones de marzo a junio de la EOH y de mayo a julio de
la EOAT (lista en `research/puerta3/PROGRESO.md`, jornada 4): **todas con la
base vigente**, incluidas las redacciones que en julio y agosto usaron la
provisional (Europa Press Madrid +1,2 % en junio; EFE Baleares +14,5 % en
marzo; El Debate/EP Castilla y León −4,4 % en junio; Galicia Press en junio).
El único 2b nuevo, E066 (El Nuevo Digital Murcia, EOAT0526: apartamentos
+60 % con la provisional, +34,5 % con la vigente), sale de una redacción
murciana, como E056 (MurciaEconomía). El control natural se sostiene y se
afina: el mecanismo es del redactor y del turno, no de la edición ni de la
operación; y con lo recolectado se concentra en las ediciones de verano
(CTH0726, CTH0826) más EOAT0526. Es una observación, no una prueba: la
comprobación barata es EOAT0826 (30-09) y CTH0926 (23-10).

### 4f. Cuota de emisor para la jornada 4

Al cerrar la jornada 3 el INE está en 39 de 57 casos (68,4 %) con tope del
70 %. La jornada 4 trae casos de SEPE, Portal Estadístico de Criminalidad y
Banco de España antes que más INE; si no, la cuota bloquea el conjunto.
Restricciones vigentes: Interior 2T2026 vetado (DEC-025), tope de tres
controles por edición (Interior 1T2026 tiene dos, SEPE agosto 2026 uno más un
D, BdE julio 2026 uno).

**Resultado (jornada 4, 2026-09-27).** Cuota cumplida: INE 41/66 = 62,1 %
(antes 68,4 %). SEPE julio 2026 ×3 (E058–E060, tope de controles), BdE junio
2026 ×2 (E061, E062), Portal 1T2026 ×2 (E063 A, con el que la edición llega al
tope; E064 D). Todos los PDF mensuales del SEPE (nueve ediciones) y las notas
del BdE respondieron 200 al agente identificado. B de la jornada = 1 (E066):
por la regla §4b se para y decide Mateo.

### 4g. Cubeta B declarada con 7 casos e intervalo (DEC-035, 2026-09-27)

**Decisión de Mateo tras la jornada 4.** La cubeta B se declara con los
**7 casos** anotados (E031, E042, E043, E047, E053, E055, E066; E056 queda
como excedente por el tope §4c). El mínimo de 15 **baja a 7 con intervalo
declarado** y esa rebaja queda como **limitación explícita de H1**.

**Razón estructural, no de esfuerzo.** 2b es un mecanismo de redacción que
solo puede darse donde el emisor publica niveles sin la tasa por comunidad
(§4d). En el mapa cerrado de ocho operaciones eso ocurre en **dos** (EOH y
EOAT); en las otras seis el anexo o la nota traen la tasa hecha y no apareció
ninguno. El universo de B es, por tanto: dos operaciones × las ediciones
admisibles de 2026 × las piezas regionales que calculan la tasa × el tope de
tres por edición. Dentro de ese universo, las ediciones de marzo a junio dieron
0 piezas con base provisional de unas 25 comprobadas, y la jornada 4 (0,9 h,
unas 40 búsquedas dirigidas) produjo 1. **B está acotado por el universo, no
por el esfuerzo de recolección**: seguir buscando en las mismas ediciones no
cambia el número, solo el tiempo.

**Lo que se afirma y con qué intervalo.** Recall de 2b sobre 7 positivos,
Wilson 95 %: 7/7 → 100 % [64,6; 100]; 6/7 → 85,7 % [48,7; 97,4]; 5/7 →
71,4 % [35,9; 91,8]. La tesis afirma que el fenómeno existe, es computable
con dos ediciones y el sistema lo detecta con ese intervalo; **no afirma nada
sobre su frecuencia en la prensa**. H2 se evalúa igual (la edición anterior
se recuperó en los 7). La fila B de la tabla de §1 pasa a **7 (7)** con el
intervalo de arriba; §3 se lee con ese mínimo.

**Lo que no cambia.** A sigue en 50 (40): es lo que sostiene H3 y hoy está
en 31 (límite superior del FPR con 0 errores: 11,0 %; con 40, 8,8 %). C, D,
E, F y O, igual. Regla dura, DEC-021, DEC-025 y DEC-029, igual.

### 4h. Jornada 5 como prueba de predicción, no como recolección (escrita antes del 30-09)

La hipótesis de §4d predice **dónde** aparece 2b. Para que la comprobación no
sea retrospectiva, la predicción queda escrita el **2026-09-27**, en el commit
que introduce esta sección, tres días antes de la edición que la pone a
prueba.

**Edición de prueba:** EOAT agosto 2026 (`EOAT0826`), calendario del INE:
**30 de septiembre de 2026**. Edición anterior de la base: `EOAT0825`
(agosto 2025), recuperable por el conector.

**Predicción P1 (aparece).** Entre las piezas regionales que se localicen
sobre `EOAT0826` con una tasa interanual de viajeros o pernoctaciones en
apartamentos o campings por comunidad, calculada por la redacción (la nota
del INE no la trae), **al menos una** reproduce la tasa solo con la base de
`EOAT0825` y no con la vigente: un 2b.

**Predicción P2 (no aparece).** Entre las piezas regionales localizadas en la
misma jornada sobre ediciones de 2026 de las seis operaciones con tasa
publicada (ETDP, Hipotecas, Sociedades, IPI, FRONTUR, EGATUR), **ninguna**
usa una base provisional distinta de la vigente.

**Cómo se lee el resultado, fijado ahora.**

| P1: piezas localizadas con tasa propia | 2b encontrados | lectura |
|---|---|---|
| ≥ 6 | ≥ 1 | P1 confirmada para esta edición |
| ≥ 8 | 0 | P1 **refutada** para esta edición: la condición de §4d es necesaria pero no discrimina; se declara |
| < 6 | cualquiera | inconclusa: el universo localizable fue demasiado pequeño; se reporta el número |

P2 se considera refutada con un solo 2b en las seis operaciones con tasa, sea
cual sea el número de piezas. Tasa base observada hasta hoy en la EOAT: 1
pieza con base provisional de 11 localizadas (EOAT0526 1/3, EOAT0626 0/3,
EOAT0726 0/5), así que P1 es una predicción con riesgo real de fallar.

**Lo que P1 no discrimina.** `EOAT0826` es una edición de verano; un 2b ahí
es compatible con §4d y con la observación de §4e ampliado (el patrón se
concentra en julio y agosto). La edición que separa ambas lecturas es
`CTH0926` (23 de octubre): §4d admite 2b; la lectura estacional lo hace menos
probable. Por eso **`CTH0926` es necesaria, no opcional** (decisión de Mateo,
2026-09-27, enmienda a DEC-035): es la única edición fuera del verano
disponible antes de cerrar la Puerta, y sin ella la predicción P1 no separa
§4d de la lectura estacional. La jornada 5 no se cierra hasta trabajarla; la
prueba de predicción se lee con las dos ediciones (P1 sobre `EOAT0826`, P1'
sobre `CTH0926` con la misma tabla de lectura, y P2 sobre ambas).

**Método de la jornada 5, el mismo de las jornadas 3 y 4:** tabla de tasas
provisional/vigente por CCAA con `EOAT0825` (anexo) y la API, búsqueda de las
cifras que solo salen con la provisional, criba (a) y (b) por caso, cronómetro
por caso, tope de tres B por edición. Se cuentan y se listan **todas** las
piezas localizadas, con la base que usan, no solo las que dan B.

### 4i. La jornada 5 completa A hasta 40, sin INE

H3 necesita 40 controles y hay 31. En la misma jornada se recolectan **al
menos 9 controles A sin emisor INE** (cuota, §4f): SEPE (junio y agosto 2026,
y septiembre si sale el 2 de octubre; tres por edición), Banco de España
(deuda por CCAA del segundo trimestre, que se publica el 30 de septiembre;
notas de mayo y julio de 2026) y Portal Estadístico de Criminalidad (edición
anual 2025, publicada en marzo de 2026, si no está vetada; 1T2026 ya llegó al
tope). Cada control con criba, cronómetro y la misma regla de tres por
edición. `CTH0926` (23 de octubre) es **necesaria** (§4h, enmienda a DEC-035):
la jornada 5 queda abierta hasta trabajarla, y el cierre de la Puerta 3 espera
a esa edición.

### 4j. Vía descartada: rastrear las redacciones que ya mostraron el mecanismo

Se propuso y **se descarta (DEC-035)**. Seguir edición a edición a El Nuevo
Digital Murcia, MurciaEconomía, EFE Baleares, Europa Press Madrid o Galicia
Press produciría B barato, pero sesga justo lo que el control natural de §4e
mide: la proporción de redacciones que calculan con una base u otra sobre la
misma edición. Un conjunto enriquecido con esas redacciones diría que 2b es
frecuente porque se buscó donde ya se sabía que estaba. Queda anotado como
vía descartada y por qué.
