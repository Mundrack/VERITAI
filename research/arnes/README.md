# Arnés de evaluación (Puerta 3)

Mide. No recolecta, no anota, no corre la API.

```
anotacion.csv  ──┐
                 ├──► arnes.py ──► <salida>.md  (tablas para el informe)
resultados/*.json┘                <salida>.json (los números)
```

- **Entrada 1:** el CSV de anotación con el esquema de `pilot-crudo-trabajados.csv`
  (o `PILOT-40.csv`). Obligatorias: `case_id`, `truth`, `context`, `clase_primaria`.
  Las columnas de recuperación (`current_edition_found`, `previous_edition_found`,
  `alcanzable_por_agente`, `recuperabilidad`, `minutes_*`, `cronometrado_por`) hacen
  falta para las cinco métricas de R02 §7; si falta una, esa métrica sale `n/d`.
- **Entrada 2:** los `resultados/<case_id>.json` que escribe
  `research/puerta2/ejecutar_casos.py` (respuesta completa de `POST /analisis`).
- **Guardia (DEC-025):** solo evalúa casos con `conjunto = evaluacion`. Con
  desarrollo se niega; `--desarrollo` lo permite y marca la salida como **HUMO**.

Qué calcula, con IC 95 % de Wilson (y regla de tres cuando k = 0):

| Bloque | Qué | De dónde |
|---|---|---|
| 1 | Las cinco de R02 §7: fuente primaria, **edición anterior** (manda), extracción A\|B, clases observadas, tiempo por caso; conservadora y leniente (DEC-019/021) | anotación |
| 2 | **FPR** sobre controles (supported + no_divergence) **con test aplicable**; señales aparte (DEC-029); secundaria sobre todo lo anotado sin divergencia; veredicto de **H3** con tasa, límite superior y n mínimo fijados a priori (`--h3-tasa 10 --h3-limite 15 --h3-min-n 40`, los del diseño) | anotación × sistema |
| 3 | Acuerdo por eje, recall de 2a anotada, abstención cuando la anotación abstiene, matriz de contexto | anotación × sistema |
| 4 | Una fila por caso | ambos |

```bash
# humo sobre los 10 casos de desarrollo de la Puerta 2 (no evalúa nada)
python research/arnes/arnes.py --anotacion research/PILOT-40.csv \
    --resultados research/puerta2/resultados --desarrollo --salida research/arnes/humo-puerta2

# tests del arnés (aritmética de intervalos, FPR/H3, guardia)
python -m pytest research/arnes -q -p no:cacheprovider
```

La aritmética de `wilson()` es la que justifica el tamaño del conjunto en
[`../PUERTA-3-DISENO.md`](../PUERTA-3-DISENO.md): con 40 controles y un falso
positivo el límite superior es 12,9 %; con 50 y dos, 13,5 %.
