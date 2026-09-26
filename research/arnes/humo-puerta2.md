> **HUMO SOBRE CONJUNTO DE DESARROLLO — NO ES UNA EVALUACIÓN (DEC-025).**

# Arnés de evaluación — DESARROLLO (humo)

Generado 2026-09-26T02:04:06+00:00 · anotación `research/PILOT-40.csv` (51 filas) · resultados `research/puerta2/resultados` (10 veredictos) · pares evaluables **7**

Anotados sin veredicto (44): C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, C15, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C28, C29, C30, C31, P01, P02, P03, P05, P06, P07, P08, P09, P10, P12, P13, P14, P15, P17, P18, P20
Veredictos sin anotación (3): N01, N03, N04

## 1. Las cinco métricas de R02 §7 (sobre la anotación de los pares)

| métrica | conservadora | leniente | semáforo |
|---|---|---|---|
| Fuente primaria localizada | n/d (columna ausente) | n/d | n/d |
| Edición anterior localizada **(manda)** | 3/7 = 42.9 % [15.8; 75.0] | 3/7 = 42.9 % [15.8; 75.0] | ambar |
| Extracción sin intervención extrema (A|B) | 6/7 = 85.7 % [48.7; 97.4] | 6/7 = 85.7 % [48.7; 97.4] | verde |
| Clases de divergencia observadas (≥ 3) | 2: 2_baseline_selection, 3_absolute_vs_relative | — | ambar |
| Tiempo medio por caso, agente (< 20 min) | 2.4 min (n = 3, máx 3.3) | — | verde |

## 2. Falsos positivos (H3)

- **FPR sobre controles con test aplicable:** 0/1 = 0.0 % [0.0; 79.3] (regla de tres: 100.0)
- Falsos positivos: ninguno
- Controles con señal registrada (no cuentan, DEC-029): ninguno
- Controles sin test aplicable (fuera del denominador): ninguno
- Secundaria, disparos sobre todo lo anotado sin divergencia (incluye claims falsos): 1/2 = 50.0 % [9.5; 90.5] → C17
- **H3: no_evaluable** (tasa fijada 10 %, límite superior IC95 ≤ 15 %, mínimo n = 40)

## 3. Acuerdo sistema / anotación (adicional; no es de R02 §7)

- Verdad: 4/7 = 57.1 % [25.0; 84.2] · Contexto: 3/7 = 42.9 % [15.8; 75.0]
- 2a anotada detectada como 2a (recall): 1/1 = 100.0 % [20.7; 100.0] → P11
- Abstención cuando la anotación abstiene: 3/4 = 75.0 % [30.1; 95.4]

| contexto anotado → sistema | casos |
|---|---|
| divergence_detected -> divergence_detected | 1 |
| divergence_detected -> undetermined | 2 |
| no_divergence_detected -> divergence_detected | 1 |
| no_divergence_detected -> no_divergence_detected | 1 |
| no_divergence_detected -> undetermined | 1 |
| undetermined -> undetermined | 1 |

## 4. Casos

| caso | anotado (truth / context / clase) | sistema (truth / context / clase) | test | señales | acuerdo |
|---|---|---|---|---|---|
| P04 | contradicted / divergence_detected / 3_absolute_vs_relative | insufficient_evidence / undetermined / none | n/a | — | false / false |
| P11 | supported / divergence_detected / 2_baseline_selection | supported / divergence_detected / 2_baseline_selection | DISPARA cambio_de_signo | — | true / true |
| P16 | contradicted / no_divergence_detected / none | insufficient_evidence / undetermined / none | n/a | — | false / false |
| P19 | mixed / divergence_detected / 3_absolute_vs_relative | insufficient_evidence / undetermined / none | n/a | — | false / false |
| C11 | supported / undetermined / none | supported / undetermined / none | n/a | — | true / true |
| C16 | supported / no_divergence_detected / none | supported / no_divergence_detected / none | no dispara | — | true / true |
| C17 | contradicted / no_divergence_detected / none | contradicted / divergence_detected / 2_baseline_selection | DISPARA valor_atribuido_a_otro_periodo | — | true / false |
