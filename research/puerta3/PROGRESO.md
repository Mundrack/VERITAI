# Recolección del conjunto de evaluación — progreso

Reloj: marca `P3-J1 t0` en `research/cronometro.log` (2026-09-26T02:37Z).
Jornada = 4 h de reloj; tope 16 h; **revisión intermedia a las 8 h o a los 55
casos**, lo que llegue antes. Las pausas se marcan `P3-PAUSA<n>` (t0 inicio,
t2 fin) y el validador las descuenta.

Emisores del conjunto: **INE, FMI e Interior/DGT** (DEC-024).

Ediciones **vetadas** por DEC-025 (usadas por el piloto o la Puerta 2): IPC
agosto 2026 (C11), EPA 2T2026 tasa de paro juvenil (C16, C17, P19), IPV 4T2025
(N01), EPA sector público 1T2026 (N03), IPC medias anuales 2020–2024 (N04),
sociedades mercantiles 2018 (P11), Balance de Criminalidad 2T2026 (C18),
condenados por delitos sexuales (P04), horas extra EPA (P16), y todo lo que
liste `PILOT-40.csv` (el validador lo comprueba por URL y texto).

## REVISIÓN INTERMEDIA ANTICIPADA (2026-09-26 ~13:15Z)

Se para antes de las 8 h / 55 casos por dos bloqueos que necesitan decisión
de Mateo, no por falta de candidatos:

1. **Herramienta:** el presupuesto de búsquedas web de la sesión se agotó
   (200 de 200). Sin búsqueda no hay criba contra verificadores, y sin criba
   no se admite ningún candidato nuevo (regla dura, DEC-018). Tres candidatos
   quedaron a medio cribar y **no se registran como admitidos**:
   - ECP 1 de julio de 2026 (población 49,8 M, máximo histórico; Infobae
     2026-08-06 / Moncloa.com 2026-08-06): criba (a) limpia, (b) sin hacer.
   - ICM julio 2026 (ventas −0,2 %, recorta empleo por primera vez en casi
     cinco años; pressdigital 2026-08-28): sin criba.
   - Ejecuciones hipotecarias 2T2026 (+27,5 % vivienda habitual, máximo en
     nueve años; idealista 2026-09-16): sin criba.
2. **Publicadores:** `imf.org` devuelve **403** al agente identificado en API,
   HTML y PDF (E007; comprobado una vez por vía) e `interior.gob.es` devuelve
   **403** al PDF del Balance (E025). Dos de los tres emisores de DEC-024 no
   son recuperables-por-agente sin evadir (DEC-018). La DGT sí sirve su PDF de
   2026, pero su listado no enlaza notas de 2025 (E026: edición anterior no
   localizable). **Solo el INE alimenta la cubeta A hoy.**

Estado del lote al parar (salida de `validar_evaluacion.py`, ver bitácora):
31 candidatos, 26 admitidos y trabajados (E001–E026), 5 rechazados.

## Al reanudar (cuando Mateo decida)

1. `python research/scripts/cronometro.py P3-PAUSA2 t2 "reanuda"`.
2. Si se levanta el tope de búsquedas: criba (b) de los tres candidatos de
   arriba; nuevos barridos INE (ECP, ICM, ejecuciones hipotecarias, ETCL
   1T, EPA 3T cuando salga, Estadística de nacimientos/defunciones 1S2026,
   IPC septiembre el 30-09, hipotecas julio el 28-09, sociedades 2026).
3. FMI e Interior: decisión de Mateo (P-24 propuesta en la revisión): quitar
   del alcance, sustituir, o dejar como hallazgo con cubeta E.
4. `methodology_found` de todos los INE está en `no` con `NEEDS_REVIEW`:
   una pasada única sobre las notas para comprobar el enlace metodológico.
5. Validar y commitear tras cada tanda.

## Jornada 1

| hora (UTC) | qué |
|---|---|
| 02:37 | inicio; barridos: INE compraventas/hipotecas/PIB, FMI España y LatAm, DGT verano |
| 02:41–02:43 | E001 (idealista, compraventas −5 %) |
| 02:43–12:42 | pausa 1 (descontada) |
| 12:42–12:47 | criba (b) de los 9 admitidos; E002, E003 |
| 12:46–12:50 | E004, E005, E006 (PIB 2T2026, tres lecturas de la misma nota) |
| 12:49–12:55 | E007 (FMI): 403 en API, HTML y PDF; E008–E015 cerrados como bloqueados |
| 12:55–13:12 | E016–E024: IPI, FRONTUR, EGATUR, pernoctaciones, ADR, IPRI, ETCL ×3 |
| 13:12–13:15 | E025 Interior (403), E026 DGT (2026 sí, 2025 no localizable) |
| 13:15 | parada: presupuesto de búsquedas agotado; revisión intermedia anticipada |

## Casos (orden de admisión)

| E | Q | cubeta | emisor / edición | claim (corto) | resultado |
|---|---|---|---|---|---|
| E001 | Q001 | A | INE ETDP0726 | compraventas −5 % julio | supported / no_div |
| E002 | Q002 | O | INE ETDP0726 | "la compraventa" −6,1 % = segunda mano | mixed / div, other_observed (P17) |
| E003 | Q004 | A | INE H0626 | hipotecas +10,8 % junio | supported / no_div |
| E004 | Q011 | A | INE CNTR2T26 | PIB acelera al 0,7 % | supported / no_div |
| E005 | Q013 | A | INE CNTR2T26 | PIB crece 0,7 % | supported / no_div |
| E006 | Q012 | D | INE CNTR2T26 | "revisa a la baja sus previsiones" 2,6 % | supported / undetermined |
| E007 | Q005 | E | FMI WEO jul-26 | mantiene 2,1 % España | bloqueado (403) |
| E008 | Q007 | E | FMI WEO abr-26 | Ecuador 2 → 2,5 % | bloqueado |
| E009 | Q008 | E | FMI WEO abr-26 | Chile 2,4 %, ALC 2,3 % (nivel) | bloqueado |
| E010 | Q016 | E | FMI Art. IV jul-26 | Chile 2,2 → 1,8 % | bloqueado |
| E011 | Q017 | E | FMI WEO abr-26 | Argentina 4,0 → 3,5 % | bloqueado |
| E012 | Q018 | E | FMI WEO jul-26 | Argentina mantiene 3,5 % | bloqueado |
| E013 | Q019 | E | FMI WEO abr-26 | México 1,5 → 1,6 % | bloqueado |
| E014 | Q020 | E | FMI WEO jul-26 | México 1,6 → 1,2 % | bloqueado |
| E015 | Q023 | E | FMI WEO abr-26 | Chile 2,0 → 2,4 % | bloqueado |
| E016 | Q015 | A | INE IPI0726 | producción industrial 2,6 % julio | supported / no_div |
| E017 | Q024 | A | INE FRONTUR0726 | 58,1 M turistas, +4,6 % | supported / no_div |
| E018 | Q025 | A | INE EGATUR0726 | gasto 18.200 M, +10,9 % | supported / no_div |
| E019 | Q026 | A | INE CTH0826 | pernoctaciones +1,4 % | supported / no_div |
| E020 | Q027 | D | INE CTH0826 | habitación 167 € (nivel) | supported / undetermined |
| E021 | Q028 | A | INE IPRI0826 | precios industriales 13,2 % | supported / no_div |
| E022 | Q029 | A | INE ETCL2T26 | coste laboral +4 %, 3.388 € | supported / no_div |
| E023 | Q030 | D | INE ETCL2T26 | récord en 26 años | supported / undetermined |
| E024 | Q031 | A | INE ETCL2T26 | Murcia +3,1 %, 2.900 € | supported / no_div |
| E025 | Q014 | E | Interior Balance 1T26 | homicidios +10 % | bloqueado (403) |
| E026 | Q009 | E | DGT verano 2026 | 240 muertos, +10 | edición anterior no localizable |

Rechazados: Q003 (duplicado), Q006 (Newtral 2026-09-18), Q010 (duplicado),
Q021 y Q022 (explainer de Newtral 2026-06-04 sobre la ECV 2025).
