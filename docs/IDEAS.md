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
