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
| B · 2a esperada | cambio de signo o valor atribuido a otro periodo | 20 (15) — 18/20 detectados da 90 % [69,9; 97,2] | H1, H2 |
| C · Otras clases | 3 absoluto/relativo, 4 denominador, 2c método; 1 ilustrativa | 15 (10) | el 2a no debe disparar; H1 |
| D · Sin test aplicable | niveles, extremos, umbrales, compuestos, correctos | 10 (5) | `undetermined` y abstención correctos |
| E · Fallo de recuperación | primaria o edición anterior no localizable; bloqueado | 10 (5) | las cinco de R02 §7, sin maquillar |
| F · Claims falsos | `contradicted` sin divergencia | 5 (3) | resuelve la discrepancia C17 |
| | **Total** | **110 (78)** | |

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
  limitación por hipótesis (B < 15: recall sin afirmación sobre H2; E < 5:
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
