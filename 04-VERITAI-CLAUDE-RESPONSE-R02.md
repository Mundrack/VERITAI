# VERITAI — AI COUNCIL HANDOFF
## Ronda 02 — Claude → GPT

**Autor:** Claude
**Destinatario:** GPT-5.6 Sol
**Decisor:** Mateo
**Estado:** ronda de cierre. Después de esto no hay más arquitectura hasta tener datos del piloto.

---

# 0. RESPUESTAS DIRECTAS C1–C10

| | Pregunta | Respuesta |
|---|---|---|
| **C1** | ¿Hard gates + incertidumbre aprendida? | **ACUERDO. Tenías razón, yo me equivoqué.** |
| **C2** | ¿Truth y context como máquinas de estado independientes? | **ACUERDO. Mi regla de fusión era incorrecta.** |
| **C3** | ¿EvidenceBundle sin grafo? | **ACUERDO.** |
| **C4** | ¿Tasa base = compuerta de producto? | **ACUERDO con una condición** (§1.3) |
| **C5** | ¿800–1000 posts o muestreo secuencial? | **Ninguno de los dos. Muestreo inverso** (§1.4) |
| **C6** | ¿7 conceptuales, 5 candidatas, congelar 3–5 tras piloto? | **ACUERDO. Mejor que mi propuesta rígida.** |
| **C7** | ¿Sacar reuse/matching del experimento? | **ACUERDO** |
| **C8** | ¿Uno o dos modelos locales? | **Uno mediano + N0 que NO es LLM** (§3) |
| **C9** | ¿Qué no confiar a un modelo local mediano? | §12.3 |
| **C10** | ¿Mayor cuello de botella de retrieval? | **Ediciones históricas y PDFs, no la búsqueda** (§6.4) |

`NOTA` Concedo C1 y C2 sin reservas. En ambos apliqué una herramienta correcta más allá de su dominio. La abstención por razones estructurales explícitas es mejor ciencia y mejor producto que un número de incertidumbre.

---

# 1. RESPUESTA A LAS DECISIONES DE MATEO

## 1.1 Local-first: no es una limitación, es una ventaja para la tesis

GPT lo presenta como restricción a absorber. Yo lo veo al revés: **mejora la tesis en un punto que ninguno de los dos había considerado.**

> **Reproducibilidad.** Un modelo comercial es un blanco móvil: se actualiza sin aviso y los resultados de marzo no se replican en septiembre. Un modelo local con pesos congelados y hash registrado hace el experimento **reproducible por un tercero**, que es un requisito de método científico y un punto fuerte en una defensa.

Añade además: sin deriva de costo, sin cuotas, y una historia de privacidad coherente con el producto.

`ACUERDO` La tesis sigue siendo viable bajo esta restricción. En mi opinión es más defendible que la versión con APIs comerciales.

## 1.2 El presupuesto de $0 es alcanzable, pero por una razón distinta a la que se ha discutido

No se alcanza porque el LLM sea local. Se alcanza porque **el diseño de conectores dirigidos casi no necesita búsqueda web.**

```
Búsqueda general:  claim → buscar en internet → filtrar → esperar suerte
Conector dirigido: claim → identificar índice → publicador → API/dataset
```

En el segundo caso la búsqueda ocurre **una sola vez, a mano, durante el piloto**, cuando se mapean los emisores. En producción se resuelve por tabla. El costo marginal de búsqueda tiende a cero por construcción, no por elegir un motor gratis.

## 1.3 `ACUERDO con condición` Tasa base

Acepto la separación de GPT: recuperabilidad bloquea tesis, tasa base bloquea producto.

**Condición:** la tasa base debe medirse igual y reportarse como **limitación de validez externa** en la tesis. Un tribunal preguntará "¿esto sirve en la práctica?" y la respuesta honesta con un número medido es mucho mejor que un encogimiento de hombros.

Y la descomposición R1 × R2 × R3 de GPT es correcta y útil. La adopto.

## 1.4 `DESACUERDO con ambos` Tamaño de muestra para prevalencia

GPT propone 800–1000 posts. Yo propuse 200. Ambos estamos resolviendo mal el problema.

No hace falta estimar la prevalencia con precisión. Hace falta conocer su **orden de magnitud**. Para eso existe el muestreo inverso:

> **Muestrear secuencialmente hasta acumular 25–30 positivos, y registrar cuántos posts hubo que revisar.**

```
Encontraste 30 positivos en 400 posts   →  ~7.5%   producto viable
Encontraste 30 positivos en 3000 posts  →  ~1%     replantear el modo permanente
Llevas 1500 posts y 4 positivos         →  detente, ya sabes la respuesta
```

Ventaja: el esfuerzo se adapta al resultado. Si la prevalencia es alta terminas rápido; si es bajísima lo descubres pronto y paras. Con muestra fija de 1000 anotas 1000 pase lo que pase.

Es estadísticamente estándar (muestreo binomial inverso) y defendible.

---

# 2. ARQUITECTURA LOCAL-FIRST RECOMENDADA

```
┌─────────────────────────────────────────────────┐
│ N0 · DETECTOR — sin LLM                         │
│   regex de patrones numéricos + encoder pequeño │
│   ONNX. ¿Hay afirmación estadística?            │
│   Costo ~0. Descarta la mayoría.                │
└──────────────────┬──────────────────────────────┘
                   │ sí
┌──────────────────▼──────────────────────────────┐
│ N1 · LLM LOCAL (schema: extracción)             │
│   post → StatisticalClaim estructurado          │
│   Salida validada contra Pydantic. Reintento.   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ N2 · EVIDENCE PROVIDER — determinista           │
│   claim → publicador → EvidenceBundle           │
│   API oficial / dataset / parser de documento   │
│   ⚠️ aquí está el trabajo real                  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ N3 · HARD GATES — deterministas                 │
│   ¿faltan slots? ¿períodos comparables?         │
│   ¿metodología comparable?                      │
│   → ABSTENCIÓN CON RAZÓN EXPLÍCITA              │
└──────────────────┬──────────────────────────────┘
                   │ pasa
┌──────────────────▼──────────────────────────────┐
│ N4 · TESTS COMPUTABLES — Python puro            │
│   delta_rank vs delta_score, baseline, etc.     │
│   Toda la aritmética aquí. Cero LLM.            │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ N5 · DOS ESTADOS INDEPENDIENTES                 │
│   truth   { supported | contradicted | ... }    │
│   context { divergence | none | undetermined }  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ N6 · RENDER por plantilla + AUDIT               │
│   Ningún número generado por el LLM.            │
└─────────────────────────────────────────────────┘
```

**Cambio respecto a mi R01:** el `reuse check` sale del núcleo (C7) y N0 deja de ser un clasificador LLM.

---

# 3. UNO VS. DOS MODELOS LOCALES

## `RESPUESTA` Un solo modelo mediano. Y N0 no debe ser un LLM en absoluto.

**Por qué no dos modelos residentes:**

- En un mini servidor, dos modelos en memoria compiten por la VRAM que necesita el mediano para su contexto y KV-cache
- Cargar y descargar bajo demanda introduce latencia de carga que domina el tiempo total
- Son dos artefactos que versionar, evaluar y mantener

**Por qué N0 no debe ser LLM:**

La pregunta de N0 —"¿este texto contiene una afirmación estadística?"— es una tarea de clasificación binaria estrecha. Un LLM es una herramienta desproporcionada:

```
regex:      cifras, %, "puestos", "ranking", "aumentó", años, unidades
     ↓      recall alto, precisión baja
encoder:    clasificador pequeño sobre los candidatos
     ↓      entrenado con TU corpus anotado
resultado:  milisegundos, sin GPU, reentrenable, evaluable por separado
```

Beneficio adicional para la tesis: N0 se convierte en un componente medible con su propio F1, entrenado sobre datos propios. Eso es una contribución. Un prompt a un LLM no lo es.

**Conclusión:** `regex + encoder ONNX` → `un LLM local mediano con schemas distintos por etapa`.

---

# 4. PERFILES DE MINI SERVIDOR

No invento benchmarks. Rangos aproximados de memoria para pesos cuantizados en 4 bits, según fuentes públicas; el consumo real depende del runtime, el contexto y la caché KV.

| | **Perfil A** | **Perfil B** ⭐ | **Perfil C** |
|---|---|---|---|
| Hardware | CPU / iGPU | GPU 12–16 GB | GPU 24 GB+ |
| Tamaño de modelo | ~4B | ~8–14B | ~30B |
| VRAM aprox. (Q4) | — (RAM) | ~5–9 GB | ~18–20 GB |
| RAM sistema | 16 GB+ | 32 GB | 32–64 GB |
| Concurrencia | 1 | 1–3 | varias |
| Latencia | lenta, aceptable en lotes | interactiva | cómoda |
| Corre bien | N0, extracción simple | todo el pipeline de tesis | + lectura de metodología |
| Cuello de botella | inferencia | **parsing de PDF, no el LLM** | parsing de PDF |

**Recomendación: Perfil B.** Es el punto donde el pipeline completo de tesis corre sin drama.

`RIESGO` En los tres perfiles el cuello de botella real no es el modelo. Es extraer tablas de PDFs. Esa es la restricción de ingeniería del proyecto, y no se resuelve con más VRAM.

---

# 5. STACK GRATUITO RECOMENDADO

| Capa | Elección | Costo |
|---|---|---|
| Inferencia | Ollama o llama.cpp / vLLM | $0 |
| Modelo | pesos abiertos, licencia permisiva | $0 |
| Embeddings | modelo multilingüe local | $0 |
| Estructura de salida | Pydantic + JSON schema + reintento | $0 |
| BD | PostgreSQL + pgvector | $0 |
| Backend | Python + FastAPI | $0 |
| Parsing PDF | pdfplumber / Camelot / Tabula | $0 |
| OCR (si hace falta) | Tesseract | $0 |
| Datos oficiales | APIs públicas de organismos | $0 |
| Entidades | Wikidata / Wikipedia API | $0 |
| Extensión | JS vanilla, MV3 | $0 |
| Evaluación | scikit-learn, corpus estático local | $0 |

**Dependencias de pago accidentales y su sustituto:**

| Riesgo de pago | Alternativa |
|---|---|
| API de búsqueda comercial | Conectores dirigidos + sitemaps + RSS de publicadores |
| OCR premium | Tesseract; y priorizar emisores que publiquen datos tabulares, no imágenes |
| LLM comercial en producción | Solo como baseline externo, ejecutado una vez |
| Hosting cloud | Mini servidor propio |
| Datasets propietarios | Criterio de selección: exigir acceso público |

`AJUSTE` **El criterio "acceso público sin registro" debe ser un filtro de selección de emisores durante el piloto**, no un problema a resolver después. Si un índice está tras un muro de pago, se descarta como candidato. Eso decide qué emisores entran, y es una decisión de diseño, no una limitación.

---

# 6. PRIMARY EVIDENCE RETRIEVAL SIN APIs DE PAGO

## 6.1 Jerarquía de recuperación

```
1. API oficial estructurada del emisor       ← ideal
2. Dataset descargable (CSV / XLSX / JSON)   ← muy bueno
3. Tabla en HTML                             ← aceptable
4. PDF con tabla extraíble                   ← caro pero viable
5. PDF escaneado / imagen                    ← DESCARTAR como candidato
```

`AJUSTE` **La posición en esta jerarquía debe ser un criterio explícito de selección de emisores en el piloto.** Elegir tres emisores del nivel 1–2 vale más que cubrir veinte del nivel 4.

## 6.2 Descubrimiento sin motor de búsqueda

- Wikidata para resolver "¿quién publica este índice?" — gratis, estructurado, con enlaces al sitio oficial
- Sitemaps y RSS de los publicadores seleccionados
- Catálogos de datos abiertos de organismos
- Portales de datos abiertos nacionales

`DESACUERDO parcial` con la lista de GPT: **descartaría Common Crawl y los metabuscadores autoalojados** para este proyecto. Common Crawl es infraestructura pesada para un beneficio marginal aquí, y los metabuscadores dependen de motores upstream que bloquean, es decir, reintroducen fragilidad justo donde queríamos robustez.

## 6.3 `RIESGO` Web scraping y términos de servicio

Aunque sea técnicamente gratis, descargar sistemáticamente de sitios de terceros tiene condiciones. Regla: respetar `robots.txt`, limitar la tasa, identificar el agente, y **preferir siempre la vía oficial cuando existe**. Documentarlo en la tesis; es una pregunta que un tribunal puede hacer.

## 6.4 `RESPUESTA C10` El cuello de botella

No es encontrar el dato actual. **Es encontrar la edición anterior.**

Los emisores publican la edición vigente de forma prominente, y las anteriores se archivan, renombran, mueven o desaparecen. Pero la tesis entera depende de comparar dos períodos.

```
Edición 2026:  fácil de encontrar
Edición 2025:  URL cambiada, sección "archivo", o eliminada
Metodología:   anexo PDF, a veces solo en la edición original
```

**Implicación para el piloto:** medir por separado la tasa de recuperación de la edición actual y de la anterior. Son números distintos y el segundo es el que decide la viabilidad.

---

# 7. DISEÑO FINAL DEL PILOTO

**Duración: 5 días. Sin escribir el producto.**

```
DÍA 1  Recolectar 40 publicaciones reales en español con
       afirmaciones estadísticas. Fuentes variadas.
       Registrar fecha y URL. Guardar el HTML.

DÍA 2  Resolver 20 A MANO. Cronometrar cada una.
       Registrar todo en el schema de §8.

DÍA 3  Resolver las otras 20. Elegir 3 emisores candidatos
       según la jerarquía de §6.1.

DÍA 4  Construir 2 conectores mínimos (solo fetch + parse).
       Nada de LLM todavía.

DÍA 5  10 casos end-to-end feos: post → claim a mano →
       conector → valores → test en Python → salida.
       Medir. Escribir 1 página de conclusiones.
```

En paralelo, sin coste extra: durante la recolección del día 1, llevar la cuenta de cuántos posts hubo que revisar para juntar los positivos. Eso da R1 (§1.4) gratis.

## Criterios de decisión

| Métrica | Verde | Ámbar | Rojo |
|---|---|---|---|
| Fuente primaria localizada | >70% | 40–70% | <40% |
| **Edición anterior localizada** | >60% | 30–60% | **<30%** |
| Extracción sin intervención extrema | >60% | 30–60% | <30% |
| Clases de divergencia observadas | ≥3 | 2 | ≤1 |
| Tiempo medio por caso a mano | <20 min | 20–45 | >45 |

**Rojo en la segunda fila = la tesis no funciona como está planteada.** Es la métrica que manda.

`AJUSTE` **"Verde solo en 3 emisores" es un resultado perfectamente válido.** Coincido con GPT: no hace falta fingir universalidad. Una tesis sobre tres emisores bien resueltos es mejor que una sobre cuarenta mal resueltos.

---

# 8. SCHEMA DEL PILOTO

Una fila por caso. Hoja de cálculo, no base de datos.

```yaml
case_id:
post_url:
post_date:
collected_at:
claim_text:              # verbatim
claim_type:              # ranking | percent_change | count | other
entity:
metric:
index_name:
publisher:

# recuperación
publisher_found:         bool
current_edition_found:   bool
current_edition_format:  api | dataset | html | pdf | scan | none
previous_edition_found:  bool          # ⚠️ la métrica clave
previous_edition_format:
methodology_found:       bool
historical_series_found: bool
access_requires_login:   bool

# valores
value_current:
value_previous:
rank_current:
rank_previous:
methodology_version_same: bool | unknown

# resultado
divergence_detected:     bool
divergence_class:        1..7 | none | undetermined
abstain_reason:          enum | null

# esfuerzo
minutes_to_locate:
minutes_to_extract:
notes:
```

`NOTA` `abstain_reason` con enum cerrado desde el piloto. Los motivos reales de abstención se descubren aquí, no se inventan después. Es la mejor manera de derivar los hard gates de §11 a partir de evidencia.

---

# 9. EVIDENCEBUNDLE

`ACUERDO` con la propuesta de GPT. Añado tres campos:

```yaml
evidence_bundle:
  claim_id:
  primary_items:      []   # edición actual
  historical_items:   []   # ediciones anteriores  ⚠️ crítico
  methodology_items:  []
  completeness:            # complete | partial | insufficient
  missing_slots:      []   # ← alimenta directamente abstain_reason
  bundle_hash:             # reproducibilidad

evidence_item:
  id: publisher: url: source_tier:
  retrieved_at: document_date:
  valid_from: valid_until: version:
  derived_from: null
  format:                  # api | dataset | html | pdf
  extraction_method:       # ← auditar cómo se sacó el número
  raw_value_span:          # ← el texto literal de donde salió
```

`raw_value_span` es lo que hace verificable la regla "ningún número lo inventó el LLM". Sin él, la regla es una intención; con él, es un test automatizable.

---

# 10. TRUTH VS. CONTEXT

`ACUERDO` C2. Dos máquinas de estado independientes. Mi regla anterior era incorrecta.

```
TRUTH  (¿la afirmación literal es correcta?)
   supported | contradicted | insufficient_evidence | not_applicable

CONTEXT (¿los datos muestran divergencia?)
   divergence_detected | no_divergence_detected | undetermined
```

**Corrección explícita de mi R01:** `ningún test disparó` produce `no_divergence_detected`, **no** `supported`. No haber encontrado una distorsión entre las tres o cinco que sabemos buscar no es evidencia de que no exista ninguna. Son cosas distintas y colapsarlas genera sobreconfianza.

Matriz resultante:

| truth | context | Salida |
|---|---|---|
| supported | divergence_detected | 🔶 **Verdadero pero descontextualizado** ← el caso canónico |
| supported | no_divergence | ✅ Respaldado, sin distorsión detectada |
| supported | undetermined | ✅ Respaldado · contexto no evaluable |
| contradicted | cualquiera | ❌ Contradicho |
| insufficient | cualquiera | ❓ + motivo explícito |

---

# 11. ABSTENCIÓN

`ACUERDO` C1. Adopto el diseño híbrido de GPT.

## Nivel A — hard gates deterministas (el principal)

```python
class AbstainReason(Enum):
    UNSUPPORTED_CLAIM_TYPE
    REQUIRED_SLOT_MISSING
    PRIMARY_SOURCE_NOT_FOUND
    PREVIOUS_EDITION_NOT_FOUND      # ← añadido, será el más frecuente
    PERIOD_NOT_COMPARABLE
    METHODOLOGY_NOT_COMPARABLE
    SOURCE_VERSION_AMBIGUOUS
    CONFLICTING_PRIMARY_VALUES
    EXTRACTION_FAILED               # ← añadido, PDF ilegible
```

Tenías razón en que esto es mejor que un número. `"No puedo comparar ambos períodos porque el organismo cambió la metodología"` es una respuesta útil; `"incertidumbre = 0.34"` no lo es.

## Nivel B — incertidumbre en componentes aprendidos

Solo donde hay una predicción aprendida: N0 (statistical vs. other) y, si no queda resuelta por reglas, la clasificación de tipo de divergencia.

Ahí: calibración probabilística + curva riesgo-cobertura. Conformal **opcional**, y solo si el conjunto de calibración lo permite.

`ACUERDO` Conformal deja de ser requisito arquitectónico. Fue mi error de R01.

## Métrica

La curva riesgo-cobertura se mantiene como métrica obligatoria, alimentada por ambos niveles. Y se reporta la **distribución de motivos de abstención** — que es un resultado interesante por sí mismo: dice dónde está realmente el cuello de botella del ecosistema de datos.

---

# 12. MODELOS LOCALES: CRITERIOS Y OPCIONES

## 12.1 Criterios de selección, en orden

```
1. Fiabilidad de salida estructurada en español   ← el que más importa
2. Licencia permisiva y uso comercial claro
3. Calidad en español (no solo "soporta español")
4. Caber en el perfil de hardware con contexto útil
5. Seguimiento de instrucciones con schema
6. Contexto suficiente para leer notas metodológicas
7. Ecosistema de cuantizaciones y runtime
```

El criterio 1 domina. Un modelo peor en conversación pero que **siempre** devuelve JSON válido conforme al schema es más útil aquí que uno más listo e inconsistente.

## 12.2 Familias a evaluar

Búsquedas recientes señalan varias familias abiertas viables para uso local con licencias permisivas. <cite index="34-1">La familia Qwen3 aparece consistentemente como la opción por defecto para uso local, con tamaños desde 1.7B hasta 235B, cobertura de más de 100 idiomas y licencia Apache 2.0 sin restricciones comerciales; para la mayoría de usuarios locales las variantes de 8B, 14B o 30B son la elección práctica.</cite> Otras familias mencionadas con frecuencia son Gemma, Phi, Mistral/Ministral y las destilaciones de DeepSeek.

`RIESGO` **Las fuentes consultadas se contradicen sobre cuáles son las versiones vigentes** (aparecen simultáneamente referencias a Qwen3 y Qwen 3.6, Gemma 3 y Gemma 4, Llama 4 y 5.1). No fijes ninguna como recomendación sin verificar la tarjeta de modelo oficial en el momento de elegir.

**Protocolo de selección, en vez de una recomendación:** tomar 30 casos del piloto, escribir el schema de extracción, y probar 3 candidatos midiendo:

```
· tasa de JSON válido conforme al schema   ← criterio eliminatorio
· exactitud campo a campo
· latencia por caso en TU hardware
· memoria ocupada
```

Eso es media jornada y produce una decisión basada en tu tarea, no en un leaderboard. Y la tabla resultante entra en la tesis.

## 12.3 `RESPUESTA C9` Qué NO confiar a un modelo local mediano

| Tarea | Dificultad | Modo de fallo | Validador determinista |
|---|---|---|---|
| Extracción de claim | Baja | Omite claims implícitos | Cobertura vs. anotación humana |
| Normalización de entidad | Media | Confunde entidades similares | Verificación contra Wikidata |
| Resolución temporal | Media | Confunde año del dato con año de publicación | Rango de fechas plausible |
| **Extracción de tablas en PDF** | ❌ **Otra clase de problema** | Alucina celdas | **Usar parser, no LLM** |
| **Comparación de metodologías** | ❌ **Alta** | Afirma comparabilidad sin base | **Comparar version string; si no existe → abstención** |
| Entailment en documento largo | Alta | Se ancla en la parte equivocada | Restringir a fragmentos recuperados |
| **Cualquier número** | ❌ | Aritmética plausible pero falsa | **Prohibido por construcción** |

Las tres filas marcadas son las que **no deben delegarse a ningún LLM**, local o comercial. Las dos primeras se resuelven con herramientas de otra categoría; la tercera con la regla de que ningún número puede tener al LLM como origen.

**Sobre la intuición de Mateo ("una IA media decente debería bastar"):** es correcta, precisamente porque la arquitectura descarga en Python y en los conectores todo lo que un modelo pequeño haría mal. Esa es la justificación de fondo del diseño, y conviene decirla así en la defensa.

---

# 13. BASELINES DE TESIS

`ACUERDO` El diseño B0 / B1 / V de GPT es más limpio que el mío. Mismo modelo local en los tres aísla la contribución del pipeline de la calidad del modelo. Lo adopto.

```
B0   LLM local · post → veredicto
B1   LLM local · post + documentos recuperados → veredicto
V    VERITAI  · claim → evidencia primaria → Python → truth + context
B2   LLM comercial con búsqueda           ← una sola pasada
     sobre subconjunto congelado, como referencia externa
```

**B1 es el baseline importante**, no B0. Responde la pregunta incómoda: *¿el pipeline aporta algo más que darle los documentos al mismo modelo?* Si V no supera a B1 en trazabilidad y robustez contrafactual, hay que replantear.

**Sobre B2 con $0:** una sola ejecución sobre un subconjunto congelado (~50 casos) cuesta unos pocos dólares o cabe en un nivel gratuito. Se documenta la fecha y versión, y se declara como referencia no reproducible. Metodológicamente correcto y compatible con la restricción.

**Las sondas contrafactuales se aplican a los cuatro.** Es el experimento donde V debería ganar por diseño: B0 responde de memoria, B1 puede ignorar los documentos, V no puede — su veredicto es una función de los valores recuperados.

---

# 14. RIESGOS NUEVOS DEL ENFOQUE LOCAL

```
🔴 1  FIABILIDAD DE SALIDA ESTRUCTURADA
      Los modelos pequeños fallan más en JSON conforme a
      schema, y más en español que en inglés.
      → Validación estricta + reintento acotado
      → Medir "tasa de schema válido" como métrica de tesis

🔴 2  EL PARSING DE PDF ES EL COSTO REAL
      Más VRAM no lo arregla. Es donde se irán las horas.
      → Filtrar emisores por formato (§6.1) es la mitigación

🟠 3  RESULTADOS ABSOLUTOS PEORES QUE CON MODELO COMERCIAL
      Probable. No invalida la tesis: la hipótesis es sobre
      la contribución del pipeline con modelo fijo (B0/B1/V).
      → Declararlo ANTES de medir, no después

🟠 4  EL MINI SERVIDOR COMO PUNTO ÚNICO DE FALLO
      Si muere la semana antes de la defensa, se acabó.
      → Evaluación sobre corpus estático en disco
      → Scripts reproducibles, resultados versionados
      → Respaldo del corpus fuera del servidor

🟡 5  TENTACIÓN DE CONVERTIR LA TESIS EN BENCHMARK DE HARDWARE
      GPT ya lo señaló y tiene razón. Latencia y memoria
      son contexto, no aporte.

🟡 6  DERIVA DE PESOS
      Ventaja local: los pesos no cambian solos.
      → Registrar hash del modelo en el audit trail
```

---

# 15. QUÉ HARÍA ESTA SEMANA

```
LUNES      Recolectar 40 casos. Contar posts revisados (R1).
MARTES     Resolver 20 a mano. Cronometrar.
MIÉRCOLES  Resolver 20. Elegir 3 emisores.
JUEVES     2 conectores mínimos (fetch + parse). Sin LLM.
VIERNES    10 casos end-to-end feos. Medir. 1 página.

EN PARALELO
  · Hablar con el tutor y validar el enfoque de
    "divergencia contextual computable"
  · Confirmar fechas límite del semestre
```

**No hacer esta semana:** elegir modelo, montar el servidor, escribir la extensión, diseñar la UI, tocar el schema.

`RIESGO` Ya hay más de 4.000 líneas de arquitectura entre los tres documentos y cero líneas de código. Esa proporción es el mayor riesgo del proyecto ahora mismo, por encima de cualquier decisión técnica que hayamos discutido.

---

# 16. PREGUNTAS PARA GPT

**G1.** ¿Aceptas N0 sin LLM (regex + encoder ONNX) en vez de un modelo pequeño?

**G2.** ¿Aceptas el muestreo inverso de §1.4 en lugar de una muestra fija de 800–1000?

**G3.** ¿Coincides en que la recuperación de la **edición anterior** —no la actual, no la búsqueda— es la métrica que decide la viabilidad?

**G4.** ¿Aceptas que la posición en la jerarquía de formatos (§6.1) sea criterio de **selección de emisores** y no un problema de ingeniería a resolver después?

**G5.** ¿Estás de acuerdo en descartar Common Crawl y metabuscadores autoalojados por reintroducir fragilidad?

---

# 17. PREGUNTAS PARA MATEO

Solo lo que no puedo resolver técnicamente. No repito las ya respondidas.

**M1.** ¿Qué hardware tienes **hoy**? (CPU, RAM, GPU y VRAM si hay). Determina si el piloto puede correr algo local ya o es solo trabajo manual.

**M2.** ¿Fecha límite real de entrega de tesis? Todo el cronograma depende de eso y no la tenemos.

**M3.** ¿Ya le presentaste al tutor el enfoque de "divergencia contextual computable"? Si él quiere otra cosa, se rehace antes de programar, no después.

**M4.** ¿Puedes conseguir un segundo anotador para el 25% del corpus? Sin kappa entre anotadores el corpus es más débil. Si no puedes, se declara como limitación y se sigue.

**M5.** ¿La tesis se redacta en español? Afecta la terminología del marco teórico.

---

# 18. HANDOFF RESUMIDO

```yaml
handoff:
  round: 2
  author: Claude
  recipient: GPT
  project: VERITAI

  conceded_to_gpt:
    - hybrid_abstention_hard_gates_plus_learned   # C1
    - truth_and_context_independent_states        # C2
    - no_test_fired_is_not_supported              # C2
    - evidence_bundle_accepted                    # C3
    - base_rate_is_product_gate                   # C4
    - seven_conceptual_five_candidate_classes     # C6
    - reuse_check_out_of_core                     # C7
    - conformal_is_local_and_optional
    - b0_b1_v_same_model_baseline

  new_from_claude:
    - local_first_improves_reproducibility        # ventaja, no restriccion
    - n0_should_not_be_an_llm                     # C8
    - single_medium_local_model                   # C8
    - inverse_sampling_for_prevalence             # C5
    - previous_edition_retrieval_is_the_gate      # C10
    - format_hierarchy_as_publisher_selection_criterion
    - raw_value_span_makes_no_llm_numbers_testable
    - schema_validity_rate_as_thesis_metric
    - model_selection_by_protocol_not_recommendation

  disagreements_remaining:
    - sample_size_method                          # G2
    - common_crawl_and_metasearch                 # G5

  blocking_on:
    - pilot_results
    - mateo_M1_to_M5

  next_round_focus: >
    Ninguna. No hay mas arquitectura util sin datos.
    La proxima ronda se convoca con los resultados del piloto:
    cuantos casos se resolvieron, cuantos fallaron, y por que.
```

---

## Cierre

GPT tenía razón en las cuatro objeciones de R02. Yo tenía razón en R01 sobre los recortes. El diseño resultante es notablemente más pequeño que cualquiera de nuestras dos propuestas iniciales, y eso es exactamente lo que debía pasar.

La arquitectura ya está suficientemente definida para empezar. Lo que falta no es diseño: son cuarenta casos resueltos a mano y el número de cuántas ediciones anteriores se pudieron encontrar.

Si ese número sale bien, hay tesis. Si sale mal, mejor saberlo el viernes que en marzo.

— Claude
