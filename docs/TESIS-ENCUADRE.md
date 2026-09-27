# Encuadre de la tesis — tras el piloto

**Fecha:** 2026-09-25 · **Decide:** Mateo (DEC-026, cierra P-15) · **Sustituye,
en lo que contradiga, al título, problema, objetivos y taxonomía de
`02-1-VeritAI-TESIS.md`**, que se conserva sin tocar como propuesta original.

> Los números que aparecen son **evidencia preliminar del piloto**
> (`research/PILOT-FINDINGS.md`): sirvieron para descubrir y refinar las
> hipótesis. **No las confirman.** La confirmación es de la Puerta 2, sobre
> datos que no pertenecieron al piloto (DEC-025).

---

## Título

> **Detección automática de divergencia contextual computable en afirmaciones
> estadísticas en español a partir de evidencia oficial y comparación entre
> ediciones**

Jerarquía que el título respeta: la *divergencia contextual computable* es el
objeto general; la *comparación entre ediciones* es cómo se obtiene la
evidencia, no todo el sistema.

## Pregunta de investigación

> ¿En qué medida puede un sistema detectar, de forma computable y trazable a
> evidencia oficial, la divergencia contextual en afirmaciones estadísticas en
> español, y con qué tasa de falsos positivos sobre afirmaciones correctamente
> enmarcadas?

## Definición operacional

Una afirmación estadística presenta **divergencia contextual computable**
cuando:

1. sus números son verificables contra una fuente primaria oficial y cada uno
   lleva su `raw_value_span` (el texto literal de donde salió);
2. la comparación que la afirmación establece —entre periodos, bases,
   magnitudes, denominadores o posiciones— **difiere de la que la propia fuente
   sostiene** con sus ediciones;
3. esa diferencia se decide con un **test determinístico** sobre los valores
   recuperados.

Es independiente de `truth`: el dato puede ser exacto (DEC-016). Y **no afirma
intención**: describe la comparación, no al autor. Donde la tesis diga
"engañoso" se lee "con divergencia contextual", y si se conserva la palabra,
queda así definida y separada de cualquier juicio sobre quien la escribió.

## Hipótesis

Proposiciones que la Puerta 2 pone a prueba con evidencia distinta de la del
piloto.

```
H1  Objeto.  Una parte sustancial de las afirmaciones estadisticas con
    divergencia contextual en espanol no es falsa: es una comparacion entre
    ediciones no comparables de una estadistica oficial (periodo o base
    elegida, base revisada, cambio de metodo) o una magnitud mal leida
    (absoluto/relativo, denominador).

H2  Computabilidad.  Para publicadores de nivel 1, la divergencia se decide
    con tests deterministicos sobre valores recuperados de la edicion actual
    y de la anterior, cada uno con su raw_value_span. Un modelo de lenguaje
    puede intervenir en la interpretacion del claim, la extraccion y la
    explicacion; ningun numero del veredicto lo tiene como unico origen.
    Condicion necesaria: recuperar la edicion anterior.

H3  Falsos positivos.  Sobre afirmaciones correctamente enmarcadas, el
    sistema no declara divergencia por encima de una tasa fijada ANTES de
    evaluar.
```

**Evidencia preliminar del piloto** (descubrimiento y refinamiento, no
confirmación):

| | Del piloto |
|---|---|
| H1 | 24 divergencias en alcance en 46 casos (tras DEC-027); 18 con el dato verdadero (`truth` supported o mixed). La familia "comparación de base" es 10 de 24 |
| H2 | Edición anterior recuperable por el agente: 84,2% en nivel 1; 74,2% global, lectura conservadora (DEC-021) |
| H3 | 16 controles negativos reales sobre 31 en el lote crudo (tras DEC-027): la tasa de falsos positivos pasa a ser medible |

```
Piloto    -> descubrimiento y refinamiento de H1-H3   (datos: P01-P20, C01-C31)
Puerta 2  -> evaluacion sobre datos distintos          (DEC-025: sin contaminacion)
```

## Objetivo general

> Diseñar, implementar y evaluar un sistema que detecte divergencia contextual
> computable en afirmaciones estadísticas en español, recuperando la evidencia
> oficial —edición actual y anterior— y presentando al usuario la comparación
> que la fuente sostiene, sin atribuir intención.

## Objetivos específicos

| | Objetivo | Respecto al 02 |
|---|---|---|
| O1 | Construir un corpus etiquetado de afirmaciones estadísticas **en español, con fuentes de España y Latinoamérica**, de prensa y comunicación oficial, clasificado por la taxonomía; **desequilibrio de la muestra declarado** (piloto: 21 de 31 casos de España); tamaño fijado tras la Puerta 2 | cambia: quita "latinoamericano" (Opción A de `00b`) y "300–500"; añade fuentes y desequilibrio |
| O2 | Desarrollar un módulo de detección de afirmaciones estadísticas verificables (N0) | igual |
| O3 | Implementar un motor de recuperación que localice la fuente primaria **y su edición anterior**, con `raw_value_span` por número | cambia: añade la edición anterior |
| O4 | Diseñar un modelo de confianza de dos dimensiones (evidencia + incertidumbre) y calibrarlo | igual |
| O5 | Implementar un prototipo funcional como extensión de navegador | igual |
| O6 | Evaluar el sistema por clase, con calibración y **tasa de falsos positivos sobre controles negativos**, en un conjunto **disjunto del piloto** | cambia: añade la disyunción (DEC-025) |

## Alcance declarado

| | |
|---|---|
| **Entrada** | Afirmaciones estadísticas en español que el usuario ve en su navegador. El **corpus** se recolecta de prensa y comunicación oficial; las redes sociales no se recolectan (inalcanzables sin evadir protecciones, DEC-018) |
| **Evidencia** | Publicadores de **nivel 1**: organismos estadísticos y ministerios con API, dataset o boletín en URL estable (DEC-024). Prototipo con **INE, FMI e Interior**. Niveles 3–5 como limitación escrita: 58,3% de recuperabilidad en el piloto |
| **Geografía** | Español, con fuentes de España y Latinoamérica. **No se afirma representatividad** de ninguno de los dos; el desequilibrio del corpus se declara |
| **Decisión** | Determinística sobre la evidencia recuperada. El modelo de lenguaje interviene en interpretación, extracción y explicación, nunca como origen de un número |
| **Fuera** | Intención del autor; afirmaciones sin fuente oficial de nivel 1; lo que `02` ya excluía (móvil, deepfakes, texto generado, multilingüe) |

## Taxonomía

```
Familia 2 · Comparacion de base           primera familia operacional (B)
   2a  periodo o base elegida             codigo 2_baseline_selection      C02 C15 (C21, cuerpo) · P05 P10 P11 P14
                                          SECUNDARIA desde DEC-034: 0/43 en la Puerta 3
   2b  base revisada                      codigo 2b_base_revisada          C29; latente en la primaria de C18
                                          PRINCIPAL desde DEC-034: E031 E042 E043 (Puerta 3)
   2c  cambio de metodo                   codigo 5_methodology_change      P13 (auditado)
Test 1 · ranking vs valor                 1_ranking_vs_value, ilustrativo (A)    C07 · P01
Test 3 · absoluto vs relativo             3_absolute_vs_relative           C19 C31 · P04 P19
Test 4 · denominador                      4_denominator                    C25 · P07 (+ secundarias)
other_observed                            3 de 24 en alcance tras DEC-027 (P17 C08 C10)
candidatas sin codigo (DEC-027)           P17 agregacion con subgrupos en sentido contrario
                                          C10 subtipo 2d, cambio afirmado sin edicion anterior
                                          -> clase solo si reaparecen: >=3 casos independientes,
                                             >=2 emisores, A|B, test computable; se decide una vez
```

Los códigos existentes se conservan: 2a y 2c son nombres de familia sobre
códigos que ya existían; `2b_base_revisada` es el único código nuevo. El único
caso reetiquetado es **C29**, cuya nota ya describía la revisión como causa.
Ningún otro caso cambia.

**2b y la API del INE (DEC-029).** La API Tempus sirve solo la **edición
vigente** de cada serie: una base revisada no se puede demostrar desde la API,
hace falta la nota de prensa o el PDF de la edición anterior. Por eso 2b quedó
**fuera del prototipo de la Puerta 2** y se declara como limitación del
conector, no de la clase. Y una regla que salió de esa puerta: en 2a **solo el
cambio de signo confirma** la divergencia; la magnitud ≥ 2× en una base de
horizonte largo es una *señal*, registrada y explicada, que no cuenta.

**2b es la clase principal desde DEC-034.** La jornada 2 de la Puerta 3 cerró
con 2a en 0 de 43 casos recolectados con ese método, y 2b apareció sola en tres
lotes independientes (C18, C29, E031/E042/E043). La condición para el cambio se
cumplió: la edición anterior del INE es recuperable por el agente fuera de
Tempus, por derivación del código de la nota (nota HTML, PDF y anexo XLSX;
`research/puerta3/RECUPERABILIDAD-2B.md`). El veredicto de 2b lleva dos campos
separados, `evidencia_al_publicar` y `evidencia_vigente`, cada uno con su
fecha. Es el último reencuadre del objeto: si 2b no funciona, se declara el
alcance con lo que haya y la tesis se escribe con el resultado negativo
documentado. 2a queda como clase secundaria con su 0/43, hallazgo publicable
sobre la muestra y el método.

**Amenaza a la validez de 2b.** La edición anterior se recupera por el
patrón de código de las notas del INE (`<OPERACION><MM><YY>`), que el INE no
documenta; INEbase no enlaza notas anteriores. Si el INE cambia el patrón, el
conector se rompe y 2b deja de ser computable por el agente. Se declara como
amenaza a la validez externa del conector: la mitigación es que la rotura sea
visible (abstención `PREVIOUS_EDITION_NOT_FOUND`, nunca un valor inventado) y
que las ediciones ya descargadas queden conservadas con su sha256.

**Premisa de 2b, con fuente primaria (2026-09-27).** El INE declara por escrito
la política de revisión provisional → definitivo de la EOH, la EOAP y la EOAC,
con calendario, en el Informe Metodológico Estandarizado de cada encuesta
(§14.1 y §17) y en su Política de revisión (2015); la nota de la EOAT lo repite
en su pie. Citas y evidencia en `research/puerta3/METODOLOGIA-REVISION-INE.md`.
Lo que el INE no declara es la magnitud de la revisión por comunidad.

**Limitación explícita de H1 (DEC-035).** La cubeta B del conjunto de
evaluación se declara con **7 casos** de 2b (Wilson 95 % del recall: 7/7 →
[64,6; 100]; 6/7 → [48,7; 97,4]), no con los 15 del diseño. La razón es
estructural: 2b solo puede darse donde el emisor publica niveles sin la tasa
por comunidad, y eso ocurre en dos de las ocho operaciones del mapa (EOH y
EOAT); en las seis restantes no apareció ninguno. B está acotado por el
universo, no por el esfuerzo de recolección. H1 se sostiene, si se sostiene,
como existencia y computabilidad del fenómeno con ese intervalo; **no como
frecuencia en la prensa**.

## Caso canónico: no hay todavía

Se cotejaron C29, C21 y C18 contra cinco requisitos idénticos —primaria
trazable, edición actual, edición anterior, revisión de base demostrable,
reproducible— y ninguno los cumple todos con un claim divergente
(`research/PILOT-FINDINGS.md` §5). La tesis presenta el **par C18 + C29**:

- **C18** demuestra el **mecanismo**: el Balance de Criminalidad 2T2026 compara
  contra un 2025 revisado (1.211.083) distinto del publicado en 2025
  (1.212.268); dos documentos del mismo emisor, dos cifras literales. El claim
  de prensa, en cambio, relaya bien y no diverge.
- **C29** muestra el **efecto sobre un claim**: la prensa titula "España cae 2
  puestos" restando el rank publicado en 2025 (25) del de 2026 (27), mientras
  el IEP publica "sube 4" contra su rank revisado. La revisión se infiere del
  indicador de cambio del IEP, que no imprime los valores revisados.

**El caso canónico de la familia B sale de la Puerta 2**, cumpliendo los cinco
requisitos y con la divergencia en el claim, sobre datos que no pertenecieron
al piloto.

*Puerta 2, 2026-09-25 (DEC-029): no salió.* Los 10 casos fueron 2a y el
conector no ve revisiones (arriba). El canónico de B queda para el conjunto de
evaluación, con ediciones anteriores documentales. El único 2a confirmado por
signo (P11) **no se cita** hasta cotejar su primaria (`NEEDS_REVIEW`).

## Qué afirma la tesis y qué no

**Afirma:** que existe un tipo de afirmación estadística en español cuyo dato es
verificable y cuya comparación no se sostiene contra la evidencia oficial; que,
para publicadores de nivel 1, esa divergencia se puede detectar con tests
determinísticos sobre la edición actual y la anterior, con cada número trazado
a su fuente; y que se puede medir cuántas veces el sistema se equivoca sobre
afirmaciones correctas.

**No afirma:** que el autor quiso engañar; que el dato sea falso; que el método
funcione fuera de nivel 1 (el 58,3% es una limitación, no una promesa); que el
corpus represente a España o a Latinoamérica; que 2b sea frecuente en la
prensa (B se declara con 7 casos e intervalo, DEC-035); que el piloto pruebe H1, H2 o
H3; que el sistema funcione sin modelos de lenguaje —solo que la decisión no
depende de ellos—; ni que exista todavía un caso canónico de base revisada con
los cinco requisitos.
