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
        # PENDIENTE de trabajar. Lectura previa: el -6,1% es la vivienda de SEGUNDA MANO nacional
        # (48.128), presentada en el titular como 'la compraventa de viviendas' (total: -5,1%).
        # Mismo mecanismo que N01 (subgrupo como total): candidata P17 -> cubeta O, other_observed.
        # Misma primaria que E001 (tabla 6150, serie ETDP1824); no es hermano por criba.
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
        # PENDIENTE de trabajar. Esperado: cubeta A (interanual = referencia). Operacion HPT id 40.
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
        # PENDIENTE de trabajar. Esperado: cubeta A como cambio entre EDICIONES del WEO
        # (abril 2026 -> julio 2026, cambio 0; base = edicion anterior = referencia del FMI).
        # Newtral 2026-09-18 verifica 'la que mas crece de la eurozona' (Urtasun), NO este claim.
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
        # PENDIENTE de trabajar. Cuerpo: 2% -> 2,5% (WEO abril 2026 vs edicion anterior, a
        # identificar: octubre 2025). Esperado: cubeta A (cambio entre ediciones, base = anterior).
        # Hermanos por misma primaria y consulta: El Universo, El Diario EC, Lexis (no se cuentan).
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
        # PENDIENTE de trabajar. Primaria: DGT (Interior) nota 2026-09-07 (PDF) 240 vs 230 (+10, +4%).
        # Dvuelta (asociacion, no verificador) senala que la nota DGT de 2025-09-03 decia 228: base
        # consolidada vs provisional. Patron C18 (2b latente en la primaria; el claim relaya): por
        # el precedente de DEC-026 se anotaria A con la revision registrada en notas. A decidir al
        # trabajarlo; Mateo lo ve en la muestra a ciegas.
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
        # PENDIENTE de trabajar. Esperado: cubeta A (0,7% trimestral vs 0,6% 1T; base = trimestre
        # anterior = referencia). Primaria: INE CNTR2T26 (2026-09-25), operacion 237 (CNTR2010).
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
        # PENDIENTE de trabajar. Cuerpo: interanual 2,6%, 'una decima menos de lo que habia estimado'.
        # El INE no hace previsiones: el titular llama 'previsiones' al avance. Revision avance ->
        # definitivo del propio emisor (fuera del prototipo, 2b). Esperado: cubeta D (nivel).
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
        # PENDIENTE de trabajar. Esperado: cubeta A, misma edicion CNTR2T26 que Q011 (tope 3).
    ),
]
