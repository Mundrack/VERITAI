# Preguntas abiertas

Lo que está sin resolver, quién lo decide, y qué bloquea.

> Cuando una pregunta se cierra **no se borra**: se mueve a la sección "Cerradas"
> con la decisión y la fecha. Saber qué se descartó vale tanto como saber qué se
> eligió.

**Última actualización:** 2026-09-25

---

## Abiertas — decide Mateo

### P-02 · Aprobación de `CLAUDE.md`

**Estado:** pendiente · **Bloquea:** nada

`CLAUDE.md` está en la raíz marcado como *propuesta*. El 06-PROMPT pide
explícitamente proponerlo antes de darlo por bueno. Sigue como propuesta hasta
que Mateo lo revise.

Los dos puntos que conviene mirar con atención:

- **§7, librerías prohibidas.** Es la lista que va a rechazar dependencias más
  adelante. Si algo sobra o falta, mejor saberlo ahora.
- **§5, código y documentación en español.** Es lo que se usó en todo el entorno.
  Cambiarlo después significa reescribir comentarios y nombres.

### P-09 · Rotar la contraseña de la base de datos de Supabase

**Estado:** abierto **a propósito** · **Bloquea:** cargar datos reales en Supabase

El 2026-09-24 las credenciales del proyecto Supabase se pegaron en texto plano en
una conversación. Eso incluye la **contraseña de la base de datos**, que da acceso
total al proyecto.

`DECISIÓN DE MATEO (2026-09-24)` Se mantienen las credenciales actuales por ahora.
La pregunta **no se cierra**.

`ACCIÓN` **Rotar antes de cargar datos reales o de conectar a Supabase en serio.**
En *Project Settings → Database → Reset database password*.

**Por qué es aceptable esperar.** El proyecto Supabase está vacío: no hay esquema,
no hay datos y nada de VERITAI se conecta a él. Lo único expuesto hoy es una base
de datos sin contenido. El riesgo pasa a ser real en el momento en que entre el
primer dato del corpus, que es trabajo manual irrecuperable.

**Por qué sigue abierta.** Quien tenga esa cadena puede crear objetos en el
proyecto, consumir cuota y dejar cosas dentro. Mientras no se rote, esto no es
"pendiente": es una puerta abierta que alguien conoce.

No se ha escrito ninguna credencial en ningún archivo del repositorio, ni el
`project-ref`. Cuando llegue el momento van al `.env`, que está en `.gitignore`.

`NOTA` La `publishable key` (`sb_publishable_...`) **sí es pública por diseño** y
no hace falta rotarla. Pero solo es segura si hay RLS: sin políticas, esa clave
equivale a un `SELECT *` sobre cada tabla expuesta. Es exactamente el motivo de
DEC-004.

### P-12 · ¿Reabrir las clases 6 y 7?

**Estado:** abierto, **decisión aplazada al lote crudo** · **Origen:** AUDIT-PILOT-20 §6

`DECISIÓN DE MATEO (2026-09-25)` No se reabre todavía. La decisión se toma
sobre el lote **crudo**, no sobre este, que está sesgado: reabrir clases con
datos contaminados repite el error D1.

**Desglose de los 5 `other_observed`**, que Mateo pidió antes de decidir nada.
La cifra "5 de 20" mezclaba dos cosas:

| Caso | Por qué es `other_observed` | En alcance |
|---|---|---|
| P08 | **DEC-013** (paper en inglés). Su clase real es `4_denominator` | no |
| P09 | **DEC-013**. Su clase real es `3_absolute_vs_relative` + clase 6 | no |
| P05 | Clase 7: cifra real atribuida al año equivocado | sí |
| P07 | Clase 7: numerador y denominador de ámbitos geográficos distintos | sí |
| P17 | **Ni 6 ni 7.** Agregación que oculta subgrupos en sentido contrario. El Excel ya lo marcaba como "futura ampliación de la taxonomía" | sí |

El dato real: **3 de 18 en alcance** tienen una clase fuera de la tesis, y de
esos, solo 2 son clase 7. P17 es un tipo nuevo. Con esto se compara el lote
crudo cuando exista.

`RESULTADO TAREA 2 (2026-09-25)` En el lote crudo, `other_observed` es la
clase primaria de **5 de 12** divergencias (C03, C05, C08, C10, C13). Tres de
ellas llevan una clase de la tesis como secundaria (C03 → baseline, C08 →
ranking). El patrón que más se repite fuera de la taxonomía es **la revisión
de la base de comparación** (C18, C29: el emisor revisa la serie y la prensa
compara contra la edición publicada). Está en
`research/COLECCION-LOTE-CRUDO.md` §4. La decisión sigue siendo de Mateo.

### P-15 · La clase canónica aparece 1 vez en 20

**Estado:** abierto · **Bloquea:** el objeto de estudio · **Decide:** Mateo, tras la TAREA 2

**Registrado antes de la TAREA 2, a propósito.**

`1_ranking_vs_value` es la clase que da nombre al proyecto: *"España cae 16
puestos"* con la puntuación intacta. Toda la tesis descansa en ella. En el lote
auditado aparece **una vez** (P01), y ese único caso está en `NEEDS_REVIEW`
porque el claim cubre cuatro índices y el corpus documenta uno.

```
2_baseline_selection     4
3_absolute_vs_relative   3
1_ranking_vs_value       1     <- la canonica
```

**Si en el lote crudo sigue siendo marginal, hay que replantear el objeto de
estudio.** Opciones que se abrirían entonces, sin decidir ninguna ahora:

```
A   La tesis se reencuadra sobre la clase mas frecuente (baseline o
    absoluto/relativo) y ranking_vs_value pasa a ser un caso ilustrativo.
B   El lote crudo se recolecta con cuota minima de ranking_vs_value,
    declarando el sesgo de muestreo.
C   Se mantiene el objeto y se acepta que el corpus sera pequeno para
    la clase principal, con la limitacion escrita.
```

Que quede escrito ahora: si la TAREA 2 devuelve 0 o 1 casos de la clase
canónica, no es un detalle del corpus, es una pregunta sobre la tesis.

`RESULTADO TAREA 2 (2026-09-25)` **1 en 12.** De las 12 divergencias del lote
crudo (31 trabajados), `1_ranking_vs_value` es la clase primaria de **una**
(C07, el FMI: del puesto 12 al 14 con el PIB en dólares +9,84%) y secundaria de
otra (C08). El resto: `other_observed` 5, `2_baseline_selection` 3,
`3_absolute_vs_relative` 2, `4_denominator` 1. Dos lotes independientes dicen lo
mismo. Muestreo neutral, sin cuota por clase, así que el dato no está
dirigido. Las opciones A, B y C siguen sobre la mesa; ahora con datos.

### P-16 · Qué denominador gobierna la puerta

**Estado:** abierto · **Bloquea:** la TAREA 3 · **Decide:** Mateo · **Origen:** COLECCION-LOTE-CRUDO §3

La composición del lote por cubetas (7 negativos + 6 divergencias, todos con
edición anterior; 3 + 2 sin ella) **fija la métrica del lote antes de trabajar
un solo caso**: ~71% por construcción. La tasa natural sobre los 31 admitidos
(80,6%) es la que dice cuánto encuentra un sistema partiendo de contenido
crudo. Las dos están calculadas; ninguna se ha usado para decidir.

```
A   La puerta se mide sobre TODOS los admitidos (tasa natural). Las cubetas
    quedan para la composicion del corpus, no para la metrica.        <- recomendada
B   La puerta se mide sobre el lote de 20/21, aceptando que la cuota
    condiciona el numero, y se declara.
C   Las dos, con la natural como principal y la del lote como sensibilidad.
```

Si se elige A o C, hay que reescribir la frase de la métrica en `ESTADO.md`,
`GLOSARIO.md` y `research/README.md`, que hoy dicen "del lote crudo (20)".

### P-17 · ¿Probar `curl` tras un fallo del fetcher es evasión?

**Estado:** abierto · **Bloquea:** el valor exacto de la métrica · **Decide:** Mateo · **Origen:** COLECCION-LOTE-CRUDO §6

DEC-018 prohíbe falsificar user-agent, saltar Cloudflare y raspar a quien
bloquea. Durante la TAREA 2, tras un fallo del fetcher, se probó una vez con
`curl` y su UA por defecto — sin falsificar nada, pero **cambiando de cliente**
tras una negativa. Cuatro dominios volvieron a bloquear. Dos respondieron 200:
`gob.pe` tras un **418** explícito al fetcher (C30, C31) y el ministerio de
Educación tras un `socket hang up` (C21, error de red).

```
A   Un rechazo explicito (403/406/418) al primer cliente cierra el caso.
    Un error de red (ECONNREFUSED, hang up) permite un reintento.
    -> C30 y C31 pasan a bloqueado_por_publicador; tasa natural 23/31 = 74,2%
B   Un segundo cliente honesto no es evasion; lo que se prohibe es mentir.
    -> se queda como esta: 25/31 = 80,6%
```

Las dos cifras están en el informe. La regla que salga va a `GLOSARIO.md` y a
`CLAUDE.md` cuando se fusione.

### P-18 · Formato hostil: 0 de 2

**Estado:** abierto · **Decide:** Mateo · **Origen:** COLECCION-LOTE-CRUDO §2

El pool de 38 se agotó sin un solo PDF escaneado o sin texto. Los 16 casos con
vía `pdf` se extrajeron sin OCR, incluidos los de nivel 5. El fallo de nivel 5
tomó otra forma: **no hay documento** (C22, C24, C27).

```
A   Aceptar el deficit y declararlo: en este pool el formato hostil no
    aparecio, y eso es un dato.                                      <- recomendada
B   Segunda pasada de busqueda dirigida a emisores donde vive el formato
    hostil (ayuntamientos, gobiernos provinciales, organismos pequenos),
    declarando que esa parte del lote NO es muestreo neutral.
```

B cuesta una sesión y toca `lote_crudo.py`; no cambia la métrica del agente
salvo que aparezcan casos sin edición anterior.

### P-05 · Segundo anotador

**Estado:** abierto desde el paquete · **Bloquea:** cerrar el corpus (Puerta 3)

Sin un segundo anotador sobre el 20–25% del corpus no hay kappa entre anotadores
y el corpus es metodológicamente más débil. `00b-DECISIONES-MATEO` ya fija el
plan B: declararlo como limitación y seguir.

No bloquea el piloto.

### P-06 · Plantilla de titulación de la UDLA

**Estado:** existe, pendiente de entregar · **Bloquea:** la redacción, no el código

### P-07 · Nombre definitivo

**Estado:** aplazado por decisión · **Bloquea:** invertir en marca

"VeritAI" está en uso por varias empresas. Alternativas ya evaluadas: Cotejo,
Fuente Cero, Ancla, Contexta, Primaria. No condiciona ninguna decisión técnica.

### P-08 · Tutor

**Estado:** no existe · **Riesgo aceptado**

Se arranca sin validación previa, asumiendo posible retrabajo. La mitigación de
bajo coste que propone `00b` sigue sin hacerse: enviar **una página** con el
alcance y la pregunta *"¿es un alcance aceptable para titulación?"*.

No bloquea nada. Evita rehacer.

---

## Cerradas

| # | Pregunta | Decisión | Fecha |
|---|---|---|---|
| P-01 | Remoto de git y pull requests | **En pausa.** Se trabaja en local con ramas. Nada se sube a ningún servidor | 2026-09-24 |
| P-03 | ¿Entran P08 y P09 en el alcance de tesis? | **Salen del corpus.** Se registran como `other_observed` y pasan a trabajo futuro. Ver DEC-013 | 2026-09-24 |
| P-04 | ¿Quién cronometra `minutes_to_locate`? | **Claude**, declarado como recuperabilidad-por-agente. Mateo cronometra 5 casos a mano como contraste humano. Ver DEC-014 | 2026-09-24 |
| P-10 | ¿`METRIC_AMBIGUOUS` entra en el enum de abstención? | **Sí.** 1 de cada 5 casos. El enum describe la realidad observada. Ver DEC-015 | 2026-09-25 |
| P-11 | ¿Separar en `clase` el control negativo del "falso sin divergencia"? | **No.** `truth` y `context` son ejes independientes; con ambos poblados el FPR es medible. P15 corregido a `no_divergence_detected`. Ver DEC-016 | 2026-09-25 |
| P-13 | ¿Cómo se corrigen los errores del Excel? | **El CSV es la fuente de verdad.** El Excel queda congelado con sus 4 errores: son un hallazgo. Ver DEC-017 | 2026-09-25 |
| P-14 | ¿Qué hace VERITAI con los publicadores que bloquean fetchers? | **No se evaden protecciones anti-bot. Nunca.** API → dataset → HTML → bloqueado = no recuperable. Ver DEC-018 | 2026-09-25 |
| — | Geografía del lote nuevo (D2 de la adenda) | **Opción A**: español en general, sin cuota geográfica. Cerrada en `00b` | antes del 2026-09-08 |
| — | ¿Framework en el panel web? | **No.** TypeScript vanilla, por coherencia con el stack cerrado en R02 §5. Ver DEC-008 | 2026-09-08 |
| — | ¿Alembic o runner propio? | **Runner propio**, por portabilidad a `supabase db push`. Ver DEC-006 | 2026-09-08 |
| — | ¿Qué hacer con el puerto 5432 ocupado? | **Puerto 55432 en el host.** No se apaga el Postgres de la máquina. Ver DEC-007 | 2026-09-08 |
| — | ¿Activar pgvector ya? | **No.** La imagen lo trae; la extensión espera a los *embeddings*. Ver DEC-010 | 2026-09-08 |
| — | ¿Montar el `/docs` completo del §26? | **No.** Solo el registro vivo. Ver DEC-012 | 2026-09-11 |
| — | ¿Rama de documentación sobre la de Docker? | **No.** Rama independiente desde `main`: son cambios distintos y se revisan aparte | 2026-09-24 |

---

## Contradicciones detectadas entre documentos

No son preguntas: son cosas que ya se resolvieron por jerarquía. Se registran
para que nadie las "descubra" otra vez.

**1. `00-LEER-PRIMERO.md` no existe.** Su contenido es
`07-ADENDA-CORRECCIONES-PILOTO.md`, cuyo encabezado dice *"Añadir como archivo
`00-LEER-PRIMERO.md`"*. Conviene renombrarlo para que el orden del paquete sea
el real.

**2. `02-1-VeritAI-TESIS.md` está parcialmente superado** por R02 y por `00b`:

| Dice la tesis | Vigente |
|---|---|
| Cronograma de 16 semanas | Puertas 1–4, sin fecha |
| "Español latinoamericano" | Español en general (Opción A) |
| Corpus de 300–500 publicaciones | Manda primero el piloto de 40 |
| Modelo de confianza con lógica subjetiva | `subjective_logic_tesis: false`. Abstención dura con razón explícita |
| LLM vía API con salida estructurada | Local-first, presupuesto API ~$0 |

**Jerarquía aplicada:** `00b` + R02 > START-HERE > TESIS.

**3. `START-HERE` §10 pide casos de Ecuador/Latinoamérica** en el lote nuevo.
`00b` elimina la cuota geográfica. Gana `00b`.
