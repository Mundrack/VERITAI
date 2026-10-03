# Recolección del conjunto de evaluación — progreso

Reloj: marca `P3-J1 t0` en `research/cronometro.log` (2026-09-26T02:37Z).
Jornada = 4 h de reloj; tope 16 h; **revisión intermedia a las 8 h o a los 55
casos**, lo que llegue antes. Las pausas se marcan `P3-PAUSA<n>` (t0 inicio,
t2 fin) y el validador las descuenta.

Emisores del conjunto: **INE, Interior vía Portal Estadístico de Criminalidad,
SEPE y Banco de España** (DEC-032; FMI e interior.gob.es quedan como hallazgo
de bloqueo, cubeta E).

## JORNADA 5 — preinscrita el 2026-09-27 (DEC-035): prueba de predicción sobre EOAT0826 + A hasta 40 sin INE

**Se abre el 30 de septiembre de 2026**, cuando el INE publique la EOAT de
agosto (`EOAT0826`). *Corrección (2026-09-30): el calendario del INE fija
`EOAT0826` el 1 de octubre; Mateo abrió la jornada el 30 y la sesión 1 hizo P2
y los controles; P1 espera a la nota.* Hasta entonces no se recolecta nada. La predicción está
escrita en el diseño (§4h) y en el commit de esta sección, antes de la
publicación:

- **P1:** al menos un 2b entre las piezas regionales con tasa propia sobre
  `EOAT0826` (apartamentos o campings por CCAA). Confirmada con ≥ 1 en ≥ 6
  piezas; refutada con 0 en ≥ 8; inconclusa con < 6 localizadas.
- **P2:** ningún 2b en las piezas localizadas sobre ediciones de 2026 de las
  seis operaciones con tasa publicada (ETDP, Hipotecas, Sociedades, IPI,
  FRONTUR, EGATUR). Un solo 2b la refuta.
- Tasa base observada en la EOAT hasta hoy: 1 pieza con base provisional de
  11 localizadas.

**Además, en la misma jornada:** ≥ 9 controles A sin INE (SEPE junio/agosto
2026, BdE 2T2026 por CCAA del 30-09 y notas de mayo/julio, Portal anual 2025
si no está vetado), con criba, cronómetro y tres por edición. `CTH0926`
(23-10) **necesaria** (enmienda a DEC-035: única edición fuera del verano; sin
ella §4d no se separa de la lectura estacional). **Vía descartada:** seguir a las redacciones que ya
mostraron el mecanismo (§4j).

**Cubeta B declarada con 7** (E031, E042, E043, E047, E053, E055, E066; E056
excedente): Wilson 95 % del recall 7/7 → [64,6; 100]; 6/7 → [48,7; 97,4].
Limitación explícita de H1: 2b solo existe en 2 de las 8 operaciones del
mapa.

## JORNADA 4 (cuota de emisor + 2b dirigido a EOH/EOAT): CERRADA con **B = 1 → parar y replantear**

Regla previa (diseño §4b, la misma de la jornada 3): **B por jornada ≥ 4 →
sigue; ≤ 3 → se para y se replantea el mínimo con intervalo declarado.**
Reloj `P3-J4`: 2026-09-26 17:58:09Z → 18:28:19Z y 2026-09-27 17:03:11Z →
17:29Z = **0,9 h**. Entre ambos tramos la sesión quedó suspendida;
`P3-PAUSA5` se escribió retroactivamente el 27 al detectar el salto de fecha
(t0 = última marca real, t2 = primera marca nueva). **B = 1 → se para.**

Resultado: 9 casos trabajados (E058–E066), 9 candidatos (Q067–Q075), 0
rechazados. **Cuota de emisor (§4f) cumplida**: INE pasa de 39/57 (68,4 %) a
41/66 (62,1 %): SEPE julio 2026 ×3 (A), Banco de España junio 2026 ×2 (A),
Portal 1T2026 ×2 (A + D), INE EOAT0726 ×1 (C) y EOAT0526 ×1 (B).

| cubeta | jornada 4 | acumulado | objetivo (mín.) |
|---|---|---|---|
| A controles con test | 6 | 31 | 50 (40) |
| **B 2b esperada** | **1** | **7** (+1 excedente) | 20 (15) |
| C otras clases (2a, 3, 4, 2c, 1) | 1 | 2 | 15 (10) |
| D sin test | 1 | 10 | 10 (5) |
| E fallo de recuperación | 0 | 11 | 10 (5) |
| F claim falso | 0 | 3 | 5 (3) |
| O other_observed | 0 | 1 | — |

**El B de la jornada: E066**, El Nuevo Digital Murcia (2026-07-01, el mismo
día que la nota del INE): "los apartamentos [de la Región] recibieron un 60 %
más de viajeros (11.752)" y "42.396 noches (+25 %)". Solo sale con la base
provisional de mayo 2025 (anexo EOAT0525: 7.336 viajeros, 33.809 noches); con
la vigente (8.740; 35.167) es +34,5 % y +20,6 %. **Primer 2b fuera de la EOH
(EOAT, apartamentos)** y primera edición nueva con B (EOAT0526): confirma la
hipótesis §4d en la segunda operación sin tasa por CCAA.

**Los otros ocho**: E058 Junta de Andalucía (−9.661, −1,8 %, 526.862; SEPE
julio, A), E059 El Pespunte (Sevilla, "13.005 menos en seis meses": base
elegida, mismo signo, señal de horizonte 8×; A), E060 elDiario.es Cantabria
(−250, −0,94 %; A), E061 Tercera Información (deuda 1,76 bn, +4,2 %, 101,5 %;
BdE junio, A), E062 Catalunya Press (CCAA 355.000 M, +3,6 %; A), E063 El
Periòdic (Aldaia +79,7 %; Portal 1T2026, A: tope de controles de la edición),
E064 Aldaya Decidix ("lidera el aumento en la Comunitat": ranking recomputado
sobre los 68 municipios de la tabla 09003, cuadra; D) y **E065 elDiario.es
Cantabria (C, 2a *valor atribuido a otro periodo*)**: el artículo de julio
repite literalmente la frase de apartamentos y albergues del artículo de junio
(57.049, +1,3 %), cuando julio es 111.666 (−1,49 %). Hallado al cotejar con la
API mientras se buscaba 2b.

**Método.** (1) Cuota: nueve PDF mensuales del SEPE (diciembre 2025 a julio
2026 y julio 2025, todos 200 al agente identificado, ~700 KB cada uno) para
Andalucía, Sevilla y Cantabria; notas del BdE de junio y marzo de 2026; tabla
09003 del Portal (ya descargada para E036). (2) 2b dirigido por la hipótesis
§4d: tabla de tasas provisional/vigente por CCAA y provincia para CTH0326,
CTH0426, CTH0526 y CTH0626 (anexos CTH0325–CTH0625 + API `nult=20`) y para
EOAT0526, EOAT0626 y EOAT0726 (anexos EOAT0525–EOAT0725), y unas 40 búsquedas
con las cifras que solo salen con la provisional.

**Hallazgo principal: en las ediciones de marzo a junio la prensa regional
localizada usó la base vigente.** Unas 25 piezas comprobadas, todas vigente:
CTH0326 (Última Hora/EFE Baleares +14,5 %; ara.cat Girona +18,6 %), CTH0426
(Última Hora Baleares ≈ +4 %; Murcia Confidencial −1 %; leonoticias), CTH0526
(Valencia Plaza C. Valenciana +6,6 %; La Voz de Madrid +0,7 %; Gente Digital
La Rioja −12,7 % y Valladolid −3,2 %; viaempresa Cataluña +2,8 %; fibwidiario
Baleares +5,4 %; La Voz de Almería +11,8 %), CTH0626 (madridactual/EP Madrid
+1,2 % y residentes +4,2 %; Catalunya Press −2,1 %; Gente Digital/EP CyL
−4,4 % y Cantabria −5,1 %; La Nueva Crónica y Heraldo de León −3,1 %;
Florencio Sevilla ciudad, base 258.050 = vigente; Galicia Press +3 %,
indistinguible), EOAT0526 (Cantabria Económica campings +7,1 %; moncloa.com
Canarias −8,7 %), EOAT0626 (EP Andalucía; Crónica de Cantabria campings +13,9 %
y apartamentos +1,3 %; Galicia Press/EP 90.048 → 95.756) y EOAT0726 (EP
Andalucía; elDiario.es Cantabria campings +4 %; RTVC/eldiario Canarias −4,4 %;
Noticias de Navarra apartamentos +40,4 %; Galicia Press +10,5 %). Las mismas
redacciones que usaron la provisional en julio y agosto (EP Madrid, EFE
Baleares, El Debate CyL, Galicia Press) usaron la vigente en junio. Con lo
recolectado, el patrón de base provisional se concentra en **CTH0726, CTH0826
y EOAT0526** (y en redacciones concretas: MurciaEconomía y El Nuevo Digital
Murcia, ambas en Murcia). Hipótesis abierta, no probada: el mecanismo depende
del turno de redacción (verano) más que de la operación; la prueba barata es
EOAT0826 (30-09) y CTH0926 (23-10).

**Comprobaciones de método.** Los anexos de 2026 (CTH0526, CTH0626) coinciden
con la API de hoy para 2026: el INE no ha revisado 2026, así que las tablas
provisional/vigente son válidas. La revisión de 2025 ya estaba vigente el
2026-04-23 (Girona +18,6 % y Baleares +14,5 % solo salen con la vigente): 2b
era posible en todas las ediciones de 2026. Sevilla ciudad (puntos turísticos,
fuera del mapa) usó la vigente: no hay fallo de cobertura que anotar. El BdE
avisa en cada nota de que el avance se revisa, pero el cuadro mensual del PDF
no es texto extraíble (pdfplumber): un 2b sobre el avance del BdE queda como
NEEDS_REVIEW, no evaluado. La base de El Español (E033, julio: 1.763 → 1.744)
es la de la nota de junio; no se comprobó si la nota de julio la revisa.

**Lo que decide Mateo** (regla §4b: B = 1 ≤ 3 → parar): (a) declarar la
cubeta B con lo que hay (7 + 1 excedente, tres ediciones, dos operaciones) y
el intervalo; (b) jornada 5 sobre EOAT0826 (30-09) y CTH0926 (23-10) para
probar si el patrón de verano continúa; (c) rastrear las redacciones que ya
mostraron el mecanismo (El Nuevo Digital Murcia, MurciaEconomía, EFE Baleares,
EP Madrid, Galicia Press) edición a edición, que es barato pero sesga la
muestra hacia esas redacciones y hay que declararlo.

## JORNADA 3 (vía divergencia, B = 2b, medición): CERRADA con **B = 4 → sigue**

Regla previa, fijada por Mateo (diseño §4b): **B por jornada ≥ 4 → sigue;
B ≤ 3 → se para y se replantea el mínimo con intervalo declarado.** Reloj
`P3-J3`: 15:06:00Z → 15:34:40Z = **0,48 h**. Se cerró al alcanzar el umbral y
antes de las 4 h para que Mateo decida sobre la concentración por edición
(abajo) antes de seguir; la pausa `P3-PAUSA4` queda abierta.

Resultado: 14 casos trabajados (E044–E057), 14 candidatos (Q053–Q066), 0
rechazados.

| cubeta | jornada 3 | acumulado | objetivo (mín.) |
|---|---|---|---|
| A controles con test | 8 | 25 | 50 (40) |
| **B 2b esperada** | **4** | **7** | 20 (15) |
| C otras clases (2a, 3, 4, 2c, 1) | 0 | 1 | 15 (10) |
| D sin test | 1 | 9 | 10 (5) |
| E fallo de recuperación | 0 | 11 | 10 (5) |
| F claim falso | 1 | 3 | 5 (3) |
| O other_observed | 0 | 1 | — |

Los cuatro B de la jornada: E047 (EFE/Última Hora, Baleares agosto), E053
(EP/Galicia Press, Galicia julio, **con cambio de signo**: +0,68 % publicado
frente a −0,35 % vigente), E055 (El Debate/EP, Castilla y León agosto) y E056
(MurciaEconomía y teletipo regional, Murcia julio). Todos con
`evidencia_al_publicar` y `evidencia_vigente`, cada una con su fecha.

**Método que funcionó.** Recomputar, para cada CCAA y provincia, la tasa
interanual con la base **provisional** (anexo del año anterior, descargado con
`edicion_anterior.py`) y con la **vigente** (API), y buscar en prensa las
cifras que solo salen con la provisional. Cuatro B en 0,48 h de reloj; los
barridos genéricos ("pernoctaciones + CCAA + mes") dieron sobre todo
controles.

**Hallazgo sobre el mecanismo.** En la misma edición y la misma mañana unos
redactores calculan con la provisional y otros con la vigente (CTH0726: Galicia
Press y MurciaEconomía provisional; Lanza, Andalucía Información y EP Canarias
vigente. CTH0826: EP Madrid, EFE Palma y El Debate CyL provisional; LD
Canarias, EP Andalucía, EP Valencia, Galicia Press y los teletipos provinciales
de CyL vigente). El mecanismo es del redactor, no de la edición, y el INE no
publica la tasa por CCAA en el anexo de la EOH: cada agencia la calcula.

**Concentración, para que Mateo decida antes de la jornada 4.** Los 7 B del
conjunto salen de **dos ediciones de la misma operación** (EOH: CTH0726 con
E042, E043, E053, E056; CTH0826 con E031, E047, E055), siete redacciones
distintas. En ETDP, Hipotecas, Sociedades, IPI, FRONTUR y EGATUR el anexo trae
la tasa por CCAA y el mecanismo no aparece (E029, E040 usan la del INE); en
EOAT, EP usó la vigente en los dos casos trabajados (E049, E054). Propuesta:
un tope de B por edición (3, como el de controles) y buscar 2b en las ediciones
de la EOH de septiembre (sale el 23-10) y en meses anteriores (mayo, abril),
más el Banco de España (avance mensual revisado cada mes) como segunda
operación con revisión. Sin tope, la jornada 4 puede llenar B con la EOH y H1
quedaría evaluada sobre una sola operación.

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
DEC de replanteo.** Resuelto por **DEC-034**: la cubeta B pasa a ser 2b (base
revisada) y 2a queda como clase secundaria con su 0/43. Con eso, E031, E042 y
E043 pasan de C a B: **B = 3, C = 1** (la tabla de arriba es la foto al cerrar
la jornada, antes de la DEC). La condición bloqueante (edición anterior del INE
recuperable fuera de Tempus) está cumplida: `RECUPERABILIDAD-2B.md`.

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
periodo confirma 2a), **2a no apareció en 43 casos recolectados con este
método** (dos vías, cuatro emisores). El hallazgo es sobre la muestra y el
método, no sobre la prensa (corrección de redacción de Mateo). Los B del lote
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
| E043 | Q052 | C→B (DEC-034) | INE CTH0726 | Baleares residentes +3,8 % (vigente −2,3 %) | mixed / div, 2b |
| E044 | Q053 | A | INE CTH0626 | Madrid +1,2 % junio (EFE) | supported / no_div |
| E045 | Q054 | A | INE CTH0626 | Cataluña −2,1 % junio | supported / no_div |
| E046 | Q055 | A | INE CTH0526 | Madrid +0,7 % mayo | supported / no_div |
| E047 | Q056 | B | INE CTH0826 | Baleares agosto: clientes +3,8 %, noches −0,2 % (EFE, base provisional) | mixed / div, 2b |
| E048 | Q057 | A | INE CTH0726 | Málaga ciudad, extranjeros +15,57 % julio | supported / no_div |
| E049 | Q058 | A | INE EOAT0726 | Andalucía extrahoteleras +11,6 % julio (suma de 4 encuestas) | supported / no_div |
| E050 | Q059 | F | INE EOAT0626 | Madrid extrahoteleras +15,9 % junio "desde 460.550" (base inexistente) | contradicted / no_div |
| E051 | Q060 | A | INE CTH0826 | Canarias +2,5 % agosto | supported / no_div |
| E052 | Q061 | D | INE CTH0826 | Andalucía, mejor agosto desde 1999 | supported / undetermined |
| E053 | Q062 | B | INE CTH0726 | Galicia +0,68 % julio "frente a 1.325.548" (vigente −0,35 %) | mixed / div, 2b |
| E054 | Q063 | A | INE EOAT0626 | Galicia extrahoteleras +9,33 % junio | supported / no_div |
| E055 | Q064 | B | INE CTH0826 | Castilla y León −4,5 % agosto (vigente −3,2 %) | mixed / div, 2b |
| E056 | Q065 | B | INE CTH0726 | Murcia +4,09 % julio (vigente +3,32 %) | mixed / div, 2b |
| E057 | Q066 | A | INE CTH0726 | Castilla-La Mancha −6,7 % julio | supported / no_div |
| E058 | Q067 | A | SEPE julio 2026 | Junta: Andalucía −9.661 (−1,8 %), 526.862 | supported / no_div |
| E059 | Q068 | A | SEPE julio 2026 | Sevilla "13.005 menos en seis meses" (horizonte 8×) | supported / no_div |
| E060 | Q069 | A | SEPE julio 2026 | Cantabria −250 (−0,94 %) | supported / no_div |
| E061 | Q070 | A | BdE junio 2026 | deuda 1,76 bn, +4,2 %, 101,5 % | supported / no_div |
| E062 | Q071 | A | BdE junio 2026 | CCAA 355.000 M, +3,6 % | supported / no_div |
| E063 | Q072 | A | Interior 1T2026 | Aldaia 521, +79,7 % | supported / no_div |
| E064 | Q073 | D | Interior 1T2026 | Aldaia "lidera el aumento" (ranking) | supported / undetermined |
| E065 | Q074 | C | INE EOAT0726 | Cantabria apartamentos "57.049, +1,3 %" (es junio) | mixed / div, 2a otro periodo |
| E066 | Q075 | B | INE EOAT0526 | Murcia apartamentos +60 % viajeros (vigente +34,5 %) | mixed / div, 2b |

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

### Jornada 5, sesión 1 (2026-09-30 local; cronómetro 2026-10-01 00:43Z → pausa P3-PAUSA7)

- `robots.txt` consultado antes de la primera petición a cada dominio:
  www.ine.es (permite), servicios.ine.es (conexión reiniciada tres veces,
  sin respuesta HTTP; la API respondió 200 por el canal del conector),
  bde.es (prohíbe dos xlsx), ses.mir.es (no sirve `robots.txt`: redirige a
  la aplicación y a `error/404`), **sepe.es (prohíbe `/*.pdf$`, `/*.xlsx$`,
  `/*?` y noticias 2026 a `*`; deniega todo a los bots de Claude por nombre:
  SEPE vetado para el agente)**.
- **P1:** `EOAT0826` no existe aún (404 ×3); se publica el 1-10. Pendiente.
- **P2:** 6 piezas, 9 cifras, 3 operaciones (Hipotecas, Sociedades, ETDP de
  julio 2026): todas iguales a la tasa publicada por el INE; **0 2b**. IPI,
  FRONTUR y EGATUR sin pieza regional localizada.
- **Casos:** E067–E071, E073, E074 (A, 7) y E075 (F). E072 retirado (misma
  URL que E033). Validador OK: **A 38 / B 7 / C 2 / D 10 / E 11 / F 4 / O 1 =
  74**; INE 41/74 = 55,4 %; tope de 3 controles por edición respetado (BdE
  2T2026 en 3); B por edición sin cambios.
- Evidencia nueva en `research/evidencia/`: `J5_bde_2026t2.htm`,
  `J5_bde_a1309.pdf`, `J5_bde_a1310.pdf`, `J5_bde_mayo26.htm`,
  `J5_bde_julio26.htm`, `J5_portal_4T2025_1509010.csv`,
  `J5_api_1993_nult14.json`; anexos `D2B_EOAT0825.*`, `D2B_H0726.*`,
  `D2B_SM0726.*`, `D2B_ETDP0726.*`.
- **Decide Mateo:** los seis casos SEPE anteriores, descargados sin
  consultar el `robots.txt`; y cómo cubrir los dos A que faltan (BdE julio
  2026 admite dos; Portal 2025 admite uno).

### Jornada 5, sesión 2 (01:13Z del 2026-10-01; decisiones de Mateo)

- SEPE: los seis casos se mantienen; limitación escrita en diseño §3c; SEPE
  vetado desde ahora. E075 se queda como F (nota en la ficha). Observación
  del BdE en diseño §4m, sin clase ni cubeta.
- Dos A más con la nota de julio 2026 del BdE: E076 (Forbes/EP, ratio -2,4
  pp) y E077 (elDiario.es, CCAA +2,7%); la edición llega al tope (3 con
  E033). Asturias Hoy devolvió 403 (cerrado, DEC-021); Portal 2025 queda en 2.
- Validador OK: **A 40 / B 7 / C 2 / D 10 / E 11 / F 4 / O 1 = 76**; INE
  41/76 = 53,9 %. **A alcanza el mínimo de H3.**
- Pendiente: P1 sobre `EOAT0826` (1-10, con el método de §4h sin cambios).

### Jornada 5, sesión 3 (02:30Z del 2026-10-02; 2026-10-01 local): P1 sobre EOAT0826

- `EOAT0826` publicada el 2026-10-01; nota, PDF y anexo descargados (200).
  API tablas 1993 y 2016 con agosto de 2026 (provisional) y agosto de 2025
  (definitivo). 64 de 72 celdas con la base revisada: P1 evaluable.
- **7 redacciones con tasa propia** de apartamentos o campings por comunidad
  (Andalucía ×2, Cantabria, Murcia, Galicia, Baleares, Cataluña); **1 con
  base provisional** (El Nuevo Digital Murcia: apartamentos −17 %, campings
  −44 %; vigente −27,7 % y −38,3 %). **P1 confirmada para esta edición**
  (≥ 6 piezas, ≥ 1 2b). Tabla y límites en diseño §4h.
- Caso **E078** (B, `INE EOAT0826`, primer B de la edición). Límite
  declarado: misma redacción que E066.
- Hallazgos sin caso: EP Galicia (signo invertido en noches de campings) y
  EP Baleares (−3,59 % frente a −3,50 %), candidatos a F; decide Mateo.
- Pendiente: P1' sobre `CTH0926` (23-10). La jornada 5 sigue abierta.

### 2026-10-03: el registro de P1 sobre EOAT0826, completado y corregido (sin recolección)

No es una sesión de recolección: no se buscó, no se añadió ningún caso y el
cronómetro no se reanuda. La jornada 5 sigue abierta (`P3-PAUSA8`).

- **Direcciones de las siete piezas**, con su fecha de consulta, en diseño
  §4h (adenda). Copia local de cuatro: la de Murcia (ya estaba) y tres nuevas
  (ifomo, Galicia Press, Via Empresa), con `robots.txt` consultado una vez
  por dominio, pausa de 3 s y sha256. Script:
  `copiar_piezas_p1.py`; resumen: `evidencia/J5_P1_EOAT0826_piezas.json`.
- **Tres piezas sin copia** (Europa Press Andalucía y Baleares, leídas en
  Última Hora; El Conciso): esos dos sitios vetan por nombre a `ClaudeBot` y
  `anthropic-ai`. No se pidieron las páginas. **Decide Mateo.**
- **Corrección:** Europa Press Baleares no es candidato a F. −3,59 % frente a
  −3,501 % son 0,089 puntos, dentro de la tolerancia del sistema (0,15). La
  anotación anterior se conserva, con la corrección al lado (§4h).
- **Consultas de la sesión 3:** fueron 27, no 24. Las tres omitidas son de
  la segunda tanda por comunidades. Registro completo:
  `evidencia/J5_P1_EOAT0826_consultas.json`.
- **Observación §4n:** siete piezas de cinco cabeceras (Europa Press firma
  tres), y el único 2b es de la misma cabecera que E066.
- Sin cambios: veredicto de P1 (confirmada para esta edición), criterio,
  conteo, casos, cubetas. Validador: A 40 / B 8 / C 2 / D 10 / E 11 / F 4 /
  O 1 = 77.
- Las cuatro copias se guardan byte a byte (`.gitattributes`). Otros 18
  ficheros descargados de `evidencia/` tienen en git un sha256 distinto del
  anotado, por la normalización de finales de línea; no se han tocado.
- Pendiente de Mateo: el hallazgo de Europa Press Galicia (signo invertido),
  único candidato a F que queda sin caso; las tres copias; y los 18 ficheros.
- Pendiente: P1' sobre `CTH0926` (23-10).

Más tarde, el mismo día, con tres decisiones de Mateo:

- **Las tres copias que faltan las guarda una persona, a mano**, desde el
  navegador; la abstención del agente fue correcta. Nombres de fichero en
  diseño §4h. Todavía no están en la carpeta.
- **Evidencia byte a byte:** comprobados uno por uno los 18 ficheros. En 17,
  la copia de trabajo da el sha256 anotado al descargar; corregidos con la
  regla de `.gitattributes`. `J5_portal_20254_index.htm` no tiene sha256
  anotado en ningún sitio: no se tocó. Tabla en la bitácora.
- **Europa Press Galicia:** datos entregados a Mateo; decide él.
