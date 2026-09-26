# Recolección del conjunto de evaluación — progreso

Reloj: marca `P3-J1 t0` en `research/cronometro.log` (2026-09-26T02:37Z).
Jornada = 4 h de reloj; tope 16 h; **revisión intermedia a las 8 h o a los 55
casos**, lo que llegue antes. Las pausas se marcan `P3-PAUSA<n>` (t0 inicio,
t2 fin) y el validador las descuenta.

Emisores del conjunto: **INE, Interior vía Portal Estadístico de Criminalidad,
SEPE y Banco de España** (DEC-032; FMI e interior.gob.es quedan como hallazgo
de bloqueo, cubeta E).

## JORNADA 2 (vía divergencia dirigida, medición DEC-033): CERRADA con **B = 0**

Reloj: `P3-J2 t0` 13:34:56Z → `P3-J2 t2` 14:30:15Z = **0,92 h de las 4 h
previstas**. Se cerró antes de agotar el reloj porque las vetas dirigidas se
agotaron (cada patrón se barrió con dos o tres formulaciones y en varios
emisores); seguir habría producido controles, no B. La pausa `P3-PAUSA3` queda
abierta a la espera de Mateo. Si quiere la ventana completa antes de decidir,
se reabre con `P3-PAUSA3 t2` y una nueva marca `P3-J2 t2` (manda la última).

Resultado: 17 casos trabajados (E027–E043) y 21 candidatos nuevos (Q032–Q052,
3 rechazados: Q035 Asnef, Q038 Registradores, Q048 edición vetada).

| cubeta | jornada 2 | acumulado | objetivo (mín.) |
|---|---|---|---|
| A controles con test | 6 | 17 | 50 (40) |
| **B 2a esperada** | **0** | **0** | 20 (15) |
| C otras clases | 4 | 4 | 15 (10) |
| D sin test | 5 | 8 | 10 (5) |
| E fallo de recuperación | 0 | 11 | 10 (5) |
| F claim falso | 2 | 2 | 5 (3) |
| O other_observed | 0 | 1 | — |

**Regla DEC-033 (diseño §3b): B = 0 → no se gasta la jornada 3 y se abre una
DEC de replanteo.** Pendiente de Mateo.

Vetas barridas y qué dieron:

1. **Signo mensual vs interanual** (compraventas mayo/julio, hipotecas
   abril/mayo, IPI abril, pernoctaciones junio, sociedades junio/julio; la
   criba se hizo primero sobre la API, buscando los meses con signos
   distintos): la prensa titula con la tasa del INE y deja la mensual en el
   cuerpo. 0 B.
2. **Desestacionalizado vs bruto** (paro de agosto): el Ministerio publica
   ambas; no hay base que el emisor no sostenga. 0 B.
3. **Base larga** ("desde 2018/2019/2023", "en la legislatura"): sin cambio de
   signo en las series con ediciones admisibles (IPC, salarios, compraventas,
   paro). 0 B.
4. **Institucional** (Moncloa, Ministerio de Trabajo, Juntas, Delegaciones
   del Gobierno, ayuntamientos, partidos): **un patrón B** (Delegación del
   Gobierno en Madrid: tasa por mil habitantes y "4,3 puntos menos desde
   2023" frente a +2,6 % interanual en recuento), pero en la edición 2T2026,
   **vetada por DEC-025** (Q048). Reaparece cada trimestre: la primera
   edición admisible es la del 3T2026 (diciembre). La misma veta dio un
   control del Portal (E036, Vox Alcorcón) y una clase 4 (E041, concejal de
   Alcorcón: "más del 70 % del aumento" es el 42 %).
5. **Teletipos regionales sobre la EOH** (EP, medios regionales): tres 2b
   (base provisional del año anterior: E031 Madrid agosto, E042 Madrid julio,
   E043 Baleares julio, **este último con cambio de signo**: +3,8 % frente a
   −2,3 %) y un control (E035 Canarias, base vigente). Veta productiva para
   C, no para B.
6. **Rankings y extremos**: D (E037 IPRI, E039 paro, E040 Navarra) y dos F
   (E034 euribor.com.es "desplome del 15 %", E038 Fotocasa "mejor julio desde
   2007": 2025 y 2007 fueron mayores).
7. **SEPE y Banco de España** como emisores nuevos: controles (E032, E033) y
   un D (E039). El Portal de Criminalidad sirve las tablas 1T y 2T bajo
   `DatosBalanceAct` (09001 CCAA, 09002 provincias, 09003 municipios).

Conclusión de la medición: bajo DEC-029 (solo cambio de signo o valor de otro
periodo confirma 2a), **B no aparece en la prensa española sobre INE, SEPE,
BdE y Portal**: los medios copian la comparación del emisor. Los B del lote
crudo venían de emisores institucionales (SEPE/Moncloa, CIS, Interior) y de
LatAm (DANE, INEGI): fuera del alcance actual o en ediciones vetadas. El
mecanismo dominante de la vía divergencia es **2b** (edición provisional
frente a revisada), que el prototipo no cubre porque Tempus no sirve
ediciones anteriores. Ambas cosas van a la DEC de replanteo.

Ediciones **vetadas** por DEC-025 (usadas por el piloto o la Puerta 2): IPC
agosto 2026 (C11), EPA 2T2026 tasa de paro juvenil (C16, C17, P19), IPV 4T2025
(N01), EPA sector público 1T2026 (N03), IPC medias anuales 2020–2024 (N04),
sociedades mercantiles 2018 (P11), Balance de Criminalidad 2T2026 (C18),
condenados por delitos sexuales (P04), horas extra EPA (P16), y todo lo que
liste `PILOT-40.csv` (el validador lo comprueba por URL y texto).

## REVISIÓN INTERMEDIA ANTICIPADA (2026-09-26 ~13:15Z) — histórico; resuelto con DEC-032 y DEC-033

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

## Al reanudar (lista de la revisión intermedia; histórico. Lo vigente está en la sección de la jornada 2)

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
| E027 | Q032 | D | INE ECP/censo | Xataka: 60 % de la población >45 | supported / undetermined |
| E028 | Q033 | A | Interior Portal 1T26 | homicidios +10 % | supported / no_div |
| E029 | Q036 | A | INE ETDP0726 | Euskadi −12,4 % | supported / no_div |
| E030 | Q037 | D | INE SM0726 | mejor julio en 31 años (sociedades) | supported / undetermined |
| E031 | Q039 | C | INE CTH0826 | Madrid +2,36 % agosto (base provisional) | mixed / div, 2b |
| E032 | Q041 | A | SEPE ago-26 | Madrid +2,5 % (mensual) | supported / no_div |
| E033 | Q042 | A | BdE deuda jul-26 | cae bajo el 100 % del PIB | supported / no_div |
| E034 | Q040 | F | INE H0426 | "desplome del 15 %" en abril | contradicted / no_div |
| E035 | Q044 | A | INE CTH0726 | Canarias +2,39 % julio | supported / no_div |
| E036 | Q043 | A | Interior Portal 1T26 | Alcorcón +30,2 % (Vox) | supported / no_div |
| E037 | Q045 | D | INE IPRI0826 | 13,2 %, récord en casi cuatro años | supported / undetermined |
| E038 | Q047 | F | INE ETDP0726 | Fotocasa: "mejor julio desde 2007" | contradicted / no_div |
| E039 | Q046 | D | SEPE ago-26 | mayor alza en agosto desde 2019 | supported / undetermined |
| E040 | Q049 | D | INE ETDP0726 | Navarra, donde más sube | supported / undetermined |
| E041 | Q050 | C | Interior Portal 1T26 | ciber = "más del 70 %" del aumento (42 %) | mixed / div, 4 |
| E042 | Q051 | C | INE CTH0726 | Madrid −1,43 % julio (base provisional) | mixed / div, 2b |
| E043 | Q052 | C | INE CTH0726 | Baleares residentes +3,8 % (vigente −2,3 %) | mixed / div, 2b |

Rechazados en la jornada 2: Q035 (Asnef, fuera de alcance), Q038
(Registradores, fuera de alcance), Q048 (Delegación del Gobierno en Madrid,
edición 2T2026 vetada por DEC-025: único patrón B de la jornada). Admitido sin
trabajar: Q034 (pressdigital, revisión anual del PIB; esperado D).

Rechazados: Q003 (duplicado), Q006 (Newtral 2026-09-18), Q010 (duplicado),
Q021 y Q022 (explainer de Newtral 2026-06-04 sobre la ECV 2025).

## Proyección de B por jornada (2026-09-26, tras DEC-032; antes de la jornada 2)

Base: lote crudo del piloto (31 casos desde la prensa): B 3/31 = 9,7 %, C
5/31 = 16 %, F 2/31 = 6,5 %; bajo DEC-029 (solo signo o valor de otro
periodo) B ≤ 9,7 %, se toma 6–10 %. Ritmo de la vía divergencia: 25–35 casos
admitidos por jornada de 4 h (cada candidato exige 2–3 búsquedas: descubrimiento
y dos cribas), frente a los 20+/h de la vía organismo.

```
                         por jornada        3,3 jornadas restantes
B sin dirigir (piloto)   2-3                7-10        < 15
B dirigido (patrones §1b, supuesto x2, NO medido)  4-6   13-20  >= 15 solo si el x2 se cumple
C                        4-5                13-17       ~ objetivo
F                        2                  6-7         ok
```

Cuello adicional: el tope de 200 búsquedas por sesión cubre 70–90 candidatos,
es decir, unas 2 jornadas de vía divergencia por sesión.

Propuesta al parar: **jornada 2 = una jornada de vía divergencia dirigida,
como medición**. Si al cerrarla B ≥ 4, la proyección sostiene 15 y se sigue;
si B ≤ 2, se replantea antes de gastar más (ampliar el tope en 2 jornadas, o
bajar el mínimo de B a 10 con intervalo declarado, o ambas). No se cuenta la
señal de horizonte como B (DEC-029).
