# Preguntas abiertas

Lo que está sin resolver, quién lo decide, y qué bloquea.

> Cuando una pregunta se cierra **no se borra**: se mueve a la sección "Cerradas"
> con la decisión y la fecha. Saber qué se descartó vale tanto como saber qué se
> eligió.

**Última actualización:** 2026-09-24

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

### P-10 · ¿Extender el enum de abstención con `METRIC_AMBIGUOUS`?

**Estado:** abierto · **Bloquea:** el esquema del lote crudo (TAREA 2) · **Origen:** AUDIT-PILOT-20 §6

Cuatro de veinte casos (P02, P14, P15, P19) abstienen por la misma razón: el
claim no dice qué métrica usa —*¿valor o volumen?, ¿euros o % PIB?, ¿tasa o
número?, ¿"líder" en qué?*— y el veredicto cambia según cuál se elija. Hoy se
mapea a `SOURCE_VERSION_AMBIGUOUS`, que significa otra cosa.

R02 §11 dice que los motivos reales de abstención se descubren en el piloto.
Este se ha descubierto. Uno de cada cinco casos.

Otros tres candidatos con un caso cada uno: `SCOPE_NOT_RESOLVABLE` (P07),
`GROUPS_NOT_HOMOGENEOUS` (P17), `SAMPLE_NOT_REPRESENTATIVE` (P18). Con n=1 no
justifican entrar todavía.

### P-11 · ¿Separar en `clase` el control negativo del "falso sin divergencia"?

**Estado:** abierto · **Bloquea:** el esquema del lote crudo · **Origen:** AUDIT-PILOT-20 §7

`clase = none` hoy significa dos cosas: "el claim está bien enmarcado" (P20,
control negativo) y "el claim es falso por aritmética, no hay divergencia
contextual que evaluar" (P15, P16). Para medir la tasa de falsos positivos hay
que poder contarlas por separado.

### P-12 · ¿Reabrir las clases 6 y 7?

**Estado:** abierto · **Bloquea:** la selección de clases tras el piloto · **Origen:** AUDIT-PILOT-20 §6

La adenda (D4) dejó las clases 6 (correlación/causalidad) y 7 (cifra real,
marco falso) fuera de la tesis, registrándolas como `other_observed`, y dijo
que *"la frecuencia con que aparezcan decidirá si vale la pena reabrir esa
decisión"*. En el lote auditado, `other_observed` es **la categoría más
frecuente: 5 de 20**. Y `1_ranking_vs_value`, la canónica, aparece una vez.

No es una recomendación de reabrir. Es el dato que la adenda pidió. La decisión
se toma con el lote crudo delante, no antes.

### P-13 · ¿Cómo se corrigen los errores del Excel?

**Estado:** abierto · **Bloquea:** los tests de regresión sobre los 20 · **Origen:** AUDIT-PILOT-20 §4

Cuatro errores de transcripción confirmados: P03 (+5,03% → +5,30%), P11 (8.830
es S.L., el total es 8.908), P12 (las cifras no están en la primaria citada) y
P13 (Dato B sin fuente). El Excel es el dato de partida y esta auditoría no lo
toca. Opciones:

```
A   Una v2 del Excel con las correcciones, conservando la v1.
B   El CSV normalizado pasa a ser la fuente de verdad y el Excel
    queda como registro histórico.
```

B es más limpio para los tests, porque el CSV ya tiene enums cerrados. A
conserva el formato que Mateo conoce.

### P-14 · ¿Qué hace VERITAI con los publicadores que bloquean fetchers?

**Estado:** abierto · **Bloquea:** el diseño del primer conector · **Origen:** AUDIT-PILOT-20 §5.1

Newtral (8 de 8), `interior.gob.es` (Cloudflare), NEJM y ScienceDirect
devuelven 403 a un agente y 200 a un navegador. R02 §6.3 ya pedía respetar
`robots.txt` y los términos de uso. Hay que decidir la política antes de
escribir el primer conector: ¿se registra como `PRIMARY_SOURCE_NOT_FOUND` con
un subtipo, se intenta con un User-Agent identificable de VERITAI, o se
descarta el emisor como candidato?

Y para el lote crudo, registrar por separado `alcanzable_por_humano` y
`alcanzable_por_agente`: son la razón concreta de que las dos recuperabilidades
de DEC-014 sean números distintos.

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
