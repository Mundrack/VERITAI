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
| H1 | 26 divergencias en alcance en 46 casos; 20 con el dato verdadero (`truth` supported o mixed). Con P08 y P09, fuera de alcance por DEC-013: 28 en 48 y 21 |
| H2 | Edición anterior recuperable por el agente: 84,2% en nivel 1; 74,2% global, lectura conservadora (DEC-021) |
| H3 | 15 controles negativos reales sobre 31 en el lote crudo: la tasa de falsos positivos pasa a ser medible |

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
   2b  base revisada                      codigo 2b_base_revisada          C29; latente en la primaria de C18
   2c  cambio de metodo                   codigo 5_methodology_change      P13 (auditado)
Test 1 · ranking vs valor                 1_ranking_vs_value, ilustrativo (A)    C07 · P01
Test 3 · absoluto vs relativo             3_absolute_vs_relative           C19 C31 · P04 P19
Test 4 · denominador                      4_denominator                    C25 · P07 (+ secundarias)
other_observed                            8 de 26 en alcance (4 de 21 sin hermanos) -> P-12, sin decidir
```

Los códigos existentes se conservan: 2a y 2c son nombres de familia sobre
códigos que ya existían; `2b_base_revisada` es el único código nuevo. El único
caso reetiquetado es **C29**, cuya nota ya describía la revisión como causa.
Ningún otro caso cambia.

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

## Qué afirma la tesis y qué no

**Afirma:** que existe un tipo de afirmación estadística en español cuyo dato es
verificable y cuya comparación no se sostiene contra la evidencia oficial; que,
para publicadores de nivel 1, esa divergencia se puede detectar con tests
determinísticos sobre la edición actual y la anterior, con cada número trazado
a su fuente; y que se puede medir cuántas veces el sistema se equivoca sobre
afirmaciones correctas.

**No afirma:** que el autor quiso engañar; que el dato sea falso; que el método
funcione fuera de nivel 1 (el 58,3% es una limitación, no una promesa); que el
corpus represente a España o a Latinoamérica; que el piloto pruebe H1, H2 o
H3; que el sistema funcione sin modelos de lenguaje —solo que la decisión no
depende de ellos—; ni que exista todavía un caso canónico de base revisada con
los cinco requisitos.
