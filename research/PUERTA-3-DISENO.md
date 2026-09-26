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
del conjunto, FMI + Interior ≥ 30 % como objetivo (se declara si no se
alcanza; sus conectores llegan después del diseño y los casos se anotan
igual); España / Latinoamérica sin cuota, desequilibrio declarado (DEC-026).
Esfuerzo previsto al ritmo de la TAREA 2 (31 casos en una jornada de agente,
unos 15 min por caso con criba): **cuatro jornadas** de recolección y
anotación.

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
