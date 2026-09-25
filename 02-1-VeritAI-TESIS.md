> **VeritAI — Documento 1 de 2**
> Este es el **alcance de tesis**. El producto completo está en el documento 2.

> ⚠️ **ENCUADRE VIGENTE (2026-09-25, DEC-026):** el título, el problema, los
> objetivos y la taxonomía de este documento son la **propuesta original**.
> Tras el piloto, el encuadre que manda está en
> [`docs/TESIS-ENCUADRE.md`](docs/TESIS-ENCUADRE.md): título nuevo, pregunta
> de investigación, hipótesis H1–H3, objetivos O1–O6 revisados, definición
> operacional de "divergencia contextual computable", alcance declarado a
> publicadores de nivel 1 y taxonomía reorganizada. Este archivo **no se
> edita**: se conserva como está para dejar constancia de qué cambió y por
> qué (`docs/DECISIONES.md`, DEC-023 a DEC-026).

# TESIS — Propuesta concreta

## 📌 Título propuesto

> **Detección automática de afirmaciones estadísticas engañosas en publicaciones de redes sociales en español: diseño, implementación y evaluación de un asistente de verificación contextual**

---

## 🎯 El problema, en una frase

> La desinformación más difícil de detectar **no es la mentira, es el dato verdadero presentado fuera de contexto** — y ningún sistema actual lo aborda de forma sistemática en español.

**Caso que define el proyecto:**

```
TITULAR:  "España cae 16 puestos en el ranking
           de países más seguros para mujeres"

¿ES FALSO?     No. El dato es correcto.
¿ES ENGAÑOSO?  Sí.

REALIDAD:  La puntuación de España NO cambió.
           16 países mejoraron la suya.
           España no empeoró: los demás subieron.

CLASIFICACIÓN CLÁSICA:  "Verdadero"  ❌ inútil
CLASIFICACIÓN VERITAI:  "Verdadero pero
                         descontextualizado"  ✅
```

---

## 🧩 Por qué esto sí es una tesis

| Criterio | Cumplimiento |
|---|---|
| ¿Problema real y vigente? | Sí, documentado en literatura de desinformación |
| ¿Hay un hueco identificado? | Sí — los verificadores clasifican verdadero/falso; el "verdadero pero engañoso" queda sin tratamiento automatizado |
| ¿Es acotable a un semestre? | Sí, limitando a afirmaciones estadísticas |
| ¿Es medible? | Sí, con dataset propio y métricas estándar |
| ¿Aporta algo nuevo en español? | Sí — no existe corpus ni herramienta equivalente |

---

## 🎯 Objetivos

### General

Diseñar, implementar y evaluar un sistema capaz de detectar afirmaciones estadísticas potencialmente engañosas en publicaciones en español, recuperando el dato original y presentando el contexto omitido al usuario.

### Específicos

```
O1  Construir un corpus etiquetado de 300–500 publicaciones
    en español latinoamericano con afirmaciones estadísticas,
    clasificadas por tipo de distorsión.

O2  Desarrollar un módulo de detección de afirmaciones
    estadísticas verificables (check-worthiness).

O3  Implementar un motor de recuperación que localice la
    fuente primaria del dato, no la nota de prensa.

O4  Diseñar un modelo de confianza de dos dimensiones
    (evidencia + incertidumbre) y calibrarlo.

O5  Implementar un prototipo funcional como extensión
    de navegador.

O6  Evaluar el sistema con métricas de clasificación,
    calibración y tasa de falsos positivos.
```

---

## 📖 Taxonomía de distorsión — el núcleo teórico

Esta tabla es el aporte conceptual de la tesis. Cada tipo es detectable con una estrategia distinta.

| # | Tipo | Ejemplo | Cómo se detecta |
|---|---|---|---|
| 1 | **Cambio de posición sin cambio de valor** | El caso de España | Comparar serie histórica del valor absoluto vs. la posición relativa |
| 2 | **Año base escogido a conveniencia** | "Subió 300% desde 2020" (2020 fue mínimo histórico) | Recalcular contra varios años base |
| 3 | **Absoluto vs. relativo** | "Se duplicaron los casos" (de 2 a 4) | Recuperar valores absolutos |
| 4 | **Falta el denominador** | "500 incidentes" sin decir sobre cuántos | Buscar población o total de referencia |
| 5 | **Cambio de metodología** | El índice cambió cómo mide | Revisar notas metodológicas de la fuente |
| 6 | **Correlación presentada como causa** | "Desde X, subió Y" | Detección de marcadores causales sin estudio |
| 7 | **Cifra real, marco falso** | Dato correcto, titular que no se sigue de él | Comparar afirmación del titular vs. dato |

---

## ⚙️ Arquitectura del prototipo

```
┌─────────────────────────────────────────────┐
│  EXTENSIÓN (Chromium: Chrome + Opera GX)    │
│  Lee el DOM · muestra el panel de contexto  │
└──────────────────┬──────────────────────────┘
                   │
      ┌────────────▼─────────────┐
      │  N0 · FILTRO LOCAL       │  gratis, en el navegador
      │  ¿hay dato estadístico?  │  → descarta la mayoría
      └────────────┬─────────────┘
                   │ sí
      ┌────────────▼─────────────┐
      │  N1 · EMPAREJAMIENTO     │  ¿ya fue verificado?
      │  caché + verificaciones  │  → barato
      └────────────┬─────────────┘
                   │ sin coincidencia
      ┌────────────▼─────────────┐
      │  N2 · ANÁLISIS DE        │  ⭐ APORTE ORIGINAL
      │  CONTEXTO ESTADÍSTICO    │
      │                          │
      │  · extrae métrica,       │
      │    entidad, valor, año   │
      │  · busca FUENTE PRIMARIA │
      │  · recupera serie        │
      │    histórica             │
      │  · aplica taxonomía      │
      └────────────┬─────────────┘
                   │
      ┌────────────▼─────────────┐
      │  SALIDA: contexto        │
      │  + dato original         │
      │  + confianza e           │
      │    incertidumbre         │
      └──────────────────────────┘
```

---

## 📊 Modelo de confianza

**Dos números, no uno.** Un solo score no distingue entre "las fuentes se contradicen" y "no hay fuentes".

```
score         = σ(x)   evidencia neta, entre 0 y 1
incertidumbre = f(cantidad · independencia · concordancia)
```

| score | incertidumbre | Etiqueta al usuario |
|---|---|---|
| alto | baja | ✅ Respaldado |
| bajo | baja | ❌ Contradicho |
| medio | baja | ⚠️ Fuentes en conflicto |
| — | alta | ❓ Evidencia insuficiente |
| — | — | 🔶 Verdadero pero descontextualizado |

La última etiqueta es la que justifica la tesis.

---

## 🛠️ Stack

| Capa | Tecnología |
|---|---|
| Extensión | Manifest V3, JS |
| Backend | Python + FastAPI |
| BD y caché | PostgreSQL + pgvector |
| Filtro local | Encoder pequeño cuantizado (ONNX Web) |
| Extracción y razonamiento | LLM con salida estructurada |
| Fuentes primarias | APIs de organismos estadísticos e índices internacionales |
| Verificaciones previas | API de verificaciones publicadas (ClaimReview) |

> ⚠️ Confirmar disponibilidad, cuotas y licencias de cada API antes de comprometerlas en el documento final.

---

## 🔬 Metodología

```
1  Revisión sistemática de literatura
2  Construcción del corpus (doble anotación 20%, kappa)
3  Desarrollo iterativo del prototipo
4  Evaluación cuantitativa
5  Análisis de ablación
```

---

## 📏 Evaluación

**Obligatorias**

- Precisión, recall y F1 **por clase** de la taxonomía
- **Tasa de falsos positivos** ← métrica crítica
- Calibración: Brier score, ECE, diagrama de fiabilidad
- Latencia p50 / p95 y costo por análisis

**Ablación**

- Sistema completo vs. sin recuperación de fuente primaria
- Sistema completo vs. LLM directo sin pipeline ← **si el LLM solo iguala al sistema, el diseño no se justifica. Medirlo en semana 8, no en la 14.**

---

## 🗓️ Cronograma — 16 semanas

| Sem | Entregable |
|---|---|
| 1–2 | Estado del arte · marco teórico · taxonomía formal |
| 3–4 | Manual de anotación · recolección de publicaciones |
| 5–7 | Etiquetado del corpus ‖ extensión mínima que lee el DOM |
| 8–10 | Pipeline end-to-end ‖ **baseline LLM medido** |
| 11–12 | Módulo de contexto estadístico · calibración |
| 13–14 | Evaluación completa · ablación · tablas |
| 15–16 | Redacción · defensa |

> 🚨 **Hito de riesgo (semana 10):** si el pipeline no corre completo, recortar alcance en lugar de agregar funciones.

---

## 🚫 Fuera del alcance de la tesis

```
✗ Aplicación móvil
✗ Detección de deepfakes, video, audio
✗ Detección de texto generado por IA
✗ Multilingüe
✗ Redes distintas de X
✗ Dashboard empresarial
```

Todo eso vive en el documento 2, declarado como trabajo futuro.

---

## ⚠️ Pendientes antes de programar

```
□ Conseguir tutor y validar el alcance con él
□ Confirmar APIs: disponibilidad, cuotas, licencias
□ Revisar términos de servicio vigentes de X
□ Reglamento de titulación UDLA sobre propiedad intelectual
  (antes de cualquier acuerdo con empresa patrocinadora)
□ Cambiar el nombre: "VeritAI" está en uso por varias empresas
```
