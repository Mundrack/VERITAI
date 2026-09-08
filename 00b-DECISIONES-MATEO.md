# VERITAI — DECISIONES DE MATEO

**Añadir al paquete como `00b-DECISIONES-MATEO.md`.** Se lee junto con `00-LEER-PRIMERO.md`, antes del START-HERE.

Estas decisiones están tomadas. No volver a preguntarlas.

---

## Decisiones cerradas

```yaml
geografia:
  opcion: A
  alcance: "español en general, sin afirmar foco latinoamericano"
  lote_nuevo: sin cuota geografica obligatoria
  nota: >
    Se elimina la comparacion Espana vs Ecuador del alcance de tesis.
    Los emisores se eligen por recuperabilidad, no por pais.

tutor:
  existe: false
  decision: "arrancar con el plan actual sin validacion previa"
  riesgo_aceptado: posible retrabajo si el tutor pide otro enfoque

cronograma:
  fecha_limite: no definida
  criterio: "avanzar lo mas rapido posible"
  implicacion: >
    Sin fecha, el hito de riesgo se define por entregable, no por semana.
    Puerta 1 = PILOT-DECISION.md. No se programa antes.

hardware_actual:
  cpu: Intel Core i7 9na generacion (alternativa: i5)
  ram: 16 GB DDR4
  gpu: basica, no apta para inferencia
  perfil: A (CPU-only)
  decision: "no comprar hardware hasta tener PILOT_GO"

anotacion:
  segundo_anotador: pendiente de conseguir
  fallback: declarar como limitacion metodologica

idiomas:
  interfaz_app: multiidioma desde el inicio (i18n, minimo es + en)
  analisis_del_sistema: solo español en tesis
  documento_tesis: español, con abstract en ingles
  traduccion_completa_del_documento: descartada

nombre:
  tesis: VeritAI
  decision_comercial: aplazada
  alternativas_evaluadas: [Cotejo, Fuente Cero, Ancla, Contexta, Primaria]

emisores:
  preferencia: ninguna
  criterio: recuperabilidad + acceso publico + serie historica

plantilla_udla:
  existe: si
  estado: pendiente de entregar
  implicacion: no bloquea el piloto, si bloquea la redaccion

modelo_de_negocio:
  estado: aplazado
  empresa_patrocinadora: sin decidir
  nota: no condicionar ninguna decision tecnica a esto
```

---

## Consecuencias técnicas de estas decisiones

### 1. Opción A cambia la composición del lote nuevo

Se elimina la cuota geográfica. La composición obligatoria de los 20 casos nuevos queda:

| Tipo | Cantidad |
|---|---|
| Estadísticas correctamente enmarcadas (negativos) | 7 |
| Divergencia real esperada | 6 |
| Fuente primaria no localizable | 3 |
| Edición anterior no localizable | 2 |
| Formato hostil (PDF escaneado, sin datos abiertos) | 2 |

**Se mantiene intacta la regla dura de D1:** ningún caso puede provenir de un artículo de verificación. Esa era la corrección importante y no depende de la geografía.

### 2. i18n desde el día uno

No es "multilingüe" en el sentido que se descartó. Es solo no incrustar textos en el código.

```
✅ EN TESIS
   · textos de interfaz en archivos de idioma (es, en)
   · plantillas de explicación parametrizadas por idioma
   · formatos de número y fecha por locale

❌ FUERA DE TESIS
   · análisis de contenido en otros idiomas
   · recuperación de evidencia multilingüe
   · emparejamiento translingüe de afirmaciones
```

Coste si se hace ahora: casi nulo. Coste si se hace después: reescribir toda la capa de presentación.

`ATENCIÓN` La plantilla de explicación tiene una restricción especial: los números vienen de campos calculados y se insertan por plantilla. Al traducir, **traducir la plantilla, nunca el resultado renderizado**. Traducir la salida final reintroduce el riesgo de alterar números.

### 3. Perfil A: qué se puede y qué no

```
SE PUEDE (CPU, 16 GB)
  · todo el piloto manual
  · conectores y parsers
  · N0: regex + encoder pequeño ONNX  → cómodo
  · modelo ~4B cuantizado             → lento pero usable
  · pruebas de schema y extracción

SE PUEDE CON ESFUERZO
  · modelo ~8B cuantizado (~5-6 GB)   → RAM justa, lento

NO SE PUEDE
  · modelo 14B+
  · concurrencia
  · latencia interactiva
```

**Implicación metodológica:** las pruebas de selección de modelo (§12.2 de R02) se ejecutan en este hardware y se documenta que la latencia medida corresponde al perfil A. La calidad de extracción sí es transferible; la latencia no.

### 4. Sin fecha límite: las puertas sustituyen al calendario

El cronograma de 16 semanas deja de aplicar. Se reemplaza por puertas:

```
PUERTA 1   research/PILOT-DECISION.md con PILOT_GO
           → sin esto no se escribe código de producto

PUERTA 2   Prototipo end-to-end con UNA clase y UN emisor,
           que resuelva 10 casos con trazabilidad completa
           → sin esto no se amplían clases ni emisores

PUERTA 3   Corpus completo anotado + arnés de evaluación
           → sin esto no se empieza a redactar resultados

PUERTA 4   Evaluación completa: métricas, ablación,
           sondas contrafactuales
           → sin esto no se redacta la conclusión
```

`RIESGO` Sin fecha externa, el riesgo deja de ser "no llego" y pasa a ser "no termino nunca porque siempre hay algo que mejorar". Las puertas son la mitigación: cada una se cierra explícitamente y no se reabre.

### 5. Sin tutor: mitigación de bajo costo

Enviar esta semana, en paralelo al piloto, un resumen de **una página** con:

```
· problema y caso canónico (España, ranking vs. puntuación)
· qué se mide: divergencia contextual computable
· qué NO se mide: intención ni engañosidad percibida
· alcance: español, texto, bajo demanda, extensión
· método: corpus propio + pipeline + evaluación con ablación
· pregunta concreta: "¿es un alcance aceptable para titulación?"
```

No bloquea nada. Evita rehacer.

---

## Preguntas que quedan abiertas

```
□ Plantilla de titulación de la UDLA          → antes de redactar
□ Segundo anotador                            → antes de cerrar el corpus
□ Nombre definitivo                           → antes de invertir en marca
□ Modelo de negocio y propiedad intelectual   → aplazado por decisión
```

Ninguna bloquea el piloto.

---

## Próximo paso

Ejecutar el piloto según `00-LEER-PRIMERO.md`, con la composición del lote ajustada por la opción A.

La métrica que decide sigue siendo la misma: **porcentaje de casos del lote crudo donde se localiza la edición anterior del dato.**
