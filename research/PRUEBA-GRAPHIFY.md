# Prueba de graphify — herramienta evaluada y descartada

**Fecha:** 2026-09-30 · **Decide el descarte:** Mateo · **Material para:** sección
de metodología de la tesis, "herramientas evaluadas y descartadas".
**Idea:** I-004 en `docs/IDEAS.md` (cerrada). No es una DEC: es una
herramienta, no el objeto de estudio.

## Condiciones de la prueba

- Todo ocurrió en un clon aparte, `VERITAI-GRAFO`, carpeta hermana del repo,
  en la rama `feat/puerta-3-recoleccion`, commit `18afba2`. El repo original
  no se tocó.
- Paquete: `graphifyy` (doble ye) de PyPI, instalado con `uv tool install`.
  `uv` no existía en la máquina; se instaló con autorización de Mateo
  (`pip install --user uv`, 0.12.21) y se conserva.
- Versión probada: **graphify 0.9.73**.
- Sin `--strict`, sin `graphify hook install`, sin `graphify claude install`.
- Solo el grafo de código (`--code-only`), sin llamadas a ningún modelo. El
  grafo de documentos y de PDF no se construyó.

## Instalación en el proyecto: `graphify install --project`

Escribió, dentro del clon y **fuera de `graphify-out/`**:

| Fichero | Qué es |
|---|---|
| `.claude/settings.json` | nuevo. Dos hooks `PreToolUse`: `graphify hook-guard search` sobre **Bash y Grep**, y `graphify hook-guard read` sobre **Read y Glob**. Intercepta cada lectura y cada búsqueda del agente |
| `.claude/CLAUDE.md` | nuevo, disparador `/graphify` |
| `.claude/skills/graphify/SKILL.md`, `.graphify_version` y 8 ficheros en `references/` | la skill |
| **`CLAUDE.md` del proyecto** | **modificado**: añadió al final una sección `## graphify` con reglas del tipo "para preguntas sobre el código, ejecuta primero `graphify query`" y "tras modificar código, ejecuta `graphify update .`". La salida lo anunció como "graphify section written", **no como modificación de un fichero existente** |

Nada en `.git/hooks`. Fuera del clon, solo lo propio de `uv tool`: los
ejecutables `graphify` y `graphify-mcp` en `~/.local/bin` y una caché en
`~/.cache/graphify`.

## Grafo de código

`graphify extract . --code-only`: **707 nodos, 1947 aristas, 37
comunidades, 19 segundos**, 180 ficheros de código. Saltó 93 ficheros
no-código (80 docs, 13 PDF), como se pidió. Avisos: los 5 `.sql` de
`db/migrations/` aportaron cero por faltar el extra `graphifyy[sql]`;
`pyproject.toml` produjo cero nodos; PDF saltados por faltar `pypdf`.

**Reparto de aristas por confianza** (leído de `graphify-out/graph.json`):

| Confianza | Aristas | Tipos |
|---|---|---|
| EXTRACTED | 1697 | `calls`, `contains`, `imports`, `imports_from`, `references`, `rationale_for`, `method`, `inherits`, `defines` |
| INFERRED | 250 | `uses` (242), `indirect_call` (7), `calls` (1) |

Todas las aristas llevan `_origin: ast`; la etiqueta INFERRED va en el campo
`confidence`.

## Las tres consultas

Ninguna salida de `query` muestra aristas, solo nodos: no se puede saber
qué aristas cruzó cada expansión ni si fueron INFERRED. La expansión es BFS
a 2 saltos desde nodos semilla elegidos por coincidencia léxica.

### 1. `graphify query "qué conecta el test de base revisada con el mapa de operaciones del INE"`

- **Salida:** 12 semillas (`base_revisada.py`, `mapa_anexos.py`,
  `test_edicion_anterior.py`, `test_el_mapa_cubre_ocho_operaciones_y_se_cierra_ahi()`,
  pero también `config.py` y `scripts/migrate.py`); 313 nodos encontrados,
  67 mostrados por presupuesto de ~2000 tokens, con aviso de que la
  respuesta "puede estar entre los 246 recortados". Entre los mostrados,
  `logging`, `pathlib`, `json`, `session.py`.
- **A mano:** `base_revisada.py` no importa el mapa. Quien los une es
  `infrastructure/ine/edicion_anterior.py`, que importa `mapa_anexos` y
  `base_revisada`; `application/analizar_claim.py` orquesta. Dos líneas de
  `grep`.
- **Veredicto: peor.** La arista existía en el grafo, pero quedó enterrada
  entre 313 nodos y truncada.

### 2. `graphify query "dónde se aplica la regla de raw_value_span"`

- **Salida:** semillas `regla_de_tres()` (arnés), `aplicar()`
  (`reconstruir_descubrimiento.py`), `aplicar_2b()`, `test_config.py` y
  `test_todo_numero_de_la_evidencia_lleva_span()`; 222 nodos, 68
  mostrados. Solo la última semilla es pertinente; tres entraron por las
  palabras "regla" o "aplicar".
- **A mano:** `grep raw_value_span` da 24 líneas: campo obligatorio en
  `domain/evidencia.py`, `numeros_usados` en `veredicto.py`, `NumeroUsado`
  en `plantilla.py`, el conector `edicion_anterior.py`, `proveedor.py`, el
  `repositorio.py` y el test que hace la regla automatizable,
  `tests/test_trazabilidad.py`.
- **Veredicto: peor.** Acierta el test como semilla; el resto es ruido por
  coincidencia léxica.

### 3. `graphify path "analisis" "senales"`

- **Salida:** `No directed path found between 'analisis' and 'senales'`.
  Con `--undirected` (no pedido, probado para entender): 4 saltos,
  `analisis.py → claim.py → dataclasses ← metricas.py → senales_de()`, todo
  EXTRACTED. Los une el módulo estándar `dataclasses`.
- **A mano:** `senales` es un campo de `ResultadoTest`; lo escribe
  `domain/tests/comparacion_base.py` (`SENAL_HORIZONTE`, DEC-029) y lo lee
  `domain/plantilla.py` línea 108 para el veredicto que devuelve
  `api/routes/analisis.py`. Un atributo no tiene nodo propio en el grafo; el
  único nodo "senales" es `senales_de()` del arnés.
- **Veredicto: peor.** Sin camino dirigido; el no dirigido no significa
  nada.

## Razón del descarte

1. **Calidad.** En un código de 180 ficheros, `grep` y leer los imports
   responden mejor las tres preguntas y con menos texto. La expansión a 2
   saltos sin filtrar pone `logging` y `dataclasses` al mismo nivel que
   `edicion_anterior.py`, y el presupuesto de tokens trunca justo donde
   está la respuesta.
2. **Intrusión.** `install --project` modifica `CLAUDE.md` sin declararlo
   como modificación e instala hooks que interceptan cada Read, Grep, Glob y
   Bash del agente. Va contra las reglas de trabajo del proyecto
   (`CLAUDE.md` es propuesta que aprueba Mateo; contexto antes de código).
3. **Trazabilidad.** Las respuestas no muestran las aristas que usan, así
   que no se puede auditar si una relación es extraída o inferida.
   250 aristas del grafo son INFERRED.

**No probado:** el grafo de documentos, que sí gasta modelo, para las
decisiones y bitácoras cruzadas. Es el único uso donde podría aportar, y
queda sin medir.

## Desmontaje (2026-09-30)

Carpeta `VERITAI-GRAFO` borrada; `uv tool uninstall graphifyy`; `uv` se
conserva. Comprobado: sin hooks de graphify en ningún sitio, `~/.cache/graphify`
eliminada, y `git status` del repo original solo con `AGENTS.md` sin
versionar. Detalle en `docs/BITACORA.md`.
