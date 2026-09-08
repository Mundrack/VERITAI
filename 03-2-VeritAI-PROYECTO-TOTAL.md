> **VeritAI — Documento 2 de 2**
> Este es el **proyecto completo como producto**. El alcance de tesis está en el documento 1.

# PROYECTO TOTAL

## 🧭 Qué es

> Una capa de contexto sobre lo que la gente consume en internet.
> No dice qué creer. Muestra de dónde sale cada cosa.

**Lema:** VeritAI informa. El usuario decide.

---

## 🏛️ Los cuatro ejes

El proyecto original tenía tres. El cuarto salió del caso de España y es el que más diferencia al producto.

| Eje | Pregunta | Solidez | Rol |
|---|---|---|---|
| 🔶 **Contexto** | ¿El dato está bien enmarcado? | Alta | ⭐ Diferenciador |
| ✅ **Veracidad** | ¿Es cierto? | Alta | Núcleo |
| 🎭 **Retórica** | ¿Qué técnicas de persuasión usa? | Media-alta | Diferenciador |
| 🤖 **Origen** | ¿IA o humano? | Baja | Complemento |

### 🔶 Contexto — el eje nuevo

Detecta el dato verdadero mal enmarcado: cambio de ranking sin cambio de valor, año base a conveniencia, absoluto vs. relativo, denominador ausente, cambio de metodología, correlación vendida como causa.

**Por qué importa:** es la forma de desinformación más común y la que ningún sistema automatizado aborda. Los verificadores clásicos responden verdadero/falso; aquí la respuesta correcta es "verdadero, pero".

### 🎭 Retórica

Nombra técnicas concretas —apelación al miedo, falsa autoridad, urgencia artificial, falso dilema— en vez de emitir juicios de intención.

**Ventaja:** es descriptivo, no acusatorio. Funciona aunque no exista ninguna verificación previa disponible. Y está muy poco explorado en español.

### 🤖 Origen

Los detectores estadísticos de texto son poco fiables y empeoran fuera del inglés. Prioridad a la procedencia criptográfica verificable (C2PA / Content Credentials); la señal estadística va con peso bajo y jamás como veredicto.

> Que algo sea generado por IA no lo hace falso. El eje informa procedencia, no calidad.

---

## 🔍 Motor de evidencia

### Regla de oro

```
❌  Ir al medio prestigioso que reporta el dato
✅  Ir a la fuente primaria que produjo el dato
```

**Por qué.** El caso de España lo demuestra: todos los medios serios publicaron el mismo titular engañoso. Lo que desmonta el engaño no es un medio mejor, es **abrir el informe original y mirar la serie histórica**.

El prestigio es un buen **indicio previo**, no una prueba. Y diez medios repitiendo el mismo cable de agencia son **una** fuente, no diez.

### Qué se modela de cada fuente

| Atributo | Ejemplo |
|---|---|
| **Tipo** | revisada por pares · organismo oficial · verificador acreditado · prensa · autopublicado |
| **Nivel de evidencia** | revisión sistemática > estudio individual > nota de prensa sobre el estudio |
| **Independencia** | ¿fuentes distintas o copias del mismo origen? |
| **Concordancia** | ¿coinciden o se contradicen entre sí? |
| **Primaria vs. secundaria** | ¿el dato original o alguien contándolo? |

### Multilingüe

El idioma del contenido y el idioma de la mejor evidencia son cosas distintas.

```
Afirmación médica en español  →  literatura en inglés
Política interna de un país   →  fuentes de ese país
Índice internacional          →  informe original del emisor
```

**Enrutamiento:** dominio + ámbito geográfico + ventana temporal deciden dónde y en qué idiomas buscar. Siempre se conserva el original y el enlace.

**Emparejamiento translingüe:** detectar que una afirmación en español ya fue desmentida en inglés o portugués. La desinformación viral casi nunca es original: es reciclada y traducida.

**Sobre control estatal de medios:** existe en varios países y no es exclusivo de ninguna región. El sistema **no descarta fuentes por su país de origen** —eso sería sesgo político insostenible— sino que etiqueta el tipo de fuente y su relación con estructuras estatales cuando es documentable.

---

## 📐 Modelo de confianza

### El problema de un solo número

```
8 fuentes buenas que se contradicen  →  0.5
0 fuentes encontradas                →  0.5

Son cosas opuestas. Reportarlas igual es un error.
```

### La solución: lógica subjetiva

```
        b + d + u = 1

   b = creencia       (evidencia a favor)
   d = descreencia    (evidencia en contra)
   u = incertidumbre  (falta de evidencia)
```

El espacio no es una recta, es un **triángulo**. Cada análisis es un punto dentro de él.

```
                    u = 1
                  (no sé nada)
                     ╱ ╲
                    ╱   ╲
                   ╱  ●  ╲     ← sin evidencia
                  ╱       ╲
                 ╱  ●   ●  ╲   ← conflicto
                ╱___________╲
            d = 1           b = 1
          (es falso)      (es cierto)
```

Sigues obteniendo un número entre 0 y 1 para el semáforo (`E = b + a·u`), pero ganas la capacidad de separar conflicto de ignorancia.

### 🕸️ Sobre el gráfico de estrella (radar)

**Como cálculo: no sirve.** El área del polígono depende del **orden** de los ejes — reordenas los mismos datos y el área cambia. Usar el área como puntaje es matemáticamente inválido. Y con varias series superpuestas se vuelve ilegible, como en la imagen que compartiste.

**Como visualización de UN análisis: sí sirve, y bien.** En el dashboard, con 5–6 ejes y una sola serie:

```
              Respaldo
                 ╱│╲
    Independencia │ Calidad de fuentes
              ╲  │  ╱
               ╲ │ ╱
     Retórica ───●─── Contexto
                 │
            Incertidumbre
```

> **Regla:** el triángulo para calcular, el radar para mostrar. Nunca al revés.

---

## 🚦 Salida al usuario

### Verdicto principal

| | Etiqueta | Cuándo |
|---|---|---|
| ✅ | Respaldado | La evidencia lo apoya |
| 🔶 | **Verdadero pero descontextualizado** | El dato es correcto, el marco no |
| ⚠️ | Fuentes en conflicto | Evidencia de calidad que se contradice |
| ❓ | Evidencia insuficiente | No se encontró base para decidir |
| ❌ | Contradicho | La evidencia lo refuta |
| ➖ | No aplica | Sin afirmaciones verificables |

### Insignias independientes

`procedencia` · `técnicas retóricas detectadas` · `nº de fuentes independientes`

### Grados de interrupción

```
🔕 Silencioso   respaldado · no aplica · insuficiente
🔔 Pasivo       contexto · conflicto  → insignia junto al post
🚨 Alerta       contradicho + confianza alta → banda destacada
```

> **La fatiga de alertas mata el producto.** Es preferible dejar pasar contenido dudoso que quemar la atención del usuario. Alertas por sesión es una métrica, no un detalle.

---

## 🏗️ Arquitectura

```
   ┌──────────── CLIENTES ────────────┐
   │  Extensión · App móvil · API     │
   └────────────────┬─────────────────┘
                    │
   ┌────────────────▼─────────────────┐
   │  N0  filtro local (gratis)       │
   │      ¿hay algo verificable?      │
   ├──────────────────────────────────┤
   │  N1  emparejamiento              │  ⭐ el corazón
   │      caché + verificaciones ya   │
   │      publicadas, translingüe     │
   ├──────────────────────────────────┤
   │  N2  análisis generativo (RAG)   │
   │      + módulo de contexto        │
   │      último recurso, menor       │
   │      confianza declarada         │
   ├──────────────────────────────────┤
   │  ‖   análisis retórico           │
   └────────────────┬─────────────────┘
                    │
   ┌────────────────▼─────────────────┐
   │  Contexto + fuentes + b/d/u      │
   └──────────────────────────────────┘
```

**Principio de orden:** emparejar primero, generar después. La mayoría de la desinformación ya fue investigada por alguien. Generar veredictos con un LLM es donde aparecen las alucinaciones y los falsos positivos, y donde competirías de frente contra empresas con muchos más recursos.

---

## 🗺️ Fases

| Fase | Alcance | Cierre |
|---|---|---|
| **0** Tesis | X · texto · español · extensión · eje contexto | Tesis defendida |
| **1** Producto | + inglés · Facebook · web · imágenes con C2PA | Usuarios activos · costo sostenible |
| **2** Escala | + multilingüe · emparejamiento translingüe · móvil (compartir) | Cobertura regional |
| **3** Multimodal / B2B | + video · audio · API · dashboard de campañas | Ingresos recurrentes |

> Las fases 2 y 3 son años con equipo. Se documentan para orientar decisiones de arquitectura hoy, no para prometerlas.

**Móvil:** vía flujo de compartir, no captura de pantalla. Los permisos de captura están severamente restringidos y las plataformas no autorizan lectura de contenido por esa vía.

---

## 💰 Modelo de negocio

| | Quién | Qué |
|---|---|---|
| **B2C** | Usuario final | Gratis con cuotas; plan pago sin límite |
| **B2B** | Medios, bancos, instituciones | API + dashboard de campañas |
| **LegalTech** | Estudios jurídicos | Peritaje y validación de evidencia digital |

⚠️ **Antes de comprometer nada con una empresa patrocinadora:** revisar el reglamento de titulación de la UDLA sobre propiedad intelectual. Ceder una participación mayoritaria de algo que aún no existe es una decisión que conviene consultar con la dirección de carrera y con un abogado. No es consejo legal.

⚠️ **Sobre recolectar pasivamente lo que analizan los usuarios para construir un dataset comercial:** tiene implicaciones de privacidad y de términos de servicio de las plataformas. Resolverlo antes, no después.

---

## ⚡ Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Falsos positivos destruyen la confianza | Umbral conservador · banda de abstención amplia · FPR como métrica principal |
| Fatiga de alertas | Tres grados de interrupción · sensibilidad ajustable |
| Costo del análisis permanente | Cascada de tres niveles · caché compartido · cuotas |
| Privacidad del feed completo | N0 corre local · al servidor solo hashes, vectores y lo que escala |
| Términos de servicio de las plataformas | Análisis bajo demanda del usuario · sin almacenamiento masivo |
| El LLM directo iguala al pipeline | Medirlo en semana 8, no en la 14 |
| Nombre ocupado | Cambiarlo antes de invertir en marca |

---

## 🎯 Lo que decide todo

```
1. ¿Emparejar primero o generar primero?   →  emparejar
2. ¿El eje contexto es el diferenciador?   →  sí
3. ¿Confianza de uno o dos números?        →  dos
4. ¿Veredicto o contexto?                  →  contexto
5. ¿Canal real de distribución?            →  validar con
                                              usuarios ANTES
                                              de programar
```
