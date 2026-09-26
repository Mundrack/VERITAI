# Recolección del conjunto de evaluación — progreso

Reloj: marca `P3-J1 t0` en `research/cronometro.log` (2026-09-26T02:37Z).
Jornada = 4 h de reloj; tope 16 h; **revisión intermedia a las 8 h o a los 55
casos**, lo que llegue antes, y ahí se para y se avisa a Mateo (DEC-031). Las
pausas se marcan `P3-PAUSA<n>` (t0 inicio, t2 fin) y el validador las descuenta.

Emisores del conjunto: **INE, FMI e Interior/DGT** (DEC-024: los que el sistema
puede correr). Latinoamérica entra por el FMI (WEO por país).

Ediciones **vetadas** por DEC-025 (usadas por el piloto o la Puerta 2): IPC
agosto 2026 (C11), EPA 2T2026 tasa de paro juvenil (C16, C17, P19), IPV 4T2025
(N01), EPA sector público 1T2026 (N03), IPC medias anuales 2020–2024 (N04),
sociedades mercantiles 2018 (P11), Balance de Criminalidad 2T2026 (C18),
condenados por delitos sexuales (P04), horas extra EPA (P16), y todo lo que
liste `PILOT-40.csv` (el validador lo comprueba por URL y texto).

## Estado al pausar (2026-09-26T02:43Z, `P3-PAUSA1` abierta)

```
reloj de recoleccion   ~0,1 h de 16 (solo E001 trabajado antes de la pausa)
candidatos             13 vistos (Q001-Q013; Q008 sin registrar, criba pendiente)
admitidos              10   trabajados 1 (E001, cubeta A)   pendientes de trabajar 9
rechazados             3    (Q003 duplicado, Q006 verificacion_directa Newtral, Q010 duplicado)
```

## Al reanudar, en este orden

1. `python research/scripts/cronometro.py P3-PAUSA1 t2 "reanuda"`.
2. **Criba (b)** para Q001, Q002, Q004, Q005, Q007, Q009, Q011, Q012, Q013:
   `"<claim> verificacion OR bulo OR fact-check"`. Si alguna cae, pasa a
   rechazado aunque esté trabajada (E001 incluido).
3. Q008 (Forbes Chile, FMI 2,4 % Chile 2026): criba (a) y (b); esperado D.
4. Trabajar en serie, con `t0/t1/t2` por caso: Q002 (tabla 6150 ya conocida,
   serie ETDP1824 segunda mano; cubeta O, P17), Q004 (HPT id 40: tabla de
   hipotecas sobre viviendas, número, nacional; nota H0626), Q011 y Q013
   (CNTR id 237: PIB volumen, variación trimestral; nota CNTR2T26), Q012
   (misma nota; nivel → D), Q005 y Q007 (FMI: WEO Update julio 2026 y WEO
   abril 2026; edición anterior de Ecuador = octubre 2025; datamapper solo
   sirve la vintage vigente), Q009 (DGT nota 2026-09-07 PDF y nota
   2025-09-03 con 228; patrón C18).
5. E001 `methodology_found`: comprobar si ETDP0726 enlaza la nota
   metodológica (hoy `no` con `NEEDS_REVIEW`).
6. Siguiente barrido: INE turismo (FRONTUR/EGATUR agosto, publicación
   2 de octubre: aún no), IPI y ventas minoristas de agosto (finales de
   septiembre), ECV 2025 / AROPE, ETCL 2T2026, población y nacimientos 1S2026,
   padrón; FMI por país (México, Argentina, Colombia, Perú, Chile) y WEO
   julio; Interior: Balance 1T2026 (abril), balance anual 2025, DGT semanal.
7. `python research/puerta3/validar_evaluacion.py` después de cada tanda;
   commit en `feat/puerta-3-recoleccion` con el diff a la vista.

## Jornada 1

| hora (UTC) | qué |
|---|---|
| 02:37 | inicio; barridos: INE compraventas/hipotecas/PIB, FMI España y LatAm, DGT verano |
| 02:41–02:43 | E001 trabajado (idealista, compraventas −5 %): tabla 6150, serie ETDP1826, −5,11 % |
| 02:43 | pausa (Mateo se mueve) |

## Casos (orden de admisión)

| E | Q | cubeta | emisor | claim (corto) | estado |
|---|---|---|---|---|---|
| E001 | Q001 | A | INE ETDP0726 | compraventas −5 % julio (idealista) | trabajado; criba (b) pendiente |
