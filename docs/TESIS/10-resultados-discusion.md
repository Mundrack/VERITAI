> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 10. Resultados y discusión

**Propósito.** Las cifras del arnés sobre el conjunto congelado, hipótesis
por hipótesis, con intervalos; el resultado de la predicción; el control
natural; y las amenazas a la validez y limitaciones, sin maquillar.

## Material que lo alimenta

| Qué | De dónde | Estado |
|---|---|---|
| Las cinco métricas de R02 §7 sobre el conjunto | `research/arnes/arnes.py` bloque 1 (conservadora y leniente, Wilson) | **pendiente**: correr sobre el CSV congelado |
| H3: FPR sobre controles con test aplicable | arnés bloque 2; umbral 10 % / límite ≤ 15 % (diseño §1) | **pendiente**; hoy A = 31 (0/31 daría límite 11,0 %; con 40, 8,8 %) |
| H1/H2: recall de 2b con intervalo | arnés bloque 3; diseño §4g (7/7 → [64,6; 100]) | **pendiente**; los 7 disparan en tests unitarios (`test_analisis_2b.py`) |
| Acuerdo agente–humano (kappa por eje) | arnés bloque 3; diseño §0 | **pendiente** (muestra del 25 %) |
| 2a: 0 de 43 con este método | DEC-034; `PROGRESO.md` §Jornada 2 | disponible; redacción fijada por Mateo: "2a no apareció en 43 casos recolectados con este método" |
| Hipótesis §4d: 2b solo donde el anexo no trae la tasa | diseño §4d (tabla de 8 operaciones) | disponible: 8 2b en 2 operaciones, 0 en las 6 con tasa |
| Predicción P1/P2 sobre EOAT0826 y CTH0926 | diseño §4h; `PROGRESO.md` §Jornada 5 | **pendiente** |
| Control natural: misma edición, mismo día, dos cálculos | diseño §4e (tablas CTH0726, CTH0826; ampliación jornada 4) | 7 registrados provisional frente a 6 registrados + 9 observados vigente; ~25 piezas de primavera todas vigente |
| Recuperabilidad por emisor y bloqueos | cubeta E: FMI y `interior.gob.es` 403 (DEC-032); SEPE, BdE, Portal 200 | disponible |
| Fallos de cobertura del mapa | abstención `PREVIOUS_EDITION_OUT_OF_MAP` en el arnés; puntos turísticos (tabla 2078) fuera del mapa (E048) | **pendiente** contar en el arnés |
| Amenazas a la validez | `research/PILOT-FINDINGS.md` §3 (dos poblaciones, hermanos, un buscador/una sesión, tiempos de agente); diseño §0 (anotador único que diseñó la taxonomía); encuadre (patrón de código del INE no documentado); diseño §4e ampliado (lectura estacional) | disponible |
| Limitaciones declaradas | DEC-035 (B = 7, no frecuencia); diseño §3 (A < 40 → H3 con intervalo ancho); §4g; cuota INE; España/Latinoamérica sin cuota (DEC-026) | disponible |
| Lo que la revisión de método cambió sobre la marcha | `research/PILOT-FAILURES.md` §5; DEC-029; DEC-034 ("último reencuadre del objeto") | disponible |
| Ablación y baseline LLM del `02-1` | no se hicieron | se declara |

## No entra

Ninguna cifra del piloto como confirmación (DEC-025). Ninguna afirmación
sobre intención ni sobre "la prensa española" (redacción de DEC-034).
