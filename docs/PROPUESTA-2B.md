# Propuesta: test 2b (base revisada) y conector de edición anterior

**Estado:** propuesta, pendiente del "ejecuta" de Mateo (DEC-034 §6). No se
implementa nada de esto hasta entonces. Fecha: 2026-09-26.

**Respuesta corta a las tres preguntas de Mateo.** El mapa cubre **8
operaciones del INE**, y se cierra en 8. Añadir una cuesta **alrededor de una
hora** de trabajo humano y una entrada de diez líneas, con el procedimiento de
§4.3; no se añade ninguna durante la evaluación. El patrón de código que hace
posible el conector es una **amenaza a la validez** (§5), no una nota al pie.

## 1. Qué decide el test 2b y qué no

Un claim de tipo `cambio_entre_periodos` presenta **2b** cuando la tasa que
afirma se reproduce con el valor del periodo base **tal como se publicó** en su
edición (provisional) y **no** se reproduce con el valor **vigente** que el
emisor sirve hoy (revisado). El claim no está mal calculado: está calculado
contra una base que el emisor ya no sostiene. Con o sin cambio de signo
(Baleares, E043: +3,8 % publicado frente a −2,3 % vigente).

No decide intención, no decide si la revisión es grande o pequeña por sí
misma, y no aplica a niveles, extremos ni rankings (tipos sin test → `undetermined`).

## 2. Definición del test, antes de programarlo

Entrada: `ClaimEstructurado` con `periodo_objetivo`, `periodo_base`,
`valor_objetivo`, `cambio_afirmado` (con sus decimales) y la métrica del
emisor (operación, tabla, serie).

1. **Vigente.** Como hoy: `valor_objetivo` y `valor_base` de Tempus (edición
   vigente), `tasa_vigente = objetivo / base_vigente − 1`. La verdad
   (`verdad.py`) compara `cambio_afirmado` con `tasa_vigente` con la
   tolerancia de redondeo declarada (`tolerancia_para`, mínimo 0,15 pp).
2. **Gatillo.** Si la verdad cuadra con la vigente, 2b **no aplica** (no hay
   nada que explicar): `no_divergence_detected` si ningún otro test dispara.
   Si no cuadra, se pide la edición al publicar del periodo base.
3. **Edición al publicar.** El conector deriva el código de la nota del
   periodo base (`<OPERACION><MM><YY>`), descarga el anexo XLSX y la nota
   HTML, lee la fecha de publicación de la nota y extrae del anexo la celda de
   la serie con el mapa (§4). Devuelve un `EvidenceItem` con `rol=HISTORICAL`,
   `etiqueta="base_al_publicar"`, `version=<código>`, `document_date=<fecha
   de publicación>` y el `raw_value_span` literal de la fila.
4. **Recomputación.** `tasa_al_publicar = objetivo / base_al_publicar − 1`.
   **Dispara** si `|cambio_afirmado − tasa_al_publicar| ≤ tolerancia` **y**
   `|cambio_afirmado − tasa_vigente| > tolerancia`. Subtipo:
   `cambio_de_signo` si `signo(tasa_vigente) ≠ signo(tasa_al_publicar)`,
   `magnitud` en otro caso. `calculos` guarda las dos tasas, las dos bases,
   la revisión absoluta y relativa y la tolerancia usada.
5. **Salida.** `context = divergence_detected`, `clase_primaria =
   2b_base_revisada`, `truth = mixed` (el número es rastreable a una edición
   del emisor; el marco no). El veredicto lleva **`evidencia_al_publicar`**
   (valor, edición, **fecha de publicación**, URL, span) y
   **`evidencia_vigente`** (valor, edición vigente, **fecha de consulta**,
   URL, span), ya en `Veredicto` y en la plantilla (`lineas_ediciones`).
6. **Abstención, nunca relleno.** Anexo no servido o rechazado →
   `PREVIOUS_EDITION_NOT_FOUND`; fila no encontrada o más de una →
   `EXTRACTION_FAILED` / `SOURCE_VERSION_AMBIGUOUS`; el periodo base no tiene
   nota propia (p. ej. base no mensual) → `PERIOD_NOT_COMPARABLE`. En todos:
   `context = undetermined` (DEC-029: sin test aplicable no se afirma
   ausencia de divergencia).
7. **2a sigue corriendo** como test secundario sobre la vigente, con su regla
   de signo (DEC-029). Orden: verdad → 2a → 2b. Si 2b dispara, la clase
   primaria es 2b y 2a queda en `clases_secundarias` si también disparó.

## 3. El conector

- **Puerto** (dominio, `puertos.py`): `ProveedorEdicionAnterior.obtener(metrica,
  periodo) -> EvidenceItem | None`, más `disponible(metrica) -> bool` (¿está
  la operación en el mapa?).
- **Implementación** (`infrastructure/ine/edicion_anterior.py`), a partir de
  `research/puerta3/edicion_anterior.py`, que ya demostró la recuperabilidad
  (`research/puerta3/RECUPERABILIDAD-2B.md`). Descarga solo de
  `www.ine.es` (allowlist), timeout, tope de bytes, sin redirecciones fuera
  del host, sin shell. El XLSX se valida por **bytes mágicos** (ZIP), no por
  extensión ni MIME, y se abre con `openpyxl` en modo `data_only` sobre un
  temporal aislado; la nota HTML solo se usa para leer la fecha con una
  expresión regular fija. Todo lo descargado es **dato, nunca instrucción**.
- **Fixtures**: las filas y fechas de las ediciones ya descargadas (sha256 en
  `research/evidencia/D2B_*.json`) sirven de fixtures; los tests no tocan la
  red.
- **Persistencia**: el `EvidenceItem` de la edición al publicar entra en el
  bundle y en `evidence_items` como cualquier otro; el `bundle_hash` cambia si
  cambia la edición.

## 4. El mapa: qué es, cuánto cubre, cuánto cuesta y dónde se cierra

### 4.1 Qué es

Una entrada **por tabla del anexo**, no por serie: hoja del XLSX, columna de
cada variable y un normalizador de etiquetas de fila que casa el nombre de la
serie Tempus con la etiqueta del anexo ("Madrid (Comunidad de)" ↔ "Madrid,
Comunidad de"; "Balears (Illes)" ↔ "Balears, Illes"). Unas diez líneas por
entrada, declarativas, sin código nuevo por operación.

### 4.2 Cuánto cubre: 8 operaciones, patrón verificado en las 8

| operación (código de nota) | qué es | patrón verificado (edición) | anexo XLSX | hoja/fila localizada | estado |
|---|---|---|---|---|---|
| `CTH` | Coyuntura Turística Hotelera (EOH, IPH, IRSH) | CTH0725, CTH0825 | 200 | `EOH_Hoja3` por CCAA (viajeros, pernoctaciones × residencia) | **listo** (E031, E042, E043) |
| `EOAT` | Alojamientos extrahoteleros (apartamentos, campings, rural) | EOAT0725 | 200 | `EOAL_Hoja2`, `EOAC_Hoja2`, `EOTR_Hoja1` por CCAA | fila localizada; columnas por mapear |
| `ETDP` | Transmisiones de derechos de la propiedad (compraventas) | ETDP0725 | 200 | `Hoja9` (ETDP.11 por CCAA), `Hoja3` (ETDP.5 nacional) | **listo** (TOTAL 64.730) |
| `H` | Hipotecas | H0625 | 200 | titular (41.834) y `Hoja6` (H.9 viviendas); CCAA por mapear | fila nacional localizada |
| `SM` | Sociedades mercantiles | SM0725 | 200 | `Hoja 1` (SM.1 TOTAL 10.902) | **listo** nacional; CCAA por mapear |
| `IPI` | Índice de producción industrial | IPI0725 | 200 | por mapear (índices por destino económico y CCAA) | patrón verificado |
| `FRONTUR` | Llegadas de turistas | FRONTUR0725 | 200 | `Hoja1`/`Hoja2` (TOTAL 11.023.252, +1,57 %) | fila nacional localizada |
| `EGATUR` | Gasto turístico | EGATUR0725 | 200 | `Gasto partidas` (TOTAL 16.452), `Datos acumulados` | fila nacional localizada |

Fuera del mapa, y por qué: **IPRI** (la nota IPRI0825 no tiene anexo XLSX:
404; solo HTML y PDF, y el PDF no se parsea), las **trimestrales** `CNTR`,
`IPV`, `ETCL`, `EPA` (el patrón `<OP><n>T<YY>` funciona, CNTR2T25 dio 200 ×3,
pero sus claims en el conjunto son niveles y revisiones avance→definitivo que
ya tienen tratamiento propio, y ampliar el mapa a trimestrales es abrirlo), y
todo lo que no es INE (SEPE no revisa; el Portal de Criminalidad y el Banco de
España quedan como 2b **anotable a mano**, no computable).

### 4.3 Cuánto cuesta añadir una operación

Alrededor de **una hora** de trabajo humano y una entrada de mapa:

1. Comprobar el patrón de código con `edicion_anterior.py` (un minuto).
2. Localizar hoja, etiqueta de fila y columna de cada variable en el anexo
   (15–30 minutos con la herramienta).
3. Escribir la entrada del mapa, guardar la fila como fixture y añadir un test
   que la lea sin red (30 minutos).
4. `NEEDS_REVIEW` hasta que un caso real de 2b la valide.

Si el anexo cambia de diseño entre ediciones, la entrada se rompe: el test
con fixture lo detecta en desarrollo y el conector abstiene en producción.

### 4.4 Dónde se cierra

**El alcance del conector son estas 8 operaciones y se cierra aquí.** No se
añade ninguna durante la evaluación: si un caso de 2b cae fuera del mapa, se
anota a mano como B y el prototipo lo declara `undetermined` por
`UNSUPPORTED_CLAIM_TYPE`; cuenta como fallo de cobertura en el recall, no se
maquilla. El sistema sigue siendo general en la clase (2b) y en el emisor
(INE), con un alcance de operaciones declarado y cerrado, igual que el alcance
de emisores.

## 5. Amenaza a la validez

El patrón de código de las notas no está documentado por el INE, e INEbase no
enlaza notas anteriores. **Si el INE cambia el patrón, el conector se rompe y
2b deja de ser computable por el agente.** No hay mitigación que lo evite;
la hay para que la rotura sea visible (abstención, nunca un valor inventado)
y para conservar lo ya descargado (sha256). Se declara en el diseño (§4), en
el encuadre y en la tesis como límite de validez externa del conector.

## 6. Qué se toca, en qué orden, y qué lo demuestra

1. `domain/puertos.py`: puerto `ProveedorEdicionAnterior`.
2. `domain/tests/base_revisada.py`: `aplicar_2b` puro, con tests unitarios
   sintéticos (dispara con y sin cambio de signo; no dispara si la vigente
   cuadra; abstiene sin edición).
3. `infrastructure/ine/mapa_anexos.py` (las 8 entradas) y
   `infrastructure/ine/edicion_anterior.py` (descarga, validación, extracción),
   con tests sobre fixtures de `research/evidencia/D2B_*`.
4. `application/analizar_claim.py`: orden verdad → 2a → 2b; los dos campos
   del veredicto; `PREVIOUS_EDITION_NOT_FOUND` como abstención.
5. Regresión: E031, E042 y E043 corren de extremo a extremo y disparan 2b con
   las fechas correctas; los 46 tests anteriores siguen pasando; `ruff` limpio.
6. `ARQUITECTURA.md` y `SEGURIDAD.md`: el conector y sus límites.

Dos sesiones de trabajo, con diff antes de cada commit.

## 7. Alternativas descartadas

- **Parsear el PDF de la nota** para cubrir IPRI: tablas en PDF, frágil y
  contra la regla de no extraer tablas de PDF si hay dataset; queda fuera.
- **Tempus con ediciones históricas**: no existe (limitación documentada en
  el encuadre).
- **Mapa abierto o heurístico** (buscar la fila por similitud en cualquier
  hoja): abre el mapa sin límite y hace el sistema menos general, no más; es
  lo que Mateo prohíbe.
- **Un LLM para localizar la celda**: prohibido (CLAUDE.md §7: alucina celdas).
