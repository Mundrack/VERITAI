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
    "B": (20, 15),
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
        historical_series_found="si", methodology_found="no",
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
            "sin 'Total Nacional' en el nombre (dos filtros fallidos antes de listar). methodology_found=no (NEEDS_REVIEW)."
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
        historical_series_found="si", methodology_found="no",
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
            "anota, no es divergencia. Series ADR en la operacion IRSH (180), tabla 2059. methodology_found=no (NEEDS_REVIEW)."
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
]
