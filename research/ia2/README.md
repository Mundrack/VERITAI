# Módulo IA2 · Detección de lenguaje hostil en español (línea base)

Proyecto semestral de **Inteligencia Artificial 2** (UDLA, 2026), Entrega 2.
Autor: Mateo Puga Montesdeoca (Equipo 12). Es el tercer eje de VeritAI
(`docs/EJE-MANIPULACION.md`): señales observables de hostilidad y persuasión
en el texto, con etiqueta de lista cerrada y fragmento literal, sin afirmar
intención.

## Qué hay

| Archivo | Qué es |
|---|---|
| `entrenar_linea_base.py` | Descarga los datos (si no están), entrena tres modelos clásicos en dos particiones y escribe resultados y gráficos |
| `ajustar_transformer.py` | Ajusta el DistilBERT en español con las mismas particiones y escribe `resultados/transformer.json` |
| `resultados/resultados.json` | Métricas de cada modelo, matrices de confusión, rasgos más influyentes, errores por funcionalidad y la partición por plantilla |
| `resultados/datos_resumen.json` | Tamaño, distribución de clases, funcionalidades y grupos objetivo del conjunto |
| `resultados/errores.csv` | Los errores del modelo A en la partición por caso, con su funcionalidad |
| `resultados/metricas.png`, `resultados/matriz_confusion.png` | Gráficos de la presentación |
| `datos/` | Copia local del CSV público (no se versiona; se descarga sola) |

## Datos

HateCheck en español (Röttger et al., 2022, *Multilingual HateCheck*), 3 745
casos etiquetados `hateful` / `non-hateful`, 27 funcionalidades, 7 grupos
objetivo. Licencia CC BY 4.0. Fuente:
`https://huggingface.co/datasets/Paul/hatecheck-spanish/resolve/main/test.csv`.
Limitación declarada: son frases generadas a partir de plantillas, no
publicaciones reales.

## Modelos y protocolo

- **0 · Mayoría**: predice siempre la clase más frecuente (suelo).
- **A · Línea base**: TF-IDF de palabras (1 y 2 gramas, `min_df=2`, TF sublineal) + regresión logística (`C=4`, pesos balanceados).
- **B · Variante**: TF-IDF de caracteres (`char_wb`, 2 a 5 gramas) + la misma regresión logística.
- **C · Propuesto**: DistilBERT en español (`dccuchile/distilbert-base-spanish-uncased`) ajustado 2 épocas en CPU, lote 16, lr 3e-05, máximo 48 tokens (`ajustar_transformer.py`). Los pesos se descargan a `modelos/` y no se versionan.

Dos particiones con semilla 42: **por caso** (80/20 estratificada) y **por
plantilla** (`GroupShuffleSplit` sobre `templ_id`, para que ninguna plantilla de
prueba aparezca en entrenamiento). Métricas: exactitud, F1 macro, precisión y
exhaustividad de la clase hostil, matriz de confusión, errores por funcionalidad.

## Cómo reproducirlo

```bash
pip install scikit-learn pandas matplotlib
python research/ia2/entrenar_linea_base.py --salida research/ia2/resultados

# transformer (CPU): pesos de dccuchile/distilbert-base-spanish-uncased en research/ia2/modelos/
pip install torch --index-url https://download.pytorch.org/whl/cpu transformers
python research/ia2/ajustar_transformer.py --salida research/ia2/resultados --epocas 2
```

Los modelos clásicos tardan unos 20 segundos en una CPU corriente; el transformer,
unos 7 u 8 minutos por partición en CPU (i7 de novena generación, sin GPU). Probado
con Python 3.13, scikit-learn 1.9, pandas 3.1, matplotlib 3.11, PyTorch 2.15 (CPU) y
Transformers 5.24. Si las librerías de Hugging Face fallan al registrar mensajes en
Windows, el script ya desactiva el `logging` antes de importarlas.

## Resultado principal (27 de noviembre de 2026)

| Modelo | F1 macro por caso | F1 macro por plantilla |
|---|---|---|
| 0 · Mayoría | 0,413 | 0,411 |
| A · TF-IDF palabras + RL | 0,971 | 0,688 |
| B · TF-IDF caracteres + RL | 0,982 | 0,684 |
| C · DistilBERT español | 0,974 | 0,765 |

La línea base memoriza plantillas: con frases nuevas pierde casi 30 puntos de
F1. Además asocia nombres de grupos (`trans`, `indígenas`, `mujeres`...) con
hostilidad: 14 de sus 18 errores por caso son frases no hostiles sobre grupos u
objetos. El transformer, con el mismo protocolo y solo 2 épocas, generaliza mejor
por plantilla: 0,765 frente a 0,688 de F1 macro. Detalle en
`resultados/resultados.json` y `resultados/transformer.json`.

## Uso de IA generativa

El script, los gráficos y los documentos se escribieron con ayuda de Claude
Code (Anthropic), bajo indicaciones y revisión del autor. Ninguna métrica la
produjo un modelo de lenguaje: los datos son públicos y la ejecución es
reproducible con el comando de arriba.
