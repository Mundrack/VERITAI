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

### P-12 · ¿Reabrir las clases 6 y 7? — CERRADA (DEC-027)

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

`2026-09-25` **Mateo la revisa antes de abrir la Puerta 2**: es el grupo más
grande y no se sabía qué había dentro. Dos correcciones suyas antes del
desglose:

1. **P08 y P09 estaban contados** en los "10 de 28" aunque están fuera de
   alcance por DEC-013. Contando solo divergencias **en alcance**: `other_observed`
   es **8 de 26** (30,8%). Las proporciones de FINDINGS §5 y del encuadre se
   recalcularon con ese denominador (`pilot40.py`, tabla 5b).
2. **C03, C05, C08 y C13 son hermanos por criba** (de C02, C04, C07 y C12), no
   sorteos independientes. Sin hermanos: **4 de 21** (19,0%): P05, P07, P17,
   C10. La mitad del grupo es cobertura hermana de datos ya representados.

#### Desglose, uno por uno

Formato: qué dice el claim → mecanismo → qué le faltaría para entrar en una
clase existente o justificar una nueva. `[H]` = hermano por criba.

**P05 · CIS, clase media** — *"En 2018 se consideraban de clase media dos de
cada tres; hoy apenas uno de cada dos."* Mecanismo: **valor real atribuido al
periodo equivocado**: el ~66,7% existe, pero en 2019–2023, no en 2018; la caída
real abril 2018 → abril 2026 es de 1 pp, no de 16,7. Iría a **2a** si 2a se
define como "la base declarada no lleva el valor usado": el test es
`valor(primaria, año declarado) == valor del claim`, y necesita la edición de
2018 del barómetro (recuperable: serie del CIS). No hace falta clase nueva.

**P07 · Población reclusa "50% extranjera"** — Mecanismo: **ámbito del
numerador ≠ ámbito de la afirmación**: 53,0% es Cataluña, 32,7% es España; el
dato catalán se traslada al conjunto. Ya lleva `4_denominator` como
secundaria; con "denominador" definido como *población de referencia*, entra
en **4** como primaria. Necesita la estadística mensual de IIPP y la
autonómica (recuperables; la URL del Excel era una portada). No hace falta
clase nueva.

**P17 · Frontex "caída de hasta el 60% en todas las rutas"** — Mecanismo:
**cuantificador universal sobre un agregado con subgrupos en sentido
contrario**: Canarias −67,4%, Mediterráneo Occidental +17,0%, agregado −36,1%.
No es 1–5. Test computable: `para toda ruta, signo(cambio) == signo
afirmado`, con el fichero mensual de Frontex (recuperabilidad A). **Candidata
a clase nueva** ("agregación con subgrupos en sentido contrario"); hoy 1 de 26.
Se justifica solo si reaparece en el conjunto de evaluación.

**C03 `[H]` · Paro, "peor agosto en 7 años"** — hermano de C02. Mecanismo:
**elección de métrica** (flujo mensual vs nivel): las dos lecturas son ciertas
—+44.419 es la mayor subida de agosto desde 2019; 2.355.918 es el nivel más
bajo en agosto desde 2007— y el artículo omite la del propio SEPE. No es una
comparación incorrecta: es una lectura parcial. **No es clase**: es
enriquecimiento de contexto (mostrar la otra métrica del mismo emisor), no
divergencia. Si se quisiera test: "existe en la misma nota del emisor una
métrica de signo opuesto". Recomendación: `context = no_divergence_detected`
con lectura alternativa, o dejarlo en `other_observed` con la etiqueta
"lectura parcial", sin clase.

**C05 `[H]` · Inflación de Ecuador "la más baja de la región" + "Gobierno
protege el bolsillo"** — hermano de C04. Dos capas: (a) el superlativo
regional se sostiene en una imagen sin cifras ni fuentes →
`REQUIRED_SLOT_MISSING`, abstención, no clase; verificarlo exigiría la
primaria de cada país. (b) La atribución causal es **clase 6**
(correlación/causalidad), fuera de la tesis por `00b`; el sistema abstiene con
`UNSUPPORTED_CLAIM_TYPE`. **No es clase computable** en el objeto de la tesis.

**C08 `[H]` · FMI, "Sánchez hunde la economía al puesto 14"** — hermano de
C07. Mecanismo: el núcleo computable es **`1_ranking_vs_value`** (mismo dato
que C07: puesto 12 → 14 con PIB +9,84%), ya en secundaria; encima, atribución
causal y lenguaje evaluativo ("certifica el fracaso") que son clase 6/7. Si el
sistema etiqueta por el núcleo computable, C08 es clase 1 y la capa causal es
abstención `UNSUPPORTED_CLAIM_TYPE`. No se reetiqueta ahora: sería subir la
clase ilustrativa de 2 a 3 por decisión de etiquetado, no por dato nuevo.

**C10 · Ranking fiscal, "España cae al puesto 44"** — Mecanismo: **verbo de
cambio sin edición anterior**: es la primera edición del índice; no hay desde
dónde caer. Test computable: `existe edición anterior?` → no → la afirmación
de cambio no se sostiene (`PREVIOUS_EDITION_NOT_FOUND` + truth mixed).
Encaja en la **familia 2** como subtipo candidato **2d "cambio afirmado sin
edición anterior"**, distinto de 2a (base mal elegida) y 2b (base revisada).
Hoy 1 de 26; la evidencia negativa ("no existe") es lo difícil de probar.

**C13 `[H]` · Informalidad en Colombia "llegó a 54,5%"** — hermano de C12.
Mecanismo: **dirección implícita contraria a la edición anterior**: "llegó a"
como contrapunto negativo sugiere subida; la serie del DANE baja seis julios
seguidos (54,8 → 54,5) y el trimestre móvil también. Test computable:
`dirección implícita vs signo(actual − anterior)`, con la edición anterior
(recuperable, A). Entra en **2a** si 2a incluye la comparación implícita con
el periodo anterior. Secundario: "50 de cada 100" redondea 54,5 hacia abajo
(magnitud, menor).

**Fuera de alcance (DEC-013), solo para constancia:** P08 es `4_denominator`
puro (104/127 con 905 embarazos sin seguimiento); P09 es
`3_absolute_vs_relative` + clase 6. Ambos sobre papers en inglés; no entran.

#### Lo que sale del desglose

```
en alcance (8)      a clase existente     candidata a clase nueva     no es clase
                    P05 -> 2a             P17  agregacion/subgrupos    C03  lectura parcial
                    P07 -> 4              C10  2d cambio sin edicion   C05  abstencion (slot / causal)
                    C13 -> 2a                  anterior (familia 2)
                    C08 -> 1 (nucleo)
```

Si Mateo acepta los tres encajes limpios (P05, P07, C13), `other_observed`
queda en 5 de 26 (P17, C03, C05, C08, C10); C08 es discutible. Ninguna
reetiqueta se hace hasta que lo decida: sería ajustar el corpus a la
hipótesis.

`DECISIÓN DE MATEO (2026-09-25, DEC-027)` Acepta los tres encajes limpios
(P05 → 2a, P07 → 4, C13 → 2a). C08 no se reetiqueta. C03 sale de
`other_observed` a `no_divergence_detected` con la lectura alternativa
registrada; C05 a abstención con los dos motivos. **P17 y C10 quedan como
candidatas: no se crean clases con n=1**; se deciden solo si reaparecen en
el conjunto de evaluación, con el criterio escrito en DEC-027 antes de ver
esos datos. Las clases 6 y 7 no se reabren: lo que quedaba dentro era, o
una clase existente mal nombrada, o abstención, o una candidata con n=1.

### P-20 · Cierre humano/agente

**Estado:** abierto, esperando datos · **Bloquea:** la ratificación de PILOT-DECISION · **Decide:** los datos, y Mateo

Los 5 casos manuales de Mateo (C04, C05, C11, C14, C22; DEC-014) llenan
FINDINGS §7. Al llegar: acuerdo por caso en `previous_edition_found`, razón
de tiempos humano/agente, y si C22 (el único no recuperado por el agente) lo
encuentra una persona. Si contradicen la lectura del agente, `PILOT-DECISION`
se reabre y queda constancia. El agente no mira ese CSV antes.

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
| P-16 | ¿Qué denominador gobierna la puerta? | **La tasa natural sobre todos los admitidos** (31), "la que menos manipulación tiene". La del lote por cubetas se reporta al lado. La TAREA 3 la desagrega por tipo de publicador y vía de descubrimiento. Ver DEC-020 | 2026-09-25 |
| P-17 | ¿Probar `curl` tras un fallo del fetcher es evasión? | **Un 403/406/418 al primer cliente cierra el caso** aunque otro cliente pase. C30 y C31 pasan a bloqueados; decide la conservadora **23/31 = 74,2%**, la leniente (80,6%) se reporta. Ver DEC-021 | 2026-09-25 |
| P-18 | Formato hostil 0 de 2 | **Se acepta el déficit como hallazgo**: buscando sin sesgo no aparecieron PDFs sin texto. Sin segunda pasada dirigida. Ver DEC-022 | 2026-09-25 |
| P-19 | ¿Se declara el alcance del sistema en publicadores de nivel 1? | **Sí.** Alcance declarado a nivel 1; niveles 3–5 como limitación escrita con su 58,3%. Emisores: INE, FMI, Interior. Ver DEC-024 | 2026-09-25 |
| — | ¿`PILOT_GO`? | **Ratificado por Mateo.** Puerta 1 cerrada; la Puerta 2 no arranca hasta cerrar P-15. Ver DEC-023 | 2026-09-25 |
| P-15 | La clase canónica aparece 1 vez en 20 (y 1 en 12) | **Reencuadre E / B / A, C subtipo 2b.** Objeto general: divergencia contextual computable; primera familia: comparación de base (2a, 2b, 2c); ranking ilustrativo. Título, hipótesis, objetivos y alcance en `TESIS-ENCUADRE.md`. Sin caso canónico: par C18 + C29. Ver DEC-026 | 2026-09-25 |
| P-12 | ¿Reabrir las clases 6 y 7? | **No.** Tras el desglose: P05 → 2a, P07 → 4, C13 → 2a; C03 → sin divergencia (lectura alternativa); C05 → abstención con dos motivos; C08 se queda; P17 y C10 candidatas con criterio de reaparición, sin clase con n=1. Ver DEC-027 | 2026-09-25 |
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
