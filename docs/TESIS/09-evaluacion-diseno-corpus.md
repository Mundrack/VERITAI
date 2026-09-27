> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 9. Evaluación: diseño experimental y corpus

**Propósito.** El diseño del conjunto de evaluación con sus reglas fijadas
antes de recolectar, y el corpus tal como quedó: composición, vías, emisores,
tiempos, y lo que pasó en cada jornada.

## Material que lo alimenta

| Qué | De dónde | Número (2026-09-27) |
|---|---|---|
| Diseño aprobado | `research/PUERTA-3-DISENO.md` §0–§3 (DEC-031) | cubetas A 50 (40), B 7 (7) desde DEC-035, C 15 (10), D 10 (5), E 10 (5), F 5 (3); total 97 (70) |
| Por qué 40 controles | diseño §1, tabla Wilson (n=40, k=1 → 12,9 %; n=50, k=2 → 13,5 %) | |
| Puerta 1 como antecedente del corpus | `research/PILOT-DECISION.md`, `COLECCION-LOTE-CRUDO.md` §2–§3, `PILOT-FINDINGS.md` | 31 admitidos; 23/31 = 74,2 %; por nivel de emisor en `COLECCION` §"Por nivel de emisor" |
| Composición del corpus | `research/puerta3/validar_evaluacion.py` (salida) y `evaluacion-anotacion.csv` | 66 casos (64 independientes); A 31, B 7 (+E056 excedente), C 2, D 10, E 11, F 3, O 1 |
| Emisores | validador, bloque "emisor de la primaria" | INE 41 (62,1 %), FMI 9, Interior 6, SEPE 6, BdE 3, DGT 1 |
| Vías de descubrimiento × cubeta | validador, bloque DEC-032 | busqueda_a_organismo 32 (0 divergencias), titular_prensa 34 (11 divergencias o claims falsos) |
| Ediciones y topes | validador: controles por edición ≤ 3; B por edición ≤ 3 (CTH0726 3, CTH0826 3, EOAT0526 1) | |
| Reloj y ritmo | validador: 3,0 h de 16; cronómetro por caso media 2,9 min | pausas descontadas, incluida `P3-PAUSA5` retroactiva (declarada) |
| Jornada 1 y revisión intermedia | `research/puerta3/PROGRESO.md` §Jornada 1, §Revisión intermedia (histórico); DEC-032 | |
| Jornada 2 (medición, B = 0) | `PROGRESO.md` §Jornada 2; DEC-033, DEC-034 | 2a: 0 de 43 casos con este método |
| Jornada 3 (B = 4 en 0,48 h) | `PROGRESO.md` §Jornada 3; diseño §4b | |
| Jornada 4 (cuota, B = 1) | `PROGRESO.md` §Jornada 4; diseño §4c–§4f | ~25 piezas regionales cotejadas, todas vigente salvo E066 |
| Jornada 5 (predicción P1/P2 + A hasta 40 + CTH0926 necesaria) | diseño §4h–§4i; `PROGRESO.md` §Jornada 5 preinscrita | **pendiente** (30-09 y 23-10) |
| Rechazados y vetados | `PROGRESO.md` (Q003, Q006, Q010, Q021, Q022, Q035, Q038, Q048); DEC-025 | |
| Congelado | sha256 del CSV en DEC (diseño §0) | **pendiente** |
| Muestra del 25 % anotada a ciegas por Mateo | diseño §0, DEC-031 | **pendiente** |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| 40 controles son el mínimo que tolera un falso positivo con la tasa de H3 | diseño §1 (tabla Wilson) | referencia del intervalo; el umbral sigue siendo convención (ver 3) | C7 |
| Un tope de tres casos por edición evita contar la misma nota muchas veces | diseño §1, §4c | literatura sobre pseudorréplica y muestras agrupadas | C7 |
| La cuota de emisor (INE ≤ 70 %) y ≥ 2 emisores por cubeta protegen la validez externa | diseño §1, §4f | justificación de cuotas de composición en corpus de evaluación | C7 |
| Los hermanos por criba (misma primaria, misma consulta) cuentan una vez | diseño §0 | muestras agrupadas | C7 |
| Excluir casos ya verificados es un criterio de novedad válido | diseño §0 | qué cubren los verificadores | C1, C9 |
| Una jornada tratada como medición con regla previa es un diseño legítimo | DEC-033, §4b | preinscripción | C10 |
| Declarar B con 7 e intervalo es preferible a seguir recolectando | DEC-035, §4g | reporte de estudios con n pequeño y potencia declarada | C7 |
| El 74,2 % de la Puerta 1 es la tasa natural sobre todos los admitidos | DEC-020; `PILOT-FINDINGS` §3.1 | nada bibliográfico; las amenazas ya están declaradas | — |

## No entra

Resultados del arnés (van en 10). Casos de desarrollo.
