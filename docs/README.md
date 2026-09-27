# Registro vivo de VERITAI

Aquí se guarda la información del proyecto **a medida que avanza**. No es la
documentación final de la tesis ni el aparato completo de `/docs` que pide el
START-HERE §26 — eso se monta después de `PILOT_GO`, porque montar el andamiaje
antes de saber si hay proyecto es gastar semanas en nada (adenda, D6).

Esto es otra cosa: el sitio donde no se pierde lo que ya se sabe.

---

## Qué es cada documento

| Documento | Qué guarda | Cuándo se actualiza |
|---|---|---|
| [`ESTADO.md`](ESTADO.md) | Foto del proyecto **hoy**: puerta activa, qué funciona, qué falta | Se **sobrescribe** al final de cada sesión |
| [`TESIS-ENCUADRE.md`](TESIS-ENCUADRE.md) | Encuadre **vigente** de la tesis tras el piloto: título, pregunta, hipótesis, objetivos, definición operacional, alcance, taxonomía. Manda sobre el `02` | Solo por decisión de Mateo (DEC-026 y siguientes) |
| [`BITACORA.md`](BITACORA.md) | Qué se hizo cada día, con sus verificaciones | Se **añade** una entrada por sesión. Nunca se borra nada |
| [`DECISIONES.md`](DECISIONES.md) | Cada decisión técnica, con la alternativa que se descartó y por qué | Se **añade** una entrada por decisión. Nunca se edita una pasada |
| [`ARQUITECTURA.md`](ARQUITECTURA.md) | Qué existe hoy y cómo encaja | Cuando cambia la estructura real, no cuando se planea |
| [`GLOSARIO.md`](GLOSARIO.md) | Vocabulario del proyecto y **enums cerrados** | Cuando aparece un término nuevo o se cierra un enum |
| [`PREGUNTAS-ABIERTAS.md`](PREGUNTAS-ABIERTAS.md) | Lo que está sin resolver y quién lo decide | Al abrir o cerrar una pregunta |
| [`SEGURIDAD.md`](SEGURIDAD.md) | Controles de seguridad **ya implementados**, no los planeados | Cuando se implementa o se rompe un control |
| [`../research/README.md`](../research/README.md) | Estado del piloto (Puerta 1) y material de la Puerta 2: casos, ejecutor, informe | Cuando avanza el piloto o una puerta |
| [`TESIS/`](TESIS/README.md) | Esqueleto del documento de tesis (formato UDLA, 11 secciones): solo estructura y qué material del repo alimenta cada sección. **Nada redactado** | Cuando Mateo lo pida; nombres `NEEDS_REVIEW` hasta cotejar la plantilla (P-06) |

---

## Las tres reglas que hacen que esto sirva

**1. `BITACORA.md` y `DECISIONES.md` no se reescriben.** Solo se añade al final.
Una decisión que resultó equivocada no se borra: se añade otra que la revoca y
se explica qué la cambió. El tribunal va a preguntar por el camino, no solo por
el destino.

**2. `ESTADO.md` sí se reescribe entero.** Es una foto, no un historial. Si dice
algo que ya no es verdad, está roto.

**3. Aquí solo entra lo verificado.** Si algo no se comprobó, se escribe con la
marca `NEEDS_REVIEW` al lado. Nunca se rellena con algo plausible
(START-HERE §9, 06-PROMPT).

---

## Qué NO va aquí

- **Las decisiones cerradas del paquete.** Viven en `00b-DECISIONES-MATEO.md` y
  en `04-VERITAI-CLAUDE-RESPONSE-R02.md`, que son la fuente de verdad. Aquí solo
  se registran las decisiones **nuevas**, las que se toman construyendo.
- **Las reglas permanentes.** Están en `CLAUDE.md`, en la raíz.
- **Los resultados del piloto.** Van en `research/`, que es material de tesis.

---

## Orden de lectura si llegas nuevo

1. `../README.md` — qué es VERITAI y cómo levantarlo
2. `ESTADO.md` — dónde está el proyecto hoy
3. `../CLAUDE.md` — las reglas que no se negocian
4. `GLOSARIO.md` — el vocabulario, antes de leer nada técnico
5. `ARQUITECTURA.md` — qué hay construido
