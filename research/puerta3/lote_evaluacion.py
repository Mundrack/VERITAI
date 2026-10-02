"""Datos del CONJUNTO DE EVALUACION (Puerta 3): todos los candidatos, admitidos y rechazados.

Este archivo es DATOS, no logica. La logica esta en validar_evaluacion.py, que
lo valida, escribe los CSV y los JSON de los casos, e imprime el llenado de
cubetas y la proyeccion. Mismo patron que research/scripts/lote_crudo.py.

REGLAS QUE GOBIERNAN ESTE ARCHIVO (research/PUERTA-3-DISENO.md, DEC-031)
    - Nada del piloto ni de la Puerta 2, ni hermanos suyos (DEC-025).
    - Regla dura: sin articulo de verificacion previo (DEC-018); el primer
      rechazo del publicador cierra el caso (DEC-021).
    - Enums cerrados (normalizar_a_enums.py); `undetermined` si ningun test
      aplica; la senal de horizonte NO es divergencia (DEC-029).
    - Cada admitido lleva su cubeta objetivo (A-F), su edicion primaria (para
      el tope de 3 controles por nota de prensa), su hermano si lo tiene, y la
      ESTRUCTURA del claim (lo que recibe POST /analisis), escrita a mano y
      antes de ver ningun veredicto. Los tiempos se derivan del cronometro.
    - Los ids: Q### para candidatos (orden de descubrimiento), E### para
      admitidos (orden de admision).

DOS VIAS DE DESCUBRIMIENTO (DEC-032), registradas en `descubrimiento_via`
    control (A, D)         desde el organismo: nota/tabla -> prensa que la relaya
                           -> `busqueda_a_organismo`. Produce controles, no divergencias.
    divergencia (B, C, F)  desde la prensa: titulares con cifra y comparacion propia,
                           la primaria despues -> `titular_prensa`, `busqueda_de_rankings`,
                           `busqueda_de_encuestas`, `busqueda_por_tema`, `criba_negativa`.
    La via no cambia la anotacion: un titular correcto es un control A aunque venga
    de la via divergencia. El validador imprime cubeta x via.

EMISORES (DEC-032): INE (API Tempus), Interior via el Portal Estadistico de
    Criminalidad (ses.mir.es, CSV), SEPE; Banco de Espana de reserva. imf.org e
    interior.gob.es devolvieron 403 al agente identificado: hallazgo, no se evade.

CUBETAS (objetivo / minimo)
    A  controles con test aplicable       50 / 40   supported + no_divergence, cambio con base = referencia
    B  2a esperada                        20 / 15   cambio de signo o valor atribuido a otro periodo
    C  otras clases                       15 / 10   3, 4, 2c; 1 ilustrativa
    D  sin test aplicable                 10 /  5   nivel, extremo, umbral, compuesto: undetermined
    E  fallo de recuperacion              10 /  5   primaria o edicion anterior no localizable; bloqueado
    F  claims falsos                       5 /  3   contradicted sin divergencia
"""

from __future__ import annotations

OBJETIVO_CUBETA: dict[str, tuple[int, int]] = {
    "A": (50, 40),
    "B": (7, 7),  # DEC-035: declarada con 7 e intervalo; antes (20, 15)
    "C": (15, 10),
    "D": (10, 5),
    "E": (10, 5),
    "F": (5, 3),
    # Sin objetivo: divergencias `other_observed` que aparecen solas (mecanismo
    # candidato P17 o C10, u otro). Se recogen para el criterio de reaparicion
    # (DEC-027), no para llenar nada.
    "O": (0, 0),
}

# Dominios de verificadores usados en la consulta (a) de la criba, como en la TAREA 2.
DOMINIOS_VERIFICADORES = (
    "maldita.es newtral.es factual.afp.com verificat.cat efeverifica.com "
    "ecuadorchequea.com chequeado.com colombiacheck.com verificado.com.mx"
)

# Orden: el de descubrimiento (DEC-020). Un candidato visto durante la criba de
# otro va justo detras de el y lleva hermano_de.
CANDIDATOS: list[dict] = [
    # ---- jornada 1, barrido 1 (2026-09-26 02:37Z): INE mensuales, FMI, DGT ----------------
    # Criba: consulta (a) contra dominios de verificadores hecha; consulta (b) generica
    # ("verificacion OR bulo OR fact-check") PENDIENTE al reanudar. Si (b) encuentra
    # un articulo de verificacion, el candidato pasa a rechazado aunque este trabajado.
    dict(
        cid="Q001", case_id="E001",
        claim_text="Las compraventas de viviendas retroceden otro 5% en julio, según el INE",
        claim_date="2026-09-25",
        post_url="https://www.idealista.com/news/inmobiliario/vivienda/2026/09/25/915865-las-compraventas-de-viviendas-retroceden-otro-5-en-julio-segun-el-ine",
        post_url_tipo="prensa", emisor="idealista/news", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com compraventa viviendas julio 2026 INE 5,1%",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE compraventa de viviendas julio 2026 'según el INE' '%' interanual noticia septiembre 2026",
        collected_at="2026-09-26",
        # --- trabajo 2026-09-26 (E001 t0 02:41:13Z, t1 02:41:52Z, t2 02:43:15Z) ---
        fuente_primaria="INE - Estadistica de Transmisiones de Derechos de la Propiedad (ETDP), julio 2026: nota ETDP0726 + API Tempus tabla 6150",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETDP0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/6150",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: 61.417 compraventas de viviendas inscritas (provisional), -5,1% interanual; nuevas 13.289 (-1,4%), segunda mano 48.128 (-6,1%)",
        dato_anterior="julio 2025: 64.722 (definitivo); junio 2026: 59.288 (provisional). Serie mensual completa en la tabla 6150",
        raw_value_span_actual=(
            "[INE, nota ETDP0726, 2026-09-25] 'Las compraventas de viviendas inscritas disminuyeron un 5,1% "
            "respecto a julio de 2025' | 'El 21,6% de las viviendas transmitidas por compraventa en julio eran "
            "nuevas' | [INE API, tabla 6150, ETDP1826 'Total Nacional. General. Compraventa. Numero.'] "
            "2026-M07: 61417 (Provisional) || [idealista 2026-09-25, el claim] 'Las compraventas de viviendas "
            "retroceden otro 5% en julio, segun el INE'"
        ),
        raw_value_span_anterior=(
            "[INE API, tabla 6150, ETDP1826] 2025-M07: 64722 (Definitivo) | 2026-M06: 59288 (Provisional) | "
            "ETDP1824 segunda mano 2025-M07: 51240 -> 2026-M07: 48128 | ETDP1825 nueva 13482 -> 13289"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: el claim relaya la variacion interanual, que es la referencia del INE. Calculo: "
            "61.417/64.722 - 1 = -5,11%; el titular redondea a 5%. 'Otro' remite al descenso de junio (sexto "
            "del ano segun EFE). La nota de julio es provisional y julio 2025 ya es definitivo: la cifra de "
            "2026 puede revisarse en la siguiente edicion; se anota, no cambia la etiqueta. methodology_found=no: "
            "no se busco la nota metodologica en esta pasada (NEEDS_REVIEW al reanudar)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETDP0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="6150",
                         serie_nombre="Total Nacional. General. Compraventa. Número. ",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="ETDP, compraventas de viviendas inscritas, total nacional, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=61417, cambio_afirmado=-5, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Control: base = referencia interanual del emisor. El titular redondea -5,1% a 5%.",
        ),
    ),
    dict(
        cid="Q002",
        claim_text="La compraventa de viviendas registra una caída interanual del 6,1%",
        claim_date="2026-09-25",
        post_url="https://www.navarrainformacion.es/2026/09/25/la-compraventa-de-viviendas-registra-una-caida-interanual-del-61/",
        post_url_tipo="prensa", emisor="Navarra Información", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com compraventa viviendas julio 2026 INE 5,1%",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE compraventa de viviendas julio 2026 'según el INE' '%' interanual noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E002",
        # --- trabajo 2026-09-26 (E002 t0 12:42:58Z, t1 12:42:58Z, t2 12:43:05Z; primaria ya en mano por E001) ---
        fuente_primaria="INE - Estadistica de Transmisiones de Derechos de la Propiedad (ETDP), julio 2026: nota ETDP0726 + API Tempus tabla 6150",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETDP0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/6150",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: compraventas de viviendas TOTAL 61.417 (-5,1% interanual); segunda mano 48.128 (-6,1%); nueva 13.289 (-1,4%)",
        dato_anterior="julio 2025: total 64.722; segunda mano 51.240; nueva 13.482 (definitivos)",
        raw_value_span_actual=(
            "[INE, nota ETDP0726, 2026-09-25] 'Las compraventas de viviendas inscritas disminuyeron un 5,1% "
            "respecto a julio de 2025' | 'Viviendas usadas: descenso del 6,1%' | [INE API, tabla 6150, "
            "ETDP1824 'Total Nacional. Vivienda segunda mano. Compraventa. Numero.'] 2026-M07: 48128 "
            "(Provisional) | ETDP1826 'Total Nacional. General. Compraventa. Numero.' 2026-M07: 61417 || "
            "[Navarra Informacion 2026-09-25, el claim, titular] 'La compraventa de viviendas registra una "
            "caida interanual del 6,1%' | [cuerpo] 'se registraron 48.128 compraventas de viviendas de "
            "segunda mano, un 6,1% menos que un ano antes'"
        ),
        raw_value_span_anterior="[INE API, tabla 6150] ETDP1824 2025-M07: 51240 (Definitivo) | ETDP1826 2025-M07: 64722 (Definitivo)",
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta O (sin objetivo): el titular atribuye a 'la compraventa de viviendas' (total, -5,1%) la "
            "caida de la vivienda de segunda mano (-6,1%); el cuerpo lo dice bien. Mismo mecanismo que N01 "
            "(subgrupo presentado como el total): candidata P17 'agregacion con subgrupos', tercera "
            "aparicion contando P17 y N01, pero N01 es desarrollo; para el criterio de reaparicion "
            "(DEC-027) cuenta como PRIMERA del conjunto de evaluacion. truth=mixed: contra la serie que el "
            "titular nombra (total) la magnitud no cuadra (-6,1 vs -5,1) y la direccion si. Sin test "
            "computable hoy: el sistema no puede detectarlo (esperado: mixed / no_divergence). "
            "methodology_found=no: no buscada (NEEDS_REVIEW, como E001)."
        ),
        cubeta="O", hermano_de="", mecanismo_candidato="P17_agregacion_subgrupos",
        primaria_edicion="INE ETDP0726", conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="6150",
                         serie_nombre="Total Nacional. General. Compraventa. Número. ",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="ETDP, compraventas de viviendas inscritas (total), total nacional, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            cambio_afirmado=-6.1, unidad_cambio="pct", direccion_afirmada="baja",
            notas=("El titular habla de 'la compraventa de viviendas' sin restringir: se estructura sobre el "
                   "total. El -6,1% es el de segunda mano (ETDP1824)."),
        ),
    ),
    dict(
        cid="Q008",
        claim_text="El FMI prevé un crecimiento del 2,3% para América Latina y El Caribe y del 2,4%, para Chile este año",
        claim_date="2026-04-14",
        post_url="https://forbes.cl/economia-y-finanzas/2026-04-14/el-fmi-preve-un-crecimiento-del-23-para-america-latina-y-el-caribe-y-del-24-para-chile-este-ano",
        post_url_tipo="prensa", emisor="Forbes Chile", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="CL", tema="pib",
        criba_query_a="site:chequeado.com OR site:factual.afp.com OR site:colombiacheck.com OR site:maldita.es FMI Chile 2,4% 2026 proyección crecimiento abril",
        criba_query_b="FMI Chile crecimiento 2,4% 2026 América Latina 2,3% abril Forbes verificación OR bulo OR fact-check OR chequeo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI 2026 previsión crecimiento Ecuador OR México OR Colombia OR Argentina OR Perú OR Chile 'Perspectivas de la Economía Mundial' julio OR abril 2026 '%' noticia",
        collected_at="2026-09-26", case_id="E009",
        # --- trabajo 2026-09-26 (E009 t0/t1/t2 12:54:59Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - WEO abril 2026 (Cuadro 1.1 p.28-30 y anexo p.69)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf); 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO abril 2026: 'Chile 2,3 2,4 2,6' (p.69) -> 2026 = 2,4%; 'America Latina y el Caribe 2,4 2,3 2,7' (p.28) -> 2026 = 2,3%",
        dato_anterior="WEO abril 2026, Cuadro 1.1: ALC dif. vs ene-2026 0,0; vs oct-2025 0,0. Chile: sin columna de diferencia en el anexo",
        raw_value_span_actual="[FMI, WEO abril 2026, text.pdf p.69] 'Chile 2,3 2,4 2,6 4,2 2,9 3,3 —2,3 —0,8 —1,8 8,5 8,1 7,6' | [p.28] 'America Latina y el Caribe 2,4 2,3 2,7 0,1 0,0 0,0 0,1' || [Forbes Chile 2026-04-14, el claim] 'El FMI preve un crecimiento del 2,3% para America Latina y El Caribe y del 2,4%, para Chile este ano'",
        raw_value_span_anterior="[FMI, WEO abril 2026, p.28] ALC 2026: dif. vs enero 0,0, vs octubre 0,0",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). Claim de NIVEL (dos proyecciones): sin test aplicable "
            "-> undetermined (DEC-029). Los dos numeros cuadran con el texto del PDF de abril."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO 2026-04",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="nivel",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Chile. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Chile para 2026, por edicion"),
            periodo_objetivo="2026-M04", valor_objetivo=2.4,
            notas="Nivel; el 2,3 de ALC es un segundo numero del mismo claim (una metrica por claim).",
        ),
    ),
    dict(
        cid="Q003",
        claim_text="Julio deja 61.417 operaciones de vivienda tras un descenso del 5,1% en las compraventas",
        claim_date="2026-09-25",
        post_url="https://www.andaluciainformacion.es/articulo/espana/julio-deja-61417-operaciones-vivienda-descenso-51-compraventas/202609250955223487974.html",
        post_url_tipo="prensa", emisor="Andalucía Información", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="", criba_query_b="",
        criba_resultado="rechazado",
        criba_motivo="duplicado: misma afirmacion (61.417, -5,1%) y misma nota INE ETDP0726 que Q001; teletipo. No es la regla dura",
        criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE compraventa de viviendas julio 2026 'según el INE' '%' interanual noticia septiembre 2026",
    ),
    dict(
        cid="Q004",
        claim_text="La firma de hipotecas retoma las subidas y crece un 10,8% en junio, según el INE",
        claim_date="2026-08-26",
        post_url="https://www.idealista.com/news/finanzas/hipotecas/2026/08/26/911268-la-firma-de-hipotecas-retoma-las-subidas-y-crece-un-10-8-en-junio-segun-el-ine",
        post_url_tipo="prensa", emisor="idealista/news", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com hipotecas junio 2026 INE 10,8%",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE hipotecas julio 2026 'según el INE' firma de hipotecas sube OR baja '%' noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E003",
        # --- trabajo 2026-09-26 (E003 t0 12:43:46Z, t1 12:45:51Z, t2 ~12:48Z) ---
        fuente_primaria="INE - Estadistica de Hipotecas (H), junio 2026: nota H0626 + API Tempus tabla 76316",
        primaria_url="https://www.ine.es/dyngs/Prensa/H0626.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/76316",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="junio 2026: 45.907 hipotecas sobre viviendas inscritas (provisional), +10,8% interanual; importe medio 178.365 euros (+6,0%)",
        dato_anterior="junio 2025: 41.422 (definitivo); mayo 2026: 42.213 (provisional)",
        raw_value_span_actual=(
            "[INE, nota H0626, 2026-08-26] 'El numero de hipotecas sobre viviendas inscritas en los registros "
            "de la propiedad fue de 45.907' | 'un 10,8% mas en tasa anual' | [INE API, tabla 76316, HPT34618 "
            "'Viviendas. Numero de hipotecas. Total Nacional. Base nueva. Mensual.'] 2026-M06: 45907 "
            "(Provisional) || [idealista 2026-08-26, el claim] 'La firma de hipotecas retoma las subidas y "
            "crece un 10,8% en junio, segun el INE'"
        ),
        raw_value_span_anterior="[INE API, tabla 76316, HPT34618] 2025-M06: 41422 (Definitivo) | 2026-M05: 42213 (Provisional)",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: el claim relaya la tasa anual, referencia del INE. Calculo: 45.907/41.422 - 1 = +10,83%. "
            "'Retoma las subidas' remite a que mayo bajo (no verificado aqui: solo el numero del claim). La nota "
            "no dice 'mejor junio desde 2010'; eso lo anaden otros medios (brainsre, que.es). Localizar costo mas "
            "que en E001: la tabla nacional mensual (76316) no lleva 'vivienda' en el nombre, hubo que listar las "
            "40 tablas de la operacion. methodology_found=no: no buscada (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE H0626",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="76316",
                         serie_nombre="Viviendas. Número de hipotecas. Total Nacional. Base nueva. Mensual. ",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="Estadistica de Hipotecas, hipotecas sobre viviendas inscritas, total nacional, mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=45907, cambio_afirmado=10.8, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = referencia interanual del emisor.",
        ),
    ),
    dict(
        cid="Q005",
        claim_text="El FMI mantiene que España crecerá el 2,1% en 2026, más del doble que la eurozona (0,9%)",
        claim_date="2026-07-08",
        post_url="https://www.elconciso.es/coyuntura/fmi-mantiene-crecimiento-espana-2026_0_2007365627.html",
        post_url_tipo="prensa", emisor="El Conciso", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com FMI España 2,1% 2026 julio previsión eurozona",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 actualización perspectivas 'eleva' OR 'rebaja' OR 'mantiene' previsión crecimiento España 2026 '%' noticia",
        collected_at="2026-09-26", case_id="E007",
        # --- trabajo 2026-09-26 (E007 t0 12:49:31Z, t1 12:54:14Z, t2 12:54:14Z) ---
        fuente_primaria="FMI - Actualizacion de Perspectivas de la economia mundial (WEO), julio 2026, y WEO abril 2026 (edicion anterior)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/07/08/world-economic-outlook-update-july-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf) + API datamapper; TODAS con 403 al agente identificado",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO update julio 2026: Espana 2026 = 2,1% (segun la prensa; la fila esta en la tabla-IMAGEN de la p. 16 del PDF, sin texto); zona del euro 2026 = 0,9% (texto del PDF, p. 7)",
        dato_anterior="WEO abril 2026, Cuadro 1.1 (texto, p. 28): 'Espana 2,8 2,1 1,8 —0,2 —0,1 0,1 0,1' = 2025 2,8; 2026 2,1; 2027 1,8; dif. vs ene-2026: -0,2/-0,1; vs oct-2025: +0,1/+0,1",
        raw_value_span_actual=(
            "[FMI, WEO update julio 2026, text.pdf p.7] 'En el caso de la zona del euro, se proyectan tasas de "
            "crecimiento del 0,9% en 2026' | [p.2] 'Se proyecta que el crecimiento mundial sea del 3,0% en 2026 "
            "y del 3,4% en 2027' | [p.16] tabla de proyecciones como IMAGEN: fila de Espana NO legible como "
            "texto (NEEDS_REVIEW para lectura humana) || [El Conciso 2026-07-08, el claim] 'El FMI mantiene que "
            "Espana crecera el 2,1% en 2026, mas del doble que la eurozona (0,9%)'"
        ),
        raw_value_span_anterior="[FMI, WEO abril 2026, text.pdf p.28, Cuadro 1.1] 'Espana 2,8 2,1 1,8 —0,2 —0,1 0,1 0,1' | 'Zona del euro 1,4 1,1 1,2 —0,2 —0,2 —0,1 —0,2'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO: la primera peticion del caso (API datamapper, 12:50Z) devolvio 403 al agente "
            "identificado; despues 403 en las paginas HTML (en/es) y en el PDF (prueba unica 12:54Z). DEC-021: "
            "el primer rechazo cierra el caso; los PDF que llegaron por el cliente de WebFetch no cuentan para "
            "el agente y se usan solo para la anotacion humana. HALLAZGO: imf.org rechaza al agente en las tres "
            "vias (API, HTML, PDF): el FMI, emisor de DEC-024, no es recuperable-por-agente sin evadir. Ademas "
            "la tabla de proyecciones de la actualizacion de julio es una IMAGEN dentro del PDF (formato "
            "hostil); la de abril es texto. Anotacion: abril 2,1 verificado en texto; julio 2,1 solo por prensa "
            "(NEEDS_REVIEW); 0,9 de la eurozona verificado en texto. Comparacion correcta entre ediciones: "
            "no_divergence. Estructura con emisor FMI: el sistema no lo corre hoy (sin conector)."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO update 2026-07",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO",
                         serie_nombre="España. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Espana para 2026, por edicion (mes de publicacion)"),
            periodo_objetivo="2026-M07", periodo_base="2026-M04",
            valor_objetivo=2.1, valor_base=2.1, cambio_afirmado=0, unidad_cambio="pp", direccion_afirmada="igual",
            notas="Periodos = ediciones del WEO (julio 2026 vs abril 2026). Emisor sin conector: sin veredicto hoy.",
        ),
    ),
    dict(
        cid="Q006",
        claim_text="El FMI ratifica a España como la economía que más crece de la eurozona en 2026",
        claim_date="2026-07-08",
        post_url="https://www.cronista.com/espana/economia-finanzas/el-fmi-ratifica-a-espana-como-la-economia-que-mas-crece-de-la-eurozona-en-2026/",
        post_url_tipo="prensa", emisor="El Cronista España", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com FMI España 2,1% 2026 julio previsión eurozona",
        criba_query_b="",
        criba_resultado="rechazado",
        criba_motivo="verificacion_directa: Newtral (2026-09-18) verifica 'España no es la economia de la zona euro que mas crece' sobre la misma afirmacion (dicha por Urtasun)",
        criba_url_verificacion="https://www.newtral.es/espana-zona-euro-factcheck/20260918/",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 actualización perspectivas 'eleva' OR 'rebaja' OR 'mantiene' previsión crecimiento España 2026 '%' noticia",
    ),
    dict(
        cid="Q007",
        claim_text="FMI mejora la proyección de crecimiento para la economía de Ecuador en 2026",
        claim_date="2026-04-14",
        post_url="https://www.primicias.ec/economia/fmi-mejora-proyeccion-crecimiento-pib-economia-ecuador-reuniones-primavera-120378/",
        post_url_tipo="prensa", emisor="Primicias", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="EC", tema="pib",
        criba_query_a="site:ecuadorchequea.com OR site:chequeado.com OR site:factual.afp.com OR site:colombiacheck.com FMI Ecuador crecimiento 2026 proyección abril",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI 2026 previsión crecimiento Ecuador OR México OR Colombia OR Argentina OR Perú OR Chile 'Perspectivas de la Economía Mundial' julio OR abril 2026 '%' noticia",
        collected_at="2026-09-26", case_id="E008",
        # --- trabajo 2026-09-26 (E008 t0/t1/t2 12:54:58Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - WEO abril 2026 (Cuadro anexo A4, p. 69 y p. 163 del PDF) y WEO octubre 2025 (edicion anterior)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf); 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO abril 2026, p.69: 'Ecuador 3,7 2,5 2,5' (2025, 2026, 2027) -> 2026 = 2,5%",
        dato_anterior="edicion anterior (WEO oct-2025): 2,0% segun la prensa; NO verificado en la primaria (la actualizacion de enero no cubre Ecuador)",
        raw_value_span_actual="[FMI, WEO abril 2026, text.pdf p.69] 'Ecuador 3,7 2,5 2,5 0,7 2,9 1,6 5,8 5,2 4,6 3,1 3,1 3,1' || [Primicias 2026-04-14, el claim] 'FMI mejora la proyeccion de crecimiento para la economia de Ecuador en 2026' | [cuerpo] 'preveia que la economia de Ecuador crezca 2% en 2026, pero ... proyecta un crecimiento de 2,5%'",
        raw_value_span_anterior="NEEDS_REVIEW: 2,0% (WEO octubre 2025) sin span de la primaria; solo prensa",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007; no se repitio la peticion). Anotacion humana: 2,5 "
            "verificado en el texto del PDF de abril; el 2,0 de la edicion anterior queda NEEDS_REVIEW. "
            "Comparacion entre ediciones consecutivas = referencia del FMI: no_divergence."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO 2026-04",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Ecuador. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Ecuador para 2026, por edicion"),
            periodo_objetivo="2026-M04", periodo_base="2025-M10",
            valor_objetivo=2.5, valor_base=2.0, cambio_afirmado=0.5, unidad_cambio="pp", direccion_afirmada="sube",
            notas="Periodos = ediciones del WEO. Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q009",
        claim_text="240 muertos en carreteras en verano 2026, diez más que en 2025: el balance de la DGT que alerta del aumento de accidentes",
        claim_date="2026-09-07",
        post_url="https://www.moncloa.com/2026/09/07/muertos-carreteras-verano-2026-dgt-3427559/",
        post_url_tipo="prensa", emisor="Moncloa.com", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="trafico",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com DGT verano 2026 240 fallecidos 4%",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="DGT balance verano 2026 fallecidos carreteras '%' respecto a 2025 noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E026",
        # --- trabajo 2026-09-26 (E026 t0 13:12:36Z, t1 13:12:41Z, t2 13:15:01Z) ---
        fuente_primaria="DGT (Ministerio del Interior) - nota de prensa 'Balance verano 2026' (2026-09-07, PDF); edicion anterior: nota DGT verano 2025 (2025-09-03), NO localizada por el agente",
        primaria_url="https://www.dgt.es/export/sites/web-DGT/.galleries/downloads/nota_prensa/2026/20260907-240-fallecidos-verano-2026/nota-de-prensa.pdf",
        primaria_url_tipo="PDF de nota de prensa en dgt.es (HTTP 200 al agente identificado); el listado de notas solo enlaza 2026 (categorias Balances y fallecidos sin 2025)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="no",
        historical_series_found="no", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="C", formato="pdf",
        dato_actual="verano 2026 (julio y agosto): 218 siniestros mortales, 240 fallecidos en vias interurbanas, '+4% (+10)' respecto al verano anterior; 926 hospitalizados (-10%); usuarios vulnerables -12%",
        dato_anterior="verano 2025: 230 fallecidos, IMPLICITO en la nota de 2026 (240 - 10); la nota DGT de 2025-09-03 (que segun Dvuelta decia 228) no se localizo desde el listado de la DGT",
        raw_value_span_actual=(
            "[DGT, nota 2026-09-07, PDF p.2] 'Durante los meses de julio y agosto se han registrado 218 "
            "siniestros mortales en carretera en los que han fallecido 240' | 'con el verano pasado, supone un "
            "aumento del 4% de las victimas mortales (+10)' | [p.4] 'el verano finaliza con 240 fallecidos en "
            "las carreteras, una cifra muy similar a la registrada en los dos ultimos veranos' || [Moncloa.com "
            "2026-09-07, el claim] '240 muertos en carreteras en verano 2026, diez mas que en 2025: el balance "
            "de la DGT que alerta del aumento de accidentes'"
        ),
        raw_value_span_anterior="NO LOCALIZADA por el agente: sin span de la nota 2025. Referencia externa (no verificador): Dvuelta afirma que la nota de 2025-09-03 decia 228",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="localizar", bucket_resultado="edicion_anterior_no_localizable", excedente="no",
        notas=(
            "Cubeta E: edicion anterior no localizable por el agente. dgt.es sirvio el PDF de 2026 (200) pero "
            "su listado de notas (y las categorias Balances/fallecidos) solo enlaza 2026; dos patrones de URL "
            "de 2025 dieron 404; se abandono la localizacion a los ~2,5 min (tope por caso). Un humano la "
            "localiza por buscador (Dvuelta la cita). El claim relaya la comparacion de la DGT (240 vs 230, "
            "+10): supported / no_divergence, patron C18: si la nota de 2025 decia 228 (provisional) y la de "
            "2026 usa 230 (consolidado), la comparacion provisional-vs-consolidado infraestima la subida (+5,3% "
            "vs +4%): 2b LATENTE en la primaria, no en el claim; se registra para la muestra a ciegas de Mateo. "
            "Sin conector de Interior/DGT: sin veredicto hoy."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="DGT verano 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Interior", tabla="DGT balance verano",
                         serie_nombre="Fallecidos en vias interurbanas, julio y agosto",
                         unidad="personas", referencia_principal="interanual",
                         descripcion="DGT, fallecidos en siniestros de trafico en vias interurbanas durante julio y agosto, por verano"),
            periodo_objetivo="2026", periodo_base="2025",
            valor_objetivo=240, valor_base=230, cambio_afirmado=10, unidad_cambio="abs", direccion_afirmada="sube",
            notas="Periodos anuales (verano de cada ano). Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q010",
        claim_text="240 personas mueren en las carreteras durante el verano de 2026, un 4 % más que el año pasado",
        claim_date="2026-09-08",
        post_url="https://www.thursdaydailybulletin.es/2026/09/08/240-personas-mueren-en-las-carreteras-durante-el-verano-de-2026-un-4-mas-que-el-ano-pasado/",
        post_url_tipo="prensa", emisor="Thursday Daily Bulletin", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="trafico",
        criba_query_a="", criba_query_b="",
        criba_resultado="rechazado",
        criba_motivo="duplicado: misma afirmacion y misma nota DGT 2026-09-07 que Q009. No es la regla dura",
        criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="DGT balance verano 2026 fallecidos carreteras '%' respecto a 2025 noticia septiembre 2026",
    ),
    dict(
        cid="Q011",
        claim_text="El PIB acelera su crecimiento al 0,7% en el segundo trimestre por el tirón del consumo y la inversión",
        claim_date="2026-09-25",
        post_url="https://www.teleprensa.com/nacional-3/economia/amp-pib-acelera-crecimiento-07-segundo-trimestre-tiron-consumo-inversion/202609251224042516451.html",
        post_url_tipo="prensa", emisor="Teleprensa", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com PIB segundo trimestre 2026 0,7% INE revisión",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'Contabilidad Nacional Trimestral' PIB segundo trimestre 2026 revisado OR 'datos revisados' crece '%' noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E004",
        # --- trabajo 2026-09-26 (E004 t0 12:46:47Z, t1 12:48:49Z, t2 12:48:49Z) ---
        fuente_primaria="INE - Contabilidad Nacional Trimestral (CNTR), 2T2026: nota CNTR2T26 + API Tempus tabla 67824",
        primaria_url="https://www.ine.es/dyngs/Prensa/CNTR2T26.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/67824",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: PIB volumen, ajustado, variacion trimestral 0,6847% (nota: 0,7%); interanual 2,6374% (2,6%); indice 126,4212",
        dato_anterior="1T2026: variacion trimestral 0,6298% (0,6%); interanual 2,6205%; indice 125,5615. Todo provisional",
        raw_value_span_actual=(
            "[INE, nota CNTR2T26, 2026-09-25] 'El PIB registro una variacion del 0,7% en el segundo trimestre "
            "respecto al trimestre anterior en terminos de volumen. Esta tasa fue una decima superior a la del "
            "primer trimestre de 2026.' | 'el gasto en consumo final de los hogares se incremento un 1,2%' | "
            "[INE API, tabla 67824, CNTR6653 'Total Nacional. Datos ajustados... Producto interior bruto a "
            "precios de mercado. Variacion trimestral. Indices de volumen encadenados.'] 2026-T2: 0.6847 "
            "(Provisional) | CNTR6652 (indice) 2026-T2: 126.4212 || [Teleprensa 2026-09-25, el claim] 'El PIB "
            "acelera su crecimiento al 0,7% en el segundo trimestre por el tiron del consumo y la inversion'"
        ),
        raw_value_span_anterior="[INE API, tabla 67824] CNTR6653 2026-T1: 0.6298 | CNTR6652 (indice) 2026-T1: 125.5615 (Provisional)",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: 'acelera al 0,7%' compara con el trimestre anterior (0,6%), la referencia del INE. Se "
            "estructura sobre el INDICE de volumen ajustado (CNTR6652): 126,4212/125,5615 - 1 = +0,685%. La "
            "tabla publica la tasa (CNTR6653) y el indice; el sistema recomputa desde el indice. 'Por el tiron "
            "del consumo y la inversion' es atribucion del propio INE (consumo hogares +1,2%, FBC +1,7%), no se "
            "evalua. methodology_found=no: no buscada (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CNTR2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="67824",
                         serie_nombre="Total Nacional. Datos ajustados de estacionalidad y calendario. Producto interior bruto a precios de mercado. Dato base. Índices de volumen encadenados. ",
                         unidad="indice", referencia_principal="anterior",
                         descripcion="CNTR, PIB pm en volumen encadenado, ajustado de estacionalidad y calendario, indice, trimestral"),
            periodo_objetivo="2026-T2", periodo_base="2026-T1",
            cambio_afirmado=0.7, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = trimestre anterior, referencia del emisor. El claim da la tasa redondeada (0,7).",
        ),
    ),
    dict(
        cid="Q012",
        claim_text="El INE revisa a la baja sus previsiones sobre el crecimiento económico",
        claim_date="2026-09-25",
        post_url="https://www.libertaddigital.com/libremercado/2026-09-25/el-ine-desmiente-el-triunfalismo-de-sanchez-y-revisa-a-la-baja-sus-previsiones-sobre-el-crecimiento-economico-7465884/",
        post_url_tipo="prensa", emisor="Libre Mercado", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com PIB segundo trimestre 2026 0,7% INE revisión",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'Contabilidad Nacional Trimestral' PIB segundo trimestre 2026 revisado OR 'datos revisados' crece '%' noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E006",
        # --- trabajo 2026-09-26 (E006 t0 12:48:49Z, t1 12:49:31Z, t2 12:49:31Z) ---
        fuente_primaria="INE - Contabilidad Nacional Trimestral (CNTR), 2T2026: nota CNTR2T26 (definitivo) y avCNTR2T26 (avance) + API Tempus tabla 67824",
        primaria_url="https://www.ine.es/dyngs/Prensa/CNTR2T26.htm",
        primaria_url_tipo="nota_de_prensa_html + nota de AVANCE (avCNTR2T26.htm, 2026-07-30) + API JSON wstempus DATOS_TABLA/67824",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026 (CNTR2T26, 2026-09-25): variacion interanual del PIB 2,6% (API: 2,6374); 1T2026: 2,6205",
        dato_anterior="2T2026 AVANCE (avCNTR2T26, 2026-07-30): 'La variacion interanual del PIB fue del 2,7%, tasa similar a la del trimestre precedente'",
        raw_value_span_actual=(
            "[INE, nota CNTR2T26, 2026-09-25] 'La variacion interanual del PIB fue del 2,6%, tasa similar a la "
            "del trimestre precedente.' | [INE API, tabla 67824, CNTR6654 'Total Nacional. Datos ajustados... "
            "Variacion anual. Indices de volumen encadenados.'] 2026-T2: 2.6374 | 2026-T1: 2.6205 || [Libre "
            "Mercado 2026-09-25, el claim, titular] 'El INE revisa a la baja sus previsiones sobre el "
            "crecimiento economico' | [cuerpo] 'en terminos interanuales, el PIB avanzo un 2,6%, una decima "
            "menos de lo que habia estimado inicialmente'"
        ),
        raw_value_span_anterior="[INE, nota avCNTR2T26, 2026-07-30] 'La variacion interanual del PIB fue del 2,7%, tasa similar a la del trimestre precedente.'",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D: los numeros cuadran (2,6 definitivo frente a 2,7 del avance del 30-07). La comparacion "
            "es entre dos EDICIONES del mismo periodo (avance -> definitivo), que es revision del propio emisor "
            "(territorio 2b, fuera del prototipo): ningun test computable aplica -> undetermined (DEC-029). "
            "'Previsiones' es un error de nombre: el INE no preve, estima; no cambia truth. El titular no da "
            "cifra; se estructura como nivel de la tasa interanual del 2T. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CNTR2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="nivel",
            metrica=dict(emisor="INE", tabla="67824",
                         serie_nombre="Total Nacional. Datos ajustados de estacionalidad y calendario. Producto interior bruto a precios de mercado. Variación anual. Índices de volumen encadenados. ",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="CNTR, PIB pm en volumen, variacion interanual, ajustada, trimestral"),
            periodo_objetivo="2026-T2", valor_objetivo=2.6,
            notas="Nivel: el claim es una revision avance->definitivo del mismo periodo; sin test aplicable.",
        ),
    ),
    dict(
        cid="Q013",
        claim_text="El PIB crece un 0,7%: más consumo, pero más importaciones",
        claim_date="2026-09-25",
        post_url="https://www.cronicadelhenares.com/2026/09/pib-segundo-trimestre-2026-ine-consumo-importaciones.html",
        post_url_tipo="prensa", emisor="La Crónica del Henares", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com PIB segundo trimestre 2026 0,7% INE revisión",
        criba_query_b="",  # PENDIENTE
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'Contabilidad Nacional Trimestral' PIB segundo trimestre 2026 revisado OR 'datos revisados' crece '%' noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E005",
        # --- trabajo 2026-09-26 (E005 t0/t1/t2 12:48:49Z; primaria ya en mano por E004) ---
        fuente_primaria="INE - Contabilidad Nacional Trimestral (CNTR), 2T2026: nota CNTR2T26 + API Tempus tabla 67824",
        primaria_url="https://www.ine.es/dyngs/Prensa/CNTR2T26.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/67824",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: PIB volumen ajustado, variacion trimestral 0,6847% (0,7%); indice 126,4212",
        dato_anterior="1T2026: variacion trimestral 0,6298%; indice 125,5615 (provisionales)",
        raw_value_span_actual=(
            "[INE, nota CNTR2T26, 2026-09-25] 'El PIB registro una variacion del 0,7% en el segundo trimestre "
            "respecto al trimestre anterior en terminos de volumen.' | [INE API, tabla 67824] CNTR6653 2026-T2: "
            "0.6847 | CNTR6652 (indice) 2026-T2: 126.4212 || [La Cronica del Henares 2026-09-25, el claim] 'El "
            "PIB crece un 0,7%: mas consumo, pero mas importaciones'"
        ),
        raw_value_span_anterior="[INE API, tabla 67824] CNTR6653 2026-T1: 0.6298 | CNTR6652 (indice) 2026-T1: 125.5615",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: 'crece un 0,7%' es la variacion trimestral, referencia del INE; misma edicion que E004 y "
            "E006 (tres de CNTR2T26: dos controles A y un nivel D; tope de 3 controles respetado). 'Mas "
            "importaciones' es composicion de la demanda, no se evalua. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CNTR2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="67824",
                         serie_nombre="Total Nacional. Datos ajustados de estacionalidad y calendario. Producto interior bruto a precios de mercado. Dato base. Índices de volumen encadenados. ",
                         unidad="indice", referencia_principal="anterior",
                         descripcion="CNTR, PIB pm en volumen encadenado, ajustado, indice, trimestral"),
            periodo_objetivo="2026-T2", periodo_base="2026-T1",
            cambio_afirmado=0.7, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = trimestre anterior, referencia del emisor.",
        ),
    ),
    # ---- jornada 1, barrido 2 (12:43Z): Interior 1T2026, IPI julio, FMI por pais, ECV -------
    dict(
        cid="Q014",
        claim_text="Aumento de la Criminalidad en España: Homicidios Suben un 10% y Agresiones Sexuales un 3,8% en 2026",
        claim_date="2026-06-04",
        post_url="https://www.madridactual.es/nacional/criminalidad-sube-espana-aumento-homicidios-10-agresiones-20260604-8105146.html",
        post_url_tipo="prensa", emisor="Madridactual", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com homicidios suben 10% primer trimestre 2026 balance criminalidad agresiones sexuales 3,8%",
        criba_query_b="homicidios suben 10% primer trimestre 2026 criminalidad España 1% verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'criminalidad' 'primer trimestre de 2026' sube OR crece OR baja '%' Interior balance noticia España delitos",
        collected_at="2026-09-26", case_id="E025",
        # --- trabajo 2026-09-26 (E025 t0 13:12:35Z, t1/t2 13:12:36Z) ---
        fuente_primaria="Ministerio del Interior - Balance de Criminalidad, primer trimestre 2026 (PDF) + Portal Estadistico de Criminalidad",
        primaria_url="https://www.interior.gob.es/opencms/export/sites/default/.galleries/galeria-de-prensa/documentos-y-multimedia/balances-e-informes/2026/Balance-de-Criminalidad-Primer-Trimestre-2026.pdf",
        primaria_url_tipo="PDF en interior.gob.es; HTTP 403 al agente identificado en la primera peticion",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="segun la prensa (no verificado por el agente): 1T2026 homicidios dolosos y asesinatos consumados 94 (+10,6% vs 1T2025); agresiones sexuales con penetracion 1.290 (+3,8%); criminalidad total +1,0% (595.240)",
        dato_anterior="1T2025: en el mismo Balance (columnas comparadas), no extraido",
        raw_value_span_actual="NEEDS_REVIEW: sin span de la primaria (bloqueada); [Madridactual 2026-06-04, el claim] 'Aumento de la Criminalidad en Espana: Homicidios Suben un 10% y Agresiones Sexuales un 3,8% en 2026'",
        raw_value_span_anterior="NEEDS_REVIEW: sin span",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO: interior.gob.es devolvio 403 al agente identificado en la primera peticion "
            "(PDF del Balance). DEC-021: cierra el caso. HALLAZGO: el segundo emisor de DEC-024 tras el FMI que "
            "rechaza al agente; en el piloto (C18, 2026-09-25) el mismo dominio sirvio el Balance 2T2026 (a "
            "comprobar si cambio la politica o si fue por otra ruta; NEEDS_REVIEW). Anotacion humana desde la "
            "prensa: +10,6% redondeado a 10%, interanual = referencia del Balance -> no_divergence, truth "
            "supported con NEEDS_REVIEW (sin primaria leida). El Portal Estadistico (estadisticasdecriminalidad."
            "ses.mir.es, CSV) no se probo en este caso: queda como via alternativa a evaluar antes de dar por "
            "bloqueado el emisor entero."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Interior", tabla="Balance de Criminalidad",
                         serie_nombre="Homicidios dolosos y asesinatos consumados. Total Nacional.",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="Balance de Criminalidad, homicidios dolosos y asesinatos consumados, total nacional, trimestral"),
            periodo_objetivo="2026-T1", periodo_base="2025-T1",
            cambio_afirmado=10, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Emisor sin conector y bloqueado al agente: sin veredicto hoy.",
        ),
    ),
    dict(
        cid="Q015",
        claim_text="La producción industrial modera su avance en julio al 2,6% y suma cinco meses de alzas",
        claim_date="2026-09-10",
        post_url="https://forbes.es/ultima-hora/1015903/la-produccion-industrial-modera-su-avance-en-julio-al-26-y-suma-cinco-meses-de-alzas/",
        post_url_tipo="prensa", emisor="Forbes España", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="industria",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com producción industrial julio 2026 2,6% cinco meses INE",
        criba_query_b="producción industrial julio 2026 2,6% INE cinco meses de alzas verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'producción industrial' julio 2026 'según el INE' sube OR cae '%' interanual noticia septiembre 2026 España",
        collected_at="2026-09-26", case_id="E016",
        # --- trabajo 2026-09-26 (E016 t0 12:55:06Z, t1 12:57:23Z, t2 ~13:03Z) ---
        fuente_primaria="INE - Indices de Produccion Industrial (IPI), julio 2026: nota IPI0726 + API Tempus tablas 60272 (original), 60276 (calendario), 60280 (estacional+calendario)",
        primaria_url="https://www.ine.es/dyngs/Prensa/IPI0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/60272",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: IPI total industria, serie ORIGINAL, variacion anual 2,6% (junio 3,8%); indice 113,157; serie corregida de estacionalidad y calendario 2,3% (titular de la nota); solo calendario 2,4%",
        dato_anterior="julio 2025: indice original 110,304; variacion anual 2,5%. Junio 2026: 3,8% (original)",
        raw_value_span_actual=(
            "[INE, nota IPI0726, 2026-09-10] 'La tasa anual del Indice de Produccion Industrial se situo en el 2,3% "
            "en la serie corregida de efectos estacionales y de calendario' | serie original: 2,6%, 1,2 puntos "
            "menos que en junio | [INE API, tabla 60272, IPI13868 'Total Nacional. Total industria. Variacion "
            "anual.'] 2026-M07: 2.6 | 2026-M06: 3.8 | IPI13491 (indice) 2026-M07: 113.157 || [Forbes Espana "
            "2026-09-10, el claim] 'La produccion industrial modera su avance en julio al 2,6% y suma cinco meses "
            "de alzas'"
        ),
        raw_value_span_anterior="[INE API, tabla 60272] IPI13491 2025-M07: 110.304 | IPI13868 2025-M07: 2.5 | 2026-M03..M07 anuales positivas (cinco meses)",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: el 2,6 es la tasa anual de la serie ORIGINAL (la nota titula con la corregida, 2,3): "
            "eleccion de serie entre dos cifras del mismo emisor, ambas publicadas; no es divergencia, se anota. "
            "'Modera' compara con junio (3,8, original): referencia anterior. 'Cinco meses de alzas' no se "
            "verifico mes a mes (NEEDS_REVIEW menor). Estructura sobre el indice original: 113,157/110,304 - 1 = "
            "+2,59%. La primera busqueda (60276, solo calendario) daba 2,4: hubo que comprobar tres tablas. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE IPI0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="60272",
                         serie_nombre="Total Nacional. Total industria. Índice. ",
                         unidad="indice", referencia_principal="interanual",
                         descripcion="IPI, indice general (total industria), serie original, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            cambio_afirmado=2.6, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = interanual, referencia del emisor; serie original, que es la que cita el claim.",
        ),
    ),
    dict(
        cid="Q016",
        claim_text="El FMI vuelve a bajar proyección de crecimiento para Chile hasta el 1,8% durante 2026",
        claim_date="2026-07-06",
        post_url="https://www.biobiochile.cl/noticias/economia/actualidad-economica/2026/07/06/el-fmi-vuelve-a-bajar-su-proyeccion-de-crecimiento-para-chile-hasta-el-18-en-2026.shtml",
        post_url_tipo="prensa", emisor="BioBioChile", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="CL", tema="pib",
        criba_query_a="site:chequeado.com OR site:factual.afp.com OR site:maldita.es OR site:newtral.es FMI Chile 1,8% 2026 julio proyección baja",
        criba_query_b="FMI Chile 1,8% 2026 julio 'vuelve a bajar' proyección verificación OR bulo OR fact-check OR chequeo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="site:chequeado.com OR site:factual.afp.com OR site:colombiacheck.com OR site:maldita.es FMI Chile 2,4% 2026 proyección crecimiento abril",
        collected_at="2026-09-26", case_id="E010",
        # --- trabajo 2026-09-26 (E010 t0/t1/t2 12:55:00Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - Consulta del Articulo IV con Chile (2026-07-06, comunicado/informe) y declaracion final de mayo 2026; WEO abril 2026 (2,4%)",
        primaria_url="https://www.imf.org/es/countries/chl",
        primaria_url_tipo="paginas HTML de imf.org (pais, comunicados) + PDF; 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="html",
        dato_actual="Articulo IV julio 2026: Chile 2026 = 1,8% (segun la prensa; primaria no verificada por el agente); 2027 = 2,6%",
        dato_anterior="declaracion de mayo 2026: 2,2% (prensa); WEO abril 2026, p.69: 'Chile 2,3 2,4 2,6' -> 2026 = 2,4% (verificado en texto)",
        raw_value_span_actual="NEEDS_REVIEW: sin span de la primaria (bloqueada); [BioBioChile 2026-07-06, el claim] 'El FMI vuelve a bajar proyeccion de crecimiento para Chile hasta el 1,8% durante 2026' | [cuerpo] 'desde el 2,2% proyectado en mayo'",
        raw_value_span_anterior="[FMI, WEO abril 2026, text.pdf p.69] 'Chile 2,3 2,4 2,6 4,2 2,9 3,3 —2,3 —0,8 —1,8 8,5 8,1 7,6'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). Interes para el 2a: la base del claim (2,2, mayo) no es "
            "la edicion WEO anterior (2,4, abril): recorte -0,4 vs -0,6; mismo signo, ratio 1,5 -> ni siquiera "
            "senal. Comparacion legitima entre documentos del propio FMI: no_divergence. truth supported con "
            "NEEDS_REVIEW sobre 1,8 y 2,2 (solo prensa)."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI Articulo IV Chile 2026-07",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Chile. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="FMI: proyeccion de crecimiento del PIB real de Chile para 2026, por edicion/documento"),
            periodo_objetivo="2026-M07", periodo_base="2026-M05",
            valor_objetivo=1.8, valor_base=2.2, cambio_afirmado=-0.4, unidad_cambio="pp", direccion_afirmada="baja",
            notas="Periodos = documentos del FMI (julio Art. IV vs mayo declaracion). Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q017",
        claim_text="El FMI empeora el pronóstico: inflación al 30% y recorte del crecimiento (Argentina crecerá 3,5% del PBI, medio punto menos que lo estimado en octubre)",
        claim_date="2026-04-14",
        post_url="https://eleconomista.com.ar/economia/el-fmi-empeora-pronostico-inflacion-30-recorte-crecimiento-n94122",
        post_url_tipo="prensa", emisor="El Economista (AR)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="AR", tema="pib",
        criba_query_a="site:chequeado.com OR site:factual.afp.com FMI Argentina 3,5% 2026 crecimiento inflación 30,4% abril OR julio",
        criba_query_b="FMI Argentina crecimiento 3,5% 2026 'medio punto menos' OR 'mantuvo' proyección verificación OR bulo OR fact-check OR chequeo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 México 1,6% 'una décima' OR Chile 1,8% 'vuelve a bajar' OR Argentina 3,5% previsión 2026 noticia julio 2026",
        collected_at="2026-09-26", case_id="E011",
        # --- trabajo 2026-09-26 (E011 t0/t1/t2 12:55:02Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - WEO abril 2026 (anexo p.69) y edicion anterior (WEO octubre 2025 / actualizacion enero 2026)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf); 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO abril 2026, p.69: 'Argentina 4,4 3,5 4,0 41,9 30,4 15,7' -> PIB 2026 = 3,5%; inflacion 2026 = 30,4% (medias anuales)",
        dato_anterior="edicion anterior: 4,0% segun la prensa ('octubre' en El Economista, 'enero' en La Nacion/Infobae); NO verificado en la primaria",
        raw_value_span_actual="[FMI, WEO abril 2026, text.pdf p.69] 'Argentina 4,4 3,5 4,0 41,9 30,4 15,7 —1,1 —0,8 —0,6 7,4 7,2 6,9' || [El Economista AR 2026-04-14, el claim] 'el pais crecera 3,5% del PBI, medio punto menos que lo estimado en octubre' | 'la inflacion proyectada salta de 16,4% a 30,4%'",
        raw_value_span_anterior="NEEDS_REVIEW: 4,0% (octubre 2025 o enero 2026) sin span de la primaria",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). 3,5 y 30,4 verificados en el texto del PDF de abril; la "
            "base (4,0) y su edicion (octubre vs enero) quedan NEEDS_REVIEW: si octubre y enero decian lo mismo, "
            "la eleccion de base no cambia nada. Comparacion entre ediciones: no_divergence."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO 2026-04",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Argentina. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Argentina para 2026, por edicion"),
            periodo_objetivo="2026-M04", periodo_base="2025-M10",
            valor_objetivo=3.5, valor_base=4.0, cambio_afirmado=-0.5, unidad_cambio="pp", direccion_afirmada="baja",
            notas="Periodos = ediciones del WEO. El claim dice 'octubre'; enero (G20) pudo decir lo mismo. Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q018",
        claim_text="El FMI mantuvo su proyección de crecimiento para la Argentina y anticipó cuándo la inflación podrá bajar a un dígito",
        claim_date="2026-07-08",
        post_url="https://www.infobae.com/economia/2026/07/08/el-fmi-mantuvo-su-proyeccion-de-crecimiento-para-la-argentina-y-corrigio-las-previsiones-de-la-economia-mundial/",
        post_url_tipo="prensa", emisor="Infobae (AR)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="AR", tema="pib",
        criba_query_a="site:chequeado.com OR site:factual.afp.com FMI Argentina 3,5% 2026 crecimiento inflación 30,4% abril OR julio",
        criba_query_b="FMI Argentina crecimiento 3,5% 2026 'medio punto menos' OR 'mantuvo' proyección verificación OR bulo OR fact-check OR chequeo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 México 1,6% 'una décima' OR Chile 1,8% 'vuelve a bajar' OR Argentina 3,5% previsión 2026 noticia julio 2026",
        collected_at="2026-09-26", case_id="E012",
        # --- trabajo 2026-09-26 (E012 t0/t1/t2 12:55:03Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - Actualizacion WEO julio 2026 (tabla como imagen en el PDF) y WEO abril 2026 (edicion anterior, p.69)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/07/08/world-economic-outlook-update-july-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf) + API; 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="actualizacion julio 2026: Argentina 2026 = 3,5%, 2027 = 4,0% (prensa; la fila esta en la tabla-imagen p.16, sin texto)",
        dato_anterior="WEO abril 2026, p.69: 'Argentina 4,4 3,5 4,0' -> 2026 = 3,5% (verificado en texto)",
        raw_value_span_actual="NEEDS_REVIEW: fila de julio en imagen; [Infobae AR 2026-07-08, el claim] 'El FMI mantuvo su proyeccion de crecimiento para la Argentina' | [cuerpo] 'expansion de 3,5% en 2026 y 4% en 2027'",
        raw_value_span_anterior="[FMI, WEO abril 2026, text.pdf p.69] 'Argentina 4,4 3,5 4,0 41,9 30,4 15,7 —1,1 —0,8 —0,6 7,4 7,2 6,9'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). 'Mantuvo' = cambio 0 entre julio y abril; abril "
            "verificado (3,5), julio solo por prensa e imagen (NEEDS_REVIEW). Contraste con E011: el mismo 3,5 se "
            "titula 'recorte' en abril (vs 4,0) y 'mantuvo' en julio (vs 3,5); ambos correctos con su base."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO update 2026-07",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Argentina. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Argentina para 2026, por edicion"),
            periodo_objetivo="2026-M07", periodo_base="2026-M04",
            valor_objetivo=3.5, valor_base=3.5, cambio_afirmado=0, unidad_cambio="pp", direccion_afirmada="igual",
            notas="Periodos = ediciones del WEO. Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q019",
        claim_text="FMI mejora pronóstico para PIB de México a 1.6% en 2026; advierte de riesgos por guerra en Irán",
        claim_date="2026-04-14",
        post_url="https://www.elfinanciero.com.mx/economia/2026/04/14/fmi-mejora-pronostico-de-crecimiento-para-mexico-en-2026-a-cuanto/",
        post_url_tipo="prensa", emisor="El Financiero (MX)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="MX", tema="pib",
        criba_query_a="site:verificado.com.mx OR site:factual.afp.com OR site:chequeado.com FMI México 1,6% 2026 julio proyección crecimiento",
        criba_query_b="FMI México crecimiento 1,6% 2026 julio 'una décima' proyección verificación OR bulo OR fact-check OR verificado",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 actualización 'Perspectivas de la economía mundial' México OR Argentina OR Colombia OR Perú previsión crecimiento 2026 '%' noticia eleva OR rebaja",
        collected_at="2026-09-26", case_id="E013",
        # --- trabajo 2026-09-26 (E013 t0/t1/t2 12:55:04Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - WEO abril 2026 (Cuadro 1.1 p.28, con diferencias vs enero 2026 y octubre 2025)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf); 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO abril 2026, Cuadro 1.1 p.28: 'Mexico 0,6 1,6 2,2 0,1 0,1 0,1 0,2' -> 2026 = 1,6%; dif. vs ene-2026 +0,1; vs oct-2025 +0,1",
        dato_anterior="actualizacion enero 2026: 1,5% (= 1,6 - 0,1, derivado de la columna de diferencia del propio Cuadro 1.1)",
        raw_value_span_actual="[FMI, WEO abril 2026, text.pdf p.28, Cuadro 1.1] 'Mexico 0,6 1,6 2,2 0,1 0,1 0,1 0,2' || [El Financiero MX 2026-04-14, el claim] 'FMI mejora pronostico para PIB de Mexico a 1.6% en 2026' | [cuerpo] 'una decima mas respecto a lo previsto en enero'",
        raw_value_span_anterior="[FMI, WEO abril 2026, p.28] columna 'Diferencia con las proyecciones de la Actualizacion de enero de 2026': 2026 0,1",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). Es el caso FMI mejor anotado: valor y diferencia con la "
            "edicion anterior verificados en el texto del Cuadro 1.1 de abril. 'Mejora' = +0,1 vs enero = "
            "referencia del FMI: no_divergence."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO 2026-04",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="México. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Mexico para 2026, por edicion"),
            periodo_objetivo="2026-M04", periodo_base="2026-M01",
            valor_objetivo=1.6, valor_base=1.5, cambio_afirmado=0.1, unidad_cambio="pp", direccion_afirmada="sube",
            notas="Periodos = ediciones del WEO. Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q020",
        claim_text="FMI 'desinfla' pronósticos de crecimiento para México: Baja de 1.6 a 1.2% para 2026",
        claim_date="2026-07-08",
        post_url="https://www.elfinanciero.com.mx/economia/2026/07/08/fmi-ajusta-a-la-baja-estimados-de-crecimiento-economico-de-mexico/",
        post_url_tipo="prensa", emisor="El Financiero (MX)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="MX", tema="pib",
        criba_query_a="site:verificado.com.mx OR site:factual.afp.com OR site:chequeado.com FMI México 1,6% 2026 julio proyección crecimiento",
        criba_query_b="FMI México crecimiento 1,6% 2026 julio 'una décima' proyección verificación OR bulo OR fact-check OR verificado",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FMI julio 2026 actualización 'Perspectivas de la economía mundial' México OR Argentina OR Colombia OR Perú previsión crecimiento 2026 '%' noticia eleva OR rebaja",
        collected_at="2026-09-26", case_id="E014",
        # --- trabajo 2026-09-26 (E014 t0/t1/t2 12:55:05Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - Actualizacion WEO julio 2026 (tabla como imagen; p.9 texto sobre Mexico) y WEO abril 2026 (1,6, p.28)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/07/08/world-economic-outlook-update-july-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf) + API; 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="actualizacion julio 2026: Mexico 2026 = 1,2% (prensa; tabla-imagen p.16; p.9 del texto menciona a Mexico sin la cifra en la linea extraida)",
        dato_anterior="WEO abril 2026, p.28: 'Mexico 0,6 1,6 2,2' -> 2026 = 1,6% (verificado en texto)",
        raw_value_span_actual="NEEDS_REVIEW: fila de julio en imagen; [El Financiero MX 2026-07-08, el claim] 'FMI desinfla pronosticos de crecimiento para Mexico: Baja de 1.6 a 1.2% para 2026'",
        raw_value_span_anterior="[FMI, WEO abril 2026, text.pdf p.28] 'Mexico 0,6 1,6 2,2 0,1 0,1 0,1 0,2'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). Abril 1,6 verificado; julio 1,2 solo por prensa "
            "(NEEDS_REVIEW). OBSERVACION: americaeconomica (julio) titula 'Mexico 1,6% en 2026, una decima mas "
            "que en enero', que es la cifra de ABRIL: candidato a claim falso/desactualizado, no registrado "
            "(no se localizo su URL con fecha cierta). Comparacion julio vs abril = referencia: no_divergence."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO update 2026-07",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="México. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Mexico para 2026, por edicion"),
            periodo_objetivo="2026-M07", periodo_base="2026-M04",
            valor_objetivo=1.2, valor_base=1.6, cambio_afirmado=-0.4, unidad_cambio="pp", direccion_afirmada="baja",
            notas="Periodos = ediciones del WEO. Emisor sin conector.",
        ),
    ),
    dict(
        cid="Q021",
        claim_text="La tasa de pobreza o exclusión social se mantiene en el 25,7% en España durante 2025",
        claim_date="2026-02-05",
        post_url="https://objetivocastillalamancha.es/contenidos/tasa-pobreza-o-exclusion-social-se-mantiene-257-espana-durante-2025",
        post_url_tipo="prensa", emisor="Objetivo CLM", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pobreza",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com tasa AROPE 25,7% 2025 pobreza menor en una década INE",
        criba_query_b="tasa de pobreza o exclusión 25,7% 2025 'menor' 'década' INE 13 millones verificación OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: Newtral (2026-06-04) 'Una de cada cuatro personas en Espana se encontraba en riesgo de pobreza o exclusion social en 2025' cubre la misma ECV 2025 con las mismas cifras; ademas fact-checks de Newtral sobre AROPE (2025-10-21) y Maldita (2026-09-14)",
        criba_url_verificacion="https://www.newtral.es/riesgo-pobreza-espana-2025/20260604/",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'según el INE' OR 'INE' 'riesgo de pobreza o exclusión' 25,7% 2025 noticia febrero 2026 AROPE baja OR sube",
    ),
    dict(
        cid="Q022",
        claim_text="España registra la menor tasa de pobreza en una década, aunque afecta a más de 13 millones de personas",
        claim_date="2026-02-05",
        post_url="https://www.infobae.com/espana/2026/02/05/espana-registra-la-menor-tasa-de-pobreza-en-una-decada-aunque-persiste-entre-mas-de-13-millones-de-personas/",
        post_url_tipo="prensa", emisor="Infobae España", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pobreza",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com tasa AROPE 25,7% 2025 pobreza menor en una década INE",
        criba_query_b="tasa de pobreza o exclusión 25,7% 2025 'menor' 'década' INE 13 millones verificación OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: mismo explainer de Newtral (2026-06-04) sobre la ECV 2025",
        criba_url_verificacion="https://www.newtral.es/riesgo-pobreza-espana-2025/20260604/",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'según el INE' OR 'INE' 'riesgo de pobreza o exclusión' 25,7% 2025 noticia febrero 2026 AROPE baja OR sube",
    ),
    dict(
        cid="Q023",
        claim_text="El FMI elevó al 2,4 % su proyección de crecimiento para Chile en 2026",
        claim_date="2026-04-14",
        post_url="https://www.cooperativa.cl/noticias/economia/crecimiento/el-fmi-elevo-al-2-4-su-proyeccion-de-crecimiento-para-chile-en-2026/2026-04-14/103709.html",
        post_url_tipo="prensa", emisor="Cooperativa.cl", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="CL", tema="pib",
        criba_query_a="site:chequeado.com OR site:factual.afp.com OR site:colombiacheck.com OR site:maldita.es FMI Chile 2,4% 2026 proyección crecimiento abril",
        criba_query_b="FMI Chile crecimiento 2,4% 2026 América Latina 2,3% abril Forbes verificación OR bulo OR fact-check OR chequeo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="site:chequeado.com OR site:factual.afp.com OR site:colombiacheck.com OR site:maldita.es FMI Chile 2,4% 2026 proyección crecimiento abril",
        collected_at="2026-09-26", case_id="E015",
        # --- trabajo 2026-09-26 (E015 t0/t1/t2 12:55:06Z; bloqueo comprobado en E007) ---
        fuente_primaria="FMI - WEO abril 2026 (anexo p.69) y edicion anterior (WEO octubre 2025)",
        primaria_url="https://www.imf.org/es/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026",
        primaria_url_tipo="pagina HTML del WEO + PDF (text.pdf); 403 al agente identificado (E007)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="WEO abril 2026, p.69: 'Chile 2,3 2,4 2,6' -> 2026 = 2,4% (verificado en texto)",
        dato_anterior="edicion anterior (WEO octubre 2025): 2,0% segun la prensa; NO verificado en la primaria",
        raw_value_span_actual="[FMI, WEO abril 2026, text.pdf p.69] 'Chile 2,3 2,4 2,6 4,2 2,9 3,3 —2,3 —0,8 —1,8 8,5 8,1 7,6' || [Cooperativa.cl 2026-04-14, el claim] 'El FMI elevo al 2,4 % su proyeccion de crecimiento para Chile en 2026'",
        raw_value_span_anterior="NEEDS_REVIEW: 2,0% (WEO octubre 2025) sin span de la primaria",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "Cubeta E, BLOQUEADO por imf.org (ver E007). 2,4 verificado en texto; base 2,0 NEEDS_REVIEW. Misma "
            "edicion que E009 (Forbes, nivel) y E010 usa este 2,4 como edicion WEO anterior."
        ),
        cubeta="E", hermano_de="", mecanismo_candidato="", primaria_edicion="FMI WEO 2026-04",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="FMI", tabla="WEO", serie_nombre="Chile. PIB real, variación anual, proyección para 2026",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="WEO: proyeccion de crecimiento del PIB real de Chile para 2026, por edicion"),
            periodo_objetivo="2026-M04", periodo_base="2025-M10",
            valor_objetivo=2.4, valor_base=2.0, cambio_afirmado=0.4, unidad_cambio="pp", direccion_afirmada="sube",
            notas="Periodos = ediciones del WEO. Emisor sin conector.",
        ),
    ),
    # ---- jornada 1, barrido 3 (12:55Z): INE turismo, hoteles, IPRI, coste laboral ----------------
    # Criba (a) y (b) hechas para los ocho: sin articulo de verificacion.
    dict(
        cid="Q024",
        claim_text="España supera los 58 millones de turistas hasta julio, un 4,6% más",
        claim_date="2026-09-01",
        post_url="https://bilbaohiria.com/actualidad/espana-record-turismo-frontur-58-millones-2026/",
        post_url_tipo="prensa", emisor="Bilbao Hiria", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com turistas 58 millones hasta julio 2026 4,6% FRONTUR récord",
        criba_query_b="turistas internacionales 58 millones hasta julio 2026 4,6% FRONTUR verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FRONTUR julio 2026 'según el INE' turistas internacionales 11,5 millones '4,6%' OR EGATUR gasto julio 2026 noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E017",
        # --- trabajo 2026-09-26 (E017 t0 13:01:33Z, t1/t2 ~13:05Z) ---
        fuente_primaria="INE - Estadistica de Movimientos Turisticos en Fronteras (FRONTUR), julio 2026: nota FRONTUR0726 + API Tempus tabla 75722",
        primaria_url="https://www.ine.es/dyngs/Prensa/FRONTUR0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/75722",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="enero-julio 2026: 58.106.406 turistas (acumulado, provisional), tasa acumulada +4,6%; julio 2026: 11.538.796 (+4,64%)",
        dato_anterior="enero-julio 2025: 55.552.485 (definitivo); julio 2025: 11.026.681",
        raw_value_span_actual=(
            "[INE, nota FRONTUR0726, 2026-09-01] 'En los siete primeros meses de 2026 el numero de turistas "
            "aumento un 4,6% y supero los 58,1 millones.' | 'Espana recibio 11,5 millones de turistas "
            "internacionales en julio, un 4,6% mas que en el mismo mes de 2025.' | [INE API, tabla 75722, "
            "FREG1125 'Turista. Total Nacional. Acumulado en lo que va de ano.'] 2026-M07: 58106406 (Provisional) "
            "|| [Bilbao Hiria 2026-09-01, el claim] 'Espana supera los 58 millones de turistas hasta julio, un "
            "4,6% mas'"
        ),
        raw_value_span_anterior="[INE API, tabla 75722] FREG1125 2025-M07: 55552485 (Definitivo) | FREG286 2025-M07: 11026681",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: acumulado enero-julio contra el mismo periodo de 2025, que es la referencia que publica el "
            "INE (serie 'Acumulado en lo que va de ano' y su tasa). 58.106.406/55.552.485 - 1 = +4,60%. Julio "
            "mensual tambien +4,6 (coincidencia). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE FRONTUR0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="75722",
                         serie_nombre="Turista. Total Nacional. Acumulado en lo que va de año. ",
                         unidad="personas", referencia_principal="interanual",
                         descripcion="FRONTUR, turistas internacionales, acumulado enero-mes, total nacional"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=58106406, cambio_afirmado=4.6, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: acumulado contra acumulado del ano anterior, referencia del emisor. El claim redondea 58,1 M a '58 millones'.",
        ),
    ),
    dict(
        cid="Q025",
        claim_text="El gasto de los turistas internacionales supera los 18.200 millones de euros en julio, un 10,9% más que en 2025",
        claim_date="2026-09-01",
        post_url="https://www.turiscom.org/estudios-e-informes/gasto-turistas-internacionales-supera-18200-mE-mes-julio-109-mas/20260901161345005605.html",
        post_url_tipo="prensa", emisor="Turiscom", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com gasto turistas internacionales julio 2026 18.200 millones 10,9% EGATUR",
        criba_query_b="gasto turistas internacionales julio 2026 18.200 millones 10,9% EGATUR verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="FRONTUR julio 2026 'según el INE' turistas internacionales 11,5 millones '4,6%' OR EGATUR gasto julio 2026 noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E018",
        # --- trabajo 2026-09-26 (E018 t0 13:02:48Z, t1/t2 ~13:07Z) ---
        fuente_primaria="INE - Encuesta de Gasto Turistico (EGATUR), julio 2026: nota EGATUR0726 + API Tempus tabla 75715",
        primaria_url="https://www.ine.es/dyngs/Prensa/EGATUR0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/75715",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: gasto total de turistas internacionales 18.217,95 millones de euros (provisional), +10,86% interanual; gasto medio 1.579 euros (+5,9%); acumulado enero-julio 82.053,55 M (+7,8%)",
        dato_anterior="julio 2025: 16.432,61 millones (definitivo); junio 2026: 13.579,04",
        raw_value_span_actual=(
            "[INE, nota EGATUR0726, 2026-09-01] 'El gasto total de los turistas internacionales que visitaron "
            "Espana en julio aumento un 10,9% y alcanzo los 18.218 millones de euros.' | [INE API, tabla 75715, "
            "FREG647 'Total. Turista. Gasto total. Total Nacional. Dato base.'] 2026-M07: 18217.95 (Provisional) "
            "|| [Turiscom 2026-09-01, el claim] 'El gasto de los turistas internacionales supera los 18.200 "
            "millones de euros en julio, un 10,9% mas que en 2025'"
        ),
        raw_value_span_anterior="[INE API, tabla 75715] FREG647 2025-M07: 16432.61 (Definitivo) | FREG623 (tasa anual) 2026-M07: 10.86",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: el claim reproduce la nota (18.218 M, +10,9%); 18.217,95/16.432,61 - 1 = +10,86%. La tabla "
            "vigente es la 75715 (las 23994/24746 estan vacias en la API: tablas antiguas). 'Que en 2025' = julio "
            "de 2025 = referencia interanual. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EGATUR0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="75715",
                         serie_nombre="Total. Turista. Gasto total. Total Nacional. Dato base. ",
                         unidad="millones_euros", referencia_principal="interanual",
                         descripcion="EGATUR, gasto total de los turistas internacionales, total nacional, mensual, millones de euros"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=18218, cambio_afirmado=10.9, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = interanual, referencia del emisor. El claim dice 'supera los 18.200'; se usa 18.218 (nota).",
        ),
    ),
    dict(
        cid="Q026",
        claim_text="Las pernoctaciones hoteleras suben un 1,4% en agosto y superan los 48,7 millones tras el impulso internacional",
        claim_date="2026-09-22",
        post_url="https://forbes.es/ultima-hora/1025617/las-pernoctaciones-hoteleras-suben-un-14-en-agosto-y-superan-los-487-millones-tras-el-impulso-internacional/",
        post_url_tipo="prensa", emisor="Forbes España", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras agosto 2026 1,4% 48,7 millones precios hoteles 167 euros",
        criba_query_b="pernoctaciones hoteleras agosto 2026 1,4% 48,7 millones habitación 167 euros verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE pernoctaciones hoteleras agosto 2026 'según el INE' suben OR bajan '%' noticia septiembre 2026 coyuntura turística",
        collected_at="2026-09-26", case_id="E019",
        # --- trabajo 2026-09-26 (E019 t0 13:03:48Z, t1/t2 ~13:11Z) ---
        fuente_primaria="INE - Coyuntura Turistica Hotelera (EOH/IPH/IRSH), agosto 2026: nota CTH0826 + API Tempus tabla 36570",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/36570",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="agosto 2026: 48.798.426 pernoctaciones hoteleras (provisional), +1,38% interanual; residentes -1,1%, no residentes +2,8%; IPH +6,3%; ADR 166,9 euros (+7,3%)",
        dato_anterior="agosto 2025: 48.135.610 (definitivo)",
        raw_value_span_actual=(
            "[INE, nota CTH0826, 2026-09-22] 'Las pernoctaciones en establecimientos hoteleros aumentaron un "
            "1,4% en agosto respecto al mismo mes de 2025, y superaron los 48,7 millones.' | [INE API, tabla "
            "36570, EOT25 'Nacional. Pernoctaciones. Total categorias. Total.'] 2026-M08: 48798426 || [Forbes "
            "Espana 2026-09-22, el claim] 'Las pernoctaciones hoteleras suben un 1,4% en agosto y superan los "
            "48,7 millones tras el impulso internacional'"
        ),
        raw_value_span_anterior="[INE API, tabla 36570] EOT25 2025-M08: 48135610",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: 48.798.426/48.135.610 - 1 = +1,38%; el claim reproduce la nota. 'Tras el impulso "
            "internacional' es la descomposicion del propio INE (no residentes +2,8%). La primera prueba de "
            "URL de la nota (EOH0826) dio 404: el codigo de nota es CTH; la tabla 36570 tiene la serie 'Nacional' "
            "sin 'Total Nacional' en el nombre (dos filtros fallidos antes de listar). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="36570",
                         serie_nombre="Nacional. Pernoctaciones. Total categorías. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, total nacional, mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            valor_objetivo=48798426, cambio_afirmado=1.4, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = interanual, referencia del emisor. OJO: el nombre de la serie no lleva espacio final.",
        ),
    ),
    dict(
        cid="Q027",
        claim_text="Los hoteles disparan sus precios en agosto: una habitación cuesta ya 167 euros de media",
        claim_date="2026-09-22",
        post_url="https://www.democrata.es/economia/hoteles-precios-agosto-2026-habitacion-167-euros-pernoctaciones/",
        post_url_tipo="prensa", emisor="Demócrata", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras agosto 2026 1,4% 48,7 millones precios hoteles 167 euros",
        criba_query_b="pernoctaciones hoteleras agosto 2026 1,4% 48,7 millones habitación 167 euros verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE pernoctaciones hoteleras agosto 2026 'según el INE' suben OR bajan '%' noticia septiembre 2026 coyuntura turística",
        collected_at="2026-09-26", case_id="E020",
        # --- trabajo 2026-09-26 (E020 t0 13:06:01Z, t1/t2 ~13:13Z) ---
        fuente_primaria="INE - Coyuntura Turistica Hotelera, agosto 2026: nota CTH0826 + API Tempus tabla 2059 (IRSH, ADR)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/2059",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="agosto 2026: ADR 166,90 euros por habitacion ocupada (provisional), +7,32% interanual; IPH +6,3%",
        dato_anterior="agosto 2025: ADR 155,52 (definitivo); julio 2026: 156,92",
        raw_value_span_actual=(
            "[INE, nota CTH0826, 2026-09-22] 'Los hoteles facturaron 166,9 euros de media por habitacion ocupada, "
            "un 7,3% mas que en el mismo mes del ano anterior.' | [INE API, tabla 2059, EOT16414 'ADR. Nacional. "
            "Dato.'] 2026-M08: 166.9 (Provisional) || [Democrata 2026-09-22, el claim] 'Los hoteles disparan sus "
            "precios en agosto: una habitacion cuesta ya 167 euros de media'"
        ),
        raw_value_span_anterior="[INE API, tabla 2059] EOT16414 2025-M08: 155.52 (Definitivo) | EOT16415 (tasa) 2026-M08: 7.32",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D: claim de NIVEL (167 = 166,9 redondeado); 'disparan' remite al IPH (+6,3%) y al ADR "
            "(+7,3%), correctos, pero el titular no da tasa: sin test aplicable -> undetermined (DEC-029). ADR = "
            "tarifa media diaria por habitacion ocupada, no 'precio de una habitacion' en sentido de lista; se "
            "anota, no es divergencia. Series ADR en la operacion IRSH (180), tabla 2059. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="nivel",
            metrica=dict(emisor="INE", tabla="2059",
                         serie_nombre="ADR. Nacional. Dato.",
                         unidad="euros", referencia_principal="interanual",
                         descripcion="IRSH, tarifa media diaria (ADR) por habitacion ocupada, nacional, mensual"),
            periodo_objetivo="2026-M08", valor_objetivo=167,
            notas="Nivel redondeado (166,9 -> 167). Sin test aplicable. Nombre de serie sin espacio final.",
        ),
    ),
    dict(
        cid="Q028",
        claim_text="La inflación industrial se dispara por culpa de la energía hasta el 13,2% interanual en agosto",
        claim_date="2026-09-24",
        post_url="https://theobjective.com/economia/2026-09-24/inflacion-industrial-sube-agosto-energia-guerra-iran/",
        post_url_tipo="prensa", emisor="The Objective", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="precios",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com precios industriales agosto 2026 13,2% IPRI energía",
        criba_query_b="precios industriales agosto 2026 13,2% IPRI inflación industrial verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'índice de precios industriales' OR IPRI agosto 2026 'según el INE' '%' interanual noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E021",
        # --- trabajo 2026-09-26 (E021 t0 13:06:52Z, t1/t2 13:08:57Z) ---
        fuente_primaria="INE - Indices de Precios Industriales (IPRI, base 2021), agosto 2026: nota IPRI0826 + API Tempus tabla 76655",
        primaria_url="https://www.ine.es/dyngs/Prensa/IPRI0826.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/76655",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="agosto 2026: IPRI total industria (mercado interior) indice 141,808 (provisional), variacion anual 13,2% (julio 9,4%); energia 33,3%; sin energia 3,5%; mensual 2,9%",
        dato_anterior="agosto 2025: indice 125,302 (definitivo), variacion anual -1,6%",
        raw_value_span_actual=(
            "[INE, nota IPRI0826, 2026-09-24] 'La variacion anual del Indice de Precios Industriales aumento 3,8 "
            "puntos en agosto, hasta el 13,2%.' | 'una variacion anual 12,1 puntos, hasta el 33,3%' (energia) | "
            "[INE API, tabla 76655, IPR34953 'Nacional. Mercado interior. Total industria. Variacion anual.'] "
            "2026-M08: 13.2 | IPR34522 (indice) 2026-M08: 141.808 || [The Objective 2026-09-24, el claim] 'La "
            "inflacion industrial se dispara por culpa de la energia hasta el 13,2% interanual en agosto'"
        ),
        raw_value_span_anterior="[INE API, tabla 76655] IPR34522 2025-M08: 125.302 (Definitivo) | IPR34953 2026-M07: 9.4",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: 141,808/125,302 - 1 = +13,17%; 'por culpa de la energia' es la atribucion del propio INE "
            "(energia +33,3%), no se evalua. En la API el indice general se llama 'Total industria' (no 'Indice "
            "general', que solo existe en la tabla antigua 1796, vacia): tres pasadas de busqueda. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE IPRI0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="76655",
                         serie_nombre="Nacional. Mercado interior. Total industria. Índice. ",
                         unidad="indice", referencia_principal="interanual",
                         descripcion="IPRI base 2021, indice general (total industria, mercado interior), mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            cambio_afirmado=13.2, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = interanual, referencia del emisor.",
        ),
    ),
    dict(
        cid="Q029",
        claim_text="El coste laboral sube un 4% en el segundo trimestre de 2026 y alcanza los 3.388 euros por trabajador",
        claim_date="2026-09-17",
        post_url="https://ahoraleon.com/coste-laboral-espana-2026/",
        post_url_tipo="prensa", emisor="Ahora León", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="salarios",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com coste laboral segundo trimestre 2026 4% 3.388 euros récord 26 años ETCL",
        criba_query_b="coste laboral segundo trimestre 2026 4% 3.388 euros 'récord' 26 años ETCL verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'coste laboral' segundo trimestre 2026 ETCL 'según el INE' sube '%' por trabajador noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E022",
        # --- trabajo 2026-09-26 (E022 t0 13:09:30Z, t1 13:10:08Z, t2 13:11:28Z tras corregir la serie) ---
        fuente_primaria="INE - Encuesta Trimestral de Coste Laboral (ETCL), 2T2026: nota ETCL2T26 + API Tempus tabla 6030",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETCL2T26.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/6030",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: coste laboral total por trabajador y mes 3.388,15 euros (definitivo), +4,04% interanual; coste salarial 2.512,68 (+4,0%)",
        dato_anterior="2T2025: 3.256,54 euros (definitivo); 1T2026: 3.278,01",
        raw_value_span_actual=(
            "[INE, nota ETCL2T26, 2026-09-17] 'El coste laboral de las empresas aumento un 4,0% en el segundo "
            "trimestre respecto al mismo periodo del ano anterior y se situo en 3.388,15 euros por trabajador y "
            "mes.' | [INE API, tabla 6030, ETCL68 'Industria, construccion y servicios (...). Coste laboral total. "
            "Total. Total Nacional. Costes laborales. Euros.'] 2026-T2: 3388.15 (Definitivo) || [Ahora Leon "
            "2026-09-17, el claim] 'El coste laboral sube un 4% en el segundo trimestre de 2026 y alcanza los "
            "3.388 euros por trabajador'"
        ),
        raw_value_span_anterior="[INE API, tabla 6030] ETCL68 2025-T2: 3256.54 (Definitivo) | 2026-T1: 3278.01",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A: 3388,15/3256,54 - 1 = +4,04%. Fallo de localizacion registrado: las tablas 6067 y 6070 "
            "('Coste laboral total por trabajador') son retrospectivas 2000-2007 y la serie vigente esta en la "
            "6030 (por sectores, desde 2008-T1); dos marcas t2 erroneas quedaron en el cronometro y se "
            "corrigieron con marcas posteriores (manda la ultima). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETCL2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="6030",
                         serie_nombre="Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de organizaciones y organismos extraterritoriales). Coste laboral total. Total. Total Nacional. Costes laborales. Euros. ",
                         unidad="euros", referencia_principal="interanual",
                         descripcion="ETCL, coste laboral total por trabajador y mes, total nacional, trimestral"),
            periodo_objetivo="2026-T2", periodo_base="2025-T2",
            valor_objetivo=3388, cambio_afirmado=4, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = interanual, referencia del emisor. NEEDS_REVIEW: nombre exacto de la serie (largo) al correrlo.",
        ),
    ),
    dict(
        cid="Q030",
        claim_text="Los costes laborales y los salarios suben en el segundo trimestre del año hasta cifras récord en 26 años",
        claim_date="2026-09-17",
        post_url="https://www.elespanol.com/invertia/economia/empleo/20260917/costes-laborales-salarios-suben-segundo-trimestre-cifras-record-anos/1003744386555_0.html",
        post_url_tipo="prensa", emisor="El Español", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="salarios",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com coste laboral segundo trimestre 2026 4% 3.388 euros récord 26 años ETCL",
        criba_query_b="coste laboral segundo trimestre 2026 4% 3.388 euros 'récord' 26 años ETCL verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'coste laboral' segundo trimestre 2026 ETCL 'según el INE' sube '%' por trabajador noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E023",
        # --- trabajo 2026-09-26 (E023 t0/t1 13:10:08Z, t2 13:11:28Z; primaria ya en mano por E022) ---
        fuente_primaria="INE - ETCL 2T2026: nota ETCL2T26 + API Tempus tablas 6030 (2008-2026) y 6067 (retrospectiva 2000-2007)",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETCL2T26.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/6030 y /6067",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: 3.388,15 euros; maximo de los segundos trimestres de la serie 2008-2026 (tabla 6030, n=19) y por encima de todos los 2T de 2000-2007 (tabla 6067, max 2.339,64 en 2007)",
        dato_anterior="2T2025: 3.256,54; 2T2007 (retrospectiva): 2.339,64",
        raw_value_span_actual=(
            "[INE API, tabla 6030, ETCL68] 2026-T2: 3388.15 (Definitivo); maximo de {k: 2T} 2008-2026 = 2026-T2 | "
            "[INE API, tabla 6067, ETCL5742 retrospectiva] 2007-T2: 2339.64 | [INE, nota ETCL2T26] '3.388,15 "
            "euros por trabajador y mes' || [El Espanol 2026-09-17, el claim] 'Los costes laborales y los "
            "salarios suben en el segundo trimestre del ano hasta cifras record en 26 anos'"
        ),
        raw_value_span_anterior="[INE API, tabla 6030] serie 2T 2008..2025 todas < 3388.15; [tabla 6067] serie 2T 2000..2007 todas < 2339.64",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D: extremo historico ('record en 26 anos' = desde 2000, inicio de la ETCL). Verificado en "
            "dos tablas con bases distintas (2000-2007 y 2008-2026): el maximo es 2026-T2; la nota del INE no "
            "dice 'record', lo anade la prensa (EP). Sin test computable en el prototipo -> undetermined "
            "(DEC-029). Nota: comparar bases 2000-2007 y 2008-2026 exige que sean comparables (cambio CNAE-09): "
            "el INE las publica separadas; se anota como salvedad."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETCL2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="INE", tabla="6030",
                         serie_nombre="Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de organizaciones y organismos extraterritoriales). Coste laboral total. Total. Total Nacional. Costes laborales. Euros. ",
                         unidad="euros", referencia_principal="interanual",
                         descripcion="ETCL, coste laboral total por trabajador y mes, total nacional, trimestral"),
            periodo_objetivo="2026-T2", valor_objetivo=3388.15,
            notas="Extremo historico: sin test aplicable en el prototipo.",
        ),
    ),
    dict(
        cid="Q031",
        claim_text="El coste laboral aumentó un 3,1% en la Región en el segundo trimestre: 2.900€ por trabajador y mes",
        claim_date="2026-09-17",
        post_url="https://www.murciadiario.com/actualidad-economica/murcia-economia-regional/coste-laboral/20260917103342149294.html",
        post_url_tipo="prensa", emisor="Murcia Diario", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="salarios",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com coste laboral segundo trimestre 2026 4% 3.388 euros récord 26 años ETCL",
        criba_query_b="coste laboral segundo trimestre 2026 4% 3.388 euros 'récord' 26 años ETCL verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="INE 'coste laboral' segundo trimestre 2026 ETCL 'según el INE' sube '%' por trabajador noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E024",
        # --- trabajo 2026-09-26 (E024 t0 13:10:08Z, t1/t2 13:11:45Z) ---
        fuente_primaria="INE - ETCL 2T2026 por comunidad autonoma: nota ETCL2T26 (anexo) + API Tempus tabla 6061",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETCL2T26.htm",
        primaria_url_tipo="nota_de_prensa_html (anexo de tablas por CCAA) + API JSON wstempus DATOS_TABLA/6061",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Region de Murcia, 2T2026: coste laboral total por trabajador y mes 2.900,37 euros (definitivo), +3,13% interanual",
        dato_anterior="Region de Murcia, 2T2025: 2.812,36 euros; 1T2026: 2.790,94",
        raw_value_span_actual=(
            "[INE API, tabla 6061, ETCL3763 'Murcia, Region de. Industria, construccion y servicios (...). Coste "
            "laboral total. Costes laborales. Euros.'] 2026-T2: 2900.37 (Definitivo) || [Murcia Diario "
            "2026-09-17, el claim] 'El coste laboral aumento un 3,1% en la Region en el segundo trimestre: 2.900 "
            "euros por trabajador y mes'"
        ),
        raw_value_span_anterior="[INE API, tabla 6061] ETCL3763 2025-T2: 2812.36 (Definitivo)",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, serie regional: 2900,37/2812,36 - 1 = +3,13%; el claim redondea (3,1%, 2.900). La nota "
            "nacional no lleva la cifra de Murcia en el texto: esta en el anexo y en la API. Independiente de E022 "
            "(otra serie y otro medio), misma edicion primaria (tres controles de ETCL2T26: E022, E024 y el D de "
            "E023; tope de 3 controles respetado con 2). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETCL2T26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="6061",
                         serie_nombre="Murcia, Región de. Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de organizaciones y organismos extraterritoriales). Coste laboral total. Costes laborales. Euros. ",
                         unidad="euros", referencia_principal="interanual",
                         descripcion="ETCL, coste laboral total por trabajador y mes, Region de Murcia, trimestral"),
            periodo_objetivo="2026-T2", periodo_base="2025-T2",
            valor_objetivo=2900, cambio_afirmado=3.1, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control regional: base = interanual, referencia del emisor.",
        ),
    ),
    # ---- jornada 2 (13:35Z): VIA DIVERGENCIA dirigida (DEC-032/033): titulares con comparacion propia ----
    dict(
        cid="Q032",
        claim_text="La generación Z ha conseguido bajar su tasa de paro. El problema es que ahora el 60% de los parados tiene más de 45 años",
        claim_date="2026-05-21",
        post_url="https://www.xataka.com/empresas-y-economia/espana-ha-batido-records-empleo-juvenil-mala-noticia-que-uno-cada-tres-parados-supera-50-anos",
        post_url_tipo="prensa", emisor="Xataka", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com 'uno de cada tres' parados '50 años' SEPE 2026 récord empleo juvenil",
        criba_query_b="'uno de cada tres parados' '50 años' empleo juvenil récord SEPE 2026 xataka verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'uno de cada' 'INE' 2026 noticia titular España hogares OR trabajadores OR jóvenes OR empresas",
        collected_at="2026-09-26", case_id="E027",
        # --- trabajo 2026-09-26 (E027 t0 13:37:29Z, t1/t2 13:43:01Z) ---
        fuente_primaria="SEPE - Datos estadisticos de empleo, abril 2026: PDF 'Demandas de empleo pendientes' (tabla 1.1, parados por sexo y edad)",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/empleo/datos/2026/Abril_2026/DATOS_NACIONALES-DEMANDAS_PENDIENTES.pdf",
        primaria_url_tipo="PDF mensual del SEPE (200 al agente identificado, 416.538 bytes, sha256 8cc589e7fd3338b0), enlazado desde la pagina de datos estadisticos de abril 2026",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="abril 2026: parados 2.357.044; de 45 o mas anos 1.376.550 (58,4%): 45-49 263.821, 50-54 302.379, 55-59 381.401, mayores de 59 428.949; de 50 o mas 1.112.729 (47,2%)",
        dato_anterior="edicion anterior = PDF de marzo 2026 (mismo patron de URL); no extraido: el claim es un nivel de abril",
        raw_value_span_actual=(
            "[SEPE, DATOS_NACIONALES-DEMANDAS_PENDIENTES.pdf abril 2026, p.1, tabla 1.1, columna PARADOS] "
            "'DE 45-49 ANOS ... 263.821' | 'DE 50-54 ANOS ... 302.379' | 'DE 55-59 ANOS ... 381.401' | 'MAYOR DE "
            "59 ANOS ... 428.949' | 'TOTAL EDAD 4.160.836 2.357.044' || [Xataka 2026-05-21, titular actual] 'La "
            "generacion Z ha conseguido bajar su tasa de paro. El problema es que ahora el 60% de los parados "
            "tiene mas de 45 anos' | [cuerpo] '1.376.550 desempleados tenian 45 anos o mas' | 'el 58,4% de todo "
            "el paro registrado' | '755.500 parados mayores de 50' | 'uno de cada tres desempleados supera ya "
            "los 50 anos'"
        ),
        raw_value_span_anterior="no aplica (nivel)",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (nivel): el titular vigente (60% de los parados > 45) cuadra: 1.376.550/2.357.044 = 58,4%, "
            "redondeado. OBSERVACION registrada, no anotada como claim: el titular ORIGINAL (en la URL y en el "
            "indice del buscador) decia 'uno de cada tres parados supera los 50', con '755.500 parados mayores de "
            "50' en el cuerpo; la tabla del SEPE da 1.112.729 parados de 50 o mas (47,2%, casi uno de cada DOS). "
            "El 755.500 no aparece en la tabla 1.1: viene del 'Informe del Mercado de Trabajo de mayores de 45' "
            "con otra definicion (NEEDS_REVIEW). Si Mateo decide anotar el titular original, seria "
            "4_denominator/other_observed con truth contradicted; se deja al criterio de la muestra a ciegas. "
            "Via divergencia que acaba en control: se cuenta como D. Tercer emisor (SEPE) recuperable en PDF; "
            "la pagina de datos no enlaza XLS sino PDF. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE abril 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="nivel",
            metrica=dict(emisor="SEPE", tabla="DEMANDAS_PENDIENTES",
                         serie_nombre="Parados registrados de 45 o más años sobre el total. Total Nacional.",
                         unidad="pct", referencia_principal="anterior",
                         descripcion="SEPE, paro registrado por edad, cuota de 45 o mas anos sobre el total, mensual"),
            periodo_objetivo="2026-M04", valor_objetivo=60,
            notas="Nivel redondeado (58,4 -> 60). Emisor sin conector: sin veredicto hoy.",
        ),
    ),
    dict(
        cid="Q033",
        claim_text="Criminalidad en España: se disparan homicidios, agresiones sexuales y la presión sobre la Policía Nacional",
        claim_date="2026-06-08",
        post_url="https://www.esdiario.com/nacional/260608/189913/criminalidad-espana-disparan-homicidios-agresiones-sexuales-presion-sobre-policia-nacional.html",
        post_url_tipo="prensa", emisor="ESdiario", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com criminalidad se disparan homicidios agresiones sexuales presión Policía Nacional primer trimestre 2026",
        criba_query_b="'se disparan homicidios' criminalidad España 2026 primer trimestre esdiario verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'delitos sexuales' OR 'agresiones sexuales' OR 'criminalidad' 'se disparan' OR 'aumentan un' 2026 'desde 2019' OR 'desde 2015' balance Interior noticia España",
        collected_at="2026-09-26", case_id="E028",
        # --- trabajo 2026-09-26 (E028 t0 13:43:01Z, t1/t2 13:43:50Z) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad (ses.mir.es): CSV 09001 'Balance de criminalidad 2026 - 1er trimestre - CCAA', bloque TOTAL NACIONAL",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAct/l0/09001.csv_c",
        primaria_url_tipo="CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (24.719 bytes, sha256 e80bce45a467c46f)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="enero-marzo 2026 (Total Nacional): homicidios dolosos y asesinatos consumados 94 (+10,6%); agresion sexual con penetracion 1.290 (+3,8%); delitos contra la libertad sexual 4.806 (+1,1%); total infracciones penales 595.240 (+1,0%)",
        dato_anterior="enero-marzo 2025 (misma tabla): homicidios consumados 85; agresion sexual con penetracion 1.243; total 589.113",
        raw_value_span_actual=(
            "[Portal Estadistico de Criminalidad, 09001.csv_c, TOTAL NACIONAL] '1. Homicidios dolosos y "
            "asesinatos consumados,85,94,10,6' | '5.1.-Agresion sexual con penetracion,1.243,1.290,3,8' | "
            "'III. TOTAL INFRACCIONES PENALES,589.113,595.240,1,0' || [ESdiario 2026-06-08, el claim] "
            "'Criminalidad en Espana: se disparan homicidios, agresiones sexuales y la presion sobre la Policia "
            "Nacional'"
        ),
        raw_value_span_anterior="[Portal Estadistico de Criminalidad, 09001.csv_c] columna 'enero-marzo 2025': 85 | 1.243 | 589.113",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A por la via divergencia: 'se disparan' = +10,6% (homicidios) y +3,8% (agresiones con "
            "penetracion) contra el mismo trimestre de 2025, que es la comparacion del propio Balance; el "
            "titular no da cifra, se estructura sobre los homicidios consumados (94, +10,6%). 'La presion sobre "
            "la Policia' es opinion sindical, no dato. HALLAZGO de recuperabilidad: la misma edicion que E025 "
            "(bloqueada en interior.gob.es) es recuperable en CSV por el Portal (DEC-032). El CSV llega en "
            "ISO-8859-15. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Interior", tabla="09001",
                         serie_nombre="1. Homicidios dolosos y asesinatos consumados. TOTAL NACIONAL",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="Portal Estadistico de Criminalidad, balance trimestral, homicidios dolosos y asesinatos consumados, total nacional"),
            periodo_objetivo="2026-T1", periodo_base="2025-T1",
            valor_objetivo=94, valor_base=85, cambio_afirmado=10.6, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control: base = mismo trimestre del ano anterior, referencia del Balance. Emisor sin conector (CSV del Portal): sin veredicto hoy.",
        ),
    ),
    dict(
        cid="Q034",
        claim_text="El INE rebaja el crecimiento del PIB en 2025 al 2,6%, sube el de 2024 al 3,7% y baja el de 2023 al 2,4%",
        claim_date="2026-09-18",
        post_url="https://www.pressdigital.es/articulo/economia/2026-09-18/6020002-ine-rebaja-crecimiento-pib-2025-26-sube-2024-37-baja-2023-24",
        post_url_tipo="prensa", emisor="Pressdigital", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="pib",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com INE rebaja crecimiento PIB 2025 2,6% sube 2024 3,7% baja 2023 2,4% revisión",
        criba_query_b="INE rebaja PIB 2025 al 2,6% sube 2024 al 3,7% baja 2023 al 2,4% verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'respecto a 2023' OR 'respecto a 2022' OR 'frente a 2021' OR 'que en 2020' 'según el INE' 2026 noticia '%' sube OR cae España",
        # PENDIENTE. Revision anual de la Contabilidad Nacional (2026-09-18): tres cifras revisadas.
        # Esperado: D (revision entre ediciones, sin test).
    ),
    dict(
        cid="Q035",
        claim_text="Los españoles se endeudan más: la demanda de crédito se dispara un 130%, hasta máximos históricos, y la morosidad se desploma",
        claim_date="2026-02-18",
        post_url="https://www.infobae.com/espana/2026/02/18/los-espanoles-se-endeudan-mas-la-demanda-de-credito-se-dispara-un-130-hasta-maximos-historicos-y-la-morosidad-se-desploma/",
        post_url_tipo="prensa", emisor="Infobae España", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="credito",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com demanda de crédito se dispara 130% máximos históricos morosidad Banco de España 2026",
        criba_query_b="demanda de crédito '130%' máximos históricos morosidad se desploma Banco de España 2026 verificación OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="fuera_de_alcance: la cifra del titular (demanda de credito +130%) es de Asnef/Equifax, una asociacion privada, no de un emisor del conjunto; solo la morosidad (1,71%, minimos desde 2008) es del Banco de Espana. No es la regla dura",
        criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'Banco de España' 2026 'récord' OR 'máximo histórico' OR 'desde 2008' deuda OR depósitos OR crédito OR morosidad '%' noticia titular",
    ),
    dict(
        cid="Q036",
        claim_text="La compraventa de viviendas cae un 12,4% en Euskadi y encadena tres meses de descensos",
        claim_date="2026-09-25",
        post_url="https://www.deia.eus/economia/2026/09/25/compraventa-viviendas-cae-12-4-11582445.html",
        post_url_tipo="prensa", emisor="Deia", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com compraventa viviendas Euskadi cae 12,4% julio 2026 tres meses descensos",
        criba_query_b="compraventa viviendas Euskadi cae 12,4% julio 2026 'tres meses' descensos verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'compraventa' viviendas 'agosto' 2026 '5,1%' OR '61.417' noticia -julio",
        collected_at="2026-09-26", case_id="E029",
        # --- trabajo 2026-09-26 (E029 t0 13:45:41Z, t1 13:45:48Z, t2 13:46:32Z) ---
        fuente_primaria="INE - ETDP julio 2026: nota ETDP0726 (tabla por CCAA) + API Tempus tabla 6150, serie Pais Vasco",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETDP0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/6150",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Pais Vasco, julio 2026: 2.139 compraventas de viviendas (provisional), -12,37% interanual; junio 2.138 (-5,5% interanual); mayo 1.964",
        dato_anterior="Pais Vasco, julio 2025: 2.441 (definitivo); junio 2025: 2.263",
        raw_value_span_actual=(
            "[INE API, tabla 6150, ETDP1746 'Pais Vasco. General. Compraventa. Numero.'] 2026-M07: 2139 "
            "(Provisional) | 2026-M06: 2138 | 2026-M05: 1964 || [Deia 2026-09-25, el claim] 'La compraventa de "
            "viviendas cae un 12,4% en Euskadi y encadena tres meses de descensos'"
        ),
        raw_value_span_anterior="[INE API, tabla 6150] ETDP1746 2025-M07: 2441 (Definitivo) | 2025-M06: 2263",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia: 2139/2441 - 1 = -12,37%, interanual = referencia. 'Tres meses de "
            "descensos': julio y junio comprobados (-12,4 y -5,5); mayo 2025 quedo fuera de la ventana pedida "
            "(nult=14) y no se comprobo (NEEDS_REVIEW menor). Tercer caso de la edicion ETDP0726 (A: E001, E029; "
            "O: E002). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETDP0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="6150",
                         serie_nombre="País Vasco. General. Compraventa. Número. ",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="ETDP, compraventas de viviendas inscritas, Pais Vasco, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=2139, cambio_afirmado=-12.4, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Control regional: base = interanual, referencia del emisor.",
        ),
    ),
    dict(
        cid="Q037",
        claim_text="La creación de empresas registró su mejor julio en 31 años, con 11.150 nuevas sociedades",
        claim_date="2026-09-10",
        post_url="https://theobjective.com/economia/2026-09-10/creacion-empresas-mejor-julio-31-anos/",
        post_url_tipo="prensa", emisor="The Objective", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empresas",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com creación de empresas mejor julio 31 años 11.150 sociedades 2026",
        criba_query_b="creación de empresas 'mejor julio' 31 años 11.150 sociedades 2026 verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="sociedades mercantiles julio 2026 'según el INE' creación de empresas cae OR sube OR baja '%' noticia titular",
        collected_at="2026-09-26", case_id="E030",
        # --- trabajo 2026-09-26 (E030 t0 13:46:32Z, t1/t2 13:46:48Z) ---
        fuente_primaria="INE - Estadistica de Sociedades Mercantiles (SM), julio 2026: nota SM0726 + API Tempus tabla 13913 (serie mensual desde 1995)",
        primaria_url="https://www.ine.es/dyngs/Prensa/SM0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_TABLA/13913 (nult=400)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: 11.150 sociedades mercantiles constituidas (provisional), +2,24% interanual; maximo de los 32 julios de la serie (1995-2026); siguientes: julio 2006 11.074, julio 2007 10.976",
        dato_anterior="julio 2025: 10.906 (definitivo)",
        raw_value_span_actual=(
            "[INE API, tabla 13913, SM21483 'Sociedades Constituidas. Numero de Sociedades. Total Nacional. "
            "Mercantiles.'] 2026-M07: 11150 (Provisional) | maximo de {2026-M07..1995-M07} = 2026-M07 | 2006-M07: "
            "11074 | 2007-M07: 10976 || [The Objective 2026-09-10, el claim] 'La creacion de empresas registro su "
            "mejor julio en 31 anos, con 11.150 nuevas sociedades'"
        ),
        raw_value_span_anterior="[INE API, tabla 13913] SM21483 2025-M07: 10906 (Definitivo)",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (extremo historico), via divergencia: el maximo de los julios 1995-2026 es 2026 (11.150) "
            "por 76 sociedades sobre 2006; '31 anos' = 1995-2026 cuadra. Sin test computable en el prototipo -> "
            "undetermined (DEC-029). Misma tabla que P11 (piloto) pero edicion distinta (julio 2026 vs 2018): "
            "admisible por DEC-025. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE SM0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="INE", tabla="13913",
                         serie_nombre="Sociedades Constituídas. Número de Sociedades. Total Nacional. Mercantiles. ",
                         unidad="unidades", referencia_principal="interanual",
                         descripcion="Sociedades mercantiles constituidas, total nacional, mensual"),
            periodo_objetivo="2026-M07", valor_objetivo=11150,
            notas="Extremo historico (maximo de los julios): sin test aplicable en el prototipo.",
        ),
    ),
    dict(
        cid="Q038",
        claim_text="La compraventa de vivienda cae un 7,7% en julio y registra su mayor descenso de 2026",
        claim_date="2026-09-07",
        post_url="https://www.infoconstruccion.es/noticias/20260907/compraventa-vivienda-julio-2026-hipotecas",
        post_url_tipo="prensa", emisor="Infoconstrucción", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="vivienda",
        criba_query_a="", criba_query_b="",
        criba_resultado="rechazado",
        criba_motivo="fuera_de_alcance: la cifra (-7,7%, ~60.500 operaciones) es del Colegio de Registradores (Estadistica Registral Inmobiliaria), no de un emisor del conjunto; no atribuye al INE. No es la regla dura",
        criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'compraventas' OR 'compraventa de viviendas' 2026 'desde el máximo' OR 'desde el récord' OR 'desde 2025' caen OR han caído OR retroceden '%' noticia -'mismo mes'",
    ),
    dict(
        cid="Q039",
        claim_text="Las pernoctaciones hoteleras en la Comunidad de Madrid aumentan un 2,36% en agosto, con 2,17 millones de estancias",
        claim_date="2026-09-22",
        post_url="https://www.ultimahora.es/noticias/comunidades/2026/09/22/2713683/pernoctaciones-hoteleras-comunidad-madrid-aumentan-agosto-millones-estancias.html",
        post_url_tipo="prensa", emisor="Última Hora (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras Comunidad de Madrid agosto 2026 2,36% 2,17 millones",
        criba_query_b="pernoctaciones hoteleras Comunidad de Madrid agosto 2026 '2,36%' OR '2,17 millones' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="[hallado entre los resultados del barrido de la nota CTH0826 y de la criba de E019; la consulta exacta que lo devolvio no quedo registrada: NEEDS_REVIEW] 'pernoctaciones hoteleras' 'Comunidad de Madrid' agosto 2026",
        collected_at="2026-09-26", case_id="E031",
        # --- trabajo 2026-09-26 (E031 t0 13:47:35Z, t1 13:53:39Z, t2 13:55:05Z) ---
        fuente_primaria="INE - Coyuntura Turistica Hotelera agosto 2026 (CTH0826): nota HTML + anexo de tablas CTH0826.xlsx (hoja EOH_Hoja3, fila 'Madrid, Comunidad de') + API Tempus tablas 2074/36570; edicion anterior: anexo CTH0825.xlsx (agosto 2025, provisional)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + anexo xlsx /prensa/anexo_tablas/es/CTH0826.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Comunidad de Madrid, agosto 2026 (provisional): pernoctaciones 2.165.029 (residentes 796.393; extranjeros 1.368.637); viajeros 1.082.623 (454.617 / 628.006)",
        dato_anterior="Comunidad de Madrid, agosto 2025. Edicion vigente (API, revisada): pernoctaciones 2.090.878 (780.648 / 1.310.230); viajeros 1.012.363. Edicion provisional (anexo CTH0825, 2025-09-23): pernoctaciones 2.115.059 (785.462 / 1.329.597); viajeros 1.025.795 (436.770 / 589.025)",
        raw_value_span_actual=(
            "[CTH0826.xlsx, hoja EOH_Hoja3, fila 62] 'Madrid, Comunidad de', 1082623, 454617, 628006, 2165029, "
            "796393, 1368637, 2 || [INE API tabla 2074, EOT1766 'Madrid (Comunidad de). Pernoctaciones. Total.'] "
            "2026-M08: 2165029 || [Ultima Hora/EP 2026-09-22, el claim] 'aumentaron un 2,36% en agosto ... hasta "
            "sumar 2,17 millones'; 'un 5,54% mas de turistas ... 1.082.623 viajeros'; 'residentes en Espana "
            "aumentaron un 1,39% ... un 2,94% las de los foraneos'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1766 2025-M08: 2090878 | EOT1767 (residentes) 780648 | EOT1768 (extranjero) "
            "1310230 | EOT1763 (viajeros) 1012363 || [CTH0825.xlsx, hoja EOH_Hoja3, fila 61, datos provisionales "
            "agosto 2025] 'Madrid, Comunidad de', 1025795, 436770, 589025, 2115059, 785462, 1329597, 2.06"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta C (2b, base revisada), via divergencia. El nivel (2,17 M) cuadra; la tasa no: contra la "
            "edicion vigente de agosto 2025 (2.090.878) el INE da +3,55%. Las CUATRO tasas del teletipo se "
            "reproducen exactamente con la edicion PROVISIONAL de agosto 2025 (anexo CTH0825): pernoctaciones "
            "2165029/2115059 = +2,36%; viajeros 1082623/1025795 = +5,54%; residentes 796393/785462 = +1,39%; "
            "extranjeros 1368637/1329597 = +2,94%. Contra la edicion vigente serian +3,55 / +6,94 / +2,02 / +4,46. "
            "El anexo por CCAA no trae columna de variacion: la agencia calcula la tasa con su propia base del "
            "ano anterior (provisional), no con la revisada. Mismo signo: el test 2a del prototipo no disparia "
            "(esperado: no_divergence_detected; la clase 2b esta fuera del prototipo, DEC-029/TESIS-ENCUADRE). "
            "Hermano potencial: madridactual.es 2026-09-22 (mismo teletipo, no registrado). Segundo caso de la "
            "edicion CTH0826 (E019 A, E020 D). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",  # C -> B por DEC-034
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Madrid (Comunidad de). Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Comunidad de Madrid, mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            valor_objetivo=2165029, cambio_afirmado=2.36, unidad_cambio="pct", direccion_afirmada="sube",
            # DEC-034: las dos evidencias del veredicto 2b, cada una con su fecha.
            evidencia_al_publicar=dict(
                valor=2115059, edicion="INE CTH0825 (agosto 2025, datos provisionales)", fecha="2025-09-23",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0825.xlsx",
                raw_value_span="[CTH0825.xlsx, hoja EOH_Hoja3, fila 61] 'Madrid, Comunidad de', 1025795, 436770, 589025, 2115059, 785462, 1329597, 2.06",
                verificacion="research/evidencia/D2B_CTH0825.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=2090878, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] EOT1766 2025-M08: 2090878",
            ),
            notas="Base interanual correcta en periodo, pero tomada de la edicion provisional (2.115.059) y no de la vigente (2.090.878): 2b. Sin cambio de signo.",
        ),
    ),
    dict(
        cid="Q040",
        claim_text="El Instituto Nacional de Estadística (INE) ha revelado un desplome del 15% en hipotecas nuevas en abril de 2026, la caída más dura en cinco años",
        claim_date="2026-05-31",
        post_url="https://www.euribor.com.es/2026/05/31/el-desplome-del-mercado-hipotecario-15-menos-de-firmas-en-abril-revela-la-nueva-realidad-inmobiliaria/",
        post_url_tipo="prensa", emisor="euribor.com.es", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com hipotecas abril 2026 '15%' desplome INE",
        criba_query_b="'desplome del 15%' hipotecas abril 2026 INE verificación OR bulo OR fact-check OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="hipotecas viviendas abril 2026 'caen' OR 'se desploman' OR 'bajan' 'respecto a marzo' OR 'mensual' '14%' OR '14,2%' OR '14,3%' INE noticia",
        collected_at="2026-09-26", case_id="E034",
        # Nota de criba: primero se anoto 'rechazado: fuera_de_alcance (nivel 3)'; se corrigio antes de commitear
        # porque el alcance de nivel 1 (DEC-024) es de los EMISORES DE DATOS, no de los publicadores del claim
        # (EMISOR_NIVEL admite 1-5 y el lote crudo tenia niveles 3). Cribas (a) y (b) limpias.
        # --- trabajo 2026-09-26 (E034 t0 14:06:5xZ, t1/t2 14:07:20Z) ---
        fuente_primaria="INE - Estadistica de Hipotecas abril 2026: nota H0426 (2026-06-22) + API Tempus serie HPT34618 (tabla 76316)",
        primaria_url="https://www.ine.es/dyngs/Prensa/H0426.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_SERIE/HPT34618",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="abril 2026: 40.010 hipotecas sobre viviendas (provisional), +2,3% interanual; -14,3% respecto a marzo (46.661)",
        dato_anterior="abril 2025: 39.103 (definitivo); marzo 2026: 46.661",
        raw_value_span_actual=(
            "[INE H0426, 22/06/2026] 'El numero de hipotecas sobre viviendas inscritas en los registros de la "
            "propiedad fue de 40.010, un 2,3% mas en tasa anual'; tabla resumen: '40.010', '-14,3', '2,3' || "
            "[INE API] HPT34618 2026-M04: 40010 || [euribor.com.es 2026-05-31, el claim] 'El Instituto Nacional de "
            "Estadistica (INE) ha revelado un desplome del 15% en hipotecas nuevas en abril de 2026, la caida mas "
            "dura en cinco anos'"
        ),
        raw_value_span_anterior=(
            "[INE API] HPT34618 2025-M04: 39103 | 2026-M03: 46661 || caidas mensuales mas fuertes de la serie "
            "desde 2021 (calculo propio sobre HPT34618): 2025-M08 -26,2%, 2023-M04 -26,1%, 2024-M11 -25,8%"
        ),
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="claim_falso", excedente="no",
        notas=(
            "Cubeta F (claim falso), via divergencia. Ninguna cifra del INE para abril 2026 es -15%: interanual "
            "+2,3% (22 meses de subidas), mensual -14,3% (que tampoco es 'la caida mas dura en cinco anos': -26,2% "
            "en agosto 2025, -26,1% en abril 2023). Ademas el post es del 31-05-2026 y el INE publico abril el "
            "22-06-2026: en la fecha del post el dato no existia. Origen posible, no comprobado (NEEDS_REVIEW): otra "
            "fuente (BdE, nuevas operaciones) o texto generado. Lo incorrecto es el numero, no el marco: sin "
            "divergencia contextual. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="F", hermano_de="", mecanismo_candidato="", primaria_edicion="INE H0426",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="76316",
                         serie_nombre="Viviendas. Número de hipotecas. Total Nacional. Base nueva. ",
                         unidad="hipotecas", referencia_principal="interanual",
                         descripcion="Estadistica de Hipotecas, hipotecas constituidas sobre viviendas, mensual"),
            periodo_objetivo="2026-M04", periodo_base="",
            valor_objetivo=None, cambio_afirmado=-15.0, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Base no declarada en el claim ('desplome del 15% en abril'); ni la mensual ni la interanual dan -15%.",
        ),
    ),
    dict(
        cid="Q041",
        claim_text="El paro sube un 2,5% en Madrid hasta los 280.512 desempleados y se pierden más de 36.000 cotizantes",
        claim_date="2026-09-02",
        post_url="https://gacetinmadrid.com/2026/09/02/paro-sube-25-madrid-280512-desempleados-36000-cotizantes/",
        post_url_tipo="prensa", emisor="Gacetín Madrid", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com paro Madrid agosto 2026 280.512 2,5% cotizantes",
        criba_query_b="paro 'Comunidad de Madrid' agosto 2026 '280.512' OR '2,5%' '6.881' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="paro 'Comunidad de Madrid' agosto 2026 baja OR desciende OR 'se reduce' interanual OR 'respecto al año anterior' OR 'en el último año' Ayuso OR 'Gobierno regional' noticia septiembre 2026 -'44.419'",
        collected_at="2026-09-26", case_id="E032",
        # --- trabajo 2026-09-26 (E032 t0 13:59Z; t1/t2 14:1xZ) ---
        fuente_primaria="SEPE - Paro registrado agosto 2026: nota 'El paro registrado sube en agosto en 44.419 personas...' (2026-09-02) + datos avance xls 'evolprovsectores.xls' (Evolucion mensual del paro registrado por provincias y CCAA, agosto 2026)",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_avance/xls/empleo/evolprovsectores.xls",
        primaria_url_tipo="xls de datos avance (HTTP 200 al agente identificado, 69.632 bytes) + nota HTML sepe.es/noticia/SEPE/2026/Septiembre/paro-registrado-sube-agosto-44419-personas (HTTP 200)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Comunidad de Madrid, agosto 2026: 280.512 parados registrados; +6.881 respecto a julio (+2,51%)",
        dato_anterior="Comunidad de Madrid, julio 2026: 273.631 (columna MES ANTERIOR del mismo fichero)",
        raw_value_span_actual=(
            "[evolprovsectores.xls, hoja 'Total sectores', fila 58] 53.0, 'COM. DE MADRID', 273631.0, 280512.0, "
            "6881.0, 2.514700454261396 || [fila 68] 'TOTAL', 2311499.0, 2355918.0, 44419.0, 1.9216534378773256 || "
            "[Gacetin Madrid 2026-09-02, el claim] 'El paro sube un 2,5% en Madrid hasta los 280.512 desempleados'"
        ),
        raw_value_span_anterior=(
            "[evolprovsectores.xls, hoja 'Total sectores', columna MES ANTERIOR] 'COM. DE MADRID', 273631.0 || "
            "[nota SEPE 2026-09-02] 'Aumenta en el resto de comunidades autonomas con Catalunya (14.594), Comunidad "
            "de Madrid (6.881)'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor SEPE (primer control SEPE del conjunto), via divergencia. 280512/273631 - 1 = +2,51%; "
            "la base mensual es la referencia de cabecera del SEPE ('sube en agosto en 44.419'). 'Se pierden mas de "
            "36.000 cotizantes' es afiliacion (Seguridad Social), fuera del alcance de emisores: no se evalua. "
            "Hermano potencial: madridpress.com 2026-09-02 ('sube un 2,51%'). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE paro agosto 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="SEPE", tabla="evolprovsectores.xls / Total sectores",
                         serie_nombre="COM. DE MADRID", unidad="personas", referencia_principal="mensual",
                         descripcion="Paro registrado, Comunidad de Madrid, mensual (datos avance SEPE)"),
            periodo_objetivo="2026-M08", periodo_base="2026-M07",
            valor_objetivo=280512, cambio_afirmado=2.5, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control SEPE: base mensual = referencia de cabecera del emisor.",
        ),
    ),
    dict(
        cid="Q042",
        claim_text="La deuda pública cae en julio por debajo del 100% del PIB aunque se mantiene por encima de los 1,7 billones de euros",
        claim_date="2026-09-17",
        post_url="https://www.elespanol.com/invertia/economia/20260917/deuda-publica-cae-julio-debajo-primera-vez-febrero-pandemia/1003744386741_0.html",
        post_url_tipo="prensa", emisor="El Español (Invertia)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="deuda_publica",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública julio 2026 '100% del PIB' OR '99,9%' 1,7 billones Banco de España",
        criba_query_b="'deuda pública' julio 2026 '99,9%' OR '1,744 billones' OR 'por debajo del 100%' verificación OR bulo OR fact-check OR desmiente",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'deuda pública' julio 2026 OR 'segundo trimestre' récord 'billones' sube OR aumenta 'Banco de España' '% del PIB' baja noticia septiembre 2026",
        collected_at="2026-09-26", case_id="E033",
        # --- trabajo 2026-09-26 (E033 t0 14:03:16Z, t1/t2 14:05:20Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual julio 2026: nota 'La deuda de las Administraciones Publicas se situo en julio de 2026 en el 99,9% del PIB' (17/09/2026) + PDF presbe2026-82.pdf; ediciones anteriores: junio 2026 (18/08/2026) y julio 2025",
        primaria_url="https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-julio26.html",
        primaria_url_tipo="nota_de_prensa_html (HTTP 200 al agente identificado) + PDF /f/webbe/GAP/Secciones/SalaPrensa/NotasInformativas/26/presbe2026-82.pdf; series en a11b.pdf / a12c.pdf",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="html",
        dato_actual="julio 2026: ratio deuda PDE/PIB 99,9% ('por debajo del 100% por primera vez desde febrero de 2020'); saldo 1.744 mm EUR, +3,8% interanual",
        dato_anterior="junio 2026: 101,5%, 1.763 mm EUR, +4,2% interanual (nota 18/08/2026); julio 2025: 102,3%, 1.680 mm EUR, +3,9% (nota de 2025)",
        raw_value_span_actual=(
            "[BdE deuda-aapp-julio26, 17/09/2026] 'la ratio de la deuda de las Administraciones Publicas (AAPP) "
            "segun el Protocolo de Deficit Excesivo (PDE) en relacion al Producto Interior Bruto (PIB) nominal se "
            "situo en el 99,9% en julio de 2026'; 'Segun la estimacion disponible para julio, la ratio habria "
            "descendido por debajo del 100% por primera vez desde febrero de 2020, antes de la pandemia'; '1.744 "
            "miles de millones (mm) de euros en julio de 2026, con una tasa de crecimiento interanual del 3,8%' || "
            "[El Espanol 2026-09-17, el claim] titular"
        ),
        raw_value_span_anterior=(
            "[BdE deuda-aapp-junio26, 18/08/2026] 'se situo en el 101,5% en junio de 2026'; '1.763 miles de "
            "millones (mm) de euros en junio de 2026, con una tasa de crecimiento interanual del 4,2%' || [BdE "
            "deuda-aapp-julio25] 'se situo en julio de 2025 en el 102,3% del PIB, 1,9 pp menos respecto al mismo "
            "periodo del ano anterior'; '1.680 miles de millones (mm) de euros en julio de 2025, con una tasa de "
            "crecimiento interanual del 3,9%'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor Banco de Espana (primer caso BdE del conjunto), via divergencia. Comprobado: 99,9 < "
            "100 y 'primera vez desde febrero de 2020' lo dice la propia nota; 1.744 mm > 1,7 billones; 'cae en "
            "julio' = 101,5 -> 99,9 (-1,6 pp mensual) y 1.763 -> 1.744 mm; interanual -2,4 pp (102,3 -> 99,9). "
            "Referencia del emisor: interanual (las cabeceras de 2025 van en pp interanuales) y la propia nota "
            "sostiene el descenso mensual. Mismo signo en ambas bases: no hay 2a. La nota enlaza notamet_pde.pdf "
            "(no abierto: methodology_found NEEDS_REVIEW, pasada final)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="BdE deuda-aapp-julio26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Banco de España", tabla="Deuda PDE de las AAPP (avance mensual)",
                         serie_nombre="Ratio deuda PDE / PIB nominal, total AAPP", unidad="% del PIB",
                         referencia_principal="interanual",
                         descripcion="Deuda segun el Protocolo de Deficit Excesivo, ratio sobre PIB, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2026-M06",
            valor_objetivo=99.9, cambio_afirmado=-1.6, unidad_cambio="pp", direccion_afirmada="baja",
            notas="El claim afirma direccion ('cae por debajo del 100%'); la magnitud mensual (-1,6 pp) sale de las dos notas.",
        ),
    ),
    dict(
        cid="Q043",
        claim_text="En el primer trimestre de 2026 el número total de infracciones penales en Alcorcón pasó de 1.701 en 2025 a 2.215, un incremento del 30,2%",
        claim_date="2026-09-24",
        post_url="https://www.elicebergdemadrid.com/sur/vox-alcorcon-alerta-de-un-nuevo-incremento-de-la-delincuencia/",
        post_url_tipo="declaracion", emisor="Vox Alcorcón (declaración recogida por El Iceberg de Madrid)", emisor_tipo="partido_politico",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Alcorcón criminalidad 2026 Vox 30% delincuencia",
        criba_query_b="Alcorcón criminalidad 'primer trimestre' 2026 '30,2%' OR '2.215' OR '25,1%' OR '4.367' Vox verificación OR bulo OR fact-check OR desmiente",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'criminalidad' OR 'delitos' 2026 'primer trimestre' 'desde 2018' OR 'respecto a 2019' OR 'desde que gobierna' sube OR aumenta OR 'se dispara' '%' Vox OR PP OR Marlaska OR 'Balance de Criminalidad' declaración noticia -'segundo trimestre'",
        collected_at="2026-09-26", case_id="E036",
        # --- trabajo 2026-09-26 (E036 t0 14:10:54Z, t1 14:17Z, t2 14:2xZ) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 1T2026, tabla 09003 'Capitales de provincia, municipios mayores de 20.000 habitantes e islas', bloque '28007 Alcorcon'",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAct/l0/09003.csv_c",
        primaria_url_tipo="CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (548.984 bytes, sha256 949be9399eb00fd4); evidencia en research/evidencia/E036_portal_criminalidad_1T2026_alcorcon.txt",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Alcorcon, enero-marzo 2026: 2.215 infracciones penales (convencional 1.711; cibercriminalidad 504); variacion 2026/2025 +30,2% (columna del Portal)",
        dato_anterior="Alcorcon, enero-marzo 2025: 1.701 (convencional 1.413; ciber 288), columna 'enero-marzo 2025' de la misma tabla",
        raw_value_span_actual=(
            "[09003.csv_c, bloque '28007 Alcorcón'] 'III. TOTAL INFRACCIONES PENALES,1.701,2.215,30,2,' | "
            "'I. CRIMINALIDAD CONVENCIONAL,1.413,1.711,21,1,' | 'II. CIBERCRIMINALIDAD (infracciones penales "
            "cometidas en/por medio ciber),288,504,75,0,' || [El Iceberg de Madrid 2026-09-24, el claim] 'numero "
            "total de infracciones penales pasara de 1.701 en 2025 a 2.215 en 2026, un incremento del 30,2%'"
        ),
        raw_value_span_anterior="[09003.csv_c, columna 'enero-marzo 2025'] 'III. TOTAL INFRACCIONES PENALES,1.701,2.215,30,2,'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor Interior via Portal Estadistico (segundo caso del Portal tras E028), via divergencia "
            "(declaracion de partido). 2215/1701 - 1 = +30,2% = columna 'Variacion %' del Portal; la base "
            "interanual (mismo trimestre del ano anterior) es la referencia del emisor. El resto del comunicado de "
            "Vox (1S2026: 4.367, +25,1%; 2T2026: 2.152, +20,2%) no se usa: edicion 2T2026 vetada por DEC-025 (C18). "
            "El Portal sirve las tablas de 1T y 2T bajo 'DatosBalanceAct'; la ruta 'DatosBalanceAnt/20261' devuelve "
            "una pagina de error al agente. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Ministerio del Interior", tabla="09003 (Portal Estadistico, Balance 1T2026)",
                         serie_nombre="28007 Alcorcón · III. TOTAL INFRACCIONES PENALES", unidad="hechos conocidos",
                         referencia_principal="interanual",
                         descripcion="Balance de criminalidad, infracciones penales, municipio de Alcorcon, trimestral"),
            periodo_objetivo="2026-T1", periodo_base="2025-T1",
            valor_objetivo=2215, cambio_afirmado=30.2, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control Interior/Portal: base interanual = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q044",
        claim_text="Las pernoctaciones hoteleras aumentaron un 2,39% en julio",
        claim_date="2026-08-21",
        post_url="https://rtvc.es/las-pernoctaciones-hoteleras-aumentaron-un-239-en-julio-21-agosto-2026/",
        post_url_tipo="prensa", emisor="RTVC (Radiotelevisión Canaria)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras Canarias julio 2026 2,39% 6,78 millones",
        criba_query_b="pernoctaciones hoteleras Canarias julio 2026 '2,39%' OR '6,78 millones' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' julio 2026 Europa Press 'Comunidad de Madrid' OR Baleares OR Canarias OR Andalucía OR Cataluña OR 'Comunitat Valenciana' aumentan OR caen '%' agosto 2026 -agosto",
        collected_at="2026-09-26", case_id="E035",
        # --- trabajo 2026-09-26 (E035 t0/t1/t2 14:0xZ; anexos descargados en la criba) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): anexo CTH0726.xlsx (EOH_Hoja3, fila 'Canarias') + API Tempus tabla 2074 serie EOT1544; edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (julio 2025 provisional)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/CTH0726.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Canarias, julio 2026 (provisional): 6.781.369 pernoctaciones (viajeros 1.058.995), +2,39% interanual",
        dato_anterior="Canarias, julio 2025. Edicion vigente (API): 6.622.855. Edicion provisional (anexo CTH0725): 6.552.626",
        raw_value_span_actual=(
            "[CTH0726.xlsx, hoja EOH_Hoja3, fila 24] 'Canarias', 1058995, 310471, 748524, 6781369, 1204609, "
            "5576760, 6.4 || [INE API tabla 2074] EOT1544 'Canarias. Pernoctaciones. Total.' 2026-M07: 6781369 || "
            "[RTVC 2026-08-21, el claim] 'Las pernoctaciones hoteleras aumentaron un 2,39% en julio' (Canarias, "
            "6,78 millones)"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1544 2025-M07: 6622855 || [CTH0725.xlsx, hoja EOH_Hoja3, fila 24, datos "
            "provisionales julio 2025] 'Canarias', 999568, 283655, 715913, 6552626, 1172408, 5380218, 6.56"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia. 6781369/6622855 - 1 = +2,39%: la tasa se calculo contra la "
            "edicion VIGENTE (revisada) de julio 2025, a diferencia de E031/E042/E043 (base provisional). Contra "
            "la provisional habria dado +3,49%. Hermano potencial: eldiario.es/canariasahora 2026-08-21 (mismo "
            "teletipo). Primer caso de CTH0726 (luego E042 C, E043 C). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Canarias. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Canarias, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=6781369, cambio_afirmado=2.39, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q045",
        claim_text="La inflación industrial se dispara al 13,2% en agosto por la energía y marca récord en casi cuatro años",
        claim_date="2026-09-24",
        post_url="https://www.deia.eus/economia/2026/09/24/inflacion-industrial-dispara-13-2-11578239.html",
        post_url_tipo="prensa", emisor="Deia (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="precios",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com precios industriales agosto 2026 13,2% récord energía",
        criba_query_b="'inflación industrial' OR 'precios industriales' agosto 2026 '13,2%' 'casi cuatro años' OR 'diciembre de 2022' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'producción industrial' OR 'compraventa de viviendas' 'en agosto' 2026 INE '%' noticia septiembre 2026 -julio -'agosto de 2025'",
        collected_at="2026-09-26", case_id="E037",
        # --- trabajo 2026-09-26 (E037 t0/t1/t2 14:2xZ; la serie ya estaba descargada para E021) ---
        fuente_primaria="INE - IPRI agosto 2026: nota IPRI0826 + API Tempus serie IPR34522 (tabla 76655), nult=60",
        primaria_url="https://www.ine.es/dyngs/Prensa/IPRI0826.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_SERIE/IPR34522",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="agosto 2026: IPRI general (mercado interior) 141,8; tasa anual +13,17% (julio: +9,36%)",
        dato_anterior="tasas anuales anteriores >= 13,17%: 2022-M09 35,6 | 2022-M10 25,0 | 2022-M11 20,5 | 2022-M12 14,9; ninguna entre 2023-M01 (7,8) y 2026-M07 (9,4)",
        raw_value_span_actual=(
            "[INE API] IPR34522 2026-M08: 141.8 | 2026-M07: 137.8 (tasa anual calculada 13,17%; la nota IPRI0826 "
            "dice 13,2%, ver E021) || [Deia/EP 2026-09-24, el claim] 'La inflacion industrial se dispara al 13,2% "
            "en agosto por la energia y marca record en casi cuatro anos'"
        ),
        raw_value_span_anterior=(
            "[INE API IPR34522, nult=60, tasas anuales calculadas] 2022-M12: 14,86 | 2023-M01: 7,82 | maximo de "
            "2023-M01..2026-M07 < 13,17"
        ),
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (extremo), via divergencia. 'Record en casi cuatro anos' = tasa anual mas alta desde "
            "diciembre 2022 (3 anos y 8 meses): comprobado sobre la serie, ninguna tasa >= 13,17 entre 2023-M01 y "
            "2026-M07. Segundo caso de IPRI0826 (E021, A). 'Por la energia' es atribucion causal: no se evalua. "
            "Sin test aplicable en el prototipo -> undetermined (DEC-029). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE IPRI0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="INE", tabla="76655",
                         serie_nombre="Nacional. Mercado interior. Total industria. Índice. ",
                         unidad="tasa anual %", referencia_principal="interanual",
                         descripcion="IPRI, indice general mercado interior, tasa de variacion anual, mensual"),
            periodo_objetivo="2026-M08", valor_objetivo=13.2,
            notas="Extremo: maximo de la tasa anual desde 2022-M12. Sin test aplicable.",
        ),
    ),
    dict(
        cid="Q046",
        claim_text="El paro sube en 44.419 personas, su mayor alza en agosto desde 2019, lastrado por los servicios",
        claim_date="2026-09-02",
        post_url="https://theobjective.com/economia/empleo/2026-09-02/paro-sube-44-419-personas-peor-agosto-2019-lastrado-servicios/",
        post_url_tipo="prensa", emisor="The Objective (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com paro agosto 2026 44.419 'mayor alza' OR 'mayor subida' desde 2019",
        criba_query_b="paro agosto 2026 '44.419' 'mayor alza en agosto desde 2019' OR 'mayor subida en un mes de agosto desde 2019' OR 'peor agosto desde 2019' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'el paro baja' OR 'el paro desciende' OR 'el paro se reduce' 'en agosto' 2026 '2,9%' OR '70.593' OR '2,91%' titular noticia -'sube en agosto'",
        collected_at="2026-09-26", case_id="E039",
        # --- trabajo 2026-09-26 (E039 t0 14:3xZ, t1/t2 14:4xZ) ---
        fuente_primaria="SEPE - Paro registrado agosto 2026: nota 2026-09-02 + datos avance 'evolparoseries.pdf' (Evolucion del paro registrado segun sectores, ultimos 10 anos: niveles mensuales 2017-2026)",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_avance/pdf/empleo/evolparoseries.pdf",
        primaria_url_tipo="PDF de datos avance (HTTP 200 al agente identificado, 83.086 bytes); el xls homologo (evolparoseries.xls) no lo abre xlrd (cabecera OLE corrupta) y se uso el PDF",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="pdf",
        dato_actual="agosto 2026: 2.355.918 parados registrados; julio 2026: 2.311.499; variacion +44.419",
        dato_anterior="variaciones julio->agosto recomputadas de los niveles del PDF: 2017 +46.400 | 2018 +47.047 | 2019 +54.371 | 2020 +29.780 | 2021 -82.583 | 2022 +40.428 | 2023 +24.826 | 2024 +21.884 | 2025 +21.905",
        raw_value_span_actual=(
            "[evolparoseries.pdf, tabla 'segun sectores', bloque 2026] 'JULIO 2.311.499 ...' | 'AGOSTO 2.355.918 "
            "69.384 181.016 166.106 1.696.287 243.125' || [nota SEPE 2026-09-02] 'El paro registrado sube en agosto "
            "en 44.419 personas y se situa en 2.355.918' || [The Objective/EP 2026-09-02, el claim] 'El paro sube en "
            "44.419 personas, su mayor alza en agosto desde 2019, lastrado por los servicios'"
        ),
        raw_value_span_anterior=(
            "[evolparoseries.pdf, bloque 2019] 'JULIO 3.011.433 ...' | 'AGOSTO 3.065.804 ...' (+54.371) || [bloque "
            "2025] 'JULIO 2.404.606 ...' | 'AGOSTO 2.426.511 ...' (+21.905) || [bloque 2022] 'JULIO 2.883.812 ...' | "
            "'AGOSTO 2.924.240 ...' (+40.428)"
        ),
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (extremo), emisor SEPE, via divergencia. 'Mayor alza en agosto desde 2019': recomputado sobre "
            "los niveles mensuales del PDF, agosto 2026 (+44.419) supera a todos los agostos 2020-2025 (maximo "
            "+40.428 en 2022) y queda por debajo de 2019 (+54.371): cuadra. 'Lastrado por los servicios' (+28.563 en "
            "servicios, evolprovsectores.xls) no se evalua. Sin test aplicable -> undetermined (DEC-029). Segundo "
            "caso SEPE de la edicion (E032 A). methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE paro agosto 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="SEPE", tabla="evolparoseries.pdf / Total",
                         serie_nombre="Paro registrado, total nacional", unidad="personas",
                         referencia_principal="mensual",
                         descripcion="Paro registrado, variacion mensual julio->agosto, 2017-2026"),
            periodo_objetivo="2026-M08", valor_objetivo=44419,
            notas="Extremo: mayor variacion mensual de un agosto desde 2019. Sin test aplicable.",
        ),
    ),
    dict(
        cid="Q049",
        claim_text="Navarra, donde más aumentó la compraventa de viviendas en julio",
        claim_date="2026-09-25",
        post_url="https://www.noticiasdenavarra.com/economia/2026/09/25/navarra-aumento-compraventa-viviendas-julio-11583206.html",
        post_url_tipo="prensa", emisor="Noticias de Navarra (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Navarra compraventa viviendas julio 2026 'donde más'",
        criba_query_b="'Navarra, donde más aumentó la compraventa de viviendas en julio' OR 'Navarra' compraventa viviendas julio 2026 'donde más' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="compraventa viviendas julio 2026 'respecto a junio' OR 'en tasa mensual' OR 'frente a junio' sube OR aumenta OR crece '3,6%' OR '3,5%' INE noticia",
        collected_at="2026-09-26", case_id="E040",
        # --- trabajo 2026-09-26 (E040 t0/t1/t2 14:4xZ) ---
        fuente_primaria="INE - ETDP julio 2026: anexo ETDP0726.xlsx, tabla ETDP.11 'Fincas transmitidas por comunidades autonomas' (compraventas de viviendas registradas, % variacion anual por CCAA)",
        primaria_url="https://www.ine.es/prensa/anexo_tablas/es/ETDP0726.xlsx",
        primaria_url_tipo="anexo xlsx de la nota (HTTP 200 al agente identificado, 112.453 bytes) + nota ETDP0726",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="julio 2026, % variacion anual de compraventas de viviendas por CCAA: Navarra +26,36 (652) | Galicia +10,76 (2.409) | Castilla y Leon +9,69 (3.486) | Castilla-La Mancha +7,29 | Murcia +2,57 | Canarias +2,10 | resto negativas | TOTAL -5,11 (61.417)",
        dato_anterior="la tasa del INE lleva implicita julio 2025 (Navarra: 652/1,2636 = 516 compraventas)",
        raw_value_span_actual=(
            "[ETDP0726.xlsx, hoja Hoja9, tabla ETDP.11, fila] 'Navarra, Comunidad Foral de', 2966, 0.44023..., "
            "537.31..., 652, 26.356589147286826, 118.11... || [fila] 'Galicia', ..., 2409, 10.76 || [Noticias de "
            "Navarra/EP 2026-09-25, el claim] 'Navarra, donde mas aumento la compraventa de viviendas en julio'"
        ),
        raw_value_span_anterior="[misma tabla, ranking recomputado] 1. Navarra 26,36 | 2. Galicia 10,76 | 3. Castilla y Leon 9,69 | TOTAL -5,11",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (ranking entre CCAA, tipo 'otro'), via divergencia. Navarra es la CCAA con mayor tasa anual "
            "(+26,36%) en ETDP.11: cuadra. Ranking sin test en el prototipo -> undetermined (DEC-029). Quinto caso "
            "de la edicion ETDP0726 (E001 A, E029 A, E002 O, E038 F): D no cuenta en el tope de controles A. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETDP0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="otro",
            metrica=dict(emisor="INE", tabla="ETDP.11 (anexo ETDP0726)",
                         serie_nombre="% variacion anual de compraventas de viviendas por CCAA", unidad="%",
                         referencia_principal="interanual",
                         descripcion="ETDP, compraventas de viviendas registradas por CCAA, tasa anual, julio 2026"),
            periodo_objetivo="2026-M07", valor_objetivo=26.36,
            notas="Ranking (maximo entre CCAA): sin test aplicable en el prototipo.",
        ),
    ),
    dict(
        cid="Q050",
        claim_text="El principal incremento delictivo en la localidad se concentra en la ciberdelincuencia, un fenómeno que ya representa más del 70% del aumento de las infracciones penales",
        claim_date="2026-06-22",
        post_url="https://www.soydemadrid.com/noticia-alcorcon/david-lopez-pp-y-vox-siempre-buscan-el-alarmismo-151798.aspx",
        post_url_tipo="declaracion", emisor="David López, concejal de Seguridad de Alcorcón, vía SoyDe Madrid", emisor_tipo="institucion",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Alcorcón cibercriminalidad '70%' aumento infracciones 2026",
        criba_query_b="Alcorcón 'David López' cibercriminalidad '70%' OR 'más del 70' infracciones penales 2026 verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="[aparecio en los resultados de la criba (b) de Q043] Alcorcón criminalidad 'primer trimestre' 2026 '30,2%' OR '2.215' OR '25,1%' OR '4.367' Vox verificación OR bulo OR fact-check OR desmiente",
        collected_at="2026-09-26", case_id="E041",
        # --- trabajo 2026-09-26 (E041 t0/t1/t2 14:5xZ; misma tabla que E036) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 1T2026, tabla 09003, bloque '28007 Alcorcon' (misma descarga que E036)",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAct/l0/09003.csv_c",
        primaria_url_tipo="CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (sha256 949be9399eb00fd4); evidencia en research/evidencia/E036_portal_criminalidad_1T2026_alcorcon.txt",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Alcorcon, 1T2026 vs 1T2025: total 1.701 -> 2.215 (+514); cibercriminalidad 288 -> 504 (+216, +75,0%); estafas informaticas 215 -> 453 (+238); convencional 1.413 -> 1.711 (+298). Peso de la ciber en el aumento total: 216/514 = 42,0% (estafas: 46,3%)",
        dato_anterior="columna 'enero-marzo 2025' de la misma tabla: total 1.701, ciber 288, convencional 1.413",
        raw_value_span_actual=(
            "[09003.csv_c, bloque '28007 Alcorcón'] 'III. TOTAL INFRACCIONES PENALES,1.701,2.215,30,2,' | 'II. "
            "CIBERCRIMINALIDAD (infracciones penales cometidas en/por medio ciber),288,504,75,0,' | '12.-Estafas "
            "informáticas,215,453,110,7,' | 'I. CRIMINALIDAD CONVENCIONAL,1.413,1.711,21,1,' || [SoyDe Madrid "
            "2026-06-22, el claim] 'la ciberdelincuencia, un fenomeno que ya representa mas del 70% del aumento de "
            "las infracciones penales'"
        ),
        raw_value_span_anterior="[09003.csv_c, columna 'enero-marzo 2025'] total 1.701 | ciber 288 | convencional 1.413",
        truth="mixed", context="divergence_detected",
        clase_primaria="4_denominator", clases_secundarias="3_absolute_vs_relative", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta C (clase 4, denominador), via divergencia (declaracion municipal en respuesta al claim de Q043). "
            "'Mas del 70% del aumento' no sale de la tabla: la ciber aporta 216 de los 514 hechos de mas (42,0%); "
            "el 75% es la TASA de crecimiento de la ciber (504/288 - 1), no su peso en el aumento total. Numero "
            "rastreable (75%) con denominador equivocado: mixed + divergence_detected. Lectura alternativa (F, "
            "claim falso) anotada para la muestra a ciegas: NEEDS_REVIEW. Sin test 2a aplicable (no es un cambio "
            "entre periodos de una serie). Tercer caso de la edicion 1T2026 del Portal (E028 A, E036 A). "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="C", hermano_de="", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="otro",
            metrica=dict(emisor="Ministerio del Interior", tabla="09003 (Portal Estadistico, Balance 1T2026)",
                         serie_nombre="28007 Alcorcón · II. CIBERCRIMINALIDAD / III. TOTAL INFRACCIONES PENALES",
                         unidad="hechos conocidos", referencia_principal="interanual",
                         descripcion="Cuota de la cibercriminalidad en el aumento interanual de infracciones, Alcorcon, 1T2026"),
            periodo_objetivo="2026-T1", valor_objetivo=70,
            notas="Cuota del aumento recomputada: (504-288)/(2215-1701) = 42,0%. El 70% no corresponde a ningun cociente de la tabla salvo la tasa de crecimiento de la ciber (75%).",
        ),
    ),
    dict(
        cid="Q051",
        claim_text="Las pernoctaciones hoteleras en Madrid caen un 1,43% en julio con 2,29 millones de noches",
        claim_date="2026-08-21",
        post_url="https://www.eldiariodemadrid.es/articulo/turismo/pernoctaciones-hoteleras-madrid-julio-caida-turismo-extranjero/20260821170152139820.html",
        post_url_tipo="prensa", emisor="El Diario de Madrid (Diego Domingo Rodríguez)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras Madrid julio 2026 1,43% 2,29 millones",
        criba_query_b="pernoctaciones hoteleras Madrid julio 2026 '1,43%' OR '2.297.978' OR '2,29 millones' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' 'Comunidad de Madrid' julio 2026 caen OR bajan OR descienden '1,4%' OR '1,41%' OR '1,05%' OR '1,1%' Europa Press agosto 2026",
        collected_at="2026-09-26", case_id="E042",
        # --- trabajo 2026-09-26 (E042 t0/t1/t2 15:0xZ; anexos y API ya en mano por E031/E035) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): anexo CTH0726.xlsx (EOH_Hoja3, fila 'Madrid, Comunidad de') + API Tempus tabla 2074 (EOT1763-EOT1768); edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (julio 2025 provisional)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/CTH0726.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Comunidad de Madrid, julio 2026 (provisional): pernoctaciones 2.297.978 (residentes 860.750; extranjeros 1.437.228); viajeros 1.139.288 (504.321 / 634.966)",
        dato_anterior="Comunidad de Madrid, julio 2025. Edicion vigente (API): pernoctaciones 2.322.289 (895.696 / 1.426.593); viajeros 1.165.046 (517.619 / 647.427). Edicion provisional (anexo CTH0725): pernoctaciones 2.330.843 (903.133 / 1.427.710); viajeros 1.179.239 (527.894 / 651.345)",
        raw_value_span_actual=(
            "[CTH0726.xlsx, hoja EOH_Hoja3, fila 61] 'Madrid, Comunidad de', 1139288, 504321, 634966, 2297978, "
            "860750, 1437228, 2.02 || [INE API tabla 2074] EOT1766 2026-M07: 2297978 | EOT1763 2026-M07: 1139288 || "
            "[El Diario de Madrid 2026-08-21, el claim] 'La Comunidad de Madrid registro 2.297.978 pernoctaciones "
            "hoteleras durante el mes de julio ... un descenso del 1,43% respecto al mismo periodo del ano "
            "anterior'; '1.139.288 viajeros ... un descenso del 3,38%'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1766 2025-M07: 2322289 | EOT1763 2025-M07: 1165046 || [CTH0725.xlsx, hoja "
            "EOH_Hoja3, fila 61, datos provisionales julio 2025] 'Madrid, Comunidad de', 1179239, 527894, 651345, "
            "2330843, 903133, 1427710, 1.98"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta C (2b, base revisada), via divergencia. Contra la edicion vigente: pernoctaciones -1,05%, "
            "viajeros -2,21%. Contra la provisional de julio 2025: -1,41% y -3,39%, que reproducen (a 0,01-0,02 pp) "
            "el -1,43% y el -3,38% del articulo; la base exacta no es reproducible al centesimo (NEEDS_REVIEW), pero "
            "solo la provisional se acerca. La nota de coyuntura de la Comunidad de Madrid (julio 2026) da -1% "
            "(vigente), lo que confirma el mecanismo. Mismo mecanismo que E031 (agosto, Ultima Hora/EP) en otra "
            "edicion y otro medio: no es hermano. Mismo signo: el test 2a no disparia. Segundo caso de CTH0726 "
            "(E035 A). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",  # C -> B por DEC-034
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Madrid (Comunidad de). Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Comunidad de Madrid, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=2297978, cambio_afirmado=-1.43, unidad_cambio="pct", direccion_afirmada="baja",
            # DEC-034: las dos evidencias del veredicto 2b, cada una con su fecha.
            evidencia_al_publicar=dict(
                valor=2330843, edicion="INE CTH0725 (julio 2025, datos provisionales)", fecha="2025-08-22",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx",
                raw_value_span="[CTH0725.xlsx, hoja EOH_Hoja3, fila 61] 'Madrid, Comunidad de', 1179239, 527894, 651345, 2330843, 903133, 1427710, 1.98",
                verificacion="research/evidencia/D2B_CTH0725.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=2322289, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] EOT1766 2025-M07: 2322289",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (2.330.843) y no de la vigente (2.322.289): 2b. Sin cambio de signo.",
        ),
    ),
    dict(
        cid="Q052",
        claim_text="Las pernoctaciones de residentes nacionales subieron alrededor de un 3,8%, de 740.149 a 768.195, mientras que las de extranjeros cayeron un 2,2%, hasta 10.015.343",
        claim_date="2026-08-21",
        post_url="https://www.economiademallorca.com/articulo/turismo-y-hosteleria/hoteles-islas-reciben-mas-dos-millones-viajeros-julio/20260821103628122733.html",
        post_url_tipo="prensa", emisor="Economía de Mallorca (Redacción)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Baleares hoteles julio 2026 pernoctaciones 1,7% viajeros 2.050.150",
        criba_query_b="Baleares pernoctaciones hoteleras julio 2026 '10.783.538' OR '1,7%' OR '2.050.150' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="pernoctaciones hoteleras Baleares julio 2026 caen OR bajan '1,9%' OR '1,86%' OR '1,8%' OR '2%' Europa Press agosto 2026 '10,78 millones' OR '10,8 millones'",
        collected_at="2026-09-26", case_id="E043",
        # --- trabajo 2026-09-26 (E043 t0 15:0xZ, t1/t2 15:0xZ; t2 corregido tras leer el articulo: 2b, no A) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): anexo CTH0726.xlsx (EOH_Hoja3, fila 'Balears, Illes') + API Tempus tabla 2074 (EOT22192-EOT22197); edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (julio 2025 provisional)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/CTH0726.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Balears, julio 2026 (provisional): pernoctaciones 10.783.538 (residentes 768.195; extranjeros 10.015.343); viajeros 2.050.150",
        dato_anterior="Balears, julio 2025. Edicion vigente (API): pernoctaciones 10.974.122 (residentes 786.273; extranjeros 10.187.848); viajeros 2.038.016. Edicion provisional (anexo CTH0725): 10.987.630 (residentes 740.149; extranjeros 10.247.481); viajeros 2.036.446",
        raw_value_span_actual=(
            "[CTH0726.xlsx, hoja EOH_Hoja3, fila 23] 'Balears, Illes', 2050150, 204284, 1845866, 10783538, 768195, "
            "10015343, 5.26 || [INE API tabla 2074] EOT22193 2026-M07: 768195 | EOT22192 2026-M07: 10015343 | "
            "EOT22194 2026-M07: 10783538 || [Economia de Mallorca 2026-08-21, el claim] 'Las pernoctaciones de "
            "residentes nacionales subieron alrededor de un 3,8%, de 740.149 a 768.195'; 'mientras que las de "
            "extranjeros cayeron un 2,2%, hasta 10.015.343'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT22193 2025-M07: 786273 | EOT22192 2025-M07: 10187848 | EOT22194 2025-M07: "
            "10974122 || [CTH0725.xlsx, hoja EOH_Hoja3, fila 23, datos provisionales julio 2025] 'Balears, Illes', "
            "2036446, 193208, 1843238, 10987630, 740149, 10247481, 5.4"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta C (2b, base revisada) CON CAMBIO DE SIGNO, via divergencia. El articulo escribe la base "
            "(740.149), que es la cifra provisional de julio 2025 (anexo CTH0725), no la vigente (786.273): con la "
            "vigente las pernoctaciones de residentes CAEN un 2,3%, no suben un 3,8%. Extranjeros: -2,27% "
            "(provisional) frente a -1,69% (vigente). Total: -1,74% vigente / -1,86% provisional (el articulo no "
            "da la tasa total). Es el 2b mas fuerte del conjunto: la revision de la edicion cambia el signo; el "
            "prototipo, que solo ve la edicion vigente, lo veria como contradicted sin test aplicable (2b fuera "
            "del prototipo, DEC-029). Tercer caso de CTH0726 (E035 A, E042 C); tercer 2b del conjunto (E031, "
            "E042). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",  # C -> B por DEC-034
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Balears, Illes. Pernoctaciones. Total categorías. Residentes en España. Dato. ",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones de residentes en Espana, Illes Balears, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=768195, cambio_afirmado=3.8, unidad_cambio="pct", direccion_afirmada="sube",
            # DEC-034: las dos evidencias del veredicto 2b, cada una con su fecha.
            evidencia_al_publicar=dict(
                valor=740149, edicion="INE CTH0725 (julio 2025, datos provisionales)", fecha="2025-08-22",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx",
                raw_value_span="[CTH0725.xlsx, hoja EOH_Hoja3, fila 23] 'Balears, Illes', 2036446, 193208, 1843238, 10987630, 740149, 10247481, 5.4",
                verificacion="research/evidencia/D2B_CTH0725.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=786273, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] EOT22193 2025-M07: 786273",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (740.149) y no de la vigente (786.273): 2b con cambio de signo (+3,8% frente a -2,3%).",
        ),
    ),
    # ------------------------------------------------------------------ jornada 3 (via divergencia, B = 2b)
    dict(
        cid="Q053",
        claim_text="El turismo hotelero en Madrid crece un 1,2% en junio",
        claim_date="2026-07-24",
        post_url="https://www.madridactual.es/noticias-regionales/turismo-madrid/pernoctaciones-hoteleras-region-crecen-1-2-junio-2-4-millones-20260724-8112720.html",
        post_url_tipo="prensa", emisor="Madrid Actual (teletipo de EFE)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones hoteleras Madrid junio 2026 1,2% 2.421.276",
        criba_query_b="pernoctaciones hoteleras Madrid junio 2026 '1,2%' OR '2.421.276' OR '2,4 millones' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' junio 2026 'Comunidad de Madrid' OR Andalucía OR Cataluña OR 'Comunitat Valenciana' OR Canarias OR Baleares OR Galicia aumentan OR caen OR suben OR bajan '%' julio 2026 Europa Press -agosto",
        collected_at="2026-09-26", case_id="E044",
        # --- trabajo 2026-09-26 (E044 t0/t1/t2 15:1xZ) ---
        fuente_primaria="INE - CTH junio 2026 (CTH0626): API Tempus tabla 2074 (EOT1763-EOT1768, nult=16); edicion anterior: API (junio 2025 vigente) y anexo CTH0625.xlsx (provisional, publicado 23/07/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0626.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/2074 + anexo xlsx de la edicion anterior (CTH0625, HTTP 200 al agente)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Comunidad de Madrid, junio 2026: pernoctaciones 2.421.276 (residentes 988.985; extranjeros 1.432.291); viajeros 1.199.893 (578.040 / 621.852)",
        dato_anterior="junio 2025. Vigente (API): pernoctaciones 2.393.431; viajeros 1.183.266 (554.663 / 628.602). Provisional (anexo CTH0625): pernoctaciones 2.412.755; viajeros 1.202.428 (565.728 / 636.700)",
        raw_value_span_actual=(
            "[INE API tabla 2074] EOT1766 2026-M06: 2421276 | EOT1763 2026-M06: 1199893 | EOT1764 2026-M06: 578040 "
            "| EOT1765 2026-M06: 621852 || [Madrid Actual/EFE 2026-07-24, el claim] 'Las pernoctaciones registradas "
            "en la region sumaron 2.421.276 en junio'; 'aumentaron un 1,2% en junio'; 'se alojaron un 1,41% mas de "
            "turistas'; 'totalizando 1.199.893 viajeros'; 'Los viajeros residentes en Espana crecieron un 4,2% "
            "interanual, mientras que los extranjeros se redujeron un 1,1%'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1766 2025-M06: 2393431 | EOT1763 2025-M06: 1183266 | EOT1764 2025-M06: 554663 "
            "| EOT1765 2025-M06: 628602 || [CTH0625.xlsx, hoja EOH_Hoja3, fila 61, datos provisionales junio 2025] "
            "'Madrid, Comunidad de', 1202428, 565728, 636700, 2412755, 976673, 1436083, 2.01"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia (jornada 3, veta 2b). Las cuatro tasas del teletipo (+1,16, +1,41, "
            "+4,21, -1,07) se reproducen con la edicion VIGENTE de junio 2025; contra la provisional habrian sido "
            "+0,35, -0,21, +2,18 y -2,33. EFE uso la base revisada: no es 2b. Primer caso de CTH0626. "
            "methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0626",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Madrid (Comunidad de). Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Comunidad de Madrid, mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=2421276, cambio_afirmado=1.2, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q054",
        claim_text="Catalunya registra 6,73 millones de pernoctaciones hoteleras en junio, un 2,1% menos",
        claim_date="2026-07-24",
        post_url="https://www.catalunyapress.es/articulo/economia/2026-07-24/5964000-catalunya-registra-673-millones-pernoctaciones-hoteleras-junio-21-menos",
        post_url_tipo="prensa", emisor="CatalunyaPress (Felipe Martínez)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Catalunya pernoctaciones hoteleras junio 2026 6,73 millones 2,1%",
        criba_query_b="Catalunya pernoctaciones hoteleras junio 2026 '6,73 millones' OR '2,1% menos' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' junio 2026 'Comunidad de Madrid' OR Andalucía OR Cataluña OR 'Comunitat Valenciana' OR Canarias OR Baleares OR Galicia aumentan OR caen OR suben OR bajan '%' julio 2026 Europa Press -agosto",
        collected_at="2026-09-26", case_id="E045",
        # --- trabajo 2026-09-26 (E045 t0/t1/t2 15:1xZ) ---
        fuente_primaria="INE - CTH junio 2026 (CTH0626): API Tempus tabla 2074 (EOT1661-EOT1666, nult=16); edicion anterior: API (junio 2025 vigente) y anexo CTH0625.xlsx (provisional, publicado 23/07/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0626.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/2074 + anexo xlsx de la edicion anterior (CTH0625, HTTP 200 al agente)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Cataluna, junio 2026: pernoctaciones 6.729.507 (residentes 1.903.239; extranjeros 4.826.268); viajeros 2.454.534 (908.260 / 1.546.274)",
        dato_anterior="junio 2025. Vigente (API): pernoctaciones 6.873.856; viajeros 2.461.312 (903.687 / 1.557.625). Provisional (anexo CTH0625): pernoctaciones 6.890.423 (1.869.312 / 5.021.111); viajeros 2.455.692 (894.453 / 1.561.240)",
        raw_value_span_actual=(
            "[INE API tabla 2074] EOT1664 2026-M06: 6729507 | EOT1661 2026-M06: 2454534 | EOT1662 2026-M06: 908260 "
            "| EOT1663 2026-M06: 1546274 || [CatalunyaPress 2026-07-24, el claim] 'Los establecimientos hoteleros "
            "de Catalunya contabilizan durante junio un total de 6.729.507 pernoctaciones ... un descenso del 2,1% "
            "respecto al mismo mes del ano anterior'; 'Durante junio se alojan en los hoteles catalanes 2.454.534 "
            "viajeros, un 0,28% menos que en el mismo periodo de 2025'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1664 2025-M06: 6873856 | EOT1661 2025-M06: 2461312 || [CTH0625.xlsx, hoja "
            "EOH_Hoja3, fila Cataluna, datos provisionales junio 2025] 'Cataluña', 2455692, 894453, 1561240, 6890423, "
            "1869312, 5021111, 2.81"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia (jornada 3, veta 2b). -2,10% y -0,28% se reproducen con la base "
            "VIGENTE de junio 2025; contra la provisional habrian sido -2,34% y -0,05%. Idescat publica la misma "
            "tasa. Segundo caso de CTH0626 (E044). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0626",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Cataluña. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Cataluna, mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=6729507, cambio_afirmado=-2.1, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q055",
        claim_text="Los hoteles de la Comunidad de Madrid registraron casi 2,6 millones de pernoctaciones en mayo, un 0,7% más que el año anterior",
        claim_date="2026-06-23",
        post_url="https://lavozmadrid.es/madrid-capital/general/hoteles-de-madrid-rozan-26-millones-de-pernoctaciones-en-mayo",
        post_url_tipo="prensa", emisor="La Voz de Madrid (Alberto Delgado Sanz)", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com hoteles Madrid mayo 2026 pernoctaciones 2.560.746 0,7%",
        criba_query_b="hoteles Madrid mayo 2026 '2.560.746' OR '696.113' OR '0,7% más' pernoctaciones verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' mayo 2026 'Comunidad de Madrid' OR Baleares OR Canarias OR Andalucía OR Cataluña OR Galicia OR Asturias aumentan OR caen OR suben OR bajan '%' junio 2026 Europa Press -junio -julio",
        collected_at="2026-09-26", case_id="E046",
        # --- trabajo 2026-09-26 (E046 t0/t1/t2 15:2xZ) ---
        fuente_primaria="INE - CTH mayo 2026 (CTH0526): API Tempus tabla 2074 (nult=16); edicion anterior: API (mayo 2025 vigente) y anexo CTH0525.xlsx (provisional, publicado 23/06/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0526.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/2074 + anexo xlsx de la edicion anterior (CTH0525, HTTP 200 al agente)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Comunidad de Madrid, mayo 2026: pernoctaciones 2.560.746; viajeros 1.232.338 (residentes 536.225; extranjeros 696.113)",
        dato_anterior="mayo 2025. Vigente (API): pernoctaciones 2.543.911; viajeros 1.199.658 (535.558 / 664.100). Provisional (anexo CTH0525): pernoctaciones 2.560.824; viajeros 1.213.258 (545.311 / 667.947)",
        raw_value_span_actual=(
            "[INE API tabla 2074] EOT1766 2026-M05: 2560746 | EOT1763 2026-M05: 1232338 | EOT1765 2026-M05: 696113 "
            "|| [La Voz de Madrid 2026-06-23, el claim] 'Los hoteles de la Comunidad de Madrid registraron casi 2,6 "
            "millones de pernoctaciones en mayo, un 0,7% mas que el ano anterior'; 'un total de 2.560.746 "
            "estancias'; 'La entrada de huespedes extranjeros crecio un 4,8%, sumando 696.113 visitas'; 'el mercado "
            "domestico mostro una ligera subida del 0,1%, con 536.225 residentes espanoles alojados'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1766 2025-M05: 2543911 | EOT1763 2025-M05: 1199658 | EOT1765 2025-M05: 664100 "
            "(residentes = 1199658 - 664100 = 535558) || [CTH0525.xlsx, hoja EOH_Hoja3, fila 61, datos provisionales "
            "mayo 2025] 'Madrid, Comunidad de', 1213258, 545311, 667947, 2560824, 976824, 1584001, 2.11"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia (jornada 3, veta 2b). +0,66%, +4,82% y +0,12% se reproducen con la "
            "base VIGENTE de mayo 2025; contra la provisional habrian sido 0,00%, +4,22% y -1,67%. Primer caso de "
            "CTH0526. La provisional de mayo 2025 (2.560.824) se reviso a 2.543.911 (-16.913). "
            "methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0526",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Madrid (Comunidad de). Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Comunidad de Madrid, mensual"),
            periodo_objetivo="2026-M05", periodo_base="2025-M05",
            valor_objetivo=2560746, cambio_afirmado=0.7, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q056",
        claim_text="Los hoteles de Baleares atendieron en agosto a 2,1 millones de huéspedes que realizaron 11,3 millones de pernoctaciones, cifras que representaron un incremento interanual de los clientes del 3,8%, pero una caída de las noches contratadas de casi el 0,2%",
        claim_date="2026-09-22",
        post_url="https://www.ultimahora.es/noticias/local/2026/09/22/2713709/clientes-hoteles-aumentan-agosto-pernoctaciones-caen.html",
        post_url_tipo="prensa", emisor="Última Hora (teletipo de EFE, Palma)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Baleares hoteles agosto 2026 clientes 3,8% pernoctaciones 0,2%",
        criba_query_b="Baleares hoteles agosto 2026 '3,8 %' OR '3,8%' clientes pernoctaciones '0,2' caen verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="economiademallorca.com hoteles Baleares pernoctaciones agosto 2026 OR junio 2026 '%' viajeros INE islas",
        collected_at="2026-09-26", case_id="E047",
        # --- trabajo 2026-09-26 (E047 t0 15:2xZ, t1/t2 15:3xZ) ---
        fuente_primaria="INE - CTH agosto 2026 (CTH0826): anexo CTH0826.xlsx (EOH_Hoja3, fila 'Balears, Illes') + API Tempus tabla 2074 (EOT22194, EOT22197); edicion anterior: API (agosto 2025 vigente) y anexo CTH0825.xlsx (provisional, publicado 23/09/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/CTH0826.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Balears, agosto 2026 (provisional): viajeros 2.137.472; pernoctaciones 11.367.443 (residentes 895.649; extranjeros 10.471.794)",
        dato_anterior="agosto 2025. Vigente (API): viajeros 2.064.436; pernoctaciones 11.418.035. Provisional (anexo CTH0825): viajeros 2.058.841; pernoctaciones 11.388.816 (856.252 / 10.532.565)",
        raw_value_span_actual=(
            "[CTH0826.xlsx, hoja EOH_Hoja3, fila 23] 'Balears, Illes', 2137472, 223438, 1914034, 11367443, 895649, "
            "10471794, 5.32 || [INE API tabla 2074] EOT22197 2026-M08: 2137472 | EOT22194 2026-M08: 11367443 || "
            "[Ultima Hora/EFE 2026-09-22, el claim] 'Los hoteles de Baleares atendieron en agosto a 2,1 millones de "
            "huespedes que realizaron 11,3 millones de pernoctaciones, cifras que representaron un incremento "
            "interanual de los clientes del 3,8%, pero una caida de las noches contratadas de casi el 0,2%'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT22197 2025-M08: 2064436 | EOT22194 2025-M08: 11418035 || [CTH0825.xlsx, hoja "
            "EOH_Hoja3, fila 23, datos provisionales agosto 2025] 'Balears, Illes', 2058841, 203250, 1855591, "
            "11388816, 856252, 10532565, 5.53"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta B (2b), via divergencia (jornada 3). Contra la edicion vigente: clientes +3,54%, pernoctaciones "
            "-0,44%. Contra la provisional de agosto 2025: +3,82% y -0,19%, que son el 3,8% y el 'casi 0,2%' del "
            "teletipo: EFE calculo con la base provisional. Mismo signo en ambas bases: subtipo magnitud. Misma "
            "edicion (CTH0826) y mecanismo que E031 (EP, Madrid): claim, agencia y region distintos, no es hermano "
            "por criba; se declara la concentracion por edicion. Cuarto 2b del conjunto. methodology_found=si: IME "
            "del INE, seccion 17 (pasada 2026-09-27, METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Balears, Illes. Pernoctaciones. Total categorías. Total. Dato. ",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Illes Balears, mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            valor_objetivo=11367443, cambio_afirmado=-0.2, unidad_cambio="pct", direccion_afirmada="baja",
            evidencia_al_publicar=dict(
                valor=11388816, edicion="INE CTH0825 (agosto 2025, datos provisionales)", fecha="2025-09-23",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0825.xlsx",
                raw_value_span="[CTH0825.xlsx, hoja EOH_Hoja3, fila 23] 'Balears, Illes', 2058841, 203250, 1855591, 11388816, 856252, 10532565, 5.53",
                verificacion="research/evidencia/D2B_CTH0825.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=11418035, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] EOT22194 2025-M08: 11418035",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (11.388.816) y no de la vigente (11.418.035): 2b sin cambio de signo (-0,19% frente a -0,44%). Los clientes: +3,82% frente a +3,54%.",
        ),
    ),
    dict(
        cid="Q057",
        claim_text="Las pernoctaciones internacionales en hoteles de Málaga suben un 15,57% en julio",
        claim_date="2026-08-28",
        post_url="https://www.andaluciainformacion.es/articulo/malaga/andalucia-malaga-turismo-pernoctaciones-hoteleras-internacionales-crecen-1557-malaga-mes-julio/202608281353043463067.html",
        post_url_tipo="prensa", emisor="Andalucía Información (Redacción)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Málaga pernoctaciones hoteleras julio 2026 15,57% internacionales",
        criba_query_b="Málaga pernoctaciones hoteleras julio 2026 '15,57%' OR '374.405' OR '283.634' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="pernoctaciones hoteleras agosto 2026 'ciudad de Madrid' OR Barcelona OR Sevilla OR Málaga OR Valencia OR 'Palma' '%' hoteles septiembre 2026 INE noticia -'Comunidad de Madrid'",
        collected_at="2026-09-26", case_id="E048",
        # --- trabajo 2026-09-26 (E048 t0/t1/t2 15:3xZ) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): API Tempus tabla 2078 (puntos turisticos; EOT2755-EOT2758, Malaga); edicion anterior: API (julio 2025 vigente). El anexo CTH0725 no lista Malaga ciudad entre los puntos con mas pernoctaciones: la edicion al publicar de esta serie no es recuperable del anexo",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/2078",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Malaga (punto turistico), julio 2026: pernoctaciones 374.405 (residentes 90.771; extranjeros 283.634); viajeros extranjeros 119.163, residentes 47.092",
        dato_anterior="julio 2025 vigente (API): pernoctaciones 359.309 (113.897 / 245.412); viajeros 60.646 / 110.208",
        raw_value_span_actual=(
            "[INE API tabla 2078] EOT2758 'Nacional. Pernoctaciones. Málaga. Residentes en el extranjero.' 2026-M07: "
            "283634 | EOT2757 2026-M07: 90771 | EOT2756 2026-M07: 119163 || [Andalucia Informacion 2026-08-28, el "
            "claim] 'Malaga recibio en julio a 166.255 viajeros hoteleros, con un total de 374.405 pernoctaciones'; "
            "'un aumento del 4,20% en las noches de hotel respecto a julio de 2025'; 'las pernoctaciones "
            "internacionales, que subieron un 15,57%'; 'Los hoteles recibieron 119.163 viajeros extranjeros, un "
            "8,13% mas que el ano anterior'"
        ),
        raw_value_span_anterior="[INE API tabla 2078] EOT2758 2025-M07: 245412 | EOT2757 2025-M07: 113897 | EOT2756 2025-M07: 110208 | EOT2755 2025-M07: 60646",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A (punto turistico), via divergencia (jornada 3). 283634/245412 - 1 = +15,57%; 374405/359309 - 1 "
            "= +4,20%; 119163/110208 - 1 = +8,13%: todas con la base vigente. Serie de punto turistico: fuera del "
            "mapa de 2b (el anexo solo lista los puntos con mas pernoctaciones y Malaga ciudad no aparece en "
            "CTH0725). Segundo A de CTH0726 (E035). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2078",
                         serie_nombre="Nacional. Pernoctaciones. Málaga. Residentes en el extranjero.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones de residentes en el extranjero, punto turistico Malaga, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=283634, cambio_afirmado=15.57, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control de punto turistico: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q058",
        claim_text="Las pernoctaciones extrahoteleras crecen en Andalucía un 11,6% en julio y superan los tres millones",
        claim_date="2026-08-31",
        post_url="https://www.teleprensa.com/articulo/sevilla/pernoctaciones-extrahoteleras-crecen-andalucia-116-julio-superan-tres-millones/202608310832252496769.html",
        post_url_tipo="prensa", emisor="Teleprensa (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Andalucía pernoctaciones extrahoteleras julio 2026 11,6% tres millones",
        criba_query_b="Andalucía pernoctaciones extrahoteleras julio 2026 '3.034.656' OR '11,6%' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'extrahoteleras' OR 'apartamentos turísticos' 'Comunidad de Madrid' OR Baleares OR Canarias OR Andalucía julio 2026 pernoctaciones '%' 'respecto al mismo mes' Europa Press agosto 2026 -junio",
        collected_at="2026-09-26", case_id="E049",
        # --- trabajo 2026-09-26 (E049 t0/t1/t2 15:3xZ) ---
        fuente_primaria="INE - EOAT julio 2026 (EOAT0726): anexo EOAT0726.xlsx (filas Andalucia en EOAP_Hoja1, EOAC_Hoja1, EOTR_Hoja1, EOAL_Hoja2) + API Tempus tablas 1993 (EOAP), 2016 (EOAC) y 61766 (EOTR, EOAL) por CCAA; edicion anterior: API (julio 2025 vigente) y anexo EOAT0725.xlsx (provisional, publicado 29/08/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/EOAT0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/EOAT0726.xlsx + API JSON (tres tablas)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Andalucia, julio 2026, pernoctaciones extrahoteleras: apartamentos 1.686.628 + campings 1.002.789 + turismo rural 223.947 + albergues 121.292 = 3.034.656",
        dato_anterior="julio 2025. Vigente (API): 1.399.886 + 985.631 + 227.550 + 105.137 = 2.718.204. Provisional (anexo EOAT0725): 1.382.026 + 915.262 + 228.564 + 105.573 = 2.631.425",
        raw_value_span_actual=(
            "[EOAT0726.xlsx] EOAP_Hoja1 fila 12 'Andalucía', 420095, 216472, 203623, 1686628, 806098, 880530, 4.01 | "
            "EOAC_Hoja1 fila 36 'Andalucía', 254454, 224465, 29989, 1002789, 888690, 114100, 3.94 | EOTR_Hoja1 fila "
            "13 'Andalucía', 48036, 30069, 17968, 223947, 108702, 115245, 4.66 | EOAL_Hoja2 fila 8 'Andalucía', "
            "36784, 19976, 16808, 121292, 79709, 41583, 3.3 || [INE API] EOT1042 2026-M07: 1686628 | EOT738 "
            "2026-M07: 1002789 | EOT1151 2026-M07: 223947 | EOT44317 2026-M07: 121292 || [Teleprensa/EP "
            "2026-08-31, el claim] titular; el cuerpo no lo sirvio la herramienta de lectura (403); la cifra "
            "3.034.656 aparece en la cobertura (HORECA Cadiz, El Conciso) y coincide con la suma"
        ),
        raw_value_span_anterior=(
            "[INE API] EOT1042 2025-M07: 1399886 | EOT738 2025-M07: 985631 | EOT1151 2025-M07: 227550 | EOT44317 "
            "2025-M07: 105137 || [EOAT0725.xlsx, provisional julio 2025] EOAP_Hoja1 'Andalucía' ... 1382026 | "
            "EOAC_Hoja1 ... 915262 | EOTR_Hoja1 ... 228564 | EOAL_Hoja2 ... 105573"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional (EOAT, primera operacion extrahotelera del conjunto), via divergencia (jornada 3). "
            "La suma de las cuatro encuestas cuadra (3.034.656) y +11,64% sale con la base VIGENTE (2.718.204); "
            "con la provisional habria sido +15,32%: EP uso la revisada. El emisor no publica el agregado por CCAA, "
            "lo calcula la agencia sumando cuatro tablas: metrica compuesta, fuera de lo que el prototipo evalua "
            "hoy (contaria como abstencion UNSUPPORTED_CLAIM_TYPE, no como falso positivo; se declara). Revision "
            "de julio 2025: +86.779 (+3,3%). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EOAT0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="1993 + 2016 + 61766 (suma de cuatro series)",
                         serie_nombre="Andalucía. Pernoctaciones extrahoteleras (EOAP + EOAC + EOTR + EOAL)",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="Suma de pernoctaciones en apartamentos, campings, turismo rural y albergues, Andalucia, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=3034656, cambio_afirmado=11.6, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control con metrica compuesta (suma de cuatro series): base interanual vigente.",
        ),
    ),
    dict(
        cid="Q059",
        claim_text="Las pernoctaciones en alojamientos extrahoteleros en la Comunidad de Madrid (apartamentos, campings, alojamientos de turismo rural y albergues) han sumado las 533.954 de estancias en junio, un 15,9% más respecto al mismo mes de 2025, cuando se registraron 460.550 pernoctas",
        claim_date="2026-07-31",
        post_url="https://www.ultimahora.es/noticias/comunidades/2026/07/31/2680839/pernoctaciones-extrahoteleras-region-disparan-junio-impulsadas-por-bad-bunny-leon-xiv.html",
        post_url_tipo="prensa", emisor="Última Hora (teletipo de Europa Press, Madrid)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com pernoctaciones extrahoteleras junio 2026 15,9% Bad Bunny León XIV",
        criba_query_b="pernoctaciones extrahoteleras junio 2026 '15,9%' Madrid apartamentos 'Bad Bunny' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' junio 2026 'Comunidad de Madrid' OR Andalucía OR Cataluña OR 'Comunitat Valenciana' OR Canarias OR Baleares OR Galicia aumentan OR caen OR suben OR bajan '%' julio 2026 Europa Press -agosto",
        collected_at="2026-09-26", case_id="E050",
        # --- trabajo 2026-09-26 (E050 t0/t1/t2 15:4xZ) ---
        fuente_primaria="INE - EOAT junio 2026 (EOAT0626): anexo EOAT0626.xlsx (filas Madrid en EOAP_Hoja1, EOAC_Hoja1, EOTR_Hoja1, EOAL_Hoja2) + API Tempus tablas 1993, 2016 y 61766; edicion anterior: API (junio 2025 vigente), anexo EOAT0625.xlsx (provisional, 31/07/2025) y mayo 2025 vigente, para descartar un valor de otro periodo",
        primaria_url="https://www.ine.es/dyngs/Prensa/EOAT0626.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON (tres tablas)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Madrid, junio 2026: apartamentos 265.965 + campings 140.905 + turismo rural 26.202 + albergues 100.882 = 533.954 (cuadra con el claim); apartamentos: 107.779 viajeros, 265.965 pernoctaciones (100.025 / 165.940)",
        dato_anterior="junio 2025 vigente (API): 279.166 + 131.422 + 28.440 + 97.891 = 536.919 (-0,55%). Provisional (EOAT0625): 280.516 + 132.622 + 26.972 + 97.891 = 538.001 (-0,75%). Mayo 2025 vigente: 254.374 + 95.015 + 26.251 + 100.404 = 476.044. Ninguna edicion ni periodo da 460.550. Apartamentos junio 2025: 279.166 vigente / 280.516 provisional (-4,7% / -5,2%, no +4,2%)",
        raw_value_span_actual=(
            "[EOAT0626.xlsx] EOAP_Hoja1 fila 24 'Madrid, Comunidad de', 107779, 44550, 63229, 265965, 100025, 165940, "
            "2.47 | EOAC_Hoja1 fila 48 'Madrid, Comunidad de', 43716, 37341, 6374, 140905, 125213, 15692, 3.22 | "
            "EOTR_Hoja1 fila 25 'Madrid, Comunidad de', 15013, 13510, 1503, 26202, 23188, 3014, 1.75 | EOAL_Hoja2 "
            "fila 20 'Madrid, Comunidad de', 56230, 18361, 37869, 100882, 31301, 69582, 1.79 || [Ultima Hora/EP "
            "2026-07-31, el claim] 'han sumado las 533.954 de estancias en junio, un 15,9% mas respecto al mismo mes "
            "de 2025, cuando se registraron 460.550 pernoctas'; 'Las pernoctaciones en apartamentos turisticos ... "
            "han sumado 265.965, un 4,2% mas que el mismo mes de 2025'"
        ),
        raw_value_span_anterior=(
            "[INE API] EOT1114 2025-M06: 279166 | EOT810 2025-M06: 131422 | EOT1223 2025-M06: 28440 | EOT44281 "
            "2025-M06: 97891 | (mayo 2025) EOT1114 254374, EOT810 95015, EOT1223 26251, EOT44281 100404 || "
            "[EOAT0625.xlsx, provisional junio 2025] EOAP_Hoja1 fila 24 'Madrid, Comunidad de', 81994, 32643, 49351, "
            "280516, 104080, 176435, 3.42 | EOAC_Hoja1 ... 132622 | EOTR_Hoja1 ... 26972 | EOAL_Hoja2 ... 97891"
        ),
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="claim_falso", excedente="no",
        notas=(
            "Cubeta F (claim falso), via divergencia (jornada 3). Los niveles de junio 2026 cuadran (533.954; "
            "apartamentos 265.965 = 100.025 + 165.940), pero la base '460.550 en junio 2025' no existe en ninguna "
            "edicion recuperable (vigente 536.919; provisional 538.001; mayo 2025 476.044): la variacion real es "
            "-0,55% con la vigente, no +15,9%, con cambio de signo. Tampoco cuadran el +4,2% de apartamentos "
            "(-4,7% / -5,2%) ni el +54,76% de viajeros (+28% vigente). Se busco 2b y 'valor de otro periodo' y no se "
            "reproducen: contradicted. NEEDS_REVIEW para la muestra a ciegas: si Mateo localiza la base, pasa a 2a "
            "o 2b. Tercer F del conjunto. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="F", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EOAT0626",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="1993 + 2016 + 61766 (suma de cuatro series)",
                         serie_nombre="Madrid (Comunidad de). Pernoctaciones extrahoteleras (EOAP + EOAC + EOTR + EOAL)",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="Suma de pernoctaciones en apartamentos, campings, turismo rural y albergues, Comunidad de Madrid, mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=533954, cambio_afirmado=15.9, unidad_cambio="pct", direccion_afirmada="sube",
            notas="La base afirmada (460.550) no se reproduce con ninguna edicion; con la vigente la variacion es -0,55%.",
        ),
    ),
    dict(
        cid="Q060",
        claim_text="Crecen un 2,5% las pernoctaciones hoteleras este agosto en Canarias",
        claim_date="2026-09-22",
        post_url="https://www.libertaddigital.com/canarias/2026-09-22/crecen-un-2-5-por-ciento-las-pernoctaciones-hoteleras-este-agosto-en-canarias-7463875/",
        post_url_tipo="prensa", emisor="Libertad Digital Canarias (Redacción)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Canarias pernoctaciones hoteleras agosto 2026 2,5% 7.216.680",
        criba_query_b="Canarias pernoctaciones hoteleras agosto 2026 '7.216.680' OR '2,5%' OR '1.112.371' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' agosto 2026 Canarias OR Andalucía OR Cataluña OR 'Comunitat Valenciana' OR Galicia OR 'Castilla y León' OR Asturias aumentan OR caen OR suben OR bajan '%' 'mismo mes' septiembre 2026 EFE OR 'Europa Press' -Madrid -Baleares",
        collected_at="2026-09-26", case_id="E051",
        # --- trabajo 2026-09-26 (E051 t0/t1/t2 15:5xZ) ---
        fuente_primaria="INE - CTH agosto 2026 (CTH0826): anexo CTH0826.xlsx (EOH_Hoja3, fila Canarias) + API Tempus tabla 2074 (EOT1541-EOT1544); edicion anterior: API (agosto 2025 vigente) y anexo CTH0825.xlsx (provisional, 23/09/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Canarias, agosto 2026: pernoctaciones 7.216.680 (residentes 1.427.401; extranjeros 5.789.279); viajeros 1.112.371 (336.433 / 775.939)",
        dato_anterior="agosto 2025. Vigente (API): pernoctaciones 7.043.879; viajeros 1.059.785 (326.635 / 733.150). Provisional (CTH0825): pernoctaciones 7.076.919 (1.481.718 / 5.595.201); viajeros 1.056.497 (327.337 / 729.160)",
        raw_value_span_actual=(
            "[CTH0826.xlsx, hoja EOH_Hoja3, fila Canarias] 'Canarias', 1112371, 336433, 775939, 7216680, 1427401, "
            "5789279, 6.49 || [INE API tabla 2074] EOT1544 2026-M08: 7216680 | EOT1541 2026-M08: 1112371 || [LD "
            "Canarias 2026-09-22, el claim] 'Las pernoctaciones en establecimientos hoteleros en Canarias han "
            "aumentado un 2,5% en agosto'; 'hasta sumar un total de 7.216.680 pernoctaciones'; 'se alojaron un 4,96% "
            "mas de turistas ... alcanzando los 1.112.371 viajeros'; 'los viajeros residentes en Espana crecieron un "
            "3% y los extranjeros aumentaron un 5,8%'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1544 2025-M08: 7043879 | EOT1541 2025-M08: 1059785 | EOT1542 2025-M08: 326635 | "
            "EOT1543 2025-M08: 733150 || [CTH0825.xlsx, hoja EOH_Hoja3, provisional agosto 2025] 'Canarias', 1056497, "
            "327337, 729160, 7076919, 1481718, 5595201, 6.7"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia (jornada 3, veta 2b). +2,45%, +4,96%, +3,0% y +5,84% se reproducen "
            "con la base VIGENTE de agosto 2025; con la provisional habrian sido +1,97, +5,29, +2,78 y +6,42. Misma "
            "edicion CTH0826 en la que EP (Madrid, E031) y EFE (Baleares, E047) usaron la provisional: el mecanismo "
            "es del redactor, no de la edicion. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Canarias. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Canarias, mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            valor_objetivo=7216680, cambio_afirmado=2.5, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q061",
        claim_text="Andalucía alcanza en agosto \"el mejor registro de pernoctaciones hoteleras\" desde 1999 con 7,72 millones",
        claim_date="2026-09-22",
        post_url="https://www.ultimahora.es/noticias/comunidades/2026/09/22/2713681/andalucia-alcanza-agosto-mejor-registro-pernoctaciones-hoteleras-desde-1999-millones.html",
        post_url_tipo="prensa", emisor="Última Hora (teletipo de Europa Press, Sevilla)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Andalucía agosto 2026 mejor registro pernoctaciones hoteleras desde 1999 7,72 millones",
        criba_query_b="Andalucía agosto 2026 'mejor registro de pernoctaciones hoteleras' OR '7,72 millones' desde 1999 verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'pernoctaciones hoteleras' Andalucía agosto 2026 '%' 'mismo mes' OR interanual septiembre 2026 EFE OR 'Europa Press' hoteles andaluces -Málaga",
        collected_at="2026-09-26", case_id="E052",
        # --- trabajo 2026-09-26 (E052 t0/t1/t2 15:5xZ) ---
        fuente_primaria="INE - CTH agosto 2026 (CTH0826): anexo CTH0826.xlsx (fila Andalucia) + API Tempus serie EOT1454 (Andalucia, pernoctaciones total; nult=340, serie desde 1999-M01); edicion anterior: API (agosto 2025 vigente) y anexo CTH0825.xlsx (provisional)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON wstempus DATOS_SERIE/EOT1454",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Andalucia, agosto 2026: 7.717.597 pernoctaciones (+1,99% con la base vigente); maximo de los 28 agostos de la serie 1999-2026",
        dato_anterior="agostos anteriores (vigente): 2019 7.587.225 (segundo), 2025 7.566.846 (tercero), 2023 7.427.401; provisional de agosto 2025 (CTH0825): 7.586.225",
        raw_value_span_actual=(
            "[INE API] EOT1454 'Andalucía. Pernoctaciones. Total.' 2026-M08: 7717597 | maximo de {1999-M08..2026-M08} "
            "= 2026-M08 || [CTH0826.xlsx, EOH_Hoja3] 'Andalucía', 2332985, 1348406, 984579, 7717597, 4174092, 3543504, "
            "3.31 || [Ultima Hora/EP 2026-09-22, el claim] titular; 'un 2% mas que en el mismo mes de 2025 y, de "
            "confirmarse el avance provisional, el mejor registro de un mes de agosto desde el inicio de la serie "
            "historica en 1999'"
        ),
        raw_value_span_anterior="[INE API] EOT1454 2019-M08: 7587225 | 2025-M08: 7566846 | 2023-M08: 7427401 || [CTH0825.xlsx, provisional] 'Andalucía', 2287040, 1333873, 953167, 7586225, 4125912, 3460312, 3.32",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (extremo), via divergencia (jornada 3). Maximo de los agostos de la serie (1999-2026): cuadra, "
            "por 130.372 sobre 2019. El +2% sale con la base vigente (+1,99%; provisional +1,73%). El propio teletipo "
            "condiciona el record a la confirmacion del avance. Sin test aplicable -> undetermined (DEC-029). "
            "methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="D", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Andalucía. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Andalucia, mensual"),
            periodo_objetivo="2026-M08", valor_objetivo=7717597,
            notas="Extremo: maximo de los agostos desde 1999. Sin test aplicable.",
        ),
    ),
    dict(
        cid="Q062",
        claim_text="Las pernoctaciones en establecimientos hoteleros en Galicia alcanzaron los 1,3 millones en julio, lo que representa un aumento del 0,68%. En concreto, han sido 1.334.577 frente a los 1.325.548 del año anterior",
        claim_date="2026-08-21",
        post_url="https://www.galiciapress.es/articulo/economia/2026-08-21/5989983-pernoctaciones-hoteleras-aumentan-julio-galicia-068",
        post_url_tipo="prensa", emisor="Galicia Press (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Galicia pernoctaciones hoteleras julio 2026 0,68% 1.334.577",
        criba_query_b="Galicia pernoctaciones hoteleras julio 2026 '0,68%' OR '1.334.577' OR '1.325.548' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="[criba dirigida: tasa provisional recomputada +0,68% frente a vigente -0,35%] pernoctaciones hoteleras Galicia julio 2026 '0,7%' OR '0,68%' OR '0,7 %' suben OR aumentan hoteles gallegos agosto 2026 INE",
        collected_at="2026-09-26", case_id="E053",
        # --- trabajo 2026-09-26 (E053 t0/t1/t2 16:0xZ) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): anexo CTH0726.xlsx (EOH_Hoja3, fila 56 Galicia) + API Tempus tabla 2074 (EOT1733, EOT1736); edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (provisional, publicado 22/08/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx /prensa/anexo_tablas/es/CTH0726.xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Galicia, julio 2026 (provisional): pernoctaciones 1.334.577 (residentes 1.011.953; extranjeros 322.624); viajeros 644.755",
        dato_anterior="julio 2025. Vigente (API): pernoctaciones 1.339.309; viajeros 639.220. Provisional (anexo CTH0725, fila 56): pernoctaciones 1.325.548 (1.018.143 / 307.405); viajeros 635.559",
        raw_value_span_actual=(
            "[CTH0726.xlsx, hoja EOH_Hoja3, fila 56] 'Galicia', 644755, 458417, 186338, 1334577, 1011953, 322624, "
            "2.07 || [INE API tabla 2074] EOT1736 2026-M07: 1334577 | EOT1733 2026-M07: 644755 || [Galicia Press/EP "
            "2026-08-21, el claim] 'Las pernoctaciones en establecimientos hoteleros en Galicia alcanzaron los 1,3 "
            "millones en julio, lo que representa un aumento del 0,68%'; 'En concreto, han sido 1.334.577 frente a "
            "los 1.325.548 del ano anterior'; 'la cifra de viajeros se incremento, en este caso un 1,45% al pasar de "
            "635.559 en julio del ano pasado a los 644.755'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] EOT1736 2025-M07: 1339309 | EOT1733 2025-M07: 639220 || [CTH0725.xlsx, hoja "
            "EOH_Hoja3, fila 56, datos provisionales julio 2025] 'Galicia', 635559, 460844, 174716, 1325548, 1018143, "
            "307405, 2.09"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta B (2b) CON CAMBIO DE SIGNO, via divergencia (jornada 3, criba dirigida sobre la tabla "
            "provisional/vigente). El teletipo imprime la base (1.325.548), que es la cifra provisional de julio "
            "2025 del anexo CTH0725; con la vigente (1.339.309) las pernoctaciones CAEN un 0,35%, no suben un 0,68%. "
            "Viajeros: +1,45% con la provisional (635.559) frente a +0,87% con la vigente (639.220). Otro medio "
            "(atlantico.net, 2026-08-22) dio '0,4% menos' con la vigente: dos tasas de signo opuesto para el mismo "
            "dato en la misma semana. Tercer B de la edicion CTH0726 (E042, E043): se declara la concentracion. "
            "Quinto 2b del conjunto. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Galicia. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Galicia, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=1334577, cambio_afirmado=0.68, unidad_cambio="pct", direccion_afirmada="sube",
            evidencia_al_publicar=dict(
                valor=1325548, edicion="INE CTH0725 (julio 2025, datos provisionales)", fecha="2025-08-22",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx",
                raw_value_span="[CTH0725.xlsx, hoja EOH_Hoja3, fila 56] 'Galicia', 635559, 460844, 174716, 1325548, 1018143, 307405, 2.09",
                verificacion="research/evidencia/D2B_CTH0725.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=1339309, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] EOT1736 2025-M07: 1339309",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (1.325.548, impresa en el claim) y no de la vigente (1.339.309): 2b con cambio de signo (+0,68% frente a -0,35%).",
        ),
    ),
    dict(
        cid="Q063",
        claim_text="Las pernoctaciones en alojamientos turísticos extrahoteleros gallegos se situaron en 473.188 en junio, lo que representa un incremento del 9,33%",
        claim_date="2026-07-31",
        post_url="https://www.galiciapress.es/articulo/economia/2026-07-31/5971575-pernoctaciones-extrahoteleras-crecen-93-junio-galicia-frente-descenso-media",
        post_url_tipo="prensa", emisor="Galicia Press (teletipo de Europa Press)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Galicia pernoctaciones extrahoteleras junio 2026 9,33% 473.188",
        criba_query_b="Galicia pernoctaciones extrahoteleras junio 2026 '473.188' OR '9,33%' OR '9,3%' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="galiciapress pernoctaciones hoteleras Galicia agosto 2026 OR junio 2026 'frente a' año anterior '%' viajeros INE",
        collected_at="2026-09-26", case_id="E054",
        # --- trabajo 2026-09-26 (E054 t0/t1/t2 16:1xZ) ---
        fuente_primaria="INE - EOAT junio 2026 (EOAT0626): anexo EOAT0626.xlsx (filas Galicia en EOAP_Hoja1, EOAC_Hoja1, EOTR_Hoja1, EOAL_Hoja2) + API Tempus tablas 1993, 2016 y 61766; edicion anterior: API (junio 2025 vigente) y anexo EOAT0625.xlsx (provisional, 31/07/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/EOAT0626.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON (tres tablas)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Galicia, junio 2026: apartamentos 95.756 + campings 195.633 + turismo rural 41.906 + albergues 139.893 = 473.188",
        dato_anterior="junio 2025. Vigente (API): 90.048 + 158.077 + 38.393 + 146.304 = 432.822 (+9,33%). Provisional (EOAT0625): 87.654 + 166.278 + 35.978 + 142.572 = 432.482 (+9,41%)",
        raw_value_span_actual=(
            "[INE API] EOT1108 2026-M06: 95756 | EOT804 2026-M06: 195633 | EOT1217 2026-M06: 41906 | EOT44284 "
            "2026-M06: 139893 || [EOAT0626.xlsx, filas Galicia] EOAP_Hoja1 ... 95756 | EOAC_Hoja1 ... 195633 | "
            "EOTR_Hoja1 ... 41906 | EOAL_Hoja2 ... 139893 || [Galicia Press/EP 2026-07-31, el claim] 'se situaron "
            "en 473.188 en junio, lo que representa un incremento del 9,33%'; 'apartamentos turisticos de Galicia "
            "subieron de 90.048 a 95.756'; 'campings ascendieron de 158.077 a 195.633'; 'turismo rural, pasaron de "
            "38.393 a 41.906'; 'albergues ... 139.893, dato algo inferior a las 146.304'"
        ),
        raw_value_span_anterior=(
            "[INE API] EOT1108 2025-M06: 90048 | EOT804 2025-M06: 158077 | EOT1217 2025-M06: 38393 | EOT44284 "
            "2025-M06: 146304 || [EOAT0625.xlsx, provisional junio 2025, filas Galicia] EOAP_Hoja1 ... 87654 | "
            "EOAC_Hoja1 ... 166278 | EOTR_Hoja1 ... 35978 | EOAL_Hoja2 ... 142572"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional (EOAT), via divergencia (jornada 3). EP imprime las cuatro bases (90.048, 158.077, "
            "38.393, 146.304) y las cuatro son las VIGENTES: la suma da +9,33% exacto; con la provisional habria "
            "sido +9,41%. El mismo teletipo escribe 'mismo mes de 2024' donde corresponde 2025 (errata, no se "
            "evalua). Metrica compuesta (suma de cuatro series): fuera del prototipo actual, se declara (como E049). "
            "Segundo caso de EOAT0626 (E050 F). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EOAT0626",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="1993 + 2016 + 61766 (suma de cuatro series)",
                         serie_nombre="Galicia. Pernoctaciones extrahoteleras (EOAP + EOAC + EOTR + EOAL)",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="Suma de pernoctaciones en apartamentos, campings, turismo rural y albergues, Galicia, mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=473188, cambio_afirmado=9.33, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control con metrica compuesta (suma de cuatro series): base interanual vigente.",
        ),
    ),
    dict(
        cid="Q064",
        claim_text="Las pernoctaciones en establecimientos hoteleros en Castilla y León en agosto descendieron pese al tirón del eclipse total de sol. Lo hicieron un 4,5 % en comparación con el mismo mes del año anterior, hasta un total de 1.005.272",
        claim_date="2026-09-22",
        post_url="https://www.eldebate.com/espana/castilla-y-leon/20260922/pernoctaciones-hoteleras-caen-castilla-leon-pese-eclipse-precios-suben-cerca-12-agosto_461304.html",
        post_url_tipo="prensa", emisor="El Debate (edición Castilla y León; mismo texto en El Correo de Burgos y CyL Digital, teletipo)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Castilla y León pernoctaciones hoteleras agosto 2026 4,5% 1.005.272",
        criba_query_b="Castilla y León pernoctaciones hoteleras agosto 2026 '1.005.272' OR '4,5 %' OR '622.043' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="pernoctaciones hoteleras julio 2026 OR agosto 2026 'frente a los' OR 'frente a las' 'del año anterior' OR 'de 2025' comunidad OR provincia hoteles INE -Galicia -nacional",
        collected_at="2026-09-26", case_id="E055",
        # --- trabajo 2026-09-26 (E055 t0/t1/t2 16:2xZ) ---
        fuente_primaria="INE - CTH agosto 2026 (CTH0826): anexo CTH0826.xlsx (EOH_Hoja3, fila Castilla y Leon) + API Tempus tabla 2074; edicion anterior: API (agosto 2025 vigente) y anexo CTH0825.xlsx (provisional, publicado 23/09/2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0826.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Castilla y Leon, agosto 2026 (provisional): pernoctaciones 1.005.272; viajeros 622.043 (residentes 428.650; extranjeros 193.393)",
        dato_anterior="agosto 2025. Vigente (API): pernoctaciones 1.038.403; viajeros 641.977. Provisional (anexo CTH0825): pernoctaciones 1.051.890; viajeros 651.830",
        raw_value_span_actual=(
            "[INE API tabla 2074] 'Castilla y León. Pernoctaciones. Total.' 2026-M08: 1005272 | 'Castilla y León. "
            "Viajeros. Total.' 2026-M08: 622043 || [El Debate 2026-09-22, el claim] 'Lo hicieron un 4,5 % en "
            "comparacion con el mismo mes del ano anterior, hasta un total de 1.005.272 operaciones, segun datos "
            "publicados por el Instituto Nacional de Estadistica (INE)'; 'se alojaron tambien un 4,5 % menos de "
            "turistas en agosto que en el mismo mes del ano anterior, y se alcanzaron los 622.043 viajeros'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] 'Castilla y León. Pernoctaciones. Total.' 2025-M08: 1038403 | 'Castilla y León. "
            "Viajeros. Total.' 2025-M08: 641977 || [CTH0825.xlsx, hoja EOH_Hoja3, datos provisionales agosto 2025] "
            "'Castilla y León', 651830, ..., 1051890, ..."
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta B (2b), via divergencia (jornada 3). Contra la edicion vigente: pernoctaciones -3,19%, viajeros "
            "-3,11%. Contra la provisional de agosto 2025: -4,43% y -4,57%. El '4,5%' doble del teletipo solo se "
            "acerca con la provisional (a 0,1 pp; la base exacta no es reproducible al centesimo, NEEDS_REVIEW, "
            "como E042). Otros medios (heraldodeleon para Leon, y la cobertura que da -3,2% para CyL) usaron la "
            "vigente: dos tasas para el mismo dato la misma manana. Tercer B de la edicion CTH0826 (E031, E047): "
            "se declara la concentracion. Sexto 2b del conjunto. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0826",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Castilla y León. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Castilla y Leon, mensual"),
            periodo_objetivo="2026-M08", periodo_base="2025-M08",
            valor_objetivo=1005272, cambio_afirmado=-4.5, unidad_cambio="pct", direccion_afirmada="baja",
            evidencia_al_publicar=dict(
                valor=1051890, edicion="INE CTH0825 (agosto 2025, datos provisionales)", fecha="2025-09-23",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0825.xlsx",
                raw_value_span="[CTH0825.xlsx, hoja EOH_Hoja3] 'Castilla y León', 651830, ..., 1051890, ...",
                verificacion="research/evidencia/D2B_CTH0825.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=1038403, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] 'Castilla y León. Pernoctaciones. Total.' 2025-M08: 1038403",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (1.051.890) y no de la vigente (1.038.403): 2b sin cambio de signo (-4,43% frente a -3,19%).",
        ),
    ),
    dict(
        cid="Q065",
        claim_text="Los establecimientos de la Comunidad registraron 410.706 pernoctaciones, un 4,09% más que en el mismo mes de 2025, según los últimos datos publicados por el Instituto Nacional de Estadística (INE)",
        claim_date="2026-08-21",
        post_url="https://murciaeconomia.com/art/108300/los-hoteles-de-la-region-de-murcia-superan-las-410000-pernoctaciones-en-julio-y-crecen-un-4",
        post_url_tipo="prensa", emisor="MurciaEconomía (mismo texto en COPE, Murcia Plaza y Murcia Diario: teletipo regional)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Murcia pernoctaciones hoteleras julio 2026 410.706 4%",
        criba_query_b="'Región de Murcia' pernoctaciones hoteleras julio 2026 '410.706' OR '4,09%' OR '165.223' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="[criba dirigida: tasa provisional recomputada +4,09% frente a vigente +3,32%] pernoctaciones hoteleras julio 2026 'Región de Murcia' '4,1%' OR '3,3%' OR Cantabria '0,1%' OR 'estables' OR Huelva '4,2%' OR '3,1%' hoteles agosto 2026 INE",
        collected_at="2026-09-26", case_id="E056",
        # --- trabajo 2026-09-26 (E056 t0/t1/t2 16:4xZ) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): anexo CTH0726.xlsx (EOH_Hoja3, fila Murcia) + API Tempus tabla 2074; edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (provisional, publicado 22/08/2025, fila 62)",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Region de Murcia, julio 2026 (provisional): pernoctaciones 410.706 (residentes 301.143; extranjeros 109.564); viajeros 165.223 (121.005 / 44.218)",
        dato_anterior="julio 2025. Vigente (API): pernoctaciones 397.508 (285.853 / 111.655); viajeros 163.076 (115.175 / 47.901). Provisional (anexo CTH0725, fila 62): pernoctaciones 394.572 (284.106 / 110.467); viajeros 162.708 (115.570 / 47.139)",
        raw_value_span_actual=(
            "[INE API tabla 2074] 'Murcia (Región de). Pernoctaciones. Total.' 2026-M07: 410706 | 'Murcia (Región "
            "de). Viajeros. Total.' 2026-M07: 165223 || [MurciaEconomia 2026-08-21, el claim] 'Los establecimientos "
            "de la Comunidad registraron 410.706 pernoctaciones, un 4,09% mas que en el mismo mes de 2025'; 'alojaron "
            "a 165.223 turistas, un 1,55% mas que en el mismo periodo del ano anterior'; '121.005 fueron residentes "
            "en Espana, mientras que 44.218 procedieron del extranjero'; 'los turistas nacionales realizaron 301.143, "
            "frente a las 109.564'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] 'Murcia (Región de). Pernoctaciones. Total.' 2025-M07: 397508 | 'Murcia (Región "
            "de). Viajeros. Total.' 2025-M07: 163076 || [CTH0725.xlsx, hoja EOH_Hoja3, fila 62, datos provisionales "
            "julio 2025] 'Murcia, Región de', 162708, 115570, 47139, 394572, 284106, 110467, 2.43"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="si",  # 4o B de CTH0726: tope 3 (diseno 4c)
        notas=(
            "EXCEDENTE por el tope de tres B por edicion (diseno 4c): cuarto B de CTH0726 en orden de "
            "recoleccion (E042, E043, E053, E056). Se anota igual y no cuenta para la cubeta. "
            "Cubeta B (2b), via divergencia (jornada 3, criba dirigida sobre la tabla provisional/vigente). Las dos "
            "tasas del articulo (+4,09% y +1,55%) son exactamente las de la base PROVISIONAL de julio 2025 "
            "(394.572 y 162.708); con la vigente serian +3,32% y +1,32%. Mismo signo: subtipo magnitud. Cuarto B de "
            "la edicion CTH0726 (E042, E043, E053): se declara la concentracion. Septimo 2b del conjunto. "
            "methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Murcia (Región de). Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Region de Murcia, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=410706, cambio_afirmado=4.09, unidad_cambio="pct", direccion_afirmada="sube",
            evidencia_al_publicar=dict(
                valor=394572, edicion="INE CTH0725 (julio 2025, datos provisionales)", fecha="2025-08-22",
                url="https://www.ine.es/prensa/anexo_tablas/es/CTH0725.xlsx",
                raw_value_span="[CTH0725.xlsx, hoja EOH_Hoja3, fila 62] 'Murcia, Región de', 162708, 115570, 47139, 394572, 284106, 110467, 2.43",
                verificacion="research/evidencia/D2B_CTH0725.json (HTTP 200, sha256)",
            ),
            evidencia_vigente=dict(
                valor=397508, edicion="API Tempus, tabla 2074, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2074",
                raw_value_span="[INE API tabla 2074] 'Murcia (Región de). Pernoctaciones. Total.' 2025-M07: 397508",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (394.572) y no de la vigente (397.508): 2b sin cambio de signo (+4,09% frente a +3,32%).",
        ),
    ),
    dict(
        cid="Q066",
        claim_text="C-LM registra en julio 340.617 pernoctaciones hoteleras, un 6,7% menos que hace un año",
        claim_date="2026-08-21",
        post_url="https://www.lanzadigital.com/castilla-la-mancha/pernoctaciones-hotelera/",
        post_url_tipo="prensa", emisor="Lanza (Ciudad Real; mismo texto en La Cerca: teletipo)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Castilla-La Mancha pernoctaciones hoteleras julio 2026 6,7% 340.617",
        criba_query_b="Castilla-La Mancha pernoctaciones hoteleras julio 2026 '340.617' OR '6,7%' OR '184.864' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'Castilla y León' pernoctaciones hoteleras julio 2026 '7,7%' OR '7,7 %' OR '7,1%' OR '7,1 %' caen hoteles agosto 2026 INE",
        collected_at="2026-09-26", case_id="E057",
        # --- trabajo 2026-09-26 (E057 t0/t1/t2 16:5xZ) ---
        fuente_primaria="INE - CTH julio 2026 (CTH0726): API Tempus tabla 2074 + anexo CTH0726.xlsx; edicion anterior: API (julio 2025 vigente) y anexo CTH0725.xlsx (provisional, fila 38 'Castilla-La Mancha')",
        primaria_url="https://www.ine.es/dyngs/Prensa/CTH0726.htm",
        primaria_url_tipo="nota_de_prensa_html + anexo xlsx + API JSON wstempus DATOS_TABLA/2074",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Castilla-La Mancha, julio 2026: pernoctaciones 340.617 (residentes 279.330; extranjeros 61.287); viajeros 184.864 (151.217 / 33.646)",
        dato_anterior="julio 2025. Vigente (API): pernoctaciones 365.001 (297.773 / 67.228); viajeros 204.641 (167.557 / 37.083). Provisional (CTH0725, fila 38): pernoctaciones 361.760 (292.584 / 69.175); viajeros 207.407 (169.560 / 37.847)",
        raw_value_span_actual=(
            "[INE API tabla 2074] 'Castilla - La Mancha. Pernoctaciones. Total.' 2026-M07: 340617 | 'Castilla - La "
            "Mancha. Viajeros. Total.' 2026-M07: 184864 || [Lanza 2026-08-21, el claim] 'Las pernoctaciones en "
            "establecimientos hoteleros en Castilla-La Mancha en julio empeoran y descienden un 6,7%'; 'se alojaron "
            "un 9,66% menos de turistas en julio'; '151.217 eran residentes en Espana, el 81,8%, mientras que 33.646 "
            "(18,2%) fueron extranjeros'; 'los viajeros residentes en Espana disminuyeron un 9,8% y los extranjeros "
            "se redujeron un 9,3%'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 2074] 'Castilla - La Mancha. Pernoctaciones. Total.' 2025-M07: 365001 | 'Castilla - La "
            "Mancha. Viajeros. Total.' 2025-M07: 204641 || [CTH0725.xlsx, hoja EOH_Hoja3, fila 38, provisional] "
            "'Castilla-La Mancha', 207407, 169560, 37847, 361760, 292584, 69175, 1.74"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A regional, via divergencia (jornada 3). -6,68%, -9,66%, -9,75% y -9,27% son exactamente las "
            "tasas con la base VIGENTE; con la provisional habrian sido -5,84, -10,87, -10,82 y -11,10. Tercer A de "
            "CTH0726 (E035, E048): tope por edicion alcanzado. Misma manana y misma edicion en que Galicia Press "
            "(E053) y MurciaEconomia (E056) usaron la provisional: el mecanismo es del redactor. "
            "methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="INE CTH0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="2074",
                         serie_nombre="Castilla - La Mancha. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOH, pernoctaciones en establecimientos hoteleros, Castilla-La Mancha, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=340617, cambio_afirmado=-6.7, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Control regional: base interanual (edicion vigente) = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q047",
        claim_text="Las compraventas superan las 60.000 operaciones en el mejor julio desde 2007, a la espera del impacto de los tipos",
        claim_date="2026-09-25",
        post_url="https://prensa.fotocasa.es/las-compraventas-superan-las-60-000-operaciones-en-el-mejor-julio-desde-2007-a-la-espera-del-impacto-de-los-tipos/",
        post_url_tipo="nota_oficial", emisor="Fotocasa (nota de prensa; María Matos, directora de Estudios)", emisor_tipo="empresa",
        emisor_nivel=2, pais="ES", tema="vivienda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Fotocasa compraventas julio 2026 'mejor julio desde 2007'",
        criba_query_b="'mejor julio desde 2007' compraventas 2026 Fotocasa verificación OR bulo OR fact-check OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="'compraventa' viviendas julio 2026 'sube un 3,6%' OR 'aumenta un 3,6%' OR 'repunta un 3,6%' OR 'crece un 3,6%' INE titular",
        collected_at="2026-09-26", case_id="E038",
        # --- trabajo 2026-09-26 (E038 t0/t1/t2 14:2xZ; la serie ya estaba descargada) ---
        fuente_primaria="INE - ETDP julio 2026: nota ETDP0726 + API Tempus serie ETDP1826 (tabla 6150), nult=240 (todos los julios 2007-2026)",
        primaria_url="https://www.ine.es/dyngs/Prensa/ETDP0726.htm",
        primaria_url_tipo="nota_de_prensa_html (provisional) + API JSON wstempus DATOS_SERIE/ETDP1826",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="julio 2026: 61.417 compraventas de viviendas (provisional), -5,1% interanual, +3,6% mensual",
        dato_anterior="julios de la serie (2007-2026): 2025 64.722 (maximo), 2007 63.731, 2026 61.417 (tercero); siguiente 2024 56.942",
        raw_value_span_actual=(
            "[INE API] ETDP1826 2026-M07: 61417 || [Fotocasa 2026-09-25, el claim] titular; cuerpo: 'refleja un "
            "incremento mensual del 3,6% y un descenso anual del 5,1%'; 'Julio ha registrado 61.417 compraventas "
            "... se mantiene este mes por encima de la media del ejercicio anterior de 58.700 operaciones mensuales'"
        ),
        raw_value_span_anterior=(
            "[INE API, ETDP1826, valores de julio] 2007: 63731 | 2024: 56942 | 2025: 64722 | 2026: 61417 || "
            "maximo de {julio 2007..julio 2026} = 2025 (64722)"
        ),
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="claim_falso", excedente="no",
        notas=(
            "Cubeta F (claim falso), via divergencia. 'El mejor julio desde 2007' es falso con la serie del INE: "
            "julio 2025 (64.722) y julio 2007 (63.731) superan a julio 2026 (61.417), tercer julio de la serie. El "
            "cuerpo de la nota reconoce el -5,1% interanual. Es un extremo falso, no una base elegida: el numero (el "
            "ranking) es incorrecto, no el marco. Hermano potencial: blogprofesional.fotocasa.es (mismo texto). "
            "Edicion ETDP0726 ya con E001 (A), E029 (A) y E002 (O); F no cuenta en el tope de controles. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="F", hermano_de="", mecanismo_candidato="", primaria_edicion="INE ETDP0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="extremo_historico",
            metrica=dict(emisor="INE", tabla="6150",
                         serie_nombre="Total Nacional. General. Compraventa. Número. ",
                         unidad="compraventas", referencia_principal="interanual",
                         descripcion="ETDP, compraventas de viviendas inscritas, total nacional, mensual"),
            periodo_objetivo="2026-M07", valor_objetivo=61417,
            notas="Extremo afirmado (maximo de los julios desde 2007) contradicho por la serie: 2025 y 2007 son mayores.",
        ),
    ),
    dict(
        cid="Q048",
        claim_text="La criminalidad en Madrid baja a 55,7 delitos por cada mil habitantes, pero aumentan un 9,7 % las denuncias por delitos sexuales",
        claim_date="2026-09-18",
        post_url="https://www.eldiariodemadrid.es/articulo/sociedad/criminalidad-madrid-2026-tasa-delitos-cibercriminalidad-delitos-sexuales-primer-semestre/20260918143337141847.html",
        post_url_tipo="declaracion", emisor="Delegación del Gobierno en la Comunidad de Madrid (Francisco Martín), vía El Diario de Madrid", emisor_tipo="institucion",
        emisor_nivel=1, pais="ES", tema="criminalidad",
        criba_query_a="", criba_query_b="",
        criba_resultado="rechazado",
        criba_motivo=(
            "edicion_vetada: los datos son del Balance de Criminalidad 2T2026 (primer semestre), edicion usada por el "
            "piloto (C18) y vetada por DEC-025. HALLAZGO para la medicion de la jornada 2: es el unico patron B "
            "encontrado en la via dirigida. La Delegacion sostiene 'la tasa se ha situado en 55,7 delitos por cada "
            "mil habitantes' (-0,5 puntos interanual) y, segun la cobertura, 'se ha reducido 5,5 puntos desde 2019, "
            "4,3 desde 2023' [no verbatim, NEEDS_REVIEW], mientras la misma nota registra 159.644 -> 163.734 "
            "infracciones convencionales (+2,6% interanual). Base elegida (2023/2019) y tasa por poblacion frente al "
            "recuento: candidato a 2a con cambio de signo o a 4 (denominador). Reaparece en cada balance: la primera "
            "edicion admisible seria la del 3T2026 (diciembre)"
        ),
        criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="Madrid criminalidad 2026 'primer trimestre' baja OR desciende OR 'se reduce' OR 'cae' '%' Ayuso OR 'Consejería' OR 'Delegación del Gobierno' OR Marlaska OR 'Ministerio del Interior' declaración Comunidad de Madrid -Alcorcón",
    ),
    # ------------------------------------------------------------------
    # JORNADA 4 (2026-09-26, desde 17:58Z): cuota de emisor (diseno 4f).
    # Localizacion en lote 18:05-18:15Z: busquedas SEPE julio 2026, BdE junio 2026
    # y Portal 1T2026, y descarga de 9 PDF mensuales del SEPE (todos 200).
    # ------------------------------------------------------------------
    dict(
        cid="Q067",
        claim_text="El paro se redujo en Andalucía en 9.661 personas (-1,8%) en julio, situando la cifra total de desempleados en la comunidad en 526.862 personas, el registro más bajo desde diciembre de 2007",
        claim_date="2026-08-04",
        post_url="https://www.juntadeandalucia.es/organismos/empleoempresaytrabajoautonomo/servicios/actualidad/noticias/detalle/679072.html",
        post_url_tipo="nota_oficial", emisor="Junta de Andalucía (Consejería de Empleo, nota de prensa)", emisor_tipo="institucion",
        emisor_nivel=2, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com paro Andalucía julio 2026 9.661 526.862",
        criba_query_b="paro Andalucía julio 2026 '9.661' OR '526.862' 'diciembre de 2007' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="paro julio 2026 Andalucía '9.661' baja OR desciende Junta OR SEPE noticia agosto 2026 comunidad",
        collected_at="2026-09-26", case_id="E058",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E058 t0 18:16Z) ---
        fuente_primaria="SEPE - Paro registrado julio 2026: nota 'El paro sube en 19.517 personas en julio y se situa en 2.311.499' (2026-08-04) + Datos estadisticos de empleo julio 2026, PDF 'DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf' (tabla 6.2, parados por CCAA y provincia); ediciones anteriores: el mismo PDF de junio 2026 y de julio 2025",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/empleo/datos/2026/Julio_2026/DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf",
        primaria_url_tipo="PDF mensual del SEPE (HTTP 200 al agente identificado, 710.727 bytes, sha256 856b794bb982123d) + nota HTML (200); junio 2026 (200, 710.639 bytes, b59396969ece7759) y julio 2025 (200, 699.282 bytes, d4e55adbdbe8f483)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="pdf",
        dato_actual="Andalucia, julio 2026: 526.862 parados (tabla 6.2, p.4); total nacional 2.311.499",
        dato_anterior="junio 2026: Andalucia 536.523 (-> -9.661, -1,80%); total 2.291.982 (-> +19.517, +0,85%). Julio 2025: Andalucia 590.855 (-> -63.993, -10,83%); total 2.404.606 (-> -93.107, -3,87%)",
        raw_value_span_actual=(
            "[DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf julio 2026, p.4, tabla 6.2] 'ANDALUCIA 526.862 11.012 29.970 "
            "39.401 44.338 50.097 52.366 59.594 68.354 84.511 87.219' | 'TOTAL ZONA GEOGRAFICA 2.311.499 ...' || "
            "[nota SEPE 2026-08-04] 'El paro registrado baja en tres Comunidades Autonomas en cifras absolutas en "
            "Andalucia (-9.661 personas), Extremadura (-767 personas) y Cantabria (-250 personas)' || [Junta de "
            "Andalucia 2026-08-04, el claim] 'El paro se redujo en Andalucia en 9.661 personas (-1,8%)'; 'la cifra "
            "total de desempleados en la comunidad en 526.862 personas, el registro mas bajo desde diciembre de 2007'"
        ),
        raw_value_span_anterior=(
            "[mismo PDF, junio 2026, p.4] 'ANDALUCIA 536.523 11.632 31.036 ...' | 'TOTAL ZONA GEOGRAFICA 2.291.982 "
            "...' || [mismo PDF, julio 2025, p.4] 'ANDALUCIA 590.855 12.771 34.810 ...' | 'TOTAL ZONA GEOGRAFICA "
            "2.404.606 ...'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor SEPE (edicion julio 2026, primer caso), jornada 4 (cuota de emisor), via busqueda a "
            "organismo. 536523-526862 = 9.661; 9661/536523 = 1,80%: la base mensual es la referencia de cabecera del "
            "SEPE; interanual -10,83%, mismo signo: sin 2a. 'Mas bajo desde diciembre de 2007' NO evaluado: cada PDF "
            "mensual trae solo su mes; la serie por CCAA exigiria ~225 PDF (NEEDS_REVIEW). El resto de la nota "
            "(68,7% del descenso nacional: 63993/93107 = 68,7%, cuadra; 'multiplica por mas de siete la suma de los "
            "otros cuatro territorios') no se anota como claim. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE paro julio 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="SEPE", tabla="DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf / tabla 6.2",
                         serie_nombre="Parados registrados, Andalucía", unidad="personas",
                         referencia_principal="mensual",
                         descripcion="Paro registrado por comunidad autonoma, nivel mensual"),
            periodo_objetivo="2026-M07", periodo_base="2026-M06",
            valor_objetivo=526862, cambio_afirmado=-1.8, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Base mensual = referencia del emisor. El extremo ('mas bajo desde diciembre de 2007') no se evalua.",
        ),
    ),
    dict(
        cid="Q068",
        claim_text="La provincia de Sevilla registra seis meses consecutivos de descenso del paro: 13.005 personas menos en los registros del SEPE",
        claim_date="2026-08-04",
        post_url="https://www.elpespunte.es/articulo/provincia/provincia-sevilla-registra-seis-meses-consecutivos-descenso-paro-13005-personas-menos-desempleo/20260804144002144084.html",
        post_url_tipo="prensa", emisor="El Pespunte (Lucía Palop)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com paro Sevilla julio 2026 13.005 seis meses consecutivos",
        criba_query_b="paro Sevilla julio 2026 '13.005' OR '131.385' OR '1.618' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="paro julio 2026 Andalucía '9.661' baja OR desciende Junta OR SEPE noticia agosto 2026 comunidad",
        collected_at="2026-09-26", case_id="E059",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E059 t0 18:16Z) ---
        fuente_primaria="SEPE - Datos estadisticos de empleo, PDF 'DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf' (tabla 6.2, parados por provincia) de julio 2026 y de las siete ediciones anteriores (diciembre 2025 a junio 2026) y de julio 2025",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/empleo/datos/2026/Julio_2026/DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf",
        primaria_url_tipo="PDF mensual del SEPE, misma ruta con <Mes>_<Anyo>: 9 ediciones, todas HTTP 200 al agente identificado (~700 KB cada una; sha256 julio 2026 856b794bb982123d, enero 2026 0ea4bb5bb79879b3, julio 2025 d4e55adbdbe8f483)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="pdf",
        dato_actual="Sevilla (provincia), julio 2026: 131.385 parados (hombres 49.828, mujeres 81.557)",
        dato_anterior="Sevilla: dic-2025 142.010 | ene-2026 144.390 | feb 144.076 | mar 142.137 | abr 136.312 | may 134.838 | jun 133.003 | jul 131.385 (seis descensos consecutivos feb-jul; 144390-131385 = 13.005; junio->julio -1.618). Julio 2025: 145.192 (-13.807, -9,51%)",
        raw_value_span_actual=(
            "[DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf julio 2026, p.4, tabla 6.2] 'SEVILLA 131.385 2.717 7.647 10.153 "
            "11.148 12.419 13.011 15.028 17.309 21.024 20.929' | [p.5, hombres] 'SEVILLA 49.828 ...' | [p.6, mujeres] "
            "'SEVILLA 81.557 ...' || [El Pespunte 2026-08-04, el claim] '13.005 personas han salido de los registros "
            "del Servicio Publico de Empleo Estatal (SEPE) durante la primera mitad de 2026'; '1.618 personas dejaron "
            "de estar en las listas del paro en julio'; 'el desempleo se ha reducido un 9,5 % en el ultimo ano, con "
            "131.385 personas desempleadas'"
        ),
        raw_value_span_anterior=(
            "[mismo PDF, p.4, tabla 6.2, por edicion] enero 2026 'SEVILLA 144.390 ...' | febrero 'SEVILLA 144.076 "
            "...' | marzo 'SEVILLA 142.137 ...' | abril 'SEVILLA 136.312 ...' | mayo 'SEVILLA 134.838 ...' | junio "
            "'SEVILLA 133.003 ...' | julio 2025 'SEVILLA 145.192 ...' | diciembre 2025 'SEVILLA 142.010 ...'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor SEPE (edicion julio 2026, segundo caso), jornada 4, via busqueda a organismo. La "
            "ventana 'primera mitad de 2026' (enero->julio, base elegida) es distinta de las referencias del SEPE "
            "(mensual, interanual): test 2a aplicable. Recomputado: mensual -1.618, interanual -13.807, ambos "
            "descensos -> sin cambio de signo, no dispara. SENAL DE HORIZONTE (DEC-029): 13.005 frente a 1.618 "
            "mensual = 8x; se registra, no cuenta como divergencia. 'Seis meses consecutivos': feb-jul 2026 todos "
            "por debajo del mes anterior (siete PDF), cuadra. La 'tasa de paro 13,45%' es EPA, fuera del emisor: no se "
            "evalua. methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE paro julio 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="SEPE", tabla="DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf / tabla 6.2",
                         serie_nombre="Parados registrados, Sevilla (provincia)", unidad="personas",
                         referencia_principal="mensual",
                         descripcion="Paro registrado por provincia, nivel mensual"),
            periodo_objetivo="2026-M07", periodo_base="2026-M01",
            valor_objetivo=131385, cambio_afirmado=-13005, unidad_cambio="abs", direccion_afirmada="baja",
            notas="Base elegida (enero 2026, 'primera mitad de 2026'); referencias del emisor mensual (-1.618) e interanual (-13.807): mismo signo. Senal de horizonte 8x.",
        ),
    ),
    dict(
        cid="Q069",
        claim_text="Cantabria, una de las tres únicas autonomías donde bajó el paro en julio, con 250 desempleados menos (-0,94%)",
        claim_date="2026-08-04",
        post_url="https://www.eldiario.es/cantabria/cantabria-tres-unicas-autonomias-paro-julio-250-desempleados_1_13426684.html",
        post_url_tipo="prensa", emisor="elDiario.es Cantabria", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com paro Cantabria julio 2026 250 desempleados",
        criba_query_b="paro Cantabria julio 2026 '250' '26.355' OR '0,94%' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="paro julio 2026 Cantabria '250' OR Extremadura '767' OR Cádiz '3.479' baja desempleados noticia 4 agosto 2026",
        collected_at="2026-09-26", case_id="E060",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E060 t0 18:16Z) ---
        fuente_primaria="SEPE - Paro registrado julio 2026: nota 2026-08-04 + PDF 'DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf' (tabla 6.2) de julio 2026, junio 2026 y julio 2025",
        primaria_url="https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/empleo/datos/2026/Julio_2026/DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf",
        primaria_url_tipo="PDF mensual del SEPE (HTTP 200 al agente identificado, 710.727 bytes, sha256 856b794bb982123d) + nota HTML (200) + PDF de junio 2026 y julio 2025 (200)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="pdf",
        dato_actual="Cantabria, julio 2026: 26.355 parados; junio 2026: 26.605 (-> -250, -0,94%). Nota SEPE: baja en Andalucia (-9.661), Extremadura (-767) y Cantabria (-250)",
        dato_anterior="julio 2025: Cantabria 26.971 (-> -616, -2,28%); total nacional 2.404.606 -> 2.311.499 (-3,87%)",
        raw_value_span_actual=(
            "[DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf julio 2026, p.4, tabla 6.2] 'CANTABRIA 26.355 474 1.223 1.822 "
            "1.989 2.350 2.707 3.189 3.433 4.218 4.950' || [nota SEPE 2026-08-04] 'El paro registrado baja en tres "
            "Comunidades Autonomas en cifras absolutas en Andalucia (-9.661 personas), Extremadura (-767 personas) y "
            "Cantabria (-250 personas)' || [elDiario.es Cantabria 2026-08-04, el claim] 'bajo en 250 personas en "
            "julio en Cantabria en relacion al mes anterior (-0,94%)'; 'cerro el mes con 26.355 desempleados'; 'En el "
            "ultimo ano el desempleo en la comunidad autonoma acumula un descenso de 616 parados, lo que supone un "
            "2,28% menos'"
        ),
        raw_value_span_anterior="[mismo PDF, junio 2026, p.4] 'CANTABRIA 26.605 535 1.319 ...' || [mismo PDF, julio 2025, p.4] 'CANTABRIA 26.971 462 1.243 ...'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor SEPE (edicion julio 2026, tercer caso: tope de controles alcanzado), jornada 4, via "
            "busqueda a organismo. 26605-26355 = 250; 250/26605 = 0,94%; interanual 26971-26355 = 616 (2,28%): "
            "cuadra con la base mensual (referencia de cabecera) y con la interanual, mismo signo: sin 2a. 'Tres "
            "unicas autonomias': la nota del SEPE nombra exactamente esas tres. 'Cifra mas baja en un mes de julio "
            "desde 2008' y 'cinco meses consecutivos de descensos' no evaluados (NEEDS_REVIEW). methodology_found=no."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="SEPE paro julio 2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="SEPE", tabla="DATOS_POR_CCAA-DEMANDAS_PENDIENTES.pdf / tabla 6.2",
                         serie_nombre="Parados registrados, Cantabria", unidad="personas",
                         referencia_principal="mensual",
                         descripcion="Paro registrado por comunidad autonoma, nivel mensual"),
            periodo_objetivo="2026-M07", periodo_base="2026-M06",
            valor_objetivo=26355, cambio_afirmado=-0.94, unidad_cambio="pct", direccion_afirmada="baja",
            notas="Base mensual = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q070",
        claim_text="La deuda pública crece un 4,2% en junio y marca un nuevo máximo de 1,76 billones de euros, el 101,5% del PIB",
        claim_date="2026-08-18",
        post_url="https://www.tercerainformacion.es/articulo/actualidad/18/08/2026/la-deuda-publica-crece-un-42-en-junio-y-marca-un-nuevo-maximo-de-176-billones-de-euros-el-1015-del-pib/",
        post_url_tipo="prensa", emisor="Tercera Información (Agencias)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="deuda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública junio 2026 1,76 billones 101,5%",
        criba_query_b="deuda pública junio 2026 '1,76 billones' OR '1.763' '101,5%' '4,2%' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'deuda' junio 2026 '1,763' OR '1.763' OR '101,5%' 'Banco de España' récord agosto 2026 noticia comunidades OR '1,76 billones'",
        collected_at="2026-09-26", case_id="E061",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E061 t0 18:16Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual junio 2026: nota 'La deuda de las Administraciones Publicas se situo en junio de 2026 en el 101,5% del PIB' (18/08/2026) + PDF presbe2026-78.pdf; ediciones anteriores: marzo 2026 (19/05/2026, anterior maximo) y julio 2026 (17/09/2026, E033)",
        primaria_url="https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-junio26.html",
        primaria_url_tipo="nota_de_prensa_html (HTTP 200 al agente identificado; copia bde_jun26.htm) + PDF /f/webbe/GAP/Secciones/SalaPrensa/NotasInformativas/26/presbe2026-78.pdf; serie enlazada en la nota: app.bde.es/bie_www?SERIE=DMNPDE2010_P00000_PS_APU",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="html",
        dato_actual="junio 2026: ratio deuda PDE/PIB 101,5%; saldo 1.763 mm EUR; tasa interanual +4,2%",
        dato_anterior="marzo 2026 (nota 19/05/2026): 1.740 mm EUR, 101,6%, +4,3% (1763/1740 = +1,32%). Julio 2026 (E033): 1.744 mm, 99,9%",
        raw_value_span_actual=(
            "[BdE deuda-aapp-junio26, 18/08/2026] 'la ratio de la deuda de las Administraciones Publicas (AAPP) "
            "segun el Protocolo de Deficit Excesivo (PDE) en relacion al Producto Interior Bruto (PIB) nominal se "
            "situo en el 101,5% en junio de 2026'; 'el saldo de deuda ascendio a 1.763 miles de millones (mm) de "
            "euros en junio de 2026'; 'tasa de crecimiento interanual del 4,2%' || [Tercera Informacion 2026-08-18, "
            "el claim] 'La deuda de las administraciones publicas (AAPP) se situo en el mes de junio en 1,76 billones "
            "de euros'; 'un 4,2% mas que en igual mes de 2025'; 'en porcentaje del Producto Interior Bruto (PIB) se "
            "modero hasta el 101,5%'"
        ),
        raw_value_span_anterior="[BdE deuda-aapp-marzo26, 19/05/2026] 'ascendio a 1.740 miles de millones (mm) de euros en marzo de 2026'; ratio 101,6%; interanual 4,3%",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor Banco de Espana (edicion junio 2026, primer caso; segundo caso BdE del conjunto tras "
            "E033), jornada 4, via busqueda a organismo. 1.763 mm = 1,76 billones; 4,2% y 101,5% son los de la nota: "
            "la referencia interanual es la del emisor, sin 2a. 'Nuevo maximo': 1.763 > 1.740 (marzo 2026, anterior "
            "maximo segun la prensa); el maximo sobre toda la serie mensual NO se comprueba aqui (serie DMNPDE2010 "
            "enlazada en la nota, NEEDS_REVIEW). 'Avance mensual del 1,9%' (mayo 2026) no se evalua. La nota enlaza "
            "notamet_pde.pdf, no abierto: methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="BdE deuda-aapp-junio26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Banco de España", tabla="deuda-aapp-junio26 / presbe2026-78.pdf",
                         serie_nombre="Deuda PDE de las AAPP, saldo (mm EUR)", unidad="mm EUR",
                         referencia_principal="interanual",
                         descripcion="Deuda de las AAPP segun el PDE, avance mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=1763, cambio_afirmado=4.2, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Tasa interanual dada por el emisor. El extremo ('nuevo maximo') no se evalua sobre la serie completa.",
        ),
    ),
    dict(
        cid="Q071",
        claim_text="Las comunidades autónomas aumentaron sus números rojos un 3,6% en el último año, sumando un total de 355.000 millones de euros en junio de 2026",
        claim_date="2026-08-18",
        post_url="https://www.catalunyapress.es/articulo/economia/2026-08-18/5986949-deuda-publica-pulveriza-maximo-historico-roza-176-billones-euros",
        post_url_tipo="prensa", emisor="Catalunya Press (Joaquín Carles)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="deuda",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda comunidades autónomas junio 2026 355.000 millones 3,6%",
        criba_query_b="deuda comunidades autónomas junio 2026 '355.000 millones' OR '355 mm' '3,6%' verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'deuda' junio 2026 '1,763' OR '1.763' OR '101,5%' 'Banco de España' récord agosto 2026 noticia comunidades OR '1,76 billones'",
        collected_at="2026-09-26", case_id="E062",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E062 t0 18:16Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual junio 2026: nota 18/08/2026 (subsector Comunidades Autonomas) + PDF presbe2026-78.pdf; edicion anterior: nota de marzo 2026",
        primaria_url="https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-junio26.html",
        primaria_url_tipo="nota_de_prensa_html (HTTP 200 al agente identificado) + PDF presbe2026-78.pdf",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="html",
        dato_actual="Comunidades Autonomas, junio 2026: 355 mm EUR, 20,4% del PIB, variacion interanual +3,6%",
        dato_anterior="AAPP marzo 2026: 1.740 mm (anterior maximo; 1763/1740 = +1,32%, el '1,3%' del articulo). Subsector CCAA de junio 2025: implicito en la tasa del emisor (355/1,036 = 342,7 mm), no leido de una nota",
        raw_value_span_actual=(
            "[BdE deuda-aapp-junio26, 18/08/2026] 'Comunidades Autonomas: 355 mm de euros en junio de 2026, "
            "equivalente a un 20,4% del PIB, con una variacion interanual del 3,6%' || [Catalunya Press 2026-08-18, "
            "el claim] 'Sus numeros rojos aumentaron un 3,6% en el ultimo ano, sumando un total de 355.000 millones "
            "de euros'; [mismo articulo] 'supera en un 1,3% el anterior maximo historico que se habia marcado el "
            "pasado mes de marzo'"
        ),
        raw_value_span_anterior="[BdE deuda-aapp-marzo26, 19/05/2026] 'ascendio a 1.740 miles de millones (mm) de euros en marzo de 2026'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor Banco de Espana (edicion junio 2026, segundo caso), jornada 4, via busqueda a "
            "organismo. 355 mm y +3,6% interanual son los del subsector CCAA de la nota: referencia del emisor, sin "
            "2a. Observacion, no anotada como claim: el mismo articulo compara con marzo 2026 ('supera en un 1,3% el "
            "anterior maximo'): 1763/1740 = +1,32%, cuadra; base elegida (marzo) frente a la interanual (+4,2%), "
            "mismo signo, magnitud 3,2x: senal de horizonte sobre un elemento secundario, se registra. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="BdE deuda-aapp-junio26",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Banco de España", tabla="deuda-aapp-junio26 / presbe2026-78.pdf",
                         serie_nombre="Deuda PDE, subsector Comunidades Autonomas (mm EUR)", unidad="mm EUR",
                         referencia_principal="interanual",
                         descripcion="Deuda de las CCAA segun el PDE, avance mensual"),
            periodo_objetivo="2026-M06", periodo_base="2025-M06",
            valor_objetivo=355, cambio_afirmado=3.6, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Tasa interanual dada por el emisor.",
        ),
    ),
    dict(
        cid="Q072",
        claim_text="Aldaia (Valencia) alcanza las 521 infracciones penales en el primer trimestre y registra un incremento del 79,7% respecto al mismo periodo de 2025",
        claim_date="2026-06-11",
        post_url="https://www.elperiodic.com/criminalidad-municipio-municipio-comunitat-valenciana-donde-suben-delitos-donde-caen_1079239",
        post_url_tipo="prensa", emisor="El Periòdic (Redacción)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com criminalidad Aldaia 2026 79,7%",
        criba_query_b="criminalidad Aldaia 'primer trimestre' 2026 '79,7%' OR '521' infracciones verificación OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="Portal Estadístico de Criminalidad 'primer trimestre' 2026 municipio criminalidad sube '%' Torrent OR Elche OR Alicante OR Gandia OR Castellón OR Sagunto OR Orihuela junio 2026",
        collected_at="2026-09-26", case_id="E063",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E063 t0 18:16Z) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 1T2026, tabla 09003 'Capitales de provincia, municipios mayores de 20.000 habitantes e islas', bloque '46021 Aldaia'",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAct/l0/09003.csv_c",
        primaria_url_tipo="CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (548.984 bytes, sha256 949be9399eb00fd4, descargado para E036 el 2026-09-26)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Aldaia, enero-marzo 2026: 521 infracciones penales (convencional 448; ciber 73); hurtos 228; variacion 2026/2025 +79,7% (columna del Portal)",
        dato_anterior="Aldaia, enero-marzo 2025: 290 (convencional 235; ciber 55; hurtos 87), columna 'enero-marzo 2025' de la misma tabla",
        raw_value_span_actual=(
            "[09003.csv_c, bloque '46021 Aldaia'] 'III. TOTAL INFRACCIONES PENALES,290,521,79,7,' | 'I. CRIMINALIDAD "
            "CONVENCIONAL,235,448,90,6,' | '8. Hurtos,87,228,162,1,' | 'II. CIBERCRIMINALIDAD (infracciones penales "
            "cometidas en/por medio ciber),55,73,32,7,' || [El Periodic 2026-06-11, el claim] 'Aldaia (Valencia)' "
            "'521 infracciones penales' 'incremento del 79,7%'"
        ),
        raw_value_span_anterior="[09003.csv_c, columna 'enero-marzo 2025'] 'III. TOTAL INFRACCIONES PENALES,290,521,79,7,'",
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta A, emisor Interior via Portal Estadistico (edicion 1T2026, tercer control: tope alcanzado; E028, "
            "E036), jornada 4, via busqueda a organismo. 521/290 - 1 = +79,7% = columna 'Variacion %' del Portal; base "
            "interanual = referencia del emisor, sin 2a. Contexto recogido por la prensa: el Ayuntamiento atribuye "
            "parte de la subida al centro comercial Bonaire (hurtos 87 -> 228); no es una verificacion del dato. "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="A", hermano_de="", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="Ministerio del Interior", tabla="09003 (Portal Estadistico, Balance 1T2026)",
                         serie_nombre="46021 Aldaia · III. TOTAL INFRACCIONES PENALES", unidad="hechos conocidos",
                         referencia_principal="interanual",
                         descripcion="Balance de criminalidad, infracciones penales, municipio de Aldaia, trimestral"),
            periodo_objetivo="2026-T1", periodo_base="2025-T1",
            valor_objetivo=521, cambio_afirmado=79.7, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Control Interior/Portal: base interanual = referencia del emisor.",
        ),
    ),
    dict(
        cid="Q073",
        claim_text="Aldaya Decidix alerta de que el municipio lidera el aumento de la criminalidad en la Comunitat Valenciana con una subida del 79,7%",
        claim_date="2026-06-12",
        post_url="https://www.elperiodicodeaqui.com/valencia/horta/aldaya-decidix-alerta-municipio-lidera-aumento-criminalidad-con-subida-797_100116916_102.html",
        post_url_tipo="declaracion", emisor="Aldaya Decidix (declaración recogida por El Periódico de Aquí)", emisor_tipo="partido_politico",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com criminalidad Aldaia 2026 79,7%",
        criba_query_b="Aldaia 'mayor subida' OR 'donde más sube' criminalidad 'Comunitat Valenciana' 2026 municipio verificación OR bulo OR fact-check OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="criminalidad Aldaia 'primer trimestre' 2026 '79,7%' OR '521' infracciones verificación OR bulo OR fact-check",
        collected_at="2026-09-26", case_id="E064",
        # --- trabajo 2026-09-26 (localizacion en lote 18:05-18:15Z; E064 t0 18:16Z) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 1T2026, tabla 09003: los 68 municipios de las provincias 03, 12 y 46 (capitales y mayores de 20.000 habitantes), fila 'III. TOTAL INFRACCIONES PENALES'",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAct/l0/09003.csv_c",
        primaria_url_tipo="CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (548.984 bytes, sha256 949be9399eb00fd4)",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Ranking recomputado sobre los 68 municipios valencianos de la tabla 09003 (variacion 1T2026/1T2025 del total de infracciones): 1 Aldaia +79,7% (290->521) | 2 Petrer +45,9% | 3 Picassent +45,6% | 4 Vinaros +30,5% | 5 Requena +29,2%",
        dato_anterior="Aldaia 1T2025: 290 infracciones (misma tabla). Media autonomica citada por el partido: +4,7% (Comunitat Valenciana en la tabla 09001, E028/E041)",
        raw_value_span_actual=(
            "[09003.csv_c, bloque '46021 Aldaia'] 'III. TOTAL INFRACCIONES PENALES,290,521,79,7,' | [bloque '03104 "
            "Petrer'] 'III. TOTAL INFRACCIONES PENALES,170,248,45,9,' | [bloque '46194 Picassent'] 'III. TOTAL "
            "INFRACCIONES PENALES,217,316,45,6,' || [El Periodico de Aqui 2026-06-12, el claim] 'el municipio "
            "encabeza el incremento de las infracciones penales en la Comunitat Valenciana' 'subida del 79,7%'; "
            "'hurtos, que se han disparado un 162,1%'"
        ),
        raw_value_span_anterior="[09003.csv_c, columna 'enero-marzo 2025'] 'III. TOTAL INFRACCIONES PENALES,290,521,79,7,'",
        truth="supported", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Cubeta D (ranking), emisor Interior via Portal Estadistico (edicion 1T2026; no cuenta como control), "
            "jornada 4, declaracion de partido (nivel 3) hallada en la criba (b) de E063. Ranking recomputado por el "
            "agente sobre los 68 municipios de la tabla 09003 con codigo 03/12/46: Aldaia es el primero con "
            "diferencia (siguiente Petrer +45,9%). Alcance del ranking: la tabla solo cubre capitales, municipios de "
            "mas de 20.000 habitantes e islas, no 'toda la Comunitat'; se anota como limitacion, no como error. La "
            "tasa 79,7% es la del emisor (E063). Sin test aplicable al ranking -> undetermined (DEC-029). "
            "methodology_found=no (NEEDS_REVIEW)."
        ),
        cubeta="D", hermano_de="E063", mecanismo_candidato="", primaria_edicion="Interior Balance 1T2026",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="otro",
            metrica=dict(emisor="Ministerio del Interior", tabla="09003 (Portal Estadistico, Balance 1T2026)",
                         serie_nombre="III. TOTAL INFRACCIONES PENALES, municipios de las provincias 03/12/46", unidad="hechos conocidos",
                         referencia_principal="interanual",
                         descripcion="Ranking de variacion interanual 1T2026 entre municipios valencianos de la tabla 09003"),
            periodo_objetivo="2026-T1", valor_objetivo=79.7,
            notas="Ranking ('lidera el aumento'): recomputado, cuadra. Sin test aplicable.",
        ),
    ),
    dict(
        cid="Q074",
        claim_text="Además, se registraron 57.049 pernoctaciones en apartamentos, un 1,3% más que en el mismo mes de 2025, y 9.493 en albergues, con un descenso del 14,2%, el único de los extrahoteleros [julio de 2026, Cantabria]",
        claim_date="2026-08-31",
        post_url="https://www.eldiario.es/cantabria/pernoctaciones-extrahoteleras-cantabria-crecen-4-1-julio-viajeros-4-3_1_13476308.html",
        post_url_tipo="prensa", emisor="elDiario.es Cantabria", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com Cantabria pernoctaciones extrahoteleras julio 2026 apartamentos 57.049",
        criba_query_b="Cantabria apartamentos julio 2026 '57.049' OR '111.666' pernoctaciones verificación OR bulo OR fact-check OR corrección",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="Cantabria campings julio 2026 pernoctaciones apartamentos turísticos extrahoteleras 'julio' INE noticia agosto 2026 crecen OR caen",
        collected_at="2026-09-27", case_id="E065",
        # --- trabajo 2026-09-27 (E065 t0 17:03Z; hallado al cotejar el articulo con la API en la busqueda de 2b) ---
        fuente_primaria="INE - EOAT julio 2026 (EOAT0726): API Tempus tabla 1993 (apartamentos turisticos; EOT1072 'Cantabria. Pernoctaciones. Total.') + anexo EOAT0726.xlsx (EOAP_Hoja1, fila 18); edicion de junio 2026 (EOAT0626, anexo fila 18) para localizar el periodo al que pertenece la cifra",
        primaria_url="https://www.ine.es/dyngs/Prensa/EOAT0726.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/1993 + anexos EOAT0726.xlsx y EOAT0626.xlsx (HTTP 200 al agente identificado, research/puerta3/edicion_anterior.py)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Cantabria, apartamentos turisticos, julio 2026: 111.666 pernoctaciones (API y anexo EOAT0726); julio 2025 vigente 113.353 -> -1,49%. Viajeros julio 2026: 27.600 (+6,43%), cifra que el articulo si da bien",
        dato_anterior="junio 2026: 57.049 pernoctaciones (API y anexo EOAT0626, fila 18); junio 2025 vigente 56.306 -> +1,32%: la cifra y la tasa del claim son las de JUNIO, no las de julio",
        raw_value_span_actual=(
            "[INE API tabla 1993] EOT1072 'Cantabria. Pernoctaciones. Total.' 2026-M07: 111666 | 2025-M07: 113353 | "
            "2026-M06: 57049 | 2025-M06: 56306 || [EOAT0726.xlsx, hoja EOAP_Hoja1, fila 18] 'Cantabria', 27600, 24791, "
            "2808, 111666, 101605, 10061, 4.05 || [elDiario.es Cantabria 2026-08-31, el claim] 'Ademas, se registraron "
            "57.049 pernoctaciones en apartamentos, un 1,3% mas que en el mismo mes de 2025, y 9.493 en albergues, "
            "con un descenso del 14,2%, el unico de los extrahoteleros'"
        ),
        raw_value_span_anterior=(
            "[EOAT0626.xlsx, hoja EOAP_Hoja1, fila 18] 'Cantabria', 22144, 19239, 2905, 57049, 50479, 6570, 2.58 || "
            "[Cronica de Cantabria 2026-07-31, articulo de JUNIO del mismo teletipo] '57.049 pernoctaciones en "
            "apartamentos, un 1,3% mas' | '9.493 en albergues, con un descenso del 14,2%'"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta C (2a, subtipo valor atribuido a otro periodo, DEC-029), jornada 4, hallado al cotejar el "
            "articulo de julio con la API durante la busqueda de 2b. El articulo de julio repite literalmente las "
            "frases de apartamentos y albergues del articulo de junio del mismo teletipo (57.049, +1,3%; 9.493, "
            "-14,2%): 57049/56306 - 1 = +1,32% es junio 2026 sobre junio 2025; julio 2026 es 111.666 (-1,49% sobre "
            "113.353). Las demas cifras del articulo (campings 488.109 +4%, viajeros en apartamentos 27.600 +6,4%) "
            "SI son de julio y cuadran con la base vigente. Numero rastreable al emisor pero de otro periodo: mixed + "
            "divergence_detected; el prototipo lo detecta con la ventana de 2a (valor de 2026-M06 atribuido a "
            "2026-M07). Albergues fuera del mapa (no se evalua). Segundo C del conjunto (E041). Segundo caso de "
            "EOAT0726 (E054 A). methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="C", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EOAT0726",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="1993",
                         serie_nombre="Cantabria. Pernoctaciones. Total.",
                         unidad="pernoctaciones", referencia_principal="interanual",
                         descripcion="EOAT, pernoctaciones en apartamentos turisticos, Cantabria, mensual"),
            periodo_objetivo="2026-M07", periodo_base="2025-M07",
            valor_objetivo=57049, cambio_afirmado=1.3, unidad_cambio="pct", direccion_afirmada="sube",
            notas="Valor atribuido a otro periodo: 57.049 y +1,3% son los de 2026-M06 (57049/56306); 2026-M07 es 111.666 (-1,49%). 2a, subtipo valor_atribuido_a_otro_periodo.",
        ),
    ),
    dict(
        cid="Q075",
        claim_text="Buen mayo para los apartamentos de la Región, que recibieron un 60% más de viajeros: llegaron a los 11.752 y acumularon 42.396 noches (+25%)",
        claim_date="2026-07-01",
        post_url="https://elnuevodigitalmurcia.es/art/8408/buen-mayo-para-los-apartamentos-de-la-region-que-recibieron-un-60-mas-de-viajeros",
        post_url_tipo="prensa", emisor="El Nuevo Digital Murcia (Nuevo Digital)", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="turismo",
        criba_query_a="site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com apartamentos turísticos Región de Murcia mayo 2026 viajeros 60%",
        criba_query_b="apartamentos turísticos Región de Murcia mayo 2026 '60%' OR '11.752' viajeros verificación OR bulo OR fact-check OR corrección",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="titular_prensa",
        descubrimiento_query="apartamentos turísticos mayo 2026 Murcia viajeros '60%' OR '60,2%' OR Cantabria campings mayo 2026 '19%' OR Aragón apartamentos mayo 2026 '48,8%' OR '65%' extrahoteleros noticia julio 2026",
        collected_at="2026-09-27", case_id="E066",
        # --- trabajo 2026-09-27 (E066 t0/t1/t2 17:2x-17:4xZ; via divergencia dirigida por la hipotesis 4d) ---
        fuente_primaria="INE - EOAT mayo 2026 (EOAT0526, publicada 2026-07-01): API Tempus tabla 1993 (EOT1117 viajeros, EOT1120 pernoctaciones; Region de Murcia) + anexo EOAT0526.xlsx (EOAP_Hoja1, fila 26); edicion anterior: anexo EOAT0525.xlsx (EOAP_Hoja1, fila 26; nota publicada 2025-07-01)",
        primaria_url="https://www.ine.es/dyngs/Prensa/EOAT0526.htm",
        primaria_url_tipo="nota_de_prensa_html + API JSON wstempus DATOS_TABLA/1993 + anexos EOAT0526.xlsx (HTTP 200, 158.771 bytes) y EOAT0525.xlsx (HTTP 200, 157.423 bytes) descargados con research/puerta3/edicion_anterior.py",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Region de Murcia, apartamentos turisticos, mayo 2026: 11.752 viajeros (8.454 residentes, 3.299 extranjeros); 42.396 pernoctaciones (API y anexo EOAT0526, fila 26)",
        dato_anterior="mayo 2025 vigente (API): viajeros 8.740 -> +34,46%; pernoctaciones 35.167 -> +20,56%. Mayo 2025 al publicar (anexo EOAT0525, provisional): viajeros 7.336 -> +60,20%; pernoctaciones 33.809 -> +25,40%",
        raw_value_span_actual=(
            "[INE API tabla 1993] EOT1117 'Murcia (Región de). Viajeros. Total.' 2026-M05: 11752 | EOT1120 'Murcia "
            "(Región de). Pernoctaciones. Total.' 2026-M05: 42396 || [EOAT0526.xlsx, hoja EOAP_Hoja1, fila 26] "
            "'Murcia, Región de', 11752, 8454, 3299, 42396, 31148, 11249, 3.61 || [El Nuevo Digital Murcia 2026-07-01, "
            "el claim] 'los apartamentos registraron una espectacular subida de usuarios, llegando a los 11.752, un "
            "60% mas'; 'que acumularon 42.396 noches (+25%)'"
        ),
        raw_value_span_anterior=(
            "[INE API tabla 1993, edicion vigente] EOT1117 2025-M05: 8740 | EOT1120 2025-M05: 35167 || "
            "[EOAT0525.xlsx, hoja EOAP_Hoja1, fila 26, edicion al publicar] 'Murcia, Región de', 7336, 6009, 1327, "
            "33809, 26508, 7301, 4.61"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2b_base_revisada", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Cubeta B (2b, base revisada, subtipo magnitud), jornada 4, via divergencia dirigida por la hipotesis 4d "
            "(la EOAT no trae la tasa por CCAA). 11752/7336 - 1 = +60,2% y 42396/33809 - 1 = +25,4% solo salen con la "
            "base PROVISIONAL de mayo 2025 (anexo EOAT0525, nota del 2025-07-01); con la vigente: +34,5% y +20,6%. "
            "Mismo signo: 2b sin cambio de signo. Los campings del mismo articulo ('13.257 usuarios, -19%') tambien "
            "cuadran con la provisional (13257/16320 = -18,8%; vigente -19,7%). Primer B fuera de la EOH, primer B "
            "de la jornada 4 y primer caso de la edicion EOAT0526; el articulo se publico el mismo dia que la nota "
            "del INE. La misma redaccion uso en julio (EOAT0726) una base sin revision (viajeros +15%, cuadra; "
            "pernoctaciones '+15%' frente a +17,5%, inexactitud no anotada) y solo totales extrahoteleros en junio. "
            "Los totales extrahoteleros del articulo (28.514 viajeros +2,6%; 128.429 noches -3,8%) agregan cuatro "
            "encuestas y no se evaluan. methodology_found=si: IME del INE, seccion 17 'Revision de datos' (pasada 2026-09-27, research/puerta3/METODOLOGIA-REVISION-INE.md)."
        ),
        cubeta="B", hermano_de="", mecanismo_candidato="", primaria_edicion="INE EOAT0526",
        conjunto="evaluacion", etiquetado_por="agente",
        estructura=dict(
            tipo="cambio_entre_periodos",
            metrica=dict(emisor="INE", tabla="1993",
                         serie_nombre="Murcia (Región de). Viajeros. Total.",
                         unidad="viajeros", referencia_principal="interanual",
                         descripcion="EOAT, viajeros en apartamentos turisticos, Region de Murcia, mensual"),
            periodo_objetivo="2026-M05", periodo_base="2025-M05",
            valor_objetivo=11752, cambio_afirmado=60, unidad_cambio="pct", direccion_afirmada="sube",
            evidencia_al_publicar=dict(
                valor=7336, edicion="INE EOAT0525 (mayo 2025, datos provisionales)", fecha="2025-07-01",
                url="https://www.ine.es/prensa/anexo_tablas/es/EOAT0525.xlsx",
                raw_value_span="[EOAT0525.xlsx, hoja EOAP_Hoja1, fila 26] 'Murcia, Región de', 7336, 6009, 1327, 33809, 26508, 7301, 4.61",
                verificacion="descarga 2026-09-27 con research/puerta3/edicion_anterior.py (HTTP 200, 157.423 bytes; fecha de la nota leida del HTML)",
            ),
            evidencia_vigente=dict(
                valor=8740, edicion="API Tempus, tabla 1993, edicion vigente", fecha="2026-09-26",
                url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/1993",
                raw_value_span="[INE API tabla 1993] 'Murcia (Región de). Viajeros. Total.' 2025-M05: 8740",
            ),
            notas="Base interanual correcta en periodo, tomada de la edicion provisional (7.336) y no de la vigente (8.740): 2b sin cambio de signo (+60,2% frente a +34,5%). Pernoctaciones: +25,4% provisional frente a +20,6% vigente.",
        ),
    ),
    # ---- jornada 5 (2026-09-30 local, 2026-10-01Z): controles A sin INE (BdE 2T2026 por CCAA, BdE mayo y julio 2026, Interior Balance 2025 anual) + un F. SEPE vetado por su robots.txt (User-agent: * Disallow: /*.pdf$) ----
    dict(
        cid='Q076',
        claim_text='Castilla-La Mancha reduce su deuda al 28,1 % del PIB, pero sigue entre las regiones más endeudadas de España',
        claim_date='2026-09-30',
        post_url='https://www.elespanol.com/eldigitalcastillalamancha/region/20260930/castilla-la-mancha-reduce-deuda-pib-sigue-regiones-endeudadas-espana/1003744403470_0.html',
        post_url_tipo="prensa", emisor='El Español (El Digital Castilla-La Mancha)', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda comunidades autónomas 2026 Banco de España Comunitat Valenciana 40% Murcia Castilla-La Mancha',
        criba_query_b="deuda Comunitat Valenciana 40% PIB segundo trimestre 2026 verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="Banco de España deuda comunidades autónomas segundo trimestre 2026 PIB nota | deuda 'segundo trimestre' 2026 comunidad Banco de España '% del PIB' Comunidad Valenciana OR Cataluña OR Murcia OR Castilla-La Mancha noticia 30 septiembre",
        collected_at="2026-09-30", case_id='E067',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE por CCAA, segundo trimestre 2026: nota 'La deuda de las Administraciones Publicas se situo en el 101,4% del PIB en el segundo trimestre de 2026' (30/09/2026) + Boletin Estadistico, cuadros 13.9 (importes, a1309.pdf) y 13.10 (% del PIB, a1310.pdf); edicion anterior de la base: nota 2T2025 (30/09/2025) y los mismos cuadros, fila 2025 II P (vigente)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/deuda-aapp-2026t2.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_2026t2.htm, sha256 c69644c7e451b9bb) + cuadros PDF a1309.pdf (200, sha256 da0148ca7c80ee35) y a1310.pdf (200, sha256 5974039dcfa8bb06); robots.txt de bde.es consultado antes de la primera peticion: solo prohibe dos xlsx',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual='Castilla-La Mancha, 2T2026: ratio deuda PDE/PIB 28,1% (a1310, fila 2026 II A, col. 8); importe 17.029 M EUR (a1309, misma fila)',
        dato_anterior='2T2025 vigente (a1310, fila 2025 II P): 29,3% -> -1,2 pp; importe 16.751 M (a1309). 2T2025 tal como se publico (nota BdE 30/09/2025): 28,5% -> con esa base la bajada seria de 0,4 pp, no de 1,2',
        raw_value_span_actual="[BdE deuda-aapp-2026t2, 30/09/2026] 'Comunidad Valenciana, que continua liderando con una ratio del 40%, seguida de la Region de Murcia (30,8%), Cataluna (28,1%) y Castilla-La Mancha (28,1%)' || [a1310.pdf, cuadro 13.10, fila '26 II A'] '20,4 18,2 17,4 12,5 17,8 10,9 17,2 28,1 18,3 28,1 19,2 15,0 16,4 12,3 30,8 8,4 11,7 40,0' (col. 8 = Castilla-La Mancha) || [El Espanol CLM 2026-09-30, el claim] 'Castilla-La Mancha reduce su deuda al 28,1 % del PIB'; 'reduccion de 1,2 puntos porcentuales en el ultimo ano'; 'segunda comunidad que mas rebajo este indicador, solo por detras de Navarra'",
        raw_value_span_anterior="[a1310.pdf, cuadro 13.10, fila '25 II P'] '20,9 19,0 18,5 13,5 18,6 11,3 18,3 29,3 19,1 29,2 19,9 15,3 16,4 12,1 30,5 10,0 11,4 39,8' (col. 8 = 29,3) || [BdE deuda-aapp-2025t2, 30/09/2025, tal como se publico] Castilla-La Mancha 28,5%",
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Banco de Espana (edicion 2T2026 por CCAA, primer caso), jornada 5, via busqueda a organismo. 29,3 - 28,1 = 1,2 pp con la base VIGENTE del cuadro 13.10; la ratio de 2T2025 tal como se publico en septiembre de 2025 era 28,5 (el BdE revisa ratios al revisar PIB y deuda), y con ella la bajada seria 0,4 pp: la redaccion uso la vigente, que es la referencia del emisor. Es el caso inverso de 2b, anotado como evidencia de que el patron no es automatico. 'Segunda que mas rebajo, tras Navarra': recomputado sobre a1310 (Navarra 10,0->8,4 = -1,6; CLM -1,2; Cantabria, Aragon y Cataluna -1,1): cuadra, pero el ranking no es un test del sistema y no se evalua. CLM24 (2026-09-30, 'La deuda de Castilla-La Mancha se situa en 17.029 millones, el 28,1 % del PIB', 29,3 -> 28,1) es la misma afirmacion: no se admite por el tope de tres por edicion. methodology_found=no: notamet_pde.pdf enlazado, no abierto (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='BdE deuda-ccaa-2026t2',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'a1310.pdf / cuadro 13.10', 'serie_nombre': 'Deuda PDE / PIB, Castilla-La Mancha (%)', 'unidad': 'pct_pib', 'referencia_principal': 'interanual', 'descripcion': 'Ratio de deuda PDE sobre PIB por CCAA, trimestral'}, 'periodo_objetivo': '2026-T2', 'periodo_base': '2025-T2', 'valor_objetivo': 28.1, 'cambio_afirmado': -1.2, 'unidad_cambio': 'pp', 'direccion_afirmada': 'baja', 'evidencia_al_publicar': {'valor': 28.5, 'edicion': 'BdE nota 2T2025 (30/09/2025)', 'fecha': '2025-09-30', 'url': 'https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-2025t2.html', 'raw_value_span': '[BdE deuda-aapp-2025t2] Castilla-La Mancha 28,5%', 'verificacion': 'leida el 2026-09-30 de la nota HTML del BdE'}, 'evidencia_vigente': {'valor': 29.3, 'edicion': 'BdE Boletin Estadistico cuadro 13.10, fila 2025 II P', 'fecha': '2026-09-30', 'url': 'https://www.bde.es/webbe/es/estadisticas/compartido/datos/pdf/a1310.pdf', 'raw_value_span': "[a1310.pdf, fila '25 II P', col. 8] 29,3"}, 'notas': 'La redaccion calcula con la base vigente (29,3): -1,2 pp. Con la base al publicar (28,5) la bajada seria de 0,4 pp, mismo signo. Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q077',
        claim_text='La deuda de la Comunitat Valenciana aumenta 3.897 millones en un año y alcanza los 64.593 millones, el 40% del PIB',
        claim_date='2026-09-30',
        post_url='https://valenciaplaza.com/valenciaplaza/bolsas/la-deuda-de-la-comunitat-valenciana-alcanza-el-40-del-pib-y-es-la-mas-elevada-de-espana',
        post_url_tipo="prensa", emisor='Valencia Plaza (Plaza/EFE)', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda comunidades autónomas 2026 Banco de España Comunitat Valenciana 40% Murcia Castilla-La Mancha',
        criba_query_b="deuda Comunitat Valenciana 40% PIB segundo trimestre 2026 verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="Banco de España deuda comunidades autónomas segundo trimestre 2026 PIB nota | deuda 'segundo trimestre' 2026 comunidad Banco de España '% del PIB' Comunidad Valenciana OR Cataluña OR Murcia OR Castilla-La Mancha noticia 30 septiembre",
        collected_at="2026-09-30", case_id='E068',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE por CCAA, segundo trimestre 2026: nota 'La deuda de las Administraciones Publicas se situo en el 101,4% del PIB en el segundo trimestre de 2026' (30/09/2026) + Boletin Estadistico, cuadros 13.9 (importes, a1309.pdf) y 13.10 (% del PIB, a1310.pdf); edicion anterior de la base: nota 2T2025 (30/09/2025) y los mismos cuadros, fila 2025 II P (vigente)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/deuda-aapp-2026t2.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_2026t2.htm, sha256 c69644c7e451b9bb) + cuadros PDF a1309.pdf (200, sha256 da0148ca7c80ee35) y a1310.pdf (200, sha256 5974039dcfa8bb06); robots.txt de bde.es consultado antes de la primera peticion: solo prohibe dos xlsx',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual='Comunitat Valenciana, 2T2026: 64.593 M EUR (a1309, fila 2026 II A, col. 18); ratio 40,0% (a1310)',
        dato_anterior='2T2025 vigente: 60.696 M (a1309, fila 2025 II P) -> +3.897 M (+6,42%); ratio 39,8% -> +0,2 pp. 2T2025 tal como se publico (nota 30/09/2025): 39,9% -> +0,1 pp',
        raw_value_span_actual="[a1309.pdf, cuadro 13.9, fila '26 II A'] '355 241 42 070 9 407 4 095 8 691 6 897 3 325 17 029 14 778 92 770 5 570 13 357 1 986 42 296 14 254 2 446 11 679 64 593' (col. 18 = Comunitat Valenciana) || [BdE deuda-aapp-2026t2, 30/09/2026] 'Comunidad Valenciana, que continua liderando con una ratio del 40%' || [Valencia Plaza 2026-09-30, el claim] 'aumenta 3.897 millones en un ano y alcanza los 64.593 millones, el 40% del PIB'; 'dos decimas mas que hace un ano'",
        raw_value_span_anterior="[a1309.pdf, fila '25 II P', col. 18] 60 696 || [a1310.pdf, fila '25 II P', col. 18] 39,8 || [BdE deuda-aapp-2025t2, 30/09/2025] Comunidad Valenciana 39,9%",
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Banco de Espana (edicion 2T2026 por CCAA, segundo caso), jornada 5, via busqueda a organismo. 64593 - 60696 = 3.897 exacto con la base vigente del cuadro 13.9; 40,0 - 39,8 = 0,2 pp, tambien vigente (al publicar, 39,9: seria 0,1 pp). 'La mas elevada de Espana': maximo de a1310 fila 2026 II A, cuadra; ranking no evaluado. El mismo dia, Diario de Alicante ('Deuda Comunitat Valenciana: 40% del PIB y la mayor de Espana') y Actualidad Castellon ('se dispara al 40 %') dan nivel y ranking sin comparacion propia: no se admiten (serian D) y ambos repiten el '+3,8%' de EFE para el total de CCAA (ver E075). methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='BdE deuda-ccaa-2026t2',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'a1309.pdf / cuadro 13.9', 'serie_nombre': 'Deuda PDE, Comunitat Valenciana (millones EUR)', 'unidad': 'millones EUR', 'referencia_principal': 'interanual', 'descripcion': 'Deuda PDE por CCAA, importes, trimestral'}, 'periodo_objetivo': '2026-T2', 'periodo_base': '2025-T2', 'valor_objetivo': 64593, 'cambio_afirmado': 3897, 'unidad_cambio': 'abs', 'direccion_afirmada': 'sube', 'evidencia_vigente': {'valor': 60696, 'edicion': 'BdE Boletin Estadistico cuadro 13.9, fila 2025 II P', 'fecha': '2026-09-30', 'url': 'https://www.bde.es/webbe/es/estadisticas/compartido/datos/pdf/a1309.pdf', 'raw_value_span': "[a1309.pdf, fila '25 II P', col. 18] 60 696"}, 'notas': 'Diferencia absoluta con la base vigente. Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q078',
        claim_text='La Región de Murcia ya es la segunda comunidad más endeudada de España',
        claim_date='2026-09-30',
        post_url='https://murciaplaza.com/murciaplaza/region/la-region-de-murcia-ya-es-la-segunda-comunidad-mas-endeudada-de-espana',
        post_url_tipo="prensa", emisor='Murcia Plaza', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda comunidades autónomas 2026 Banco de España Comunitat Valenciana 40% Murcia Castilla-La Mancha',
        criba_query_b="deuda Comunitat Valenciana 40% PIB segundo trimestre 2026 verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="Banco de España deuda comunidades autónomas segundo trimestre 2026 PIB nota | deuda 'segundo trimestre' 2026 comunidad Banco de España '% del PIB' Comunidad Valenciana OR Cataluña OR Murcia OR Castilla-La Mancha noticia 30 septiembre",
        collected_at="2026-09-30", case_id='E069',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE por CCAA, segundo trimestre 2026: nota 'La deuda de las Administraciones Publicas se situo en el 101,4% del PIB en el segundo trimestre de 2026' (30/09/2026) + Boletin Estadistico, cuadros 13.9 (importes, a1309.pdf) y 13.10 (% del PIB, a1310.pdf); edicion anterior de la base: nota 2T2025 (30/09/2025) y los mismos cuadros, fila 2025 II P (vigente)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/deuda-aapp-2026t2.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_2026t2.htm, sha256 c69644c7e451b9bb) + cuadros PDF a1309.pdf (200, sha256 da0148ca7c80ee35) y a1310.pdf (200, sha256 5974039dcfa8bb06); robots.txt de bde.es consultado antes de la primera peticion: solo prohibe dos xlsx',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual='Region de Murcia, 2T2026: 14.254 M EUR (a1309, fila 2026 II A, col. 15); ratio 30,8% (a1310)',
        dato_anterior='1T2026 (a1309, fila 2026 I A): 14.167 M -> +87 M (+0,61%); ratio 31,0% (a1310, fila 2026 I A). 2024 (a1309, fila 24): 13.513 M -> +741 M. 2T2025 vigente: 13.317 M; 30,5%',
        raw_value_span_actual="[a1309.pdf, cuadro 13.9, fila '26 II A', col. 15] 14 254 || [a1310.pdf, cuadro 13.10, fila '26 II A', col. 15] 30,8 || [BdE deuda-aapp-2026t2, 30/09/2026] 'seguida de la Region de Murcia (30,8%)' || [Murcia Plaza 2026-09-30, el claim] '14.254 millones de euros'; '30,8%'; 14.167 millones en el primer trimestre de 2026, incremento de 87 millones; 13.513 millones en 2024, aumento de 741 millones",
        raw_value_span_anterior="[a1309.pdf, fila '26 I A', col. 15] 14 167 || [a1309.pdf, fila '24', col. 15] 13 513 || [a1310.pdf, fila '26 I A', col. 15] 31,0",
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Banco de Espana (edicion 2T2026 por CCAA, tercer caso: la edicion llega al tope), jornada 5, via busqueda a organismo. 14254 - 14167 = 87 (trimestral, la comparacion que hace la pieza) y 14254 - 13513 = 741 (frente al cierre de 2024): las dos cuadran con los cuadros vigentes. 'Segunda mas endeudada' (ratio): a1310 fila 2026 II A, Comunitat Valenciana 40,0 y Murcia 30,8, siguiente 28,1: cuadra; 'ya es' sugiere cambio de posicion, pero Murcia era segunda tambien en 1T2026 (31,0 frente a 27,8) y en 4T2025: inexactitud retorica, no se anota. Ranking no evaluado como test. Empresas de Cartagena y Murcia Diario (mismo dia) dan la ratio como '30%' y 'roza el 31%' sin comparacion propia: no se admiten. methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='BdE deuda-ccaa-2026t2',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'a1309.pdf / cuadro 13.9', 'serie_nombre': 'Deuda PDE, Region de Murcia (millones EUR)', 'unidad': 'millones EUR', 'referencia_principal': 'trimestral', 'descripcion': 'Deuda PDE por CCAA, importes, trimestral'}, 'periodo_objetivo': '2026-T2', 'periodo_base': '2026-T1', 'valor_objetivo': 14254, 'cambio_afirmado': 87, 'unidad_cambio': 'abs', 'direccion_afirmada': 'sube', 'evidencia_vigente': {'valor': 14167, 'edicion': 'BdE Boletin Estadistico cuadro 13.9, fila 2026 I A', 'fecha': '2026-09-30', 'url': 'https://www.bde.es/webbe/es/estadisticas/compartido/datos/pdf/a1309.pdf', 'raw_value_span': "[a1309.pdf, fila '26 I A', col. 15] 14 167"}, 'notas': 'La pieza compara con el trimestre anterior (referencia explicita). Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q079',
        claim_text='Deuda pública España se modera al 100,2% del PIB en mayo, hasta 1,72 billones',
        claim_date='2026-07-18',
        post_url='https://www.merca2.es/2026/07/18/deuda-publica-espana-mayo-1002-pib-2419875/',
        post_url_tipo="prensa", emisor='Merca2', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública mayo 2026 100,2% PIB Banco de España',
        criba_query_b="deuda pública mayo 2026 '100,2%' verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="deuda mayo 2026 Banco de España 'mayo' administraciones públicas '% del PIB' comunidad noticia julio 2026",
        collected_at="2026-09-30", case_id='E070',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual mayo 2026: nota 'La deuda de las Administraciones Publicas se situo en mayo de 2026 en el 100,2% del PIB' (17/07/2026); ediciones anteriores: abril 2026 y mayo 2025 (la nota da la tasa interanual y la diferencia en pp)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-mayo26.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_mayo26.htm, sha256 e3c6a62bec192349); PDF de la nota no abierto',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual='mayo 2026: saldo deuda PDE AAPP 1.729 mm EUR; ratio 100,2% del PIB; tasa interanual +4%; CCAA 343 mm (19,9%), +2,1%',
        dato_anterior='mayo 2025: ratio 102,2% (la nota: 2 pp menos); saldo implicito 1.729/1,04 = 1.663 mm. Marzo 2026 (maximo citado por la pieza): 1.739 mm',
        raw_value_span_actual="[BdE deuda-aapp-mayo26, 17/07/2026] 'se situo en mayo de 2026 en el 100,2% del PIB, 2 puntos porcentuales (pp) menos que en el mismo periodo del ano anterior'; '1.729 miles de millones (mm) de euros en mayo de 2026, con una tasa de crecimiento interanual del 4%'; 'La deuda de las CCAA ... 343 mm de euros en mayo de 2026, equivalente a un 19,9% del PIB, con una variacion interanual del 2,1%' || [Merca2 2026-07-18, el claim] '100,2%'; '1,729 billones de euros'; 'crecimiento interanual del 4%'; 'cayo un 0,58% desde el maximo historico de marzo (1,739 billones)'; 'comunidades autonomas deben 343.000 millones de euros (19,9% del PIB), tras crecer un 2,1%'",
        raw_value_span_anterior='[BdE deuda-aapp-mayo26] tasa interanual del 4% y 2 pp menos que en mayo de 2025 (la nota no imprime el saldo de mayo de 2025)',
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Banco de Espana (edicion mayo 2026, primer caso), jornada 5, via busqueda a organismo. 1.729 mm = 1,729 billones; 100,2%, +4% y el desglose por subsectores son los de la nota: referencia interanual del emisor, sin 2a. 'Cayo un 0,58% desde el maximo de marzo': 1729/1739 - 1 = -0,575%, cuadra con la nota de marzo (E061 cita 1.740 en la nota de marzo; la pieza usa 1.739: diferencia de redondeo, no anotada). methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='BdE deuda-aapp-mayo26',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'deuda-aapp-mayo26', 'serie_nombre': 'Deuda PDE de las AAPP, saldo (mm EUR)', 'unidad': 'mm EUR', 'referencia_principal': 'interanual', 'descripcion': 'Deuda de las AAPP segun el PDE, avance mensual'}, 'periodo_objetivo': '2026-M05', 'periodo_base': '2025-M05', 'valor_objetivo': 1729, 'cambio_afirmado': 4.0, 'unidad_cambio': 'pct', 'direccion_afirmada': 'sube', 'notas': 'Tasa interanual dada por el emisor. Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q080',
        claim_text='La deuda pública en España baja al 100,2% del PIB en mayo 2026: ¿qué significa para la economía?',
        claim_date='2026-07-26',
        post_url='https://www.elconfidencialdigital.com/articulo/dinero/deuda-publica-espana-baja-1002-pib-mayo-2026-que-significa-economia/202607261409141033146.html',
        post_url_tipo="prensa", emisor='El Confidencial Digital', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública mayo 2026 100,2% PIB Banco de España',
        criba_query_b="deuda pública mayo 2026 '100,2%' verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="deuda mayo 2026 Banco de España 'mayo' administraciones públicas '% del PIB' comunidad noticia julio 2026",
        collected_at="2026-09-30", case_id='E071',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual mayo 2026: nota 'La deuda de las Administraciones Publicas se situo en mayo de 2026 en el 100,2% del PIB' (17/07/2026); ediciones anteriores: abril 2026 y mayo 2025 (la nota da la tasa interanual y la diferencia en pp)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-mayo26.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_mayo26.htm, sha256 e3c6a62bec192349); PDF de la nota no abierto',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual='mayo 2026: ratio deuda PDE/PIB 100,2%; saldo 1.729 mm EUR (la pieza: 1,72 billones)',
        dato_anterior='mayo 2025: 102,2% (nota: 2 pp menos)',
        raw_value_span_actual="[BdE deuda-aapp-mayo26, 17/07/2026] 'se situo en mayo de 2026 en el 100,2% del PIB, 2 puntos porcentuales (pp) menos que en el mismo periodo del ano anterior' || [El Confidencial Digital 2026-07-26, el claim] 'se situo en mayo de 2026 en 1,72 billones de euros'; 'representando el 100,2% del PIB'; 'descenso de 2 puntos porcentuales respecto al mismo mes del ano anterior'",
        raw_value_span_anterior='[BdE deuda-aapp-mayo26] 2 pp menos que en mayo de 2025',
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Banco de Espana (edicion mayo 2026, segundo caso), jornada 5, via busqueda a organismo; hermano de E070 (misma primaria y misma consulta, redaccion distinta ocho dias despues). 100,2% y -2 pp son los de la nota; '1,72 billones' redondea 1.729 mm (tolerancia). Desglose por administraciones identico al de la nota, no anotado. methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='E070', mecanismo_candidato="", primaria_edicion='BdE deuda-aapp-mayo26',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'deuda-aapp-mayo26', 'serie_nombre': 'Deuda PDE de las AAPP / PIB (%)', 'unidad': 'pct_pib', 'referencia_principal': 'interanual', 'descripcion': 'Ratio de deuda PDE de las AAPP sobre PIB, avance mensual'}, 'periodo_objetivo': '2026-M05', 'periodo_base': '2025-M05', 'valor_objetivo': 100.2, 'cambio_afirmado': -2.0, 'unidad_cambio': 'pp', 'direccion_afirmada': 'baja', 'notas': 'Diferencia en pp dada por el emisor. Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q081',
        claim_text='Castilla y León lidera la criminalidad en 2025, mientras que en Cataluña y Madrid es donde más caen los delitos',
        claim_date='2026-02-28',
        post_url='https://www.diariosigloxxi.com/texto-ep/mostrar/20260228100030/castilla-leon-lidera-criminalidad-2025-mientras-cataluna-madrid-donde-caen-delitos',
        post_url_tipo="prensa", emisor='Diario Siglo XXI (Europa Press)', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='criminalidad',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com criminalidad 2025 balance Interior Castilla y León 5,8% Canarias comunidades',
        criba_query_b="criminalidad 2025 'Castilla y León' lidera 5,8% balance verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'balance de criminalidad' 2025 anual comunidad 'infracciones penales' 2025 'respecto a 2024' noticia marzo 2026 Castilla y León OR Andalucía OR Comunitat Valenciana OR Canarias",
        collected_at="2026-09-30", case_id='E073',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 2025 4T (enero-diciembre 2025), tabla 1509010 'Comunidades y Ciudades Autonomas' (DatosBalanceAnt), fila 'III. TOTAL INFRACCIONES PENALES' con columnas enero-diciembre 2024, enero-diciembre 2025 y variacion %",
        primaria_url='https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAnt/l0/1509010.csv_c',
        primaria_url_tipo='CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (25.286 bytes, ISO-8859-15, sha256 92a6d23332de66cc; copia research/evidencia/J5_portal_4T2025_1509010.csv). El dominio no sirve robots.txt (redirige a la aplicacion y a error/404)',
        via_de_acceso='dataset', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='dataset',
        dato_actual='Castilla y Leon, enero-diciembre 2025: 96.625 infracciones penales; variacion 2025/2024 +5,8% (columna del Portal). Cataluna 495.742 (-2,9%); Madrid 392.168 (-1,7%); total nacional 2.474.156 (+0,8%)',
        dato_anterior='Castilla y Leon, enero-diciembre 2024: 91.335 (misma tabla) -> 96625/91335 - 1 = +5,79%. Cataluna 510.499; Madrid 399.088; nacional 2.454.206',
        raw_value_span_actual="[1509010.csv_c, Balance 2025 4T, bloque CASTILLA Y LEON] 'III. TOTAL INFRACCIONES PENALES,91.335,96.625,5,8' || [bloque CATALUNA] '510.499,495.742,-2,9' || [bloque MADRID (COMUNIDAD DE)] '399.088,392.168,-1,7' || [bloque TOTAL NACIONAL] '2.454.206,2.474.156,0,8' || [Diario Siglo XXI / EP 2026-02-28, el claim] 'Castilla y Leon (+5,8%) es la comunidad autonoma que lidera el aumento de la criminalidad'; 'Baleares (+5,6%) y Asturias (+5,4%)'; 'Cataluna (-2,9%) y Comunidad de Madrid (-1,7%)'; 'En 2025 la criminalidad ha vuelto a repuntar un 0,8%'",
        raw_value_span_anterior="[1509010.csv_c, columna 'enero-diciembre 2024'] Castilla y Leon 91.335",
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Ministerio del Interior via Portal (edicion Balance 2025 anual, primer caso; 1T2026 esta al tope y 2T2026 vetado por DEC-025), jornada 5, via busqueda a organismo. +5,8% es la columna de variacion del Portal y 96625/91335 la reproduce; la referencia anual es la del emisor, sin 2a. 'Lidera el aumento': maximo de la columna entre las 17 CCAA (CyL 5,8; Baleares 5,6; Asturias 5,4) y 'donde mas caen' (Cataluna -2,9; Madrid -1,7; luego Melilla -0,8, que es ciudad autonoma; 'En el extranjero' -12,4 no es territorio): cuadran, pero el ranking no es un test y no se evalua. Infobae y Teleprensa publican el mismo teletipo de EP: no se admiten (hermanos). methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='Interior Balance 2025 anual',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Ministerio del Interior', 'tabla': 'Portal Estadistico de Criminalidad, Balance 2025 4T, tabla 1509010', 'serie_nombre': 'Infracciones penales, Castilla y Leon (hechos conocidos)', 'unidad': 'infracciones', 'referencia_principal': 'interanual', 'descripcion': 'Total de infracciones penales por CCAA, acumulado enero-diciembre'}, 'periodo_objetivo': '2025', 'periodo_base': '2024', 'valor_objetivo': 96625, 'cambio_afirmado': 5.8, 'unidad_cambio': 'pct', 'direccion_afirmada': 'sube', 'notas': 'El nivel (96.625) no esta en la pieza; se toma de la primaria para el test. La pieza afirma solo la tasa y el ranking.'},
    ),
    dict(
        cid='Q082',
        claim_text='La criminalidad aumenta un 3,1% en Canarias en 2025, según el balance del Ministerio del Interior',
        claim_date='2026-02-28',
        post_url='https://radioinsular.es/la-criminalidad-aumenta-un-31-en-canarias-en-2025-segun-el-balance-del-ministerio-del-interior/',
        post_url_tipo="prensa", emisor='Radio Insular', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='criminalidad',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com criminalidad 2025 balance Interior Castilla y León 5,8% Canarias comunidades',
        criba_query_b="criminalidad 2025 'Castilla y León' lidera 5,8% balance verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="'balance de criminalidad' 2025 anual comunidad 'infracciones penales' 2025 'respecto a 2024' noticia marzo 2026 Castilla y León OR Andalucía OR Comunitat Valenciana OR Canarias",
        collected_at="2026-09-30", case_id='E074',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Ministerio del Interior - Portal Estadistico de Criminalidad, Balance 2025 4T (enero-diciembre 2025), tabla 1509010 'Comunidades y Ciudades Autonomas' (DatosBalanceAnt), fila 'III. TOTAL INFRACCIONES PENALES' con columnas enero-diciembre 2024, enero-diciembre 2025 y variacion %",
        primaria_url='https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_c/DatosBalanceAnt/l0/1509010.csv_c',
        primaria_url_tipo='CSV (jaxiPx) del Portal Estadistico; HTTP 200 al agente identificado (25.286 bytes, ISO-8859-15, sha256 92a6d23332de66cc; copia research/evidencia/J5_portal_4T2025_1509010.csv). El dominio no sirve robots.txt (redirige a la aplicacion y a error/404)',
        via_de_acceso='dataset', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='dataset',
        dato_actual='Canarias, enero-diciembre 2025: 110.325 infracciones penales; variacion 2025/2024 +3,1% (columna del Portal); nacional 2.474.156 (+0,8%)',
        dato_anterior='Canarias, enero-diciembre 2024: 106.985 -> 110325/106985 - 1 = +3,12%',
        raw_value_span_actual="[1509010.csv_c, Balance 2025 4T, bloque CANARIAS] 'III. TOTAL INFRACCIONES PENALES,106.985,110.325,3,1' || [bloque TOTAL NACIONAL] '2.454.206,2.474.156,0,8' || [Radio Insular 2026-02-28, el claim] 'La criminalidad aumenta un 3,1% en Canarias en 2025'; '2.474.156 infracciones penales'; '489.248 ciberdelitos en 2025 (19,8% del total)'; 'aumento del 5,3% en cibercriminalidad'",
        raw_value_span_anterior="[1509010.csv_c, columna 'enero-diciembre 2024'] Canarias 106.985",
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='control_negativo', excedente="no",
        notas="Cubeta A, emisor Ministerio del Interior via Portal (edicion Balance 2025 anual, segundo caso), jornada 5, via busqueda a organismo. +3,1% es la columna del Portal y 110325/106985 la reproduce. Las cifras nacionales de ciberdelitos (489.248; 19,8%; +5,3%) estan en la misma tabla (bloque TOTAL NACIONAL, filas de cibercriminalidad) y no se anotan como claim. 'Entre las comunidades con mayor incremento': Canarias es novena de 17 en la columna de variacion (5,8; 5,6; 5,4; 4,9; 4,7; 4,6; 3,3; 3,3; 3,1): la afirmacion es vaga, no es un test y no se evalua. Tiempo de Canarias publico una pieza equivalente cuya URL redirige a la portada (no recuperable). methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='', mecanismo_candidato="", primaria_edicion='Interior Balance 2025 anual',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Ministerio del Interior', 'tabla': 'Portal Estadistico de Criminalidad, Balance 2025 4T, tabla 1509010', 'serie_nombre': 'Infracciones penales, Canarias (hechos conocidos)', 'unidad': 'infracciones', 'referencia_principal': 'interanual', 'descripcion': 'Total de infracciones penales por CCAA, acumulado enero-diciembre'}, 'periodo_objetivo': '2025', 'periodo_base': '2024', 'valor_objetivo': 110325, 'cambio_afirmado': 3.1, 'unidad_cambio': 'pct', 'direccion_afirmada': 'sube', 'notas': 'El nivel (110.325) no esta en la pieza; se toma de la primaria para el test.'},
    ),
    dict(
        cid='Q083',
        claim_text='La deuda de CCAA baja al 20,4 % del PIB en segundo trimestre pero el importe marca récord',
        claim_date='2026-09-30',
        post_url='https://www.infobae.com/espana/agencias/2026/09/30/la-deuda-de-ccaa-baja-al-204-del-pib-en-segundo-trimestre-pero-el-importe-marca-record/',
        post_url_tipo="prensa", emisor='Infobae (EFE)', emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda comunidades autónomas 2026 Banco de España Comunitat Valenciana 40% Murcia Castilla-La Mancha',
        criba_query_b="deuda Comunitat Valenciana 40% PIB segundo trimestre 2026 verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
        descubrimiento_via="busqueda_a_organismo",
        descubrimiento_query="Banco de España deuda comunidades autónomas segundo trimestre 2026 PIB nota | deuda 'segundo trimestre' 2026 comunidad Banco de España '% del PIB' Comunidad Valenciana OR Cataluña OR Murcia OR Castilla-La Mancha noticia 30 septiembre",
        collected_at="2026-09-30", case_id='E075',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5; localizacion en lote 00:49-00:55Z; t0 00:52Z) ---
        fuente_primaria="Banco de Espana - Deuda PDE por CCAA, segundo trimestre 2026: nota 'La deuda de las Administraciones Publicas se situo en el 101,4% del PIB en el segundo trimestre de 2026' (30/09/2026) + Boletin Estadistico, cuadros 13.9 (importes, a1309.pdf) y 13.10 (% del PIB, a1310.pdf); edicion anterior de la base: nota 2T2025 (30/09/2025) y los mismos cuadros, fila 2025 II P (vigente)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/deuda-aapp-2026t2.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_2026t2.htm, sha256 c69644c7e451b9bb) + cuadros PDF a1309.pdf (200, sha256 da0148ca7c80ee35) y a1310.pdf (200, sha256 5974039dcfa8bb06); robots.txt de bde.es consultado antes de la primera peticion: solo prohibe dos xlsx',
        via_de_acceso='html', access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato='html',
        dato_actual="Total CCAA, 2T2026: 355.241 M EUR (a1309, fila 2026 II A, col. 1); ratio 20,4% (a1310); la nota del BdE: 'crecimiento interanual del 3,6%'",
        dato_anterior="2T2025 vigente: 342.799 M (a1309, fila 2025 II P) -> 355241/342799 - 1 = +3,63%; ratio 20,9% -> -0,5 pp. 2T2025 tal como se publico (nota 30/09/2025): '343 mm de euros (21% del PIB)' -> 355241/343000 - 1 = +3,57%. Ninguna base conocida da +3,8% (haria falta 342.236 M)",
        raw_value_span_actual="[BdE deuda-aapp-2026t2, 30/09/2026] 'La deuda de las Comunidades Autonomas (CCAA) ... 355 mm de euros (20,4% del PIB), con un crecimiento interanual del 3,6%' || [a1309.pdf, cuadro 13.9, fila '26 II A', col. 1] 355 241 || [a1310.pdf, fila '26 II A', col. 1] 20,4 || [Infobae / EFE 2026-09-30, el claim] 'La deuda de las comunidades autonomas bajo al 20,4 % del PIB en el segundo trimestre, 5 decimas menos que un ano antes, pero con un importe record de 355.241 millones de euros, un 3,8 % mas que en el mismo trimestre del ano anterior'",
        raw_value_span_anterior="[a1309.pdf, fila '25 II P', col. 1] 342 799 || [a1310.pdf, fila '25 II P', col. 1] 20,9 || [BdE deuda-aapp-2025t2, 30/09/2025] 'la deuda de las Comunidades Autonomas (CCAA) segun el PDE fue de 343 mm de euros (21% del PIB), con un crecimiento interanual del 1,6%'",
        truth='contradicted', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado='claim_falso', excedente="no",
        notas="Cubeta F (claim falso por la regla de tolerancia), emisor Banco de Espana (edicion 2T2026 por CCAA; cuarto caso de la edicion, pero F no cuenta para el tope de controles), jornada 5, hallado al cotejar la pieza de EFE. El importe (355.241), la ratio (20,4) y las 5 decimas (20,9 -> 20,4, base vigente) cuadran; la tasa interanual del importe NO: el emisor publica +3,6% y los cuadros dan +3,63% (vigente) o +3,57% (base tal como se publico); la pieza dice +3,8%. Diferencia 0,17 pp sobre una tasa con un decimal: tolerancia_para(3.8, 3.63) = 0,05, asi que truth=contradicted. No es 2a (la referencia es la del emisor) ni 2b (ninguna edicion de la base reproduce 3,8): se registra como inexactitud de origen no identificado; la hipotesis de que EFE copiara el '+3,8%' de la deuda total de las AAPP de julio (E033) es especulacion y no se anota como hecho. 'Importe record': 355.241 es el maximo de la columna 1 del cuadro 13.9 (anterior 346.929, 1T2026), cuadra, no evaluado. Actualidad Castellon y Murcia Diario repiten el '+3,8%' el mismo dia (hermanos de este teletipo, no admitidos). Decision de Mateo (2026-09-30): se queda como F, contradicted. La tolerancia (0,05 pp: media unidad del ultimo decimal del claim, minimo 0,5% del valor) se fijo antes de medir y no se mueve para acomodar un caso; la diferencia observada, 0,17 pp, triplica el limite y aun asi se deja constancia de que es la contradiccion mas pequena del conjunto.",
        cubeta='F', hermano_de='', mecanismo_candidato="", primaria_edicion='BdE deuda-ccaa-2026t2',
        conjunto="evaluacion", etiquetado_por="agente",
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'a1309.pdf / cuadro 13.9', 'serie_nombre': 'Deuda PDE, total Comunidades Autonomas (millones EUR)', 'unidad': 'millones EUR', 'referencia_principal': 'interanual', 'descripcion': 'Deuda PDE del conjunto de CCAA, importes, trimestral'}, 'periodo_objetivo': '2026-T2', 'periodo_base': '2025-T2', 'valor_objetivo': 355241, 'cambio_afirmado': 3.8, 'unidad_cambio': 'pct', 'direccion_afirmada': 'sube', 'evidencia_al_publicar': {'valor': 343000, 'edicion': "BdE nota 2T2025 (30/09/2025), '343 mm'", 'fecha': '2025-09-30', 'url': 'https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-2025t2.html', 'raw_value_span': "[BdE deuda-aapp-2025t2] 'fue de 343 mm de euros (21% del PIB)'", 'verificacion': 'leida el 2026-09-30 de la nota HTML del BdE; redondeada a mm por el emisor'}, 'evidencia_vigente': {'valor': 342799, 'edicion': 'BdE Boletin Estadistico cuadro 13.9, fila 2025 II P', 'fecha': '2026-09-30', 'url': 'https://www.bde.es/webbe/es/estadisticas/compartido/datos/pdf/a1309.pdf', 'raw_value_span': "[a1309.pdf, fila '25 II P', col. 1] 342 799"}, 'notas': '+3,8% no se reproduce con la base vigente (+3,63%) ni con la base al publicar (+3,57%). Contradicted en la tasa; importe y ratio correctos.'},
    ),
    # ---- jornada 5, sesion 2 (2026-10-01Z): los dos A que faltaban para 40, con la nota de julio 2026 del BdE (tope de la edicion) ----
    dict(
        cid='Q084',
        claim_text='La deuda pública cae en julio por debajo del 100% por primera vez desde febrero de 2020, antes de la pandemia',
        claim_date='2026-09-17',
        post_url='https://forbes.es/ultima-hora/1022211/la-deuda-publica-cae-en-julio-por-debajo-del-100-por-primera-vez-desde-febrero-de-2020-antes-de-la-pandemia/',
        post_url_tipo='prensa', emisor='Forbes España (Europa Press)', emisor_tipo='prensa_digital',
        emisor_nivel=1, pais='ES', tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública julio 2026 99,9% Banco de España',
        criba_query_b="deuda pública julio 2026 '99,9%' verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado='admitido', criba_motivo='', criba_url_verificacion='',
        descubrimiento_via='busqueda_a_organismo',
        descubrimiento_query="'99,9%' deuda pública julio 2026 Banco de España Europa Press OR EFE noticia '17 de septiembre' | deuda pública julio 2026 1,744 billones 99,9% PIB noticia bolsamania OR eleconomista OR cincodias OR expansion OR europapress",
        collected_at='2026-09-30', case_id='E076',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5, sesion 2; t0 01:2xZ) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual julio 2026: nota 'La deuda de las Administraciones Publicas se situo en julio de 2026 en el 99,9% del PIB' (17/09/2026; misma primaria que E033); edicion anterior: julio 2025 (la nota da la diferencia en pp y la tasa interanual por subsector)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-julio26.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_julio26.htm, sha256 f8c07585ae51958c); robots.txt de bde.es consultado antes de la primera peticion del dia',
        via_de_acceso='html', access_requires_login='no',
        current_edition_found='si', previous_edition_found='si',
        historical_series_found='si', methodology_found='no',
        alcanzable_por_agente='si', alcanzable_por_humano='si',
        recuperabilidad='A', formato='html',
        dato_actual='julio 2026: ratio deuda PDE/PIB de las AAPP 99,9%; saldo 1.744 mm EUR, +3,8% interanual; CCAA 349 mm (20%), +2,7%',
        dato_anterior='julio 2025: ratio 102,3% (la nota: 2,4 pp menos). Junio 2026: 101,5% (E061)',
        raw_value_span_actual="[BdE deuda-aapp-julio26, 17/09/2026] 'se situo en julio de 2026 en el 99,9% del PIB, 2,4 puntos porcentuales menos que en el mismo periodo del ano anterior'; 'por debajo del 100% por primera vez desde febrero de 2020'; '1.744 miles de millones (mm) de euros en julio de 2026, con una tasa de crecimiento interanual del 3,8%' || [Forbes Espana / EP 2026-09-17, el claim] 'se situo en el mes de julio en el 99,9% del Producto Interior Bruto (PIB), 2,4 puntos porcentuales menos que en el mismo periodo del ano anterior'; '1,744 billones de euros'; 'crecimiento interanual del 3,8%'; 'la deuda de las comunidades autonomas fue de 349.305 millones de euros en julio de 2026, equivalente a un 20% del PIB, con una variacion interanual del 2,7%'",
        raw_value_span_anterior='[BdE deuda-aapp-julio26] 2,4 pp menos que en julio de 2025 (la nota no imprime la ratio de julio de 2025; 99,9 + 2,4 = 102,3)',
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias='', abstain_reason='',
        abandonado_por_tiempo='', bucket_resultado='control_negativo', excedente='no',
        notas="Cubeta A, emisor Banco de Espana (edicion julio 2026, segundo caso tras E033), jornada 5 sesion 2, via busqueda a organismo; hermano de E033 (misma primaria, mismo teletipo de EP en otra cabecera). Se estructura la ratio y su diferencia interanual (-2,4 pp), que E033 no estructura (E033 lleva el saldo y el +3,8%). 'Por primera vez desde febrero de 2020' es afirmacion de la propia nota del BdE; el extremo no se recomputa sobre la serie (NEEDS_REVIEW, como en E061). El desglose por subsectores coincide con la nota y no se anota. methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='E033', mecanismo_candidato='', primaria_edicion='BdE deuda-aapp-julio26',
        conjunto='evaluacion', etiquetado_por='agente',
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'deuda-aapp-julio26', 'serie_nombre': 'Deuda PDE de las AAPP / PIB (%)', 'unidad': 'pct_pib', 'referencia_principal': 'interanual', 'descripcion': 'Ratio de deuda PDE de las AAPP sobre PIB, avance mensual'}, 'periodo_objetivo': '2026-M07', 'periodo_base': '2025-M07', 'valor_objetivo': 99.9, 'cambio_afirmado': -2.4, 'unidad_cambio': 'pp', 'direccion_afirmada': 'baja', 'notas': 'Diferencia en pp dada por el emisor. Sin 2a ni 2b.'},
    ),
    dict(
        cid='Q085',
        claim_text='La deuda pública cerró julio por debajo del 100% del PIB por primera vez desde el estallido de la pandemia',
        claim_date='2026-09-17',
        post_url='https://www.eldiario.es/economia/deuda-publica-cerro-julio-debajo-100-pib-primera-vez-estallido-pandemia_1_13516813.html',
        post_url_tipo='prensa', emisor='elDiario.es', emisor_tipo='prensa_digital',
        emisor_nivel=1, pais='ES', tema='deuda',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com deuda pública julio 2026 99,9% Banco de España',
        criba_query_b="deuda pública julio 2026 '99,9%' verificación OR bulo OR 'fact-check' OR desmentido",
        criba_resultado='admitido', criba_motivo='', criba_url_verificacion='',
        descubrimiento_via='busqueda_a_organismo',
        descubrimiento_query="'99,9%' deuda pública julio 2026 Banco de España Europa Press OR EFE noticia '17 de septiembre' | deuda pública julio 2026 1,744 billones 99,9% PIB noticia bolsamania OR eleconomista OR cincodias OR expansion OR europapress",
        collected_at='2026-09-30', case_id='E077',
        # --- trabajo 2026-09-30 local / 2026-10-01Z (jornada 5, sesion 2; t0 01:2xZ) ---
        fuente_primaria="Banco de Espana - Deuda PDE de las AAPP, avance mensual julio 2026: nota 'La deuda de las Administraciones Publicas se situo en julio de 2026 en el 99,9% del PIB' (17/09/2026; misma primaria que E033); edicion anterior: julio 2025 (la nota da la diferencia en pp y la tasa interanual por subsector)",
        primaria_url='https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/deuda-aapp-julio26.html',
        primaria_url_tipo='nota_de_prensa_html (HTTP 200 al agente identificado; copia research/evidencia/J5_bde_julio26.htm, sha256 f8c07585ae51958c); robots.txt de bde.es consultado antes de la primera peticion del dia',
        via_de_acceso='html', access_requires_login='no',
        current_edition_found='si', previous_edition_found='si',
        historical_series_found='si', methodology_found='no',
        alcanzable_por_agente='si', alcanzable_por_humano='si',
        recuperabilidad='A', formato='html',
        dato_actual='julio 2026, Comunidades Autonomas: 349 mm EUR (20% del PIB), +2,7% interanual (la pieza: 349.300 millones). AAPP: 99,9%, 1.744 mm, +3,8% (E033)',
        dato_anterior='julio 2025, CCAA: saldo implicito 349/1,027 = 340 mm; la nota da la tasa',
        raw_value_span_actual="[BdE deuda-aapp-julio26, 17/09/2026] 'La deuda de las CCAA ... 349 mm de euros en julio de 2026, equivalente a un 20% del PIB, con una variacion interanual del 2,7%' || [elDiario.es 2026-09-17, el claim] 'Comunidades Autonomas: 349.300 millones de euros (un 20% del PIB), un 2,7% mas que hace un ano'; '99,9% del PIB, la ratio mas baja desde febrero de 2020'; '1,744 billones de euros, un 3,8% mas que hace un ano'",
        raw_value_span_anterior='[BdE deuda-aapp-julio26] variacion interanual del 2,7% (CCAA); la nota no imprime el saldo de julio de 2025',
        truth='supported', context='no_divergence_detected',
        clase_primaria='none', clases_secundarias='', abstain_reason='',
        abandonado_por_tiempo='', bucket_resultado='control_negativo', excedente='no',
        notas="Cubeta A, emisor Banco de Espana (edicion julio 2026, tercer caso: la edicion llega al tope con E033 y E076), jornada 5 sesion 2, via busqueda a organismo; hermano de E033 (misma primaria; redaccion propia, no teletipo). Se estructura el subsector CCAA, que ni E033 ni E076 estructuran: 349.300 millones redondea los 349 mm de la nota (dentro de tolerancia), 20% y +2,7% son los de la nota. 'La ratio mas baja desde febrero de 2020' es afirmacion de la nota del BdE, no recomputada (NEEDS_REVIEW). Hispanidad (17-09, '1,744 billones ... 99,9%', 'julio 2025 era 102,3%') seria un cuarto control de la misma nota: no se admite por el tope. methodology_found=no (NEEDS_REVIEW).",
        cubeta='A', hermano_de='E033', mecanismo_candidato='', primaria_edicion='BdE deuda-aapp-julio26',
        conjunto='evaluacion', etiquetado_por='agente',
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'Banco de España', 'tabla': 'deuda-aapp-julio26', 'serie_nombre': 'Deuda PDE de las CCAA, saldo (millones EUR)', 'unidad': 'millones EUR', 'referencia_principal': 'interanual', 'descripcion': 'Deuda PDE de las Comunidades Autonomas, avance mensual'}, 'periodo_objetivo': '2026-M07', 'periodo_base': '2025-M07', 'valor_objetivo': 349300, 'cambio_afirmado': 2.7, 'unidad_cambio': 'pct', 'direccion_afirmada': 'sube', 'notas': 'Tasa interanual dada por el emisor. Sin 2a ni 2b.'},
    ),
    # ---- jornada 5, sesion 3 (2026-10-01 local, 2026-10-02Z): P1 sobre EOAT0826 (diseno 4h). Un 2b entre siete redacciones con tasa propia ----
    dict(
        cid='Q086',
        claim_text='Apartamentos, camping y casas rurales perdieron en agosto un 30% de viajeros y un 23% de pernoctaciones: los 21.362 viajeros que optaron por un apartamento fueron un 17% menos que en agosto de 2025',
        claim_date='2026-10-01',
        post_url='https://elnuevodigitalmurcia.es/art/9286/apartamentos-camping-y-casas-rurales-perdieron-en-agosto-un-30-de-viajeros-y-un-23-de-pernoctaciones',
        post_url_tipo='prensa', emisor='El Nuevo Digital Murcia (Nuevo Digital)', emisor_tipo='prensa_digital',
        emisor_nivel=2, pais='ES', tema='turismo',
        criba_query_a='site:maldita.es OR site:newtral.es OR site:verificat.cat OR site:efeverifica.com apartamentos turísticos campings agosto 2026 Región de Murcia viajeros pernoctaciones extrahoteleros',
        criba_query_b='Murcia apartamentos campings agosto 2026 viajeros 17% menos OR 30% extrahoteleros verificación OR bulo OR fact-check OR desmentido',
        criba_resultado='admitido', criba_motivo='', criba_url_verificacion='',
        descubrimiento_via='titular_prensa',
        descubrimiento_query='extrahoteleros agosto Región de Murcia OR Comunitat Valenciana pernoctaciones apartamentos campings INE octubre 2026 cae OR sube (consulta generica por comunidad, una de siete que cubren las 17 CCAA; no es rastreo de la redaccion, diseno 4j)',
        collected_at='2026-10-01', case_id='E078',
        # --- trabajo 2026-10-02Z (E078 t0 02:26Z; jornada 5 sesion 3, prediccion P1) ---
        fuente_primaria='INE - EOAT agosto 2026 (EOAT0826, publicada 2026-10-01): API Tempus tablas 1993 (EOT1117 viajeros, EOT1120 pernoctaciones) y 2016 (EOT813, EOT816), Region de Murcia + anexo EOAT0826.xlsx (EOAP_Hoja1 fila 26; EOAC_Hoja1 fila 50); edicion anterior: anexo EOAT0825.xlsx (mismas filas; nota publicada 2025-10-01)',
        primaria_url='https://www.ine.es/dyngs/Prensa/EOAT0826.htm',
        primaria_url_tipo='nota_de_prensa_html (200, 42.477 bytes, sha256 c89b0d7f2444bd9b) + API JSON wstempus DATOS_TABLA/1993 (sha256 424690b0569f149f) y 2016 (3231652fc31e1d68) + anexos EOAT0826.xlsx (200, 159.457 bytes, 2ea0199335efec0e) y EOAT0825.xlsx (200, 158.958 bytes, eeb28bf6c7c556ee), descargados con research/puerta3/edicion_anterior.py; robots.txt de www.ine.es consultado antes de la primera peticion del dia',
        via_de_acceso='api', access_requires_login='no',
        current_edition_found='si', previous_edition_found='si',
        historical_series_found='si', methodology_found='si',
        alcanzable_por_agente='si', alcanzable_por_humano='si',
        recuperabilidad='A', formato='api',
        dato_actual='Region de Murcia, agosto 2026. Apartamentos turisticos: 21.365 viajeros (17.554 residentes, 3.812 extranjeros); 124.748 pernoctaciones. Campings: 16.191 viajeros; 108.832 pernoctaciones (API y anexo EOAT0826)',
        dato_anterior='Agosto 2025 vigente (API, dato definitivo): apartamentos 29.538 viajeros -> -27,67%; 215.277 pernoctaciones -> -42,05%. Campings 26.228 viajeros -> -38,27%; 148.874 pernoctaciones -> -26,90%. Agosto 2025 al publicar (anexo EOAT0825, provisional): apartamentos 25.803 viajeros -> -17,20%; 150.328 pernoctaciones -> -17,02%. Campings 29.227 viajeros -> -44,60%; 155.672 pernoctaciones -> -30,09%',
        raw_value_span_actual='[INE API tabla 1993] EOT1117 Murcia (Región de). Viajeros. Total. 2026-M08: 21365 | EOT1120 Murcia (Región de). Pernoctaciones. Total. 2026-M08: 124748 || [INE API tabla 2016] EOT813 Viajeros 2026-M08: 16191 | EOT816 Pernoctaciones 2026-M08: 108832 || [EOAT0826.xlsx, hoja EOAP_Hoja1, fila 26] Murcia, Región de, 21365, 17554, 3812, 124748, 110158, 14590, 5.84 || [EOAT0826.xlsx, hoja EOAC_Hoja1, fila 50] Murcia, Región de, 16191, 14152, 2039, 108832, 95384, 13448, 6.72 || [El Nuevo Digital Murcia 2026-10-01, el claim; copia J5_E078_elnuevodigitalmurcia.htm, sha256 a64aec717be56847] Los 21.362 viajeros que optaron por un apartamento fueron un 17% menos que en agosto de 2025; los 16.191 campistas registrados fueron casi la mitad (-44%) que un año antes',
        raw_value_span_anterior='[INE API tabla 1993, edicion vigente] EOT1117 2025-M08: 29538 | EOT1120 2025-M08: 215277 || [INE API tabla 2016, edicion vigente] EOT813 2025-M08: 26228 | EOT816 2025-M08: 148874 || [EOAT0825.xlsx, hoja EOAP_Hoja1, fila 26, edicion al publicar] Murcia, Región de, 25803, 19645, 6158, 150328, 132659, 17669, 5.83 || [EOAT0825.xlsx, hoja EOAC_Hoja1, fila 50, edicion al publicar] Murcia, Región de, 29227, 24977, 4250, 155672, 133335, 22337, 5.33',
        truth='mixed', context='divergence_detected',
        clase_primaria='2b_base_revisada', clases_secundarias='', abstain_reason='',
        abandonado_por_tiempo='', bucket_resultado='divergencia_real', excedente='no',
        notas='Cubeta B (2b, base revisada, subtipo magnitud), jornada 5 sesion 3: es el caso que decide la prediccion P1 del diseno 4h sobre EOAT0826. 21365/25803 - 1 = -17,2% (apartamentos) y 16191/29227 - 1 = -44,6% (campings; la pieza dice -44 y casi la mitad) solo salen con la base PROVISIONAL de agosto 2025 (anexo EOAT0825, nota del 2025-10-01); con la vigente: -27,7% y -38,3%. Mismo signo en las dos: 2b sin cambio de signo; en apartamentos la caida real es mayor que la publicada, en campings menor. La pieza escribe 21.362 viajeros donde el INE da 21.365: errata de 3, dentro de tolerancia, no anotada. Los totales (30% de viajeros, 23% de pernoctaciones) y el -21% de turismo rural agregan o usan otras encuestas y no se evaluan. LIMITE DECLARADO: es la misma redaccion que E066 (EOAT0526); se localizo con la consulta generica por comunidad que se lanzo para las 17 CCAA, no rastreando la cabecera (diseno 4j), pero el 2b de esta edicion viene de una redaccion que ya habia mostrado el mecanismo. Primer B de la edicion EOAT0826. methodology_found=si: IME del INE, seccion 17 (research/puerta3/METODOLOGIA-REVISION-INE.md).',
        cubeta='B', hermano_de='', mecanismo_candidato='', primaria_edicion='INE EOAT0826',
        conjunto='evaluacion', etiquetado_por='agente',
        estructura={'tipo': 'cambio_entre_periodos', 'metrica': {'emisor': 'INE', 'tabla': '1993', 'serie_nombre': 'Murcia (Región de). Viajeros. Total.', 'unidad': 'viajeros', 'referencia_principal': 'interanual', 'descripcion': 'EOAT, viajeros en apartamentos turisticos, Region de Murcia, mensual'}, 'periodo_objetivo': '2026-M08', 'periodo_base': '2025-M08', 'valor_objetivo': 21362, 'cambio_afirmado': -17, 'unidad_cambio': 'pct', 'direccion_afirmada': 'baja', 'evidencia_al_publicar': {'valor': 25803, 'edicion': 'INE EOAT0825 (agosto 2025, datos provisionales)', 'fecha': '2025-10-01', 'url': 'https://www.ine.es/prensa/anexo_tablas/es/EOAT0825.xlsx', 'raw_value_span': "[EOAT0825.xlsx, hoja EOAP_Hoja1, fila 26] 'Murcia, Región de', 25803, 19645, 6158, 150328, 132659, 17669, 5.83", 'verificacion': 'descarga 2026-09-30 con research/puerta3/edicion_anterior.py (HTTP 200, 158.958 bytes, sha256 eeb28bf6c7c556ee; fecha de la nota leida del HTML: 1 de octubre de 2025)'}, 'evidencia_vigente': {'valor': 29538, 'edicion': 'API Tempus, tabla 1993, edicion vigente (dato definitivo)', 'fecha': '2026-10-01', 'url': 'https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/1993', 'raw_value_span': "[INE API tabla 1993] EOT1117 'Murcia (Región de). Viajeros. Total.' 2025-M08: 29538 (T3_TipoDato definitivo)"}, 'notas': 'Base interanual correcta en periodo, tomada de la edicion provisional (25.803) y no de la vigente (29.538): 2b sin cambio de signo (-17,2% frente a -27,7%). Campings del mismo articulo: -44,6% provisional frente a -38,3% vigente.'},
    ),
]
