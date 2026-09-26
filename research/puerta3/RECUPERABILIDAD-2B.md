# Recuperabilidad de la edición anterior del INE fuera de Tempus (condición bloqueante de DEC-034)

**Pregunta.** ¿Puede el agente identificado (DEC-018) recuperar el dato **tal como
se publicó** en una edición anterior de una estadística del INE, sin la API
Tempus, que solo sirve la edición vigente? Sin eso, 2b (base revisada) no se
puede demostrar y no sirve como clase principal.

**Respuesta: sí, en las cinco ediciones probadas** (cuatro operaciones distintas
más la base del caso E031). Los tres artefactos de cada edición anterior
responden `200` al agente identificado y el valor publicado difiere del vigente.

## Método

Herramienta: [`edicion_anterior.py`](edicion_anterior.py). Deriva las URLs del
**código de la nota** (`<OPERACION><MM><YY>` mensual, `<OPERACION><n>T<YY>`
trimestral), las descarga con el agente identificado, timeout y tope de bytes,
guarda estado HTTP, tamaño y sha256, lee en la nota HTML la fecha de publicación
y el titular, extrae la fila pedida del anexo y la contrasta con la serie
vigente de la API.

```
https://www.ine.es/dyngs/Prensa/<CODIGO>.htm             nota HTML
https://www.ine.es/dyngs/Prensa/<CODIGO>.pdf             nota PDF
https://www.ine.es/prensa/anexo_tablas/es/<CODIGO>.xlsx  anexo de tablas
```

Ejecución (2026-09-26, 14:49–14:53Z; marcas `D2B-*` en `cronometro.log`):

```
python research/puerta3/edicion_anterior.py CTH  2025-07 --fila "Balears, Illes" --hoja EOH_Hoja3 --serie EOT22194 --periodo-serie 2025-M07
python research/puerta3/edicion_anterior.py ETDP 2025-07 --fila TOTAL --serie ETDP1826 --periodo-serie 2025-M07
python research/puerta3/edicion_anterior.py H    2025-06 --fila TOTAL --serie HPT34618 --periodo-serie 2025-M06
python research/puerta3/edicion_anterior.py SM   2025-07 --fila TOTAL --serie SM21483  --periodo-serie 2025-M07
python research/puerta3/edicion_anterior.py CTH  2025-08 --fila "Madrid, Comunidad de" --hoja EOH_Hoja3 --serie EOT1766 --periodo-serie 2025-M08
```

## Resultado

| # | edición anterior | publicada | HTML / PDF / XLSX | valor **al publicar** (anexo) | valor **vigente** (API, 2026-09-26) | revisión |
|---|---|---|---|---|---|---|
| 1 | `CTH0725` EOH julio 2025 | 22/08/2025 | 200 / 200 / 200 | Balears, pernoctaciones: **10.987.630** (EOH_Hoja3, fila 23) | EOT22194 2025-M07: **10.974.122** | −13.508 |
| 2 | `ETDP0725` ETDP julio 2025 | 25/09/2025 | 200 / 200 / 200 | compraventas de viviendas, TOTAL: **64.730** (ETDP.5 y ETDP.11) | ETDP1826 2025-M07: **64.722** | −8 |
| 3 | `H0625` Hipotecas junio 2025 | 27/08/2025 | 200 / 200 / 200 | hipotecas sobre viviendas: **41.834** (titular: "fue de 41.834, un 31,7% más en tasa anual"; H.9) | HPT34618 2025-M06: **41.422** | −412 |
| 4 | `SM0725` Sociedades julio 2025 | 11/09/2025 | 200 / 200 / 200 | sociedades creadas, TOTAL: **10.902** (SM.1) | SM21483 2025-M07: **10.906** | +4 |
| 5 | `CTH0825` EOH agosto 2025 (base de E031) | 23/09/2025 | 200 / 200 / 200 | Madrid, pernoctaciones: **2.115.059** (EOH_Hoja3, fila 61) | EOT1766 2025-M08: **2.090.878** | −24.181 |

Los resúmenes con estado HTTP, tamaño, sha256, fecha, titular y fila extraída
están en `research/evidencia/D2B_<CODIGO>.json`; la nota HTML de cada edición
se guarda como `D2B_<CODIGO>.htm`. Los PDF y XLSX no se versionan (1,7 MB en
total): se vuelven a descargar y se comprueban por sha256.

## Qué demuestra y qué no

- **Recuperable por el agente:** sí, por derivación determinista del código de
  la nota; no hace falta buscador ni listado. Tiempo por edición: 5–40 s (tres
  descargas). Sin rechazos: el INE no bloquea al agente identificado.
- **La edición anterior existe como artefacto propio**, con su fecha de
  publicación dentro del documento ("publicados 22 de agosto de 2025"), lo que
  permite el campo `evidencia_al_publicar` con fecha, separado de
  `evidencia_vigente` con fecha de consulta (DEC-034).
- **Las revisiones son reales y de tamaño variable:** desde +4 sociedades hasta
  −24.181 pernoctaciones; en Baleares (residentes, E043) la revisión cambia el
  signo de la tasa interanual.
- **AMENAZA A LA VALIDEZ (no una nota al pie):** INEbase enlaza solo la
  última nota de cada operación y no hay un listado oficial de notas
  anteriores que el agente pueda recorrer (la ruta `notasPrensaAnteriores`
  devuelve 404). La recuperabilidad depende del **patrón de código de las
  notas, que el INE no documenta**. Es estable en las operaciones probadas,
  pero es una convención observada, no un contrato: **si el INE cambia el
  patrón, el conector de edición anterior se rompe y 2b deja de ser
  computable por el agente.** La mitigación no evita la rotura, la hace
  visible: el conector abstiene con `PREVIOUS_EDITION_NOT_FOUND` (nunca un
  valor inventado), las ediciones ya descargadas se conservan con su sha256,
  y la amenaza se declara en la tesis como límite de validez externa del
  conector, no de la clase. `NEEDS_REVIEW` para operaciones con códigos
  irregulares (p. ej. `IPV1T26`, `CNTR2T26`, EPA trimestrales) antes de darlo
  por general.
- **Límite:** el anexo cambia de hoja y de etiqueta entre operaciones
  (`EOH_Hoja3`, `Hoja9`, `Hoja 1`); el conector de 2b necesitará un mapa
  fila/hoja por operación, no una extracción genérica.
