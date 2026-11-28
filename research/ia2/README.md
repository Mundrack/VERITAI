# Módulo IA2 · Detección de lenguaje hostil en español

Proyecto semestral de **Inteligencia Artificial 2** (UDLA, 2026), Entrega 3.
Autor: Mateo Puga Montesdeoca (Equipo 12). Es la primera tarea del tercer eje
de VeritAI (`docs/EJE-MANIPULACION.md`): señales observables de hostilidad en el
texto, con etiqueta de lista cerrada y fragmento literal, sin afirmar intención.

Pregunta: ¿qué rendimiento obtiene un modelo de IA para identificar lenguaje
hostil en español frente a un método tradicional, y qué parte de ese rendimiento
sobrevive cuando se controla la **fuga por plantillas** y se mide el **sesgo por
grupo**?

## Qué hay

| Archivo | Qué es |
|---|---|
| `datos.py` | Carga los dos conjuntos con un formato común; los descarga la primera vez a `datos/` (no versionado) |
| `entrenar_linea_base.py` | Tres modelos clásicos (mayoría, TF-IDF palabras + RL, TF-IDF caracteres + RL) en las particiones del protocolo; `--datos hatecheck\|haternet` |
| `ajustar_transformer.py` | Ajusta DistilBERT en español con las mismas particiones; `--semilla`, `--epocas`, `--datos`, `--nombre` |
| `analisis.py` | Media y desviación por semilla, sesgo por grupo objetivo, errores por funcionalidad y las figuras |
| `explicar.py` | Qué parte del texto sostiene el veredicto: contribución exacta por n-grama (A) y ocultación por palabra (C) |
| `graficos.py` | Gráfico comparativo de la Entrega 2 |
| `test_modulo.py` | Pruebas: carga de datos, particiones y exactitud de la explicación de A (`python -m pytest -q test_modulo.py`) |
| `requirements.txt` | Librerías probadas |
| `resultados/` | Todo lo medido: `resultados*.json`, `transformer_*.json`, `pred_*.csv` (predicción por ejemplo), `analisis.json`, `explicaciones.json`, figuras |
| `datos/`, `modelos/` | Datos y pesos descargados; no se versionan |

## Datos

- **HateCheck en español** (Röttger et al., 2022, *Multilingual HateCheck*, WOAH;
  DOI 10.18653/v1/2022.woah-1.15). 3 745 frases generadas a partir de plantillas,
  27 funcionalidades, 7 grupos objetivo, 70,3 % hostiles. CC BY 4.0.
  `https://huggingface.co/datasets/Paul/hatecheck-spanish/resolve/main/test.csv`.
- **HaterNet** (Quijano-Sánchez, Pereira-Kohatsu, Liberatore y Camacho-Collados,
  2019; Zenodo, DOI 10.5281/zenodo.2592149). 6 000 tuits reales en español
  etiquetados odio / no odio, 26,1 % de odio. CC BY 4.0.
  `https://zenodo.org/records/2592149/files/labeled_corpus_6K.txt`.

Los dos conjuntos miden cosas distintas: HateCheck controla el fenómeno pero no
la variedad del lenguaje; HaterNet tiene la variedad pero no controla el
fenómeno ni publica el autor.

## Modelos y protocolo

- **0 · Mayoría**: predice siempre la clase más frecuente (suelo).
- **A · Línea base**: TF-IDF de palabras (1 y 2 gramas, `min_df=2`, TF sublineal) + regresión logística (`C=4`, pesos balanceados).
- **B · Variante**: TF-IDF de caracteres (`char_wb`, 2 a 5 gramas) + la misma regresión logística.
- **C · Propuesto**: DistilBERT en español (`dccuchile/distilbert-base-spanish-uncased`), AdamW, lr 3e-05 con calentamiento del 10 % y decaimiento lineal, lote 16, 3 épocas, máximo 48 tokens (HateCheck) o 64 (HaterNet). CPU.

Particiones con semilla 42, idénticas para los cuatro modelos:

- HateCheck **por caso**: 80/20 estratificada (2 996 / 749). La habitual.
- HateCheck **por plantilla**: `GroupShuffleSplit` sobre `templ_id` (3 026 / 719,
  151 plantillas de prueba). Ninguna plantilla de prueba se ve en entrenamiento:
  mide la generalización a frases nuevas.
- HaterNet: 80/20 estratificada (4 800 / 1 200). Sin plantillas ni autor para agrupar.

El transformer se entrena con tres semillas del modelo (42, 7, 123) por
configuración; se reporta media ± desviación. Métrica principal: F1 macro.
Hiperparámetros fijados de antemano, sin búsqueda ni conjunto de validación
(limitación declarada).

## Cómo reproducirlo

```bash
pip install -r research/ia2/requirements.txt      # torch desde https://download.pytorch.org/whl/cpu si no hay GPU
cd research/ia2

python entrenar_linea_base.py --salida resultados                    # HateCheck, clásicos (~20 s)
python entrenar_linea_base.py --salida resultados --datos haternet   # HaterNet, clásicos (~20 s)

# transformer: pesos de dccuchile/distilbert-base-spanish-uncased en modelos/distilbert-base-spanish-uncased/
for s in 42 7 123; do
  python ajustar_transformer.py --salida resultados --epocas 3 --semilla $s --nombre transformer_s${s}_e3
  python ajustar_transformer.py --salida resultados --epocas 3 --max-len 64 --datos haternet --semilla $s --nombre transformer_haternet_s${s}_e3
done

python analisis.py                                   # semillas, sesgo por grupo, figuras
python explicar.py --parte ambas --conjunto ambos    # fragmentos que sostienen el veredicto (reentrena C una vez)
python -m pytest -q test_modulo.py
```

Tiempos en CPU (i7 de novena generación, 16 GB, sin GPU): clásicos, unos 20 s;
transformer, unos 10 min por ajuste en HateCheck y unos 35 min en HaterNet.
Probado con Python 3.13, scikit-learn 1.9, pandas 3.1, matplotlib 3.11, PyTorch
2.15 (CPU) y Transformers 5.24. Si las librerías de Hugging Face fallan al
registrar mensajes en Windows, los scripts ya desactivan el `logging` antes de
importarlas.

## Resultados (27 de noviembre de 2026)

F1 macro en prueba. Transformer: media ± desviación de 3 semillas.

| Modelo | HateCheck por caso | HateCheck por plantilla | HaterNet (tuits reales) |
|---|---|---|---|
| 0 · Mayoría | 0,413 | 0,411 | 0,425 |
| A · TF-IDF palabras + RL | 0,971 | 0,688 | 0,739 |
| B · TF-IDF caracteres + RL | 0,982 | 0,684 | 0,736 |
| C · DistilBERT español | 0,988 ± 0,005 | **0,795 ± 0,031** | 0,761 ± 0,003 |

1. **Fuga por plantillas.** La línea base pierde 28 puntos de F1 macro cuando se
   le exige clasificar frases de plantillas que no vio (0,971 → 0,688): memoriza
   plantillas. El transformer pierde menos (0,988 → 0,795).
2. **Tuits reales.** La tarea es más difícil para todos. La línea base reconoce
   seis de cada diez tuits de odio (exhaustividad 0,629) con precisión parecida
   (0,604). El transformer sube a 0,761 ± 0,003 de F1 macro, 2 puntos por encima de la línea base, con una exhaustividad de odio de 0,623 y una precisión de 0,667. La ventaja es menor que en frases nuevas de HateCheck.
3. **Sesgo por grupo objetivo** (partición por plantilla, frases *no hostiles*
   marcadas como hostiles): la línea base da falsas alarmas en el 45–50 % de las
   frases no hostiles de cada grupo; el transformer las baja al 14–18 % en los 8
   grupos. En HateCheck los rasgos léxicos más hostiles son nombres de grupos
   (`trans`, `indígenas`, `mujeres`); en HaterNet son insultos (`subnormal`,
   `mierda`, `escoria`), y los nombres de grupos pesan hacia *no* odio.
4. **Explicación por fragmentos** (`resultados/explicaciones.json`): en "No conozco
   a muchos gays", no hostil para la referencia, el modelo A dice hostil y el
   rasgo que más pesa es `gays` (1,95). El atajo queda visible.

Detalle: `resultados/analisis.json`, `resultados/resultados*.json`,
`resultados/transformer_*.json`.

## Lo que quedó fuera

La tarea de técnicas de persuasión (SemEval-2023 Task 3) se declara fuera del
alcance: los datos exigen registro con verificación manual, su uso está
restringido a la tarea compartida y el español aparece solo como lengua de
prueba, sin datos de entrenamiento. Queda como trabajo futuro con el diseño ya
definido (etiqueta de lista cerrada por técnica y fragmento literal).

## Uso de IA generativa

Los scripts, las figuras, el artículo y la presentación se escribieron con ayuda
de Claude Code (Anthropic), bajo indicaciones y revisión del autor. Ninguna
métrica la produjo un modelo de lenguaje: los datos son públicos y la ejecución
es reproducible con los comandos de arriba.
