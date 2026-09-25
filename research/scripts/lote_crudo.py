"""Datos del lote crudo: todos los candidatos, admitidos y rechazados.

Este archivo es DATOS, no logica. La logica esta en validar_lote_crudo.py,
que lo valida y emite los dos CSV.

POR QUE UN MODULO PYTHON Y NO EDITAR EL CSV A MANO
    Cada candidato lleva su justificacion en texto y el CSV se regenera
    siempre desde aqui. Un CSV editado a mano pierde el porque; este archivo
    no. Es el mismo patron que normalizar_a_enums.py en la TAREA 1.

ESTRUCTURA DE UN CANDIDATO
    Todos tienen los campos de identidad y de criba. Solo los admitidos tienen
    ademas case_id y los campos de trabajo (primaria, recuperacion, valores,
    etiquetas, cubeta). Los tiempos NO se escriben aqui: se derivan de
    research/cronometro.log.

    Los valores permitidos de cada campo estan en validar_lote_crudo.py y, para
    los enums compartidos con la TAREA 1, en normalizar_a_enums.py.
"""

from __future__ import annotations

# Dominios de verificadores usados en la consulta (a) de la criba.
DOMINIOS_VERIFICADORES = (
    "maldita.es newtral.es factual.afp.com verificat.cat efeverifica.com "
    "ecuadorchequea.com chequeado.com colombiacheck.com verificado.com.mx"
)

# Orden: el de descubrimiento. Los candidatos que aparecieron DURANTE la criba
# de otro (K35-K40) van justo detras de su hermano, que es cuando se vieron.
# Ese orden es el que manda para "los primeros 6 divergentes" (muestreo neutral).
#
# criba_motivo lleva un prefijo que se cuenta aparte en el resumen:
#   verificacion_directa:  un verificador emitio veredicto sobre ESA afirmacion
#   cobertura_explainer:   un verificador cubrio esa misma publicacion primaria
#                          sin veredicto; el trabajo de ir a la fuente ya esta hecho
CANDIDATOS: list[dict] = [
    # ---- tanda 1: descubrimiento 2026-09-25, criba 2026-09-25 -------------------
    dict(
        cid="K01", case_id="C01",
        claim_text="El paro registrado sube en agosto en 44.419 personas y se situa en 2.355.918, su valor mas bajo en este mes desde 2007",
        claim_date="2026-09-02",
        post_url="https://www.sepe.es/noticia/SEPE/2026/Septiembre/paro-registrado-sube-agosto-44419-personas",
        post_url_tipo="nota_oficial", emisor="SEPE (Ministerio de Trabajo)", emisor_tipo="organismo_estadistico",
        emisor_nivel=1, pais="ES", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="SEPE - Estadistica mensual de paro registrado y contratos (datos de avance)",
        primaria_url="https://www.sepe.es/noticia/SEPE/2026/Septiembre/paro-registrado-sube-agosto-44419-personas",
        primaria_url_tipo="nota_oficial_mensual + libro nacional XLS/PDF en /datos-estadisticos/municipios/2026/agosto",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="agosto 2026: 2.355.918 parados; +44.419 mensual (+1,92%); -70.593 interanual (-2,91%)",
        dato_anterior="julio 2026: 2.311.499 parados; +19.517 mensual (+0,85%); -93.107 interanual (-3,87%)",
        raw_value_span_actual=(
            "[SEPE, nota 2026-09-02] 'El paro registrado total se situa en 2.355.918, por debajo de la "
            "barrera los 2,4 millones.' | 'Es su nivel mas bajo en un mes de agosto desde 2007, en el "
            "periodo previo a la crisis financiera.' | 'ha aumentado en 44.419 personas en relacion con "
            "el mes anterior (1,92%)' | 'Respecto a agosto de 2025, el paro ha descendido en 70.593 "
            "personas (-2,91%).'"
        ),
        raw_value_span_anterior=(
            "[SEPE, nota 2026-08-04] 'El paro registrado se situa en 2.311.499, la cifra mas baja en "
            "este mes desde 2007.' | 'ha subido en 19.517 personas en relacion con el mes anterior' | "
            "'En terminos interanuales el paro ha descendido en 93.107 personas (-3,87%)'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "El claim ES la nota oficial del emisor, asi que localizar la primaria es trivial; la prueba "
            "real era la edicion anterior, y aparecio a la primera busqueda (nota de julio, 2026-08-04). "
            "La nota presenta juntos el alza mensual (+44.419) y el nivel ('mas bajo en agosto desde "
            "2007'): correctamente enmarcado. LIMITE: 'desde 2007' se toma del emisor, no se contrasto "
            "contra la serie 2007-2025 de agostos (haria falta el libro XLS). La cifra de agosto 2025 "
            "(2.426.511) solo se deriva: la nota da la variacion, no el nivel. Dataset: libro nacional "
            "XLS de 4 MB por mes; sin navegacion entre meses pero el patron /2026/<mes> funciona. "
            "Ninguna de las dos notas enlaza a metodologia."
        ),
        criba_query_a="paro registrado agosto 2026 44.419 mas bajo desde 2007",
        criba_query_b="paro agosto 2026 44.419 bulo OR verificacion OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K02", case_id="C02",
        claim_text="Paro y empleo en agosto de 2026: Espana pierde 162.840 afiliados y suma 44.419 desempleados",
        claim_date="2026-09-02",
        post_url="https://www.eldiariodemadrid.es/articulo/sociedad/paro-empleo-agosto-2026-afiliados-seguridad-social-desempleo/20260902105338140547.html",
        post_url_tipo="prensa", emisor="El Diario de Madrid", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Ministerio de Inclusion, Seguridad Social y Migraciones - afiliacion media mensual (nota oficial via La Moncloa; informes PDF en seg-social.es)",
        primaria_url="https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/inclusion/Paginas/2026/020926-balance-afiliados-agosto.aspx",
        primaria_url_tipo="nota_oficial_mensual (espejo oficial en La Moncloa; el dominio del ministerio devolvio 403)",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="agosto 2026: afiliacion media 22.345.226 (serie original), -162.840 vs julio; desestacionalizada 22.371.964 (+83.844); +679.023 interanual (+3,13%)",
        dato_anterior="julio 2026: afiliacion media 22.508.065 (maximo historico), +41.727 vs junio; desestacionalizada 22.288.120; +642.562 interanual",
        raw_value_span_actual=(
            "[Moncloa/Inclusion, nota 2026-09-02] 'En el ultimo ano, la Seguridad Social experimenta un "
            "aumento de 679.023 afiliados en la serie original, con una tasa interanual del 3,13%.' | "
            "'resta 162.840 ocupados respecto a julio' | '22.345.226' (serie original) | "
            "'22.371.964' y '83.844 afiliados mas' (descontada estacionalidad y calendario)"
        ),
        raw_value_span_anterior=(
            "[Moncloa/Inclusion, nota 2026-08-04] 'La afiliacion media aumenta en 41.727 personas en "
            "julio' | 'alcanza un nuevo maximo historico, con 22.508.065 ocupados' | 'Si se descuenta la "
            "estacionalidad y el efecto calendario, la afiliacion alcanza 22.288.120 ocupados' | "
            "'en los ultimos 12 meses, la afiliacion ha ganado 642.562 afiliados'"
        ),
        truth="supported", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Los dos numeros del titular son literales de sus primarias (162.840 = caida de la "
            "afiliacion MEDIA, cosa que el articulo no aclara). La divergencia esta en el encuadre "
            "mensual: la primaria dice que la caida es 'normal' para agosto y que, descontada la "
            "estacionalidad, la afiliacion SUBIO en 83.844. El titular presenta como perdida un dato "
            "de un mes estacional sin esa correccion, que el propio emisor publica en la misma nota. "
            "Patron identico a P11 (calculo correcto, comparacion mal elegida). Matiz: el cuerpo del "
            "articulo si da el interanual (+679.023) y el record para agosto (22,34 M), asi que la "
            "omision esta en el titular, no en el texto. Coherencia interna: 22.508.065 - 162.840 = "
            "22.345.225, cuadra con 22.345.226 (redondeo de medias). DEC-018: inclusion.gob.es "
            "devolvio 403 al fetcher; NO se reintento. La misma nota esta publicada por La Moncloa, "
            "canal oficial del mismo Gobierno, que si responde: no es rodear nada, es el mismo "
            "emisor. Se registra igualmente que el dominio del ministerio bloquea agentes. "
            "seg-social.es ofrece informes mensuales en PDF ('Afiliados medios y con ajuste estacional', "
            "agosto 2026, 869 KB) y avisa de que la nueva clasificacion CNAE25 paraliza temporalmente "
            "un informe: senal de cambio metodologico, sin nota metodologica localizada."
        ),
        criba_query_a="paro registrado agosto 2026 44.419 mas bajo desde 2007",
        criba_query_b="paro agosto 2026 44.419 bulo OR verificacion OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K35", case_id="C03",
        claim_text="El paro se dispara en 44.419 personas y registra su peor agosto en 7 anos",
        claim_date="2026-09-02",
        post_url="https://okdiario.com/economia/empleo/paro-dispara-44-419-personas-registra-peor-agosto-desde-hace-7-anos-20213431/amp",
        post_url_tipo="prensa", emisor="okdiario", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="SEPE - notas mensuales de paro registrado (la variacion de agosto de cada ano, 2019-2026)",
        primaria_url="https://www.sepe.es/noticia/SEPE/2026/Septiembre/paro-registrado-sube-agosto-44419-personas",
        primaria_url_tipo="nota_oficial_mensual; la serie de agostos se reconstruye con 8 notas SEPE/Moncloa",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="agosto 2026: +44.419 mensual (+1,92%); nivel 2.355.918 (mas bajo en agosto desde 2007)",
        dato_anterior=(
            "agosto 2025: +21.905 (+0,91%); nivel 2.426.511. Serie de variaciones de agosto: 2019 +54.371 | "
            "2020 +29.780 | 2021 -82.583 | 2022 +40.428 | 2023 +24.826 | 2024 +21.884 | 2025 +21.905 | "
            "2026 +44.419. Maximo intermedio 40.428 (2022) < 44.419: el claim es cierto"
        ),
        raw_value_span_actual=(
            "[SEPE, nota 2026-09-02] 'ha aumentado en 44.419 personas en relacion con el mes anterior "
            "(1,92%)' | 'El paro registrado total se situa en 2.355.918' | 'Es su nivel mas bajo en un "
            "mes de agosto desde 2007' || [okdiario 2026-09-02, el claim] 'la subida ha sido la mas "
            "pronunciada en un octavo mes del ano desde 2019, hace siete anos, cuando el desempleo "
            "subio en 54.371 personas'"
        ),
        raw_value_span_anterior=(
            "[SEPE, nota 2025-09-02] 'aumento en 21.905 personas' | 'El paro total registrado se ha "
            "situado en 2.426.511 personas.' | 'Se trata del nivel mas bajo desde agosto de 2007' || "
            "[Moncloa, nota 2019-09-03, base del claim] 'En el mes de agosto, el paro ha subido en "
            "54.371 personas en relacion con el mes anterior.' | 'la cifra total de parados registrados "
            "es de 3.065.804'"
        ),
        truth="supported", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="2_baseline_selection", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "El claim es CIERTO: +44.419 es la mayor subida de agosto desde 2019, en absoluto y tambien "
            "en porcentaje (1,92% sobre 2,31 M frente a 1,80% sobre 3,01 M en 2019). La divergencia es "
            "de encuadre: el mismo dato admite dos lecturas verdaderas que apuntan en direcciones "
            "opuestas (flujo mensual 'peor en 7 anos' vs nivel 'mas bajo en 19 anos'), y okdiario "
            "reproduce solo la primera; la segunda es el titular del propio SEPE y no aparece en el "
            "articulo salvo para el paro femenino. Par natural con C01. Clase: no es baseline ni "
            "absoluto/relativo en sentido estricto, es eleccion de metrica (flujo vs stock) omitiendo la "
            "lectura del emisor; other_observed con baseline como secundaria. LIMITE de trazabilidad: "
            "los cinco puntos intermedios de la serie (2020-2024) proceden del resumen del buscador "
            "sobre las notas oficiales de La Moncloa (URLs: 2020/020920-paro, 2021/020921-paroagosto, "
            "2022/020922-paroagosto, 2023/040923-paro-registrado-agosto, 2024/030924-paro-aumenta-agosto), "
            "sin span literal capturado; 2019, 2025 y 2026 si son literales. Para el veredicto basta "
            "porque el maximo intermedio queda 4.000 por debajo. La pagina de series del SEPE es una "
            "instantanea de enero de 2020 con XLS que el agente no puede leer: la serie 'existe' pero "
            "para un agente solo es alcanzable nota a nota. Localizar y extraer fueron el mismo acto."
        ),
        criba_query_a="paro registrado agosto 2026 44.419 mas bajo desde 2007",
        criba_query_b="paro agosto 2026 44.419 bulo OR verificacion OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K03", case_id="C04",
        claim_text="Inflacion de Ecuador marca 1,12% en agosto y queda entre las mas bajas de Sudamerica",
        claim_date="2026-09-23",
        post_url="https://www.eldiario.ec/negocios/inflacion-de-ecuador-112-agosto-2026-23092026/",
        post_url_tipo="prensa", emisor="El Diario (Ecuador)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="EC", tema="precios",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEC - Indice de Precios al Consumidor, Boletin Tecnico N 08-2026-IPC (agosto 2026)",
        primaria_url="https://www.ecuadorencifras.gob.ec/documentos/web-inec/Inflacion/2026/agosto/BOLETIN_TECNICO_IPC_2026_08.pdf",
        primaria_url_tipo="pdf_boletin_mensual con tabla de serie; URL por patron /Inflacion/<anio>/<mes>/BOLETIN_TECNICO_IPC_<anio>_<mm>.pdf",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="agosto 2026: inflacion anual 1,12%; mensual 0,04%; acumulada 1,34%; indice 100,84 (base jul-2025/jun-2026=100); CFBC USD 828,06",
        dato_anterior="julio 2026: inflacion anual 1,39%; mensual -0,09%; acumulada 1,30%; indice 100,79. Referencia agosto 2025: anual 0,81%",
        raw_value_span_actual=(
            "[INEC, Boletin Tecnico N 08-2026-IPC, agosto 2026, p.3] 'La variacion mensual en agosto "
            "2026, respecto a julio 2026, fue de 0,04%. La variacion anual de precios de agosto 2026, "
            "respecto a agosto 2025, alcanzo 1,12%; como referencia, en agosto 2025 fue de 0,81%. La "
            "variacion acumulada de precios de agosto 2026, respecto a diciembre 2025, fue de 1,34%.' | "
            "[tabla serie] 'Jul-26 100,79 -0,09% 1,39% 1,30% Ago-26 100,84 0,04% 1,12% 1,34%'"
        ),
        raw_value_span_anterior=(
            "[INEC, Boletin N 08-2026, p.9, referencia al mes anterior] 'la variacion anual en agosto "
            "2026 fue de 1,12%, en el mes anterior fue de 1,39% y la de agosto 2025 se ubico en 0,81%.' "
            "|| [INEC, Boletin Tecnico N 07-2026-IPC, julio 2026: PDF de 16 pp localizado por enlace "
            "desde la nota INEC del 2026-08-10 y descargado; ver notas para el span propio]"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "El 1,12% es literal del INEC y el titular se cubre con 'entre las mas bajas de "
            "Sudamerica', que se sostiene con la lista que difunde el Ministerio de Desarrollo Economico "
            "(Paraguay 1,50%, Peru 4,06%, Chile 4,10%, Brasil 4,22%, Uruguay 4,55%, Bolivia 5,02%). "
            "LIMITE: ese comparador es una compilacion gubernamental, no las primarias de cada pais, y "
            "no incluye Guyana ni Surinam; la version sin cobertura ('LA mas baja') es la de C05. "
            "HALLAZGOS de la primaria: (1) el boletin trae la serie mensual en tabla (indice, mensual, "
            "anual, acumulada), asi que la edicion anterior esta dentro de la edicion actual; (2) el "
            "INEC cambio la base del IPC a julio 2025-junio 2026 = 100 y documenta 'factores de empalme "
            "que garantizan la comparabilidad historica' con la base 2014: cambio metodologico que NO "
            "rompe la serie, mismo patron que P13 (AEMET); enlaza a la metodologia. (3) La pagina del "
            "IPC en ecuadorencifras.gob.ec esta 'temporalmente en mantenimiento' y no lista documentos, "
            "pero los PDF responden por patron de URL: para un agente, el patron es el acceso, no el "
            "portal. Boletin de julio: localizado por el enlace de la nota INEC del 10 de agosto y "
            "descargado (16 pp); el fetcher no le extrae texto, pypdf si."
        ),
        criba_query_a="inflacion Ecuador agosto 2026 mas baja de la region",
        criba_query_b="inflacion Ecuador 1,12% agosto 2026 \"mas baja\" region verificacion OR bulo OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K36", case_id="C05",
        claim_text="Gobierno de Noboa protege el bolsillo de los ecuatorianos: inflacion de Ecuador es la mas baja de la region",
        claim_date="2026-09-22",
        post_url="https://www.economicoproductivo.gob.ec/gobierno-de-noboa-protege-el-bolsillo-de-los-ecuatorianos-inflacion-de-ecuador-es-la-mas-baja-de-la-region/",
        post_url_tipo="nota_oficial", emisor="Ministerio de Desarrollo Economico y Productivo (Ecuador)", emisor_tipo="gobierno",
        emisor_nivel=1, pais="EC", tema="precios",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEC - IPC Boletin Tecnico N 08-2026 (agosto 2026); para el ranking regional NO hay primaria: el ministerio compara en una imagen sin citar fuentes",
        primaria_url="https://www.ecuadorencifras.gob.ec/documentos/web-inec/Inflacion/2026/agosto/BOLETIN_TECNICO_IPC_2026_08.pdf",
        primaria_url_tipo="pdf_boletin_mensual (misma primaria que C04)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="agosto 2026: inflacion anual 1,12% (INEC). Comparador regional: grafico en imagen dentro de la nota ministerial, sin cifras en texto ni fuente",
        dato_anterior="julio 2026: inflacion anual 1,39% (INEC, Boletin N 07-2026)",
        raw_value_span_actual=(
            "[Ministerio de Desarrollo Economico, nota 2026-09-22, el claim] 'Gobierno de Noboa protege "
            "el bolsillo de los ecuatorianos: inflacion de Ecuador es la mas baja de la region' | 'en "
            "agosto de 2026 la inflacion anual cerro en 1,12%, siendo la cifra mas baja de Sudamerica' | "
            "'El Gobierno de Daniel Noboa cuida el poder adquisitivo' || [INEC, Boletin N 08-2026, p.3] "
            "'La variacion anual de precios de agosto 2026, respecto a agosto 2025, alcanzo 1,12%'"
        ),
        raw_value_span_anterior=(
            "[INEC, Boletin Tecnico N 07-2026-IPC, julio 2026, p.3] 'La variacion anual de precios de "
            "julio 2026, respecto a julio 2025, alcanzo 1,39%; como referencia, en julio 2025 fue de 0,72%.'"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="", abstain_reason="REQUIRED_SLOT_MISSING",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Tres capas en un claim: (1) '1,12%' es literal del INEC: supported. (2) 'la mas baja de "
            "Sudamerica', sin la cobertura de C04: el comparador esta en un grafico-imagen de la propia "
            "nota, sin cifras en texto y sin citar de donde salen las de los demas paises; Guyana y "
            "Surinam no aparecen. Para verificarlo hacen falta las primarias de cada pais: "
            "REQUIRED_SLOT_MISSING. (3) 'Gobierno protege el bolsillo': atribucion causal de un dato "
            "macro a la accion del Gobierno, sin mecanismo ni evidencia. Es clase 6 (correlacion/"
            "causalidad), fuera de la tesis: other_observed. Truth global = mixed. La divergencia "
            "computable esta en (2): un superlativo regional cuyo soporte es una imagen. Par natural con "
            "C04, que reproduce el mismo dato con cobertura ('entre las mas bajas') y con la lista en "
            "texto. Localizar y extraer no costaron nada porque la primaria ya estaba en mano (C04)."
        ),
        criba_query_a="inflacion Ecuador agosto 2026 mas baja de la region",
        criba_query_b="inflacion Ecuador 1,12% agosto 2026 \"mas baja\" region verificacion OR bulo OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K04", case_id="C06",
        claim_text="Espana cae seis puestos en 2026 en la Clasificacion Mundial de Libertad de Prensa",
        claim_date="2026-04-30",
        post_url="https://www.infobae.com/espana/agencias/2026/04/30/espana-cae-seis-puestos-en-2026-en-la-clasificacion-mundial-de-libertad-de-prensa/",
        post_url_tipo="prensa", emisor="Infobae (agencias)", emisor_tipo="prensa_digital",
        emisor_nivel=4, pais="ES", tema="rankings",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Reporteros Sin Fronteras - Clasificacion Mundial de la Libertad de Prensa (ficha de Espana + CSV anual)",
        primaria_url="https://rsf.org/es/pais/espa%C3%B1a",
        primaria_url_tipo="ficha_pais_html con puesto, score e indicadores de 2026 y 2025; CSV por edicion en /sites/default/files/import_classement/<anio>.csv",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="2026: puesto 29/180, puntuacion 75,42; indicadores politico 71,26, economico 55,68, legislativo 80,59, social 79,05, seguridad 96,46",
        dato_anterior="2025: puesto 23/180, puntuacion 77,35 (Infobae escribe 77,93: error de la secundaria, 0,58 puntos)",
        raw_value_span_actual=(
            "[RSF, ficha Espana] '29/ 180' | '75,42' | 'Indicador politico' '71,26' | 'Indicador economico' "
            "'55,68' | 'Indicador legislativo' '80,59' | 'Indicador social' '79,05' | 'Indicador de "
            "seguridad' '96,46' || [Infobae 2026-04-30, el claim] 'Espana desciende hasta el puesto 29 en "
            "la Clasificacion Mundial de la Libertad de Prensa de 2026 de Reporteros Sin Fronteras (RSF) "
            "con una puntuacion global de 75,42 puntos, frente a los 77,93 puntos y el puesto 23 que "
            "ocupada en el ano 2025.'"
        ),
        raw_value_span_anterior=(
            "[RSF, Clasificacion 2025, fila Espana] '23/ 180' | '77,35' || [RSF, ficha Espana, "
            "comparacion 2025] '23/ 180' | '77,35' || CSV: https://rsf.org/sites/default/files/"
            "import_classement/2025.csv"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Titular de ranking que NO es ranking_vs_value: la puntuacion de Espana tambien cayo "
            "(77,35 -> 75,42, -1,93), asi que el descenso de 6 puestos refleja un empeoramiento real y "
            "no solo el avance de otros; Infobae ademas reporta puesto y puntuacion juntos. "
            "Correctamente enmarcado. PERO la secundaria tiene un error numerico: da 77,93 como "
            "puntuacion de 2025 cuando RSF publica 77,35 tanto en la Clasificacion 2025 como en la "
            "ficha de pais; el titular no se ve afectado. Primaria ejemplar para un agente: ficha HTML "
            "con edicion actual y anterior en la misma pagina, selector de anos 2002-2026, CSV por "
            "edicion y metodologia publicada (vigente 'from 2022 onwards', dos componentes: recuento "
            "cuantitativo de abusos + cuestionario cualitativo). Leccion para P-15: un titular 'cae N "
            "puestos' no es de la clase canonica hasta comprobar que el valor propio no se movio."
        ),
        criba_query_a="Espana cae seis puestos libertad de prensa 2026 RSF",
        criba_query_b="Espana cae seis puestos clasificacion libertad de prensa 2026 verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K05", case_id="C07",
        claim_text="Espana se aleja de las potencias economicas y cae en el ranking del FMI al puesto 14, adelantada por Australia y Mexico",
        claim_date="2026-08-28",
        post_url="https://www.elespanol.com/invertia/economia/macroeconomia/20260828/espana-aleja-potencias-economicas-cae-ranking-fmi-puesto-adelantada-australia-mexico/1003744365763_0.html",
        post_url_tipo="prensa", emisor="El Espanol", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="economia",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="FMI - World Economic Outlook abril 2026, indicador NGDPD (PIB a precios corrientes, miles de millones USD), via DataMapper API",
        primaria_url="https://www.imf.org/external/datamapper/api/v1/NGDPD?periods=2024,2025,2026",
        primaria_url_tipo="api_json (todos los paises y anios); la pagina HTML del DataMapper es solo JS; la base WEO oct-2025 en imf.org/en/Publications devolvio 403",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2026 (proyeccion WEO abr-2026): ESP 2.091,2 -> puesto 14 de 197; AUS 2.124,0 (12), MEX 2.120,9 (13)",
        dato_anterior="2025: ESP 1.903,8 -> puesto 12; KOR 1.872,4 (13), AUS 1.840,0 (14), MEX 1.832,6 (15). ESP 2025->2026: +9,84% en USD",
        raw_value_span_actual=(
            "[FMI DataMapper API, NGDPD, WEO abril 2026] 'ESP': {'2025': 1903.826, '2026': 2091.222} | "
            "'AUS': {'2025': 1839.961, '2026': 2123.963} | 'MEX': {'2025': 1832.641, '2026': 2120.855} | "
            "indicador: 'GDP, current prices' 'Billions of U.S. dollars' source: 'World Economic Outlook "
            "(April 2026)' || ranking calculado en research/evidencia/C07_fmi_ngdpd_ranking.txt || "
            "[El Espanol 2026-08-28, el claim] 'Espana se aleja de las potencias economicas y cae en el "
            "ranking del FMI al puesto 14, adelantada por Australia y Mexico' | 'Nuestro pais ocupaba la "
            "posicion 12 en 2025' | 'poco mas de 2 billones de dolares' (2026) | '1,9 billones de "
            "dolares' (2025)"
        ),
        raw_value_span_anterior=(
            "[misma API, valores 2025] 'ESP': 1903.826 -> puesto 12 entre 197 paises (excluidos agregados "
            "regionales). La PUBLICACION anterior (base de datos WEO octubre 2025, "
            "imf.org/en/Publications/WEO/weo-database/2025/October) devolvio HTTP 403 al fetcher"
        ),
        truth="supported", context="divergence_detected",
        clase_primaria="1_ranking_vs_value", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "CASO CANONICO, verificado por API en menos de 3 minutos. El puesto cae de 12 a 14 y todas "
            "las cifras del articulo cuadran con el FMI, pero el PIB de Espana en dolares SUBE un 9,84% "
            "(1.903,8 -> 2.091,2): Espana no 'se aleja', Australia y Mexico crecen mas rapido en dolares "
            "y la adelantan por 33.000 y 30.000 millones. Ranking baja, valor sube: 1_ranking_vs_value. "
            "Matiz temporal: 2026 es una PROYECCION del WEO de abril y el titular la cuenta en presente "
            "('cae'); el cuerpo dice 'previsiones'. Recuperacion: la pagina HTML del DataMapper es solo "
            "JS (nada para el fetcher), la API JSON del mismo publicador lo da todo, y el ranking se "
            "calcula en local excluyendo los agregados regionales del FMI (MAE, APQ, WHQ..., que tienen "
            "codigo de 3 letras como los paises: hay que filtrar con /api/v1/countries). DEC-018: la "
            "base WEO de octubre 2025 en imf.org/en/Publications devolvio 403, no se reintento; la "
            "edicion anterior del DATO (2025) esta en la misma API, la PUBLICACION anterior no es "
            "alcanzable para el agente. Sin nota metodologica localizada (solo metadatos del indicador)."
        ),
        criba_query_a="Espana ranking FMI puesto 14 2026 Australia Mexico",
        criba_query_b="Espana cae ranking FMI puesto 14 potencias economicas verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K37", case_id="C08",
        claim_text="El FMI certifica el fracaso economico espanol, Sanchez hunde nuestra economia al puesto 14",
        claim_date="2026-08-28",
        post_url="https://www.libertaddigital.com/libremercado/2026-08-28/el-fmi-certifica-el-fracaso-economico-espanol-sanchez-hunde-nuestra-economia-al-puesto-14-7452556/",
        post_url_tipo="prensa", emisor="Libertad Digital", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="economia",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="FMI - WEO abril 2026, NGDPD via DataMapper API (misma primaria que C07)",
        primaria_url="https://www.imf.org/external/datamapper/api/v1/NGDPD?periods=2024,2025,2026",
        primaria_url_tipo="api_json (ver C07)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2026 (proyeccion): ESP 2.091,2 puesto 14; AUS 2.124,0 (12); MEX 2.120,9 (13). El articulo: 'Australia (2,12 billones), Mexico (2,12 billones) y Espana (2,09 billones)'",
        dato_anterior="2025: ESP 1.903,8 puesto 12. ESP 2025->2026: +9,84% en USD (el articulo no lo menciona)",
        raw_value_span_actual=(
            "[Libertad Digital 2026-08-28, el claim] 'El FMI certifica el fracaso economico espanol, "
            "Sanchez hunde nuestra economia al puesto 14' | 'Australia (2,12 billones de dolares), Mexico "
            "(2,12 billones de dolares) y Espana (2,09 billones de dolares)' | 'desde 2010, el pais se ha "
            "situado entre el duodecimo y el decimocuarto puesto' || [FMI API] ver C07"
        ),
        raw_value_span_anterior="[FMI API, 2025] 'ESP': 1903.826 -> puesto 12 (ver C07 y research/evidencia/C07_fmi_ngdpd_ranking.txt)",
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="1_ranking_vs_value", abstain_reason="UNSUPPORTED_CLAIM_TYPE",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "Mismo dato que C07 con dos capas mas de encuadre. (1) Los numeros del cuerpo son correctos "
            "y cuadran con la API al decimal. (2) 'Sanchez hunde nuestra economia': atribucion causal "
            "que solo existe en el titular; el cuerpo no la sostiene, explica la caida por poblacion y "
            "reconoce que Espana lleva 'entre el duodecimo y el decimocuarto puesto desde 2010'. Es "
            "clase 6/7, fuera de tesis: other_observed, y para la componente causal el sistema "
            "abstiene con UNSUPPORTED_CLAIM_TYPE. (3) 'hunde' con un PIB que crece 9,84% en dolares es "
            "la misma divergencia ranking-vs-valor de C07, aqui en secundaria. (4) 'certifica el fracaso': "
            "el FMI publica una proyeccion, no un veredicto. Truth = mixed. Localizar y extraer no "
            "costaron nada: la primaria ya estaba en mano."
        ),
        criba_query_a="Espana ranking FMI puesto 14 2026 Australia Mexico",
        criba_query_b="Espana cae ranking FMI puesto 14 potencias economicas verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K06", case_id="C09",
        claim_text="Espana ya no esta entre los lideres de Internet: cae 12 puestos en un ranking global",
        claim_date="2026-07",
        post_url="https://www.adslzone.net/noticias/internet/espana-internet-cae-global-puestos-ranking-lideres/",
        post_url_tipo="prensa", emisor="ADSLZone", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="ES", tema="tecnologia",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Saily (eSIM de Nord Security) - Internet Connectivity Index 2026, 97 paises, 4 pilares",
        primaria_url="https://saily.com/internet-connectivity-index/",
        primaria_url_tipo="pagina_de_indice_corporativo; el buscador la describe como 'scored countries in four pillars in 2025 and 2026' (ambas ediciones en la misma pagina)",
        via_de_acceso="bloqueado", access_requires_login="no_verificable",
        current_edition_found="no", previous_edition_found="no",
        historical_series_found="no", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="probable",
        recuperabilidad="D", formato="html",
        dato_actual="2026 (segun las secundarias): puesto 17 de 97, 58,75 puntos. NO extraido de la primaria",
        dato_anterior="2025 (segun las secundarias): puesto 5, sin puntuacion. NO extraido de la primaria",
        raw_value_span_actual=(
            "[SECUNDARIA adslzone 2026-07-08] 'Espana ya no esta entre los lideres de Internet: cae 12 "
            "puestos en un ranking global' | 'puesto 17' 'puntuacion global de 58,75 puntos' | 'Espana no "
            "ha empeorado de forma clara, sino que el resto del mundo ha acelerado' || [SECUNDARIA "
            "zonamovilidad 2026-07-11] 'situa a Espana en la decimoseptima posicion entre los 97 paises "
            "analizados' | 'El descenso de Espana desde el quinto puesto alcanzado en la edicion anterior "
            "hasta la posicion numero 17' | 'cuatro grandes indicadores con el mismo peso: ciberseguridad, "
            "calidad del servicio, asequibilidad de los datos moviles y libertad en internet'"
        ),
        raw_value_span_anterior="",
        truth="insufficient_evidence", context="undetermined",
        clase_primaria="1_ranking_vs_value", clases_secundarias="", abstain_reason="PRIMARY_SOURCE_NOT_FOUND",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "PRIMER BLOQUEO DEL LOTE. saily.com/internet-connectivity-index/ devuelve HTTP 403 al "
            "fetcher y tambien a curl con su user-agent por defecto (5.526 bytes de pagina de bloqueo). "
            "DEC-018: no se prueba con otro UA ni se busca copia. La primaria esta localizada (URL "
            "conocida, indexada por el buscador con descripcion de contenido) y un humano con navegador "
            "probablemente la abre; el agente no. Ninguna de las dos secundarias enlaza a la fuente. "
            "Clase 1_ranking_vs_value es HIPOTESIS de la propia secundaria ('no ha empeorado... el resto "
            "ha acelerado'), no verificacion: sin la puntuacion de 2025 no se puede saber si el valor de "
            "Espana se movio. Subtipo de abstencion: bloqueado_por_publicador. Cuenta como NO "
            "recuperable-por-agente en la metrica de la puerta; para la humana, probable. Emisor de "
            "nivel 5 (indice corporativo de una marca de eSIM): prediccion 4 y 5 del plan, las dos."
        ),
        criba_query_a="Espana cae 12 puestos ranking Internet conectividad 2026",
        criba_query_b="Espana cae 12 puestos ranking Internet lideres 2026 verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K07", case_id="C10",
        claim_text="Espana cae al puesto 44 del ranking fiscal para mudarse al extranjero: Malta y Chipre lideran Europa",
        claim_date="2026-09",
        post_url="https://www.elboletin.com/espana-cae-al-puesto-44-del-ranking-fiscal-para-mudarse-al-extranjero-malta-y-chipre-lideran-europa/",
        post_url_tipo="prensa", emisor="El Boletin", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="ES", tema="fiscalidad",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Global Citizen Solutions / Global Intelligence Unit - briefing 'Tax Optimization for Global Citizens: Comparing 48 Jurisdictions' (2026-09-16)",
        primaria_url="https://www.globalcitizensolutions.com/briefing/tax-optimization-for-global-citizens/",
        primaria_url_tipo="pagina_html_con_tabla (indice corporativo); sin descarga de datos",
        via_de_acceso="html", access_requires_login="no",
        current_edition_found="si", previous_edition_found="no",
        historical_series_found="no", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="html",
        dato_actual="2026, primera edicion (2026-09-16): Espana puesto 44 de 48, compuesto 36,9 (Tax Burden 25, Tax Structure 49, Investment Migration n/a); Malta 6o 74,4; Chipre 10o 73,4",
        dato_anterior="NO EXISTE: es la primera edicion del indice. GCS publica ediciones 2025 de otros informes (pasaportes, nomadas digitales, retiro), no de este",
        raw_value_span_actual=(
            "[GCS, briefing 2026-09-16, tabla] 'Spain | Europe | 36.9 | 25 | 49 | n/a' (puesto 44) | 'Malta "
            "| Europe | 74.4 | 82 | 63 | 83' (6) | 'Cyprus | Europe | 73.4 | 82 | 63 | 78' (10) | 'The "
            "jurisdictions are evaluated across 11 indicators grouped into three pillars, selected for "
            "their practical bearing on where a mobile individual can efficiently establish tax residence.' "
            "|| [SECUNDARIA elboletin, titular via snippet de busqueda; el articulo devolvio 403] 'Espana "
            "cae al puesto 44 del ranking fiscal para mudarse al extranjero: Malta y Chipre lideran Europa'"
        ),
        raw_value_span_anterior="",
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="", abstain_reason="PREVIOUS_EDITION_NOT_FOUND",
        abandonado_por_tiempo="", bucket_resultado="edicion_anterior_no_localizable", excedente="no",
        notas=(
            "El puesto (44 de 48) y las puntuaciones son literales de la tabla del emisor. Pero el "
            "indice es de PRIMERA EDICION (publicado 2026-09-16; el sitio de GCS no tiene una version "
            "2025 de este briefing, aunque si de otros informes) y el titular dice 'cae al puesto 44': "
            "no hay edicion anterior desde la que caer. Es el patron temporal de P05: cifra real, marco "
            "cronologico no respaldado. Matiz linguistico: en titulares espanoles 'cae al puesto N' a "
            "veces significa solo 'queda en el puesto N'; aun asi, el verbo connota descenso y el "
            "sistema deberia responder 'no existe edicion anterior'. Truth = mixed (numero si, 'cae' no). "
            "Cubeta: edicion_anterior_no_localizable por construccion, no por fallo de busqueda. "
            "Acceso: la primaria respondio al fetcher (200, contenido real) pero devolvio 403 a curl con "
            "UA por defecto, y el articulo de El Boletin devolvio 403 al fetcher: 'alcanzable por "
            "agente' depende del agente; se registra tal cual. Metodologia: 11 indicadores en 3 pilares, "
            "descrita en la pagina. Emisor de nivel 5 que SI es productor de su dato: la prediccion 4 "
            "('la primaria de la prensa es otra secundaria') no aplica aqui."
        ),
        criba_query_a="Espana puesto 44 ranking fiscal mudarse extranjero Malta Chipre",
        criba_query_b="Espana puesto 44 ranking fiscal expatriados Malta Chipre verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K09", case_id="C11",
        claim_text="El IPC de agosto de 2026 se dispara al 4,3%: la tasa mas alta en mas de tres anos",
        claim_date="2026-09-15",
        post_url="https://www.que.es/2026/09/15/ipc-agosto-2026-maximo-tres-anos/",
        post_url_tipo="prensa", emisor="Que.es", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="precios",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INE - Indice de Precios de Consumo: notas de prensa mensuales (base 2025) + API JSON tabla 50913 (base 2021, hasta dic-2025)",
        primaria_url="https://www.ine.es/dyngs/Prensa/IPC0826.htm",
        primaria_url_tipo="nota_de_prensa_html con anexo XLSX (/prensa/anexo_tablas/es/IPC0826.xlsx) y metodologia; serie historica por API wstempus",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="agosto 2026: variacion anual 4,3% (base 2025), mensual 0,7%, subyacente 2,9%; 'la mas alta desde febrero de 2023'",
        dato_anterior=(
            "julio 2026: anual 3,6%, mensual 0,3%, subyacente 3,0%. Serie 2026 (notas): ene 2,3 | feb 2,3 | "
            "mar 3,4 | abr 3,2 | may 3,2 | jun 3,2 | jul 3,6 | ago 4,3. Serie base 2021 (API tabla 50913, "
            "serie IPC251856 Nacional): feb-2023 6,0; maximo mar-2023..dic-2025 = 4,1 (abr-2023). "
            "Ver research/evidencia/C11_ine_ipc_variacion_anual.txt"
        ),
        raw_value_span_actual=(
            "[INE, nota IPC0826, 2026-09-15] 'La tasa de variacion anual del IPC del mes de agosto se "
            "situo en el 4,3%, siete decimas por encima de la registrada en julio.' | 'Es la mas alta "
            "desde febrero de 2023.' | 'En agosto la tasa mensual del IPC general fue del 0,7%.' | 'La "
            "variacion anual de la inflacion subyacente (indice general sin alimentos no elaborados ni "
            "productos energeticos) se situo en el 2,9%.' || [que.es 2026-09-15, el claim] 'El IPC de "
            "agosto de 2026 se dispara al 4,3%: la tasa mas alta en mas de tres anos' | 'su nivel mas "
            "alto desde febrero de 2023'"
        ),
        raw_value_span_anterior=(
            "[INE, nota IPC0726, 2026-08-13] 'La tasa de variacion anual del IPC del mes de julio se "
            "situo en el 3,6%, cuatro decimas por encima de la registrada en junio.' | 'La variacion "
            "mensual del indice general fue del 0,3%.' || [INE API, tabla 50913, serie IPC251856] "
            "2023-02: 6.0 | 2023-04: 4.1 (max intermedio) | 2025-12: 2.9"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Verificado sin fiarse de la frase del emisor: 'mas alta desde febrero de 2023' se contrasto "
            "contra la serie completa. feb-2023 = 6,0 >= 4,3 y ningun mes entre mar-2023 y jul-2026 "
            "supera 4,1. 'Mas de tres anos' = 3 anos y 6 meses: correcto. Que.es reproduce la nota, "
            "atribuye la subida a carburantes (coincide con el INE: transporte) y enlaza al INE. "
            "HALLAZGO de recuperabilidad: el INE cambio el IPC a base 2025 en enero de 2026 ('publica "
            "hoy, por primera vez, el IPC e IPCA definitivos en la nueva base 2025') y la tabla de la API "
            "que sirve la serie historica (50913, base 2021) TERMINA en dic-2025; la tabla de la base "
            "nueva no se localizo por id, asi que 2026 se reconstruyo con 8 notas mensuales. La serie "
            "existe y es continua para un humano; para un agente esta partida en dos tablas con ids "
            "distintos. Tambien: el filtro de comunidad autonoma de la API (tv=70:9003) resulto ser "
            "Castilla y Leon, no el total nacional; hubo que pedir las 20 series y elegir 'Nacional' por "
            "nombre. Metodologia: 'Principales caracteristicas del IPC base 2025' enlazada en la nota."
        ),
        criba_query_a="IPC agosto 2026 4,3% tasa mas alta tres anos",
        criba_query_b="IPC agosto 2026 4,3% inflacion Espana bulo OR verificacion OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K12", case_id="C12",
        claim_text="Desempleo en Colombia: a julio del 2026 el indicador presento una baja y se ubico en el 8,1%",
        claim_date="2026-08-31",
        post_url="https://www.portafolio.co/economia/desempleo-en-colombia-a-julio-del-2026-el-indicador-presento-una-baja-y-se-ubico-en-el-8-501496",
        post_url_tipo="prensa", emisor="Portafolio", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="CO", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="DANE - GEIH, Boletin tecnico Principales indicadores del mercado laboral, julio 2026 (2026-08-31)",
        primaria_url="https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-jul2026.pdf",
        primaria_url_tipo="pdf_boletin_mensual por patron bol-GEIH-<mes><anio>.pdf; anexos XLSX (anex-GEIH-jul2026.xlsx, anex-GEIH-Desestacionalizado-jul2026.xlsx); metodologia y ficha metodologica enlazadas",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="julio 2026: TD nacional 8,1% (-0,7 pp vs julio 2025: 8,8%); TGP 64,8%; TO 59,5%; 13 ciudades 8,5% (vs 8,4%)",
        dato_anterior="junio 2026: TD nacional 8,0% (junio 2025: 8,6%); 13 ciudades 8,0% (vs 8,3%). Portafolio escribe 'junio 8,2%': error",
        raw_value_span_actual=(
            "[DANE, Boletin tecnico GEIH julio 2026, 2026-08-31, p.1] 'Para el mes de julio de 2026, la "
            "tasa de desocupacion del total nacional fue 8,1%, lo que represento una disminucion de 0,7 "
            "puntos porcentuales respecto al mismo mes de 2025 (8,8%). La tasa global de participacion se "
            "ubico en 64,8% y la tasa de ocupacion en 59,5%' | 'En julio de 2026, la tasa de desocupacion "
            "en el total de las 13 ciudades y areas metropolitanas fue 8,5%, mientras que en el mismo mes "
            "de 2025 fue 8,4%' || [Portafolio 2026-08-31, el claim] 'Desempleo en Colombia: a julio del "
            "2026 el indicador presento una baja y se ubico en el 8,1%' | 'hace un ano la tasa de desempleo "
            "estuvo en 8,8%, lo que representa una caida de 0,7%' | 'En junio de 2026, ambos dominios "
            "habian registrado una tasa de 8,2%'"
        ),
        raw_value_span_anterior=(
            "[DANE, Boletin tecnico GEIH junio 2026, 2026-07-31, p.1] 'Para junio de 2026, la tasa de "
            "desocupacion del total nacional fue 8,0%, mientras que en el mismo mes de 2025 fue 8,6%.' | "
            "'En junio de 2026, la tasa de desocupacion en el total de las 13 ciudades y areas "
            "metropolitanas fue 8,0%, mientras que en el mismo mes de 2025 fue 8,3%.'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "El titular es correcto y esta bien enmarcado (comparacion interanual del mismo mes). Dos "
            "imprecisiones en el cuerpo de la secundaria: (a) 'una caida de 0,7%' donde el DANE dice "
            "'0,7 puntos porcentuales' (8,8 -> 8,1 es -8% relativo, -0,7 pp absoluto); (b) 'en junio de "
            "2026 ambos dominios habian registrado 8,2%' cuando el boletin de junio da 8,0% en los dos "
            "dominios. Ninguna afecta al claim. La frase 'la tasa de desocupacion mas baja para un julio' "
            "es cita del director del DANE en prensa, no esta en el boletin; no se contrasto contra la "
            "serie de julios (esta en el anexo XLSX, no extraido). Primaria ejemplar: PDF con texto, "
            "patron de URL por mes, anexos XLSX, desestacionalizado, metodologia y ficha metodologica. "
            "El fetcher no lee el PDF; pypdf si. La informalidad (54,5%) que menciona Portafolio no esta "
            "en este boletin: es de otra publicacion del DANE (ver C13)."
        ),
        criba_query_a="desempleo Colombia julio 2026 8,1% DANE",
        criba_query_b="desempleo Colombia 8,1% julio 2026 verificacion OR bulo OR fact-check OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K38", case_id="C13",
        claim_text="Desempleo en Colombia cayo a 8,1% en julio, pero la informalidad llego a 54,5%: de cada 100 ocupados, 50 estan en el rebusque",
        claim_date="2026-08-31",
        post_url="https://www.radiosantafe.com/2026/08/31/desempleo-en-colombia-cayo-a-81-en-julio-pero-la-informalidad-llego-a-545-de-cada-100-ocupados-50-estan-en-el-rebusque/",
        post_url_tipo="prensa", emisor="Radio Santa Fe", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="CO", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="DANE - GEIH: presentacion rueda de prensa julio 2026 (serie mensual de informalidad) + Ocupacion informal, boletin GEIHEISS trimestre movil may-jul 2026",
        primaria_url="https://www.dane.gov.co/files/operaciones/GEIH/pres-GEIH-jul2026.pdf",
        primaria_url_tipo="pdf_presentacion (69 pp, serie de julios en etiquetas de grafico) + pdf_boletin GEIHEISS por patron; anexos XLSX; dos docs de metodologia",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="julio 2026 (mensual): proporcion de informalidad 54,5%. Trimestre movil may-jul 2026: 54,6% (mismo periodo 2025: 55,0%)",
        dato_anterior="julio 2025 (mensual): 54,8%. Serie de julios: 2021 58,9 | 2022 58,1 | 2023 56,3 | 2024 56,0 | 2025 54,8 | 2026 54,5 -> la informalidad BAJA seis anos seguidos",
        raw_value_span_actual=(
            "[DANE, presentacion GEIH julio 2026, slide Informalidad, etiquetas del grafico] '58,9 58,1 "
            "56,3 56,0 54,8 54,5' para 'Jul 21 Jul 22 Jul 23 Jul 24 Jul 25 Jul 26' | 'Proporcion de "
            "informalidad (PI) % PI = I / OC * 100' || [DANE, boletin GEIHEISS may-jul 2026, 2026-09-11] "
            "'Para el total nacional, en el trimestre movil mayo - julio 2026 la proporcion de personas "
            "ocupadas informales fue 54,6%, mientras que en el mismo periodo del ano anterior fue 55,0%.' "
            "|| [SECUNDARIA Radio Santa Fe 2026-08-31, titular via snippet; el sitio rechazo la conexion] "
            "'Desempleo en Colombia cayo a 8,1% en julio, pero la informalidad llego a 54,5%: de cada 100 "
            "ocupados, 50 estan en el rebusque'"
        ),
        raw_value_span_anterior=(
            "[DANE, presentacion GEIH julio 2026] etiqueta 'Jul 25' = '54,8' || [DANE, boletin GEIHEISS "
            "may-jul 2026] 'en el mismo periodo del ano anterior fue 55,0%' || [DANE, boletin GEIHEISS "
            "abr-jun 2026, 2026-08-13, descargado] 'la proporcion de hombres ocupados informales en el "
            "trimestre abril - junio 2026 fue 56,7%, mientras que las mujeres ocupadas informales fueron "
            "el 51,5%' (la frase del total nacional no se capturo con el patron de busqueda)"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="other_observed", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="no",
        notas=(
            "54,5% es literal (julio 2026, total nacional). Dos problemas de encuadre: (1) 'pero la "
            "informalidad LLEGO a 54,5%' presenta el dato como contrapunto negativo al descenso del paro, "
            "sugiriendo subida, cuando la serie del propio DANE muestra que BAJA por sexto julio "
            "consecutivo (54,8 en 2025) y el trimestre movil tambien cae (55,0 -> 54,6); Portafolio, con "
            "el mismo dato, escribio 'se redujo en todos los dominios'. (2) 'de cada 100 ocupados, 50' "
            "redondea 54,5 hacia abajo: son 55 de cada 100 (o 'mas de la mitad'). 'Rebusque' es "
            "coloquial por informal. Truth = mixed; la divergencia computable es la direccion omitida: "
            "cifra real sin su edicion anterior, marco no respaldado (clase 7 -> other_observed). SEXTO "
            "divergente: llena la cubeta. Primaria: la informalidad esta en una operacion aparte del "
            "DANE (GEIHEISS, trimestre movil) y el dato MENSUAL solo aparece en las etiquetas del grafico "
            "de la presentacion de prensa (PDF de 69 pp, extraible con pypdf), no en el boletin del "
            "mercado laboral. La secundaria (radiosantafe.com) rechazo la conexion: claim registrado "
            "desde el snippet del buscador."
        ),
        criba_query_a="desempleo Colombia julio 2026 8,1% DANE",
        criba_query_b="desempleo Colombia 8,1% julio 2026 verificacion OR bulo OR fact-check OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K13a", case_id="C14",
        claim_text="Inflacion en agosto de 2026 se ubica en 3.26%: Inegi",
        claim_date="2026-09-09",
        post_url="https://www.razon.com.mx/negocios/2026/09/09/inflacion-en-agosto-de-2026-se-ubica-en-326-inegi/",
        post_url_tipo="prensa", emisor="La Razon de Mexico", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="MX", tema="precios",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEGI - Boletin de indicador 586/26, INPC agosto 2026 (publicado 2026-09-09)",
        primaria_url="https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_09.pdf",
        primaria_url_tipo="pdf_boletin_mensual con tabla; TRAMPA: el sufijo _MM es el mes de PUBLICACION (agosto = _09, julio = _08); API del INEGI requiere token",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="agosto 2026: inflacion general anual 3,26%; mensual +0,20%; INPC 145,462; subyacente anual 3,88%; agosto 2025: anual 3,57%",
        dato_anterior="julio 2026 (boletin 481/26, 2026-08-07): inflacion anual 3,12%; INPC 145,169; subyacente 3,95%",
        raw_value_span_actual=(
            "[INEGI, boletin 586/26, 2026-09-09, p.1] 'La inflacion anual fue de 3.26 % en agosto de "
            "2026' | 'En agosto de 2026, el INPC presento un nivel de 145.462 puntos: aumento 0.20 % "
            "respecto al mes anterior. Con este resultado, la inflacion general anual se ubico en 3.26 "
            "por ciento. En el mismo mes de 2025, la inflacion mensual fue de 0.06 % y la anual, de 3.57 "
            "%' | [cuadro 1, fila INPC, anual 2024/2025/2026] '4.99 3.57 3.26' || [La Razon 2026-09-09, "
            "el claim] 'Inflacion en agosto de 2026 se ubica en 3.26%: Inegi' | 'la inflacion general "
            "anual se ubico en 3.26 por ciento'"
        ),
        raw_value_span_anterior=(
            "[INEGI, boletin 481/26, 2026-08-07, p.1] 'La inflacion anual fue de 3.12 % en julio de 2026' "
            "| 'En julio de 2026, el INPC presento un nivel de 145.169 puntos: aumento 0.03 % respecto al "
            "mes anterior' || [INEGI, boletin 514/25, 2025-09-09] 'La inflacion anual fue de 3.57 %, en "
            "agosto de 2025'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Titular neutro que reproduce el dato sin afirmar direccion, con INPC, mensual y subyacente "
            "correctos al decimal. Control negativo. HALLAZGO de recuperabilidad: el patron de URL de "
            "los boletines del INEGI (inpc_2q<anio>_<MM>.pdf) usa el mes de PUBLICACION: _08 (boletin "
            "481/26, 7 de agosto) reporta JULIO y _09 (586/26, 9 de septiembre) reporta AGOSTO. Un agente "
            "que infiera la URL por el mes del dato extrae la edicion equivocada, como paso aqui en el "
            "primer intento; se corrigio leyendo la cabecera del PDF. El fetcher no lee estos PDF, pypdf "
            "si. La API del INEGI exige token (no se uso); el boletin y el BIE no. Sin documento de "
            "metodologia localizado en esta pasada (el boletin da la definicion del INPC, no la "
            "metodologia)."
        ),
        criba_query_a="inflacion Mexico agosto 2026 3.26% Inegi",
        criba_query_b="inflacion Mexico agosto 2026 3.26 \"baja\" OR \"sube\" verificacion OR bulo OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K13b", case_id="C15",
        claim_text="Inflacion en Mexico baja a 3.26% anual en agosto de 2026",
        claim_date="2026-09-09",
        post_url="https://enfoquenoticias.com.mx/noticias/inflacion-mexico-agosto-2026-inpc-3-26-por-ciento",
        post_url_tipo="prensa", emisor="Enfoque Noticias", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="MX", tema="precios",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEGI - Boletin 586/26, INPC agosto 2026 (misma primaria que C14)",
        primaria_url="https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_09.pdf",
        primaria_url_tipo="pdf_boletin_mensual (ver C14)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="agosto 2026: anual 3,26%. Contra julio 2026 (3,12): SUBE 0,14 pp. Contra agosto 2025 (3,57): BAJA 0,31 pp",
        dato_anterior="julio 2026: 3,12% (boletin 481/26). agosto 2025: 3,57% (boletin 514/25)",
        raw_value_span_actual=(
            "[INEGI, boletin 586/26] 'La inflacion anual fue de 3.26 % en agosto de 2026' | 'aumento "
            "0.20 % respecto al mes anterior' | 'En el mismo mes de 2025, la inflacion mensual fue de 0.06 "
            "% y la anual, de 3.57 %' || [SECUNDARIA Enfoque Noticias 2026-09-09, titular via snippet; el "
            "articulo devolvio 403] 'Inflacion en Mexico baja a 3.26% anual en agosto de 2026'"
        ),
        raw_value_span_anterior="[INEGI, boletin 481/26] 'La inflacion anual fue de 3.12 % en julio de 2026' || [INEGI, boletin 514/25] 'La inflacion anual fue de 3.57 %, en agosto de 2025'",
        truth="mixed", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="si",
        notas=(
            "'Baja a 3.26% anual' no dice contra que. Contra el mes anterior (3,12), que es la lectura "
            "estandar de un dato mensual y la que abre el propio boletin ('aumento 0.20 % respecto al "
            "mes anterior'; tras cuatro meses de descensos, la anual se acelera), es FALSO. Contra agosto "
            "de 2025 (3,57) es cierto, y el boletin da esa comparacion en la misma frase. Par natural con "
            "C14 (mismo dato, titular neutro) y con la prensa que titulo 'se acelera' / 'repunta' (La "
            "Jornada, Lopez-Doriga, La Voz de Michoacan). Truth = mixed (cierto bajo una base, falso bajo "
            "la habitual); divergencia por base no declarada: 2_baseline_selection. EXCEDENTE: la cubeta "
            "de divergencia_real ya tenia 6 (C02, C03, C05, C07, C08, C13) cuando se trabajo este caso; "
            "no entra en los 20 pero se conserva. La secundaria (enfoquenoticias.com.mx) devolvio 403; "
            "no se pudo ver si el cuerpo declara la base. Sin costo de localizacion: primaria en mano."
        ),
        criba_query_a="inflacion Mexico agosto 2026 3.26% Inegi",
        criba_query_b="inflacion Mexico agosto 2026 3.26 \"baja\" OR \"sube\" verificacion OR bulo OR falso",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K15", case_id="C16",
        claim_text="La tasa de paro juvenil cae al 23,77% pese a sumar 19.600 desempleados",
        claim_date="2026-07-28",
        post_url="https://www.infobae.com/espana/agencias/2026/07/28/la-tasa-de-paro-juvenil-cae-al-2377-pese-a-sumar-19600-desempleados/",
        post_url_tipo="prensa", emisor="Infobae (agencias)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INE - EPA 2T2026 via API JSON: tasas por grupo de edad (tabla 65334) y parados por grupo de edad en miles (tabla 65218)",
        primaria_url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65334?nult=3&tip=A",
        primaria_url_tipo="api_json; la nota de prensa EPA2T26.htm no trae el desglose por edad en texto, enlaza anexo ZIP, tablas y metodologia; la tabla antigua 4247 termina en 2023-T4",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: tasa de paro menores de 25 = 23,77%; parados 16-19 = 145,7 mil + 20-24 = 314,3 mil = 460,0 mil. Tasa general 9,87%, parados 2.495.300",
        dato_anterior="1T2026: tasa menores de 25 = 24,54%; parados 16-19 = 111,9 + 20-24 = 328,5 = 440,4 mil. 2T-1T: tasa -0,77 pp, parados +19,6 mil. (2025-T4: 23,01%; 407,9 mil)",
        raw_value_span_actual=(
            "[INE API, tabla 65334, serie EPA452436 'Tasa de paro de la poblacion. Ambos sexos. Total "
            "Nacional. Menores de 25 anos.'] 2026-T2: 23.77 | [INE API, tabla 65218] EPA387809 'De 16 a "
            "19 anos. Parados. Valor absoluto.' 2026-T2: 145.7 | EPA387815 'De 20 a 24 anos. Parados. "
            "Valor absoluto.' 2026-T2: 314.3 || [INE, nota EPA2T26, 2026-07-28] 'La tasa de paro fue del "
            "9,87% este trimestre, 96 centesimas menos que en el anterior.' | 'El paro bajo en 213.300 "
            "personas, hasta 2.495.300.' || [Infobae 2026-07-28, el claim] 'La tasa de paro juvenil cae "
            "al 23,77 % pese a sumar 19.600 desempleados' | 'La tasa de paro entre los menores de 25 anos "
            "se situo en el segundo trimestre en el 23,77 %, 0,77 puntos por debajo de la del primer "
            "trimestre' | 'un total de 460.000 menores de 25 anos en situacion de desempleo' || ver "
            "research/evidencia/C16_ine_epa_paro_juvenil.txt"
        ),
        raw_value_span_anterior=(
            "[INE API, tabla 65334, EPA452436] 2026-T1: 24.54 | [tabla 65218] EPA387809 2026-T1: 111.9 | "
            "EPA387815 2026-T1: 328.5 (suma 440.4)"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="no",
        notas=(
            "Las dos cifras del titular son exactas al decimal segun la API del INE: la tasa baja 0,77 pp "
            "(24,54 -> 23,77) y los parados menores de 25 suben 19,6 mil (440,4 -> 460,0). Tasa y numero "
            "se mueven en sentido contrario porque la poblacion activa joven crecio mas que el paro; el "
            "titular no lo explica, pero presenta las dos magnitudes juntas y con 'pese a', sin elegir "
            "una para enganar: es la version bien enmarcada del patron de P19. Control negativo; llena la "
            "cubeta (7/7). Recuperacion: la nota de prensa de la EPA no da el desglose por edad en texto "
            "(esta en el anexo ZIP y en las tablas); la API lo da directo. Mismo patron que el IPC: la "
            "tabla antigua (4247) se congelo en 2023-T4 con la nueva base de la EPA y hay que saber que "
            "la vigente es la 65334; el agregado 'Menores de 25' existe en tasas pero en parados hay que "
            "sumar 16-19 y 20-24. Verificacion cruzada gratuita: 2025-T4 suma 407,9 mil, el '407.900' "
            "que citaba P19 en la auditoria."
        ),
        criba_query_a="paro juvenil 23,77% segundo trimestre 2026 Espana",
        criba_query_b="paro juvenil Espana 23,77% 2T 2026 verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K39", case_id="C17",
        claim_text="La tasa de paro juvenil escala hasta el 24,5% en el segundo trimestre",
        claim_date="2026-07-28",
        post_url="https://www.pressdigital.es/articulo/economia/2026-07-28/5967467-tasa-paro-juvenil-escala-hasta-245-segundo-trimestre",
        post_url_tipo="prensa", emisor="Pressdigital", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INE - EPA 2T2026 via API JSON (tablas 65334 y 65218), misma primaria que C16",
        primaria_url="https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65334?nult=3&tip=A",
        primaria_url_tipo="api_json (ver C16)",
        via_de_acceso="api", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="2T2026: tasa de paro menores de 25 = 23,77% (BAJA 0,77 pp). El titular dice 24,5% y 'escala'",
        dato_anterior="1T2026: 24,54% (el 24,5% del titular es este, el del trimestre ANTERIOR)",
        raw_value_span_actual=(
            "[INE API, tabla 65334, EPA452436] 2026-T1: 24.54 | 2026-T2: 23.77 || [pressdigital 2026-07-28, "
            "el claim, titular] 'La tasa de paro juvenil escala hasta el 24,5% en el segundo trimestre' | "
            "[mismo articulo, cuerpo] '23,77% a cierre del segundo trimestre, 0,74 puntos porcentuales por "
            "debajo del primer trimestre del ano (24,5%)' | 'bajo' | '460.000 jovenes en situacion de "
            "desempleo al finalizar junio'"
        ),
        raw_value_span_anterior="[INE API, tabla 65334, EPA452436] 2026-T1: 24.54",
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="claim_falso", excedente="no",
        notas=(
            "El titular es falso en el numero y en la direccion: la tasa del 2T es 23,77% y BAJA; 24,5% "
            "es la del 1T. El propio cuerpo del articulo lo dice bien ('23,77% ... 0,74 puntos por debajo "
            "del primer trimestre (24,5%)', 'bajo'), asi que el titular contradice su texto: error de "
            "edicion, no de dato. No hay divergencia contextual que evaluar (context = "
            "no_divergence_detected): el eje truth basta, es la celda contradicted x no_divergence de "
            "DEC-016. Cubeta nueva claim_falso, sin objetivo. El '0,74' del cuerpo frente al 0,77 del INE "
            "sale de redondear 24,54 a 24,5 antes de restar. Par natural con C16 (mismo dato, titular "
            "correcto). Sin costo de localizacion."
        ),
        criba_query_a="paro juvenil 23,77% segundo trimestre 2026 Espana",
        criba_query_b="paro juvenil Espana 23,77% 2T 2026 verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K16", case_id="C18",
        claim_text="La criminalidad en Espana registra un aumento del 0,5% hasta junio de 2026 por delitos sexuales, rinas y trafico de drogas",
        claim_date="2026-09-17",
        post_url="https://www.cordobabn.com/nacional/criminalidad-espana-sube-05-junio-2026-aumento-delitos-sexuales-rinas-trafico-drogas/20260917155447267986.html",
        post_url_tipo="prensa", emisor="Cordoba Buenas Noticias", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Ministerio del Interior - Balance Trimestral de Criminalidad, segundo trimestre 2026 (enero a junio), via Portal Estadistico de Criminalidad",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/publico/portalestadistico/dam/jcr:23d540f0-d4aa-40a9-a3c4-6378b6f3e017/Balance%20de%20Criminalidad%20Segundo%20Trimestre%202026.pdf",
        primaria_url_tipo="pdf_balance (512 pp, texto extraible) en el portal del ministerio; el mismo PDF en interior.gob.es devuelve 403 (Cloudflare); tablas PC-Axis 09004-09006 en /sec/dynPx/",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="ene-jun 2026: 1.217.476 infracciones penales, +0,5% sobre ene-jun 2025 (base revisada 1.211.083); libertad sexual +4,0% (10.545 -> 10.971); con penetracion +3,5% (2.654 -> 2.747); secuestro 51 -> 60 (+17,6%); patrimonio -3,6%",
        dato_anterior="ene-jun 2025 (Balance 2T2025): 1.212.268, -0,9% sobre 2024 (base 1.222.956). En el Balance 2T2026 la cifra de 2025 aparece REVISADA a 1.211.083",
        raw_value_span_actual=(
            "[Interior, Balance 2T2026, p. de resumen] 'el numero total de infracciones penales "
            "registradas en el periodo de enero a junio de 2026 suma un total de 1.217.476, con un "
            "aumento del +0,5% sobre el ano 2025' | 'los delitos contra la libertad sexual crecen un 4,0 % "
            "sobre 2025. Los delitos contra la libertad sexual con penetracion crecen en 2026 un 3,5% "
            "respecto a 2025' | 'han disminuido en conjunto un -3,6%' | [tabla nacional] 'III. TOTAL "
            "CRIMINALIDAD 1.211.083 1.217.476 0,5' | '4. Secuestro 51 60 17,6' | '5. Delitos contra la "
            "libertad sexual 10.545 10.971 4,0' || [cordobabn 2026-09-17, el claim] 'La criminalidad en "
            "Espana registra un aumento del 0,5% hasta junio de 2026 por delitos sexuales, rinas y trafico "
            "de drogas' | 'aumento del 17,5%, al pasar de 51 casos en el primer semestre de 2025 a 60 en 2026'"
        ),
        raw_value_span_anterior=(
            "[Interior, Balance 2T2025] 'el numero total de infracciones penales registradas en el periodo "
            "de enero a junio de 2025 suma un total de 1.212.268, con un descenso del -0,9% sobre el ano "
            "2024' | [tabla nacional] 'III. TOTAL CRIMINALIDAD 1.222.956 1.212.268 -0,9'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="si",
        notas=(
            "Reproduce fielmente el resumen del ministerio, con los mismos motores del aumento que "
            "senala el propio Balance. Control negativo; EXCEDENTE porque la cubeta ya tenia 7. Detalle: "
            "cordobabn da +17,5% en secuestros y el Balance +17,6% (60/51 = +17,65%), redondeo. HALLAZGO "
            "de revision: el Balance 2T2025 publico 1.212.268 para ene-jun 2025, pero el 2T2026 compara "
            "contra 1.211.083 (revisado, -1.185); el +0,5% se calcula sobre la base revisada, contra la "
            "cifra original seria +0,4%. Un sistema que guarde la edicion anterior tiene que saber que las "
            "bases se revisan. DEC-018: el PDF en interior.gob.es devolvio 403 (Cloudflare) y no se "
            "reintento; el Portal Estadistico de Criminalidad del MISMO ministerio publica el mismo PDF y "
            "tablas PC-Axis por trimestre (09004 CCAA, 09005 provincias, 09006 municipios): es la via "
            "dataset del mismo emisor, no un rodeo. Las paginas JAXI son solo JS; el indice pcaxis si "
            "lista los .px. Metodologia: PDFs por indicador en /metodologia.html."
        ),
        criba_query_a="criminalidad Espana aumento 0,5% primer semestre 2026 delitos sexuales",
        criba_query_b="criminalidad sube 0,5% hasta junio 2026 Espana verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K17", case_id="C19",
        claim_text="La criminalidad crece seis veces mas en la Comunidad de Madrid respecto al conjunto de Espana",
        claim_date="2026-09-18",
        post_url="https://zigzagdigital.com/art/31982/la-criminalidad-crece-seis-veces-mas-en-la-comunidad-de-madrid-respecto-al-conjunto-de-espana",
        post_url_tipo="prensa", emisor="ZigZag Digital", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Ministerio del Interior - Balance Trimestral de Criminalidad 2T2026, tabla 'MADRID (COMUNIDAD DE) Acumulado enero a junio' (p. 418 del PDF) y resumen nacional",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/publico/portalestadistico/dam/jcr:23d540f0-d4aa-40a9-a3c4-6378b6f3e017/Balance%20de%20Criminalidad%20Segundo%20Trimestre%202026.pdf",
        primaria_url_tipo="pdf_balance (misma primaria que C18); tabla PC-Axis 09004 (CCAA) como via dataset",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Comunidad de Madrid ene-jun 2026: 203.953 infracciones, +2,9% (base 198.127). Espana: 1.217.476, +0,5% (base 1.211.083). Ratio de tasas 2,9/0,5 = 5,8; con decimales 2,94/0,53 = 5,6",
        dato_anterior="Comunidad de Madrid ene-jun 2025: 198.127 (columna 2025 de la misma tabla). Aumento absoluto Madrid +5.826; Espana +6.393: Madrid concentra el 91% del aumento nacional, el resto de Espana sube +567 (+0,06%)",
        raw_value_span_actual=(
            "[Interior, Balance 2T2026, p. 418] 'MADRID (COMUNIDAD DE) Acumulado enero a junio' | "
            "'TIPOLOGIA PENAL 2025 2026 Var.% 26/25' | 'III. TOTAL CRIMINALIDAD 198.127 203.953 2,9' | "
            "'Datos pendientes de consolidar' | [resumen nacional] 'suma un total de 1.217.476, con un "
            "aumento del +0,5% sobre el ano 2025' || [zigzagdigital 2026-09-18, el claim] 'La criminalidad "
            "crece seis veces mas en la Comunidad de Madrid respecto al conjunto de Espana' | '2,9%' vs '0,5%'"
        ),
        raw_value_span_anterior=(
            "[Interior, Balance 2T2026, p. 418, columna 2025] 'III. TOTAL CRIMINALIDAD 198.127 203.953 2,9' "
            "(la cifra 2025 viene en la misma tabla como base de comparacion)"
        ),
        truth="supported", context="divergence_detected",
        clase_primaria="3_absolute_vs_relative", clases_secundarias="4_denominator", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="si",
        notas=(
            "Truth: 2,9/0,5 = 5,8, 'seis veces' es un redondeo defendible de un cociente de dos tasas "
            "publicadas. Context (PROVISIONAL, NEEDS_REVIEW): el 'seis veces' es un cociente de variaciones "
            "relativas sobre una base casi nula (0,5%): 2,4 puntos porcentuales de diferencia se presentan "
            "como 'x6'. Con la base de 2025 del propio Balance, si Espana hubiese subido 0,3% seria 'x10', si "
            "1,0% 'x3': la magnitud del titular depende casi por entero del denominador pequeno "
            "(3_absolute_vs_relative). Secundaria: el comparador 'conjunto de Espana' incluye a Madrid, que "
            "aporta el 91% del aumento nacional; contra el resto de Espana (+0,06%) el cociente seria ~50, "
            "contra Espana entera 5,8: el multiplicador no es estable al cambiar el denominador "
            "(4_denominator). Divergencia; EXCEDENTE porque la cubeta ya tenia 6. El articulo cita 28,6 vs "
            "24,6 infracciones por 1.000 habitantes; esa tasa para Madrid NO aparece en el PDF (el Balance da "
            "solo tasas nacionales: 40,5 convencional y 10,0 ciber por mil), origen no localizado. La pagina "
            "de Madrid lleva 'Datos pendientes de consolidar'. Misma primaria que C18 y C20: el coste de "
            "localizar fue cero porque ya estaba en mano; minutes_to_locate no es representativo."
        ),
        criba_query_a="criminalidad Espana aumento 0,5% primer semestre 2026 delitos sexuales",
        criba_query_b="criminalidad sube 0,5% hasta junio 2026 Espana verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K40", case_id="C20",
        claim_text="La criminalidad sube un 2,9% en la Comunidad de Madrid: 203.953 delitos en el primer semestre",
        claim_date="2026-09-18",
        post_url="https://www.que.madrid/2026/09/18/criminalidad-madrid-2026-delitos-semestre-598697/",
        post_url_tipo="prensa", emisor="Que.madrid", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="criminalidad",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Ministerio del Interior - Balance Trimestral de Criminalidad 2T2026, tabla 'MADRID (COMUNIDAD DE) Acumulado enero a junio' (p. 418 del PDF)",
        primaria_url="https://estadisticasdecriminalidad.ses.mir.es/publico/portalestadistico/dam/jcr:23d540f0-d4aa-40a9-a3c4-6378b6f3e017/Balance%20de%20Criminalidad%20Segundo%20Trimestre%202026.pdf",
        primaria_url_tipo="pdf_balance (misma primaria que C18/C19); tabla PC-Axis 09004 (CCAA) como via dataset",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="Comunidad de Madrid ene-jun 2026: 203.953 infracciones, +2,9%; delitos contra la libertad sexual 1.724, +9,3%",
        dato_anterior="Comunidad de Madrid ene-jun 2025: 198.127 infracciones; libertad sexual 1.578 (columna 2025 de la misma tabla)",
        raw_value_span_actual=(
            "[Interior, Balance 2T2026, p. 418] 'MADRID (COMUNIDAD DE) Acumulado enero a junio' | "
            "'III. TOTAL CRIMINALIDAD 198.127 203.953 2,9' | '5. Delitos contra la libertad sexual 1.578 "
            "1.724 9,3' | 'Datos pendientes de consolidar' || [que.madrid 2026-09-18, el claim] 'La "
            "criminalidad sube un 2,9% en la Comunidad de Madrid: 203.953 delitos en el primer semestre' | "
            "'registro 203.953 ilicitos penales en el primer semestre de 2026, un 2,9% mas' | '1.578 "
            "infracciones entre enero y junio de 2025' y '1.724 en el mismo tramo de 2026'"
        ),
        raw_value_span_anterior=(
            "[Interior, Balance 2T2026, p. 418, columna 2025] 'III. TOTAL CRIMINALIDAD 198.127 203.953 2,9' | "
            "'5. Delitos contra la libertad sexual 1.578 1.724 9,3'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="si",
        notas=(
            "Relay fiel de la tabla regional: cifra, variacion y desglose de delitos sexuales coinciden "
            "literalmente. No compara con el dato nacional ni usa tasas por habitante. Control negativo; "
            "EXCEDENTE porque la cubeta ya tenia 7. Mismo dato de partida que C19 (ZigZag): dos medios, "
            "misma tabla, uno relaya y otro construye 'seis veces': par util para el corpus. Misma primaria "
            "que C18/C19, ya en mano: minutes_to_locate no es representativo."
        ),
        criba_query_a="criminalidad Espana aumento 0,5% primer semestre 2026 delitos sexuales",
        criba_query_b="criminalidad sube 0,5% hasta junio 2026 Espana verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    # ---- rechazados de la tanda 1 ------------------------------------------------
    dict(
        cid="K08",
        claim_text="Espana cae 20 puestos en el ranking de mejores paises para ser mujer",
        claim_date="2026-03-09",
        post_url="https://blog.elabogado.com/blog/2026/03/09/espana-cae-20-puestos-en-el-ranking-de-mejores-paises-para-ser-mujer/",
        post_url_tipo="prensa", emisor="Blog de elAbogado", emisor_tipo="blog_corporativo",
        emisor_nivel=4, pais="ES", tema="rankings",
        criba_query_a="Espana cae puestos ranking mejores paises para ser mujer 2026",
        criba_query_b="Espana cae 20 puestos ranking mujer WPS 2026 verificacion OR bulo",
        criba_resultado="rechazado",
        criba_motivo="verificacion_directa: Verificat explica que Espana no retrocedio 20 posiciones, cambio la metodologia del indice WPS entre 2017 y 2025",
        criba_url_verificacion="https://www.verificat.cat/es/que-dice-realmente-el-indice-de-seguridad-de-las-mujeres-espana-no-ha-retrocedido-20-posiciones-ha-cambiado-la-metodologia/",
    ),
    dict(
        cid="K10",
        claim_text="Ecuador registra 86 mil personas menos en situacion de desempleo en mayo de 2026, frente a mayo de 2025",
        claim_date="2026-06-22",
        post_url="https://www.ecuadorencifras.gob.ec/institucional/ecuador-registra-86-mil-personas-menos-en-situacion-de-desempleo-en-mayo-de-2026-frente-a-mayo-de-2025/",
        post_url_tipo="nota_oficial", emisor="INEC", emisor_tipo="organismo_estadistico",
        emisor_nivel=1, pais="EC", tema="empleo",
        criba_query_a="Ecuador 86 mil personas menos desempleo mayo 2026 INEC",
        criba_query_b="Ecuador desempleo 3,1% mayo 2026 86 mil menos verificacion OR bulo OR falso",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: Ecuador Chequea cubrio la publicacion ENEMDU de mayo 2026 ('El empleo adecuado se estanca pese a leve baja del desempleo'). Sin veredicto, pero el trabajo de ir a la primaria ya esta hecho por un verificador",
        criba_url_verificacion="https://ecuadorchequea.com/el-empleo-adecuado-se-estanca-en-ecuador-pese-a-leve-baja-del-desempleo/",
    ),
    dict(
        cid="K14",
        claim_text="Espana lidera la lista de desempleo juvenil de la Union Europea",
        claim_date="2026",
        post_url="https://www.rrhhdigital.com/secciones/formacion/764478/espana-lidera-la-lista-de-desempleo-juvenil-de-la-union-europea/",
        post_url_tipo="prensa", emisor="RRHH Digital", emisor_tipo="prensa_digital",
        emisor_nivel=2, pais="ES", tema="empleo",
        criba_query_a="Espana lidera desempleo juvenil Union Europea 2026",
        criba_query_b="Espana lidera paro juvenil UE 2026 verificacion OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="verificacion_directa: Newtral 2025-10-30 verifica exactamente 'Espana lidera la tasa de paro juvenil de la UE' y la da por falsa (cuarto puesto en agosto de 2025)",
        criba_url_verificacion="https://www.newtral.es/paro-juvenil-ue-factcheck/20251030/",
    ),
    # ---- tanda 2: descubrimiento 2026-09-25, criba 2026-09-25 -------------------
    dict(
        cid="K20", case_id="C21",
        claim_text="El abandono educativo temprano sigue en descenso y marca su minimo historico con un 12,8%",
        claim_date="2026-01-28",
        post_url="https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/educacion-fp-deportes/paginas/2026/280126-abandono-educativo-minimo-historico.aspx",
        post_url_tipo="nota_oficial", emisor="Ministerio de Educacion, FP y Deportes (via La Moncloa)", emisor_tipo="gobierno",
        emisor_nivel=1, pais="ES", tema="educacion",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Ministerio de Educacion, FP y Deportes - Explotacion de las variables educativas de la EPA (EDUCAbase, tabla aban_1_06 'Abandono educativo temprano por nivel de formacion, nacionalidad, sexo y ano' + nota resumen); contraste: Eurostat edat_lfse_14",
        primaria_url="https://estadisticas.educacion.gob.es/EducaJaxiPx/files/_px/es/csv_bdsc/laborales/epa/aban/l0/aban_1_06.csv_bdsc?nocab=1",
        primaria_url_tipo="csv_dataset (EDUCAbase; tambien .px y .xlsx); nota resumen PDF en educacionfpydeportes.gob.es/dam/jcr:43237823-.../nota-resu.pdf; API Eurostat edat_lfse_14?geo=ES",
        via_de_acceso="dataset", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="api",
        dato_actual="Abandono temprano 2025: 12,80% (CSV; 12,8 en nota y en Eurostat); hombres 15,91, mujeres 9,50. Media UE-27 2025: 9,1 (Eurostat)",
        dato_anterior="Abandono temprano 2024: 12,98% en el CSV del ministerio (13,0 en la nota 2026 y en Eurostat; el 2025-01-28 se publico como '13%'); hombres 15,75, mujeres 10,04. UE-27 2024: 9,6 (Eurostat 2026-09); la nota de Moncloa de 2026-01 usaba 9,4",
        raw_value_span_actual=(
            "[MEFD, CSV aban_1_06] 'TOTAL;TOTAL;AMBOS SEXOS;2025;12,80' | 'TOTAL;TOTAL;Hombres;2025;15,91' | "
            "'TOTAL;TOTAL;Mujeres;2025;9,50' | [MEFD, nota-resu.pdf, ed. 2026] 'En el ano 2025 el abandono "
            "temprano de la educacion y la formacion en Espana se situa en el 12,8%, lo que supone respecto "
            "al ano anterior una disminucion de 0,2 puntos porcentuales (13,0% en 2024), proporcionando el "
            "dato anual mas bajo de la serie historica' | 'dejando en 3,7 puntos la distancia a la media de "
            "la Union Europea (9,1% en 2025)' | [Eurostat edat_lfse_14] Spain 2025 => 12.8; EU27_2020 2025 "
            "=> 9.1 || [Moncloa 2026-01-28, el claim] 'El abandono educativo temprano sigue en descenso y "
            "marca su minimo historico con un 12,8%' | 'pasando del 20% en 2015 al 12,8% en 2025' | 'se "
            "reduce a 3,4 puntos la distancia respecto a la media de la Union Europea (9,4% en 2024)'"
        ),
        raw_value_span_anterior=(
            "[MEFD, CSV aban_1_06] 'TOTAL;TOTAL;AMBOS SEXOS;2024;12,98' | 'TOTAL;TOTAL;Hombres;2024;15,75' | "
            "'TOTAL;TOTAL;Mujeres;2024;10,04' | [Eurostat edat_lfse_14] Spain 2024 => 13.0; EU27_2020 2024 "
            "=> 9.6 | [MEFD nota de prensa 2025-01-28, titulo] 'El abandono educativo temprano marco en "
            "2024 su minimo historico con un 13%'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="si",
        notas=(
            "El claim (titular) es exacto: 12,8 es el minimo de la serie (CSV desde 2002; Eurostat desde "
            "2015) y baja respecto a 2024. Control negativo; EXCEDENTE porque la cubeta ya tenia 7. "
            "HALLAZGOS fuera del titular, para el corpus (NEEDS_REVIEW, no etiquetan al claim): (1) el "
            "'descenso de 0,2 puntos' es 12,98 -> 12,80 = 0,18 pp; el ministerio publica tabla de errores de "
            "muestreo (aban_1_11) y advierte de 'tamanos muestrales pequenos' por CCAA. (2) La nota de "
            "Moncloa dice 'se reduce a 3,4 puntos la distancia respecto a la media de la UE (9,4% en 2024)': "
            "compara Espana 2025 con la UE 2024 (anos distintos). Con anos emparejados la distancia era 3,4 "
            "en 2024 (13,0-9,6) y es 3,7 en 2025 (12,8-9,1): la brecha NO se redujo, se amplio 0,3; la propia "
            "nota-resu del ministerio, ya actualizada, dice '3,7 puntos'. Es una divergencia de "
            "2_baseline_selection en el cuerpo de una nota oficial de nivel 1. (3) La URL del ministerio "
            "(pagina EPA) devolvio 'socket hang up' dos veces al fetcher y 200 a curl con UA por defecto: "
            "error de red del fetcher, no bloqueo; no se cuenta como DEC-018."
        ),
        criba_query_a="abandono educativo temprano 12,8% minimo historico 2025",
        criba_query_b="abandono escolar 12,8% minimo historico 2026 verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K21", case_id="C22",
        claim_text="La brecha territorial del abandono escolar se agranda en Espana: del 18,6% de La Rioja al 6,1% de Navarra",
        claim_date="2026-04-30",
        post_url="https://www.elconfidencialdigital.com/articulo/estado-autonomico/brecha-territorial-abandono-escolar-agranda-espana-186-rioja-61-navarra/202604300750521291302.html",
        post_url_tipo="prensa", emisor="El Confidencial Digital", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="ES", tema="educacion",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="NO LOCALIZADA. El articulo atribuye a 'datos del INE a partir de la EPA del primer trimestre de 2026' una tasa trimestral de abandono temprano por CCAA que el INE no publica como tabla. Lo mas cercano: INE 69786 (ICV, anual 2004-2024), INE 71120 y 12543 (anual), MEFD aban_1_01 (anual por CCAA)",
        primaria_url="",
        primaria_url_tipo="ninguna; candidatas revisadas: servicios.ine.es DATOS_TABLA/69786 (anual), TABLAS_OPERACION/EPA (1.039 tablas, ninguna de abandono), ine.es/jaxi tpx=71120 (anual), EDUCAbase aban_1_01 (anual)",
        via_de_acceso="none", access_requires_login="no",
        current_edition_found="no", previous_edition_found="no",
        historical_series_found="no", methodology_found="si",
        alcanzable_por_agente="no", alcanzable_por_humano="no",
        recuperabilidad="D", formato="none",
        dato_actual="Segun el articulo (1T2026): La Rioja 18,6%, Navarra 6,1%, media nacional 13,04%, brecha 12,5 pp. NO verificable: ningun organismo publica ese valor",
        dato_anterior="No localizado para el indicador citado. Referencia ANUAL mas cercana (MEFD aban_1_01 / INE 69786): La Rioja 17,03 (2024) -> 15,53 (2025); Navarra 9,94 -> 7,83; Pais Vasco 5,02 -> 3,63 (el minimo anual es Pais Vasco, no Navarra); Murcia 18,22 -> 20,58 (el maximo anual es Murcia, no La Rioja)",
        raw_value_span_actual=(
            "[elconfidencialdigital 2026-04-30, el claim] 'La brecha territorial del abandono escolar se "
            "agranda en Espana: del 18,6% de La Rioja al 6,1% de Navarra' | 'la media nacional en el "
            "13,04%' | 'La diferencia entre La Rioja (18,6%) y Navarra (6,1%) alcanza los 12,5 puntos "
            "porcentuales' | [atribucion, identica en miciudadreal, infoclm y andaluciainformacion, "
            "2026-04-29/30] 'segun datos del INE a partir de la Encuesta de Poblacion Activa "
            "correspondiente al primer trimestre de 2026' || [contraste, MEFD CSV aban_1_01, ANUAL] "
            "'Rioja, La (3);Ambos sexos;2025;15,53' | 'Navarra, Comunidad Foral de (3);Ambos sexos;2025;7,83' "
            "| 'Pais Vasco;Ambos sexos;2025;3,63' | 'TOTAL;Ambos sexos;2025;12,80'"
        ),
        raw_value_span_anterior="",
        truth="insufficient_evidence", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="PRIMARY_SOURCE_NOT_FOUND",
        abandonado_por_tiempo="", bucket_resultado="primaria_no_localizable", excedente="no",
        notas=(
            "PRIMARIA NO LOCALIZABLE genuina (no bloqueo): el valor atribuido al INE no existe como dato "
            "publicado. Recorrido API -> dataset -> HTML: INE Tempus (112 operaciones; 'abandono' solo en "
            "12543/12544 anuales de 'Mujeres y Hombres'), tabla 69786 (anual, ICV, ultima 2024), tpx 71120 "
            "(anual), las 1.039 tablas de la EPA 1T2026 (ninguna de abandono; las de 'cursa estudios' no "
            "dan la tasa), EDUCAbase del ministerio (anual). Una tasa trimestral por CCAA solo es derivable "
            "de los microdatos EPA; el texto identico en 4 medios apunta a una agencia o instituto regional "
            "que la calculo. No se persigue (plan: no buscar donde se movio la fuente). Prediccion 4 "
            "confirmada en variante: la 'primaria' citada existe (INE/EPA) pero no contiene el valor. "
            "Contexto NO etiquetable, pero anotado: el minimo/maximo anual 2025 son Pais Vasco (3,6) y "
            "Murcia (20,6), no Navarra y La Rioja; La Rioja anual va 9,7 (2023) -> 17,0 (2024) -> 15,5 "
            "(2025) y el ministerio publica intervalos de confianza por CCAA (aban_1_11) advirtiendo de "
            "'tamanos muestrales pequenos': un dato trimestral de La Rioja es aun mas ruidoso. Tiempo real "
            "t1-t0 = 5,2 min; la nota del log 't1' dice 'tope casi agotado' por error (corregido con "
            "comentario en el log). alcanzable_* = no significa 'no hay nada que alcanzar', no bloqueo."
        ),
        criba_query_a="abandono escolar brecha territorial La Rioja 18,6% Navarra 6,1%",
        criba_query_b="brecha territorial abandono escolar se agranda La Rioja Navarra 2026 verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K22", case_id="C23",
        claim_text="AEMET avisa de un otono mas calido y lluvioso: el verano de 2026, el mas caluroso en 157 anos",
        claim_date="2026-09-21",
        post_url="https://www.deia.eus/actualidad/sociedad/2026/09/21/aemet-avisa-otono-calido-lluvioso-11568036.html",
        post_url_tipo="prensa", emisor="Deia", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="clima",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="AEMET - nota 'Un verano de cuatro meses bate records de calor en, al menos, siglo y medio' (21/09/2026) + 'Avance climatico nacional. Verano 2026' (PDF, 10 pp)",
        primaria_url="https://www.aemet.es/documentos/es/noticias/2026/09/avance_climatico_nacional_verano_2026.pdf",
        primaria_url_tipo="pdf_avance_climatico (texto extraible) enlazado desde la nota HTML aemet.es/es/noticias/2026/09/resumen_verano2026; edicion anterior con el mismo patron de URL (verano_2025)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="Verano 2026 (1 jun-31 ago): T media Espana peninsular 24,5 C, +2,4 C sobre 1991-2020; el mas calido desde 1961 (serie oficial), +0,3 C sobre 2025; reconstruccion desde 1869 => sin precedente en 157 anos. Precipitacion 39,6 mm (56% de lo normal), tercero mas seco desde 1961",
        dato_anterior="Verano 2025 (avance AEMET sept. 2025): T media 24,2 C, +2,1 C; el mas calido desde 1961, +0,1 C sobre 2022. Precipitacion 57,0 mm (81%), decimo cuarto mas seco",
        raw_value_span_actual=(
            "[AEMET, avance verano 2026, p.1] 'La temperatura media en la Espana peninsular ha sido de "
            "24,5C, lo que supone que se ha superado en 2,4 C la temperatura media en el periodo de "
            "referencia 1991-2020. El verano de 2026 ha sido el mas calido desde 1961, superando en + 0,3 "
            "C al verano de 2025' | [AEMET, nota 21/09/2026] 'El trimestre veraniego de 2026 fue el mas "
            "calido en Espana desde, al menos, 1869' | 'Aunque la incertidumbre en los datos aumenta "
            "conforme mas nos alejamos en el tiempo, tambien puede afirmarse que el verano de 2026 ha sido "
            "el mas calido desde, al menos, 1869. No hay precedentes, por lo tanto, de un verano con "
            "temperaturas tan altas como el de 2026 en los ultimos 157 anos' | [avance, p.7] 'precipitacion "
            "media sobre la Espana peninsular de 39,6 mm, valor que representa el 56 % del valor normal' | "
            "'el tercero mas seco desde el comienzo de la serie en 1961' || [Deia 2026-09-21, el claim, "
            "titular via buscador; el articulo devuelve 406] 'AEMET avisa de un otono mas calido y "
            "lluvioso: el verano de 2026, el mas caluroso en 157 anos'"
        ),
        raw_value_span_anterior=(
            "[AEMET, avance verano 2025, p.1] 'una temperatura media en la Espana peninsular de 24,2 C, "
            "valor que queda 2,1 C por encima de la media de esta estacion (periodo de referencia "
            "1991-2020). Ha sido el verano mas calido desde el comienzo de la serie en 1961, habiendo "
            "superado en 0,1 C al verano de 2022, que era hasta ahora el mas calido de la serie' | [p.7] "
            "'57,0 mm, valor que representa el 81 % del valor normal' | 'el decimo cuarto mas seco'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="si",
        notas=(
            "El titular reproduce la afirmacion literal de AEMET ('157 anos' = 1869-2026). Control "
            "negativo; EXCEDENTE porque la cubeta ya tenia 7. Matiz para el corpus (no dispara test): "
            "'157 anos' empalma la serie oficial (desde 1961) con una reconstruccion (Chazarra, Lorenzo y "
            "Nunez, AEMET 2025) cuya incertidumbre la propia AEMET declara; el titular omite el 'al menos' "
            "de AEMET pero no cambia la afirmacion. DEC-018: deia.eus devolvio '406 WAF Forbidden' al "
            "fetcher y a curl con UA por defecto; la edicion hermana noticiasdealava.eus tambien 406. No se "
            "reintento. El bloqueo afecta al CONTENIDO del claim (secundaria), no a la primaria: el "
            "claim_text viene del titular indexado por el buscador. La edicion anterior se localizo por el "
            "patron de URL de AEMET (avance_climatico_nacional_verano_<ano>.pdf), verificado con la nota "
            "aemet.es/es/noticias/2025/09/resumen_verano_2025 (200)."
        ),
        criba_query_a="verano 2026 mas calido 157 anos AEMET",
        criba_query_b="verano 2026 mas caluroso en 157 anos AEMET verificacion OR bulo OR fact-check",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K24", case_id="C24",
        claim_text="El 60% de los espanoles priorizan el turismo nacional y la gastronomia local en sus viajes en 2026",
        claim_date="2026-09-23",
        post_url="https://www.pressdigital.es/articulo/economia/2026-09-23/6025405-60-espanoles-priorizan-turismo-nacional-gastronomia-local-viajes-2026",
        post_url_tipo="prensa", emisor="Pressdigital", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="ES", tema="turismo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="NO LOCALIZADA. El articulo atribuye las cifras al 'Informe de Tendencias de Viaje 2026' de Booking.com 'publicado con motivo del Dia Mundial del Turismo'. Ese informe no aparece en el newsroom de Booking.com en espanol ni hay enlace, muestra o metodologia en ninguna de las 5 versiones del texto",
        primaria_url="",
        primaria_url_tipo="ninguna; revisado: news.booking.com/es (indice, pagina 2, busqueda 'tendencias' y 'tendencias de viaje 2026'), nota 'Predicciones de Viaje 2026' (2025-12-04, 10a ed., 29.000 viajeros en 33 paises) que NO contiene las cifras del articulo",
        via_de_acceso="none", access_requires_login="no",
        current_edition_found="no", previous_edition_found="no",
        historical_series_found="no", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="no",
        recuperabilidad="D", formato="none",
        dato_actual="Segun el articulo: 60% (titular) / 59% 'considera que Espana todavia guarda numerosos lugares por conocer'; 46% turismo de proximidad; 89% gastronomia como motivacion; 88% descanso mental; 91% entornos naturales; 30% temporada baja; 28% destinos cercanos. Sin muestra ni fechas de campo",
        dato_anterior="No localizado: no hay edicion anterior identificable de un informe que no se localiza",
        raw_value_span_actual=(
            "[pressdigital 2026-09-23, el claim] 'El 60% de los espanoles priorizan el turismo nacional y "
            "la gastronomia local en sus viajes en 2026' | 'El 59% de los viajeros espanoles considera que "
            "Espana todavia guarda numerosos lugares por conocer, una percepcion que situa al turismo de "
            "proximidad como la opcion preferida para casi la mitad de la poblacion (46%)' | [atribucion, "
            "identica en theobjective, forbes.es, capital.es, elnoticierodigital] 'Asi lo refleja el "
            "Informe de Tendencias de Viaje 2026 publicado por la plataforma Booking.com con motivo del "
            "Dia Mundial del Turismo' || [Booking newsroom, nota 2025-12-04, la unica 'tendencias 2026' "
            "localizada] 'Segun datos de mas de 29.000 viajeros de 33 paises y territorios' (sin 59/46/89)"
        ),
        raw_value_span_anterior="",
        truth="insufficient_evidence", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="PRIMARY_SOURCE_NOT_FOUND",
        abandonado_por_tiempo="", bucket_resultado="primaria_no_localizable", excedente="no",
        notas=(
            "PRIMARIA NO LOCALIZABLE genuina (no bloqueo: news.booking.com respondio 200 a todo). Patron "
            "'encuesta corporativa via nota de prensa': cinco medios publican el mismo texto el mismo dia, "
            "ninguno enlaza el informe, ninguno da muestra, campo ni empresa de campo. Booking.com publica "
            "en su newsroom otras notas de 2026 (eclipse, LGTBIQ+, hoteleros) pero no esta. Prediccion 4 "
            "confirmada (nivel 5). Observacion para el corpus, no etiquetable sin primaria: el titular dice "
            "'60% priorizan el turismo nacional y la gastronomia local' y el cuerpo dice '59% considera que "
            "Espana guarda lugares por conocer' y '46% turismo de proximidad': la cifra y el enunciado del "
            "titular no estan en el cuerpo. alcanzable_* = no por inexistencia del documento, no por "
            "bloqueo. Tiempo t1-t0 segun log."
        ),
        criba_query_a="60% espanoles priorizan turismo nacional gastronomia local 2026",
        criba_query_b="\"60% de los espanoles\" priorizan turismo nacional 2026 estudio verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K25", case_id="C25",
        claim_text="El 55% de los espanoles elegira Espana como destino para sus vacaciones en 2026",
        claim_date="2026-05-11",
        post_url="https://www.navarrainformacion.es/2026/05/11/el-55-de-los-espanoles-elegira-espana-como-destino-para-sus-vacaciones-en-2026/",
        post_url_tipo="prensa", emisor="Navarra Informacion", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="ES", tema="turismo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Europ Assistance Espana / Ipsos - 'Barometro de Vacaciones 2026' (edicion 25; PDF 200 pp en europ-assistance.es; campo 27 feb-7 abr 2026; 26 paises; 1.000 espanoles) + blog edicion 25 (2026-04-30)",
        primaria_url="https://europ-assistance.es/hubfs/bar%C3%B3metros/Bar%C3%B3metro%20Travel%20Europ%20Assistance%20Espa%C3%B1a.pdf",
        primaria_url_tipo="pdf_informe (texto extraible, 200 pp); el articulo enlaza una copia en Google Drive con sha256 identico; la URL del emisor no lleva ano (se sobreescribira en 2027)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="no",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="NEWQ2 'Cuando piensas en las vacaciones ideales de 2026, a donde te gustaria ir principalmente?' (base: todos) ES: propio pais 55, extranjero 30, me quedo en casa 6, no lo se 9. P21BIS 'A donde planeas ir de viaje este verano?' (base: quienes planean un viaje y ya conocen su destino) Spain 69% (+3 vs 2025). P15 intencion de viajar ES: 77 (2026) 80 (2025) 82 (2024) 78 (2023)",
        dato_anterior="NO LOCALIZADA la edicion 24 (2025) como documento: el blog de 2025 dice 'puedes ver el estudio completo aqui' sin enlace, dos URL hubfs probadas dan 404, el buscador no devuelve PDF. La pregunta NEWQ2 es nueva en 2026 (prefijo NEW), asi que el 55 no tiene edicion anterior en ningun caso. Valores 2025 conocidos solo por secundarias/comparativas embebidas: intencion 80%, 'dos de cada tres' en el propio pais (P21BIS 66), presupuesto 1.763 EUR, campo 24 feb-26 mar 2025",
        raw_value_span_actual=(
            "[Europ Assistance, Barometro 2026, p.44] 'NEWQ2. Cuando piensas en las vacaciones ideales de "
            "2026, a donde te gustaria ir principalmente? Base: Para todos' | 'la mayoria ve sus vacaciones "
            "ideales en su propio pais, forma un arco sur que incluye Espana, Portugal e Italia' | fila "
            "'Viajar por mi propio pais' (EU FR UK BE DE CH AT ES PT IT PL CZ): '36 51 29 14 26 19 25 55 47 "
            "50 46 30' => ES 55 | [p.47] 'P21BIS. A donde planeas ir de viaje [este verano]? Base: Para "
            "quienes planean hacer un viaje y ya conocen su destino ... Spain 69%' | [p.29, P15] 'Italia "
            "Espana Portugal 77 808278' => ES 77 (2026), 80 (2025) | [p.5] '1000 Espanoles' | 'Fechas de "
            "trabajo de campo: Del 27 de febrero al 7 de abril' || [blog Europ Assistance 2026-04-30] 'el "
            "77 % de los espanoles tiene previsto viajar este verano, solo tres puntos menos que en 2025' | "
            "'el 55 % planea quedarse en Espana' | 'el presupuesto medio para viajar se situa en 1.758 EUR' "
            "|| [navarrainformacion 2026-05-11, el claim] 'El 55% de los espanoles elegira Espana como "
            "destino para sus vacaciones en 2026' | 'un 77% de los espanoles tienen la intencion de viajar "
            "este ano' | '1.758 EUR'"
        ),
        raw_value_span_anterior="",
        truth="mixed", context="divergence_detected",
        clase_primaria="4_denominator", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="edicion_anterior_no_localizable", excedente="no",
        notas=(
            "NEEDS_REVIEW (etiqueta provisional). El 55 existe en la primaria pero para otra pregunta: "
            "'vacaciones IDEALES, a donde te gustaria ir' (base todos), no 'elegira Espana como destino'. "
            "La pregunta de destino planeado (P21BIS) da 69% para Espana con base 'quienes planean y "
            "conocen destino'. El titular presenta una preferencia ideal como eleccion efectiva, y el "
            "valor cambia (55 vs 69) al cambiar pregunta y base: 4_denominator provisional; alternativa "
            "razonable: METRIC_AMBIGUOUS. El propio blog del emisor ya hace la misma lectura ('planea "
            "quedarse en Espana'): el medio relaya al emisor; la divergencia nace en la nota del emisor, "
            "no en la prensa. EDICION ANTERIOR NO LOCALIZABLE: la edicion 24 (2025) existe (blog, Infobae, "
            "SegurosNews) pero el documento no esta enlazado ni indexado; y NEWQ2 es pregunta nueva en "
            "2026, sin edicion anterior posible. El PDF 2026 embebe comparativas con 2025 (P15, P21BIS) "
            "que permiten reconstruir 66 y 80 sin ver el documento de 2025. Riesgo de URL: el PDF del "
            "emisor no lleva ano en la ruta. Prediccion 8 (la cubeta mas dificil de distinguir): este es "
            "el caso limite exacto."
        ),
        criba_query_a="55% de los espanoles elegira Espana destino vacaciones 2026",
        criba_query_b="\"55% de los espanoles\" elegira Espana destino vacaciones 2026 verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K26", case_id="C26",
        claim_text="Mas del 59 % de los espanoles preve viajar en 2026 segun Avoris Travel Insights",
        claim_date="2026-04",
        post_url="https://gacetadelturismo.com/gacetadelturista/mas-del-59-de-los-espanoles-preve-viajar-en-2026-segun-avoris-travel-insights/",
        post_url_tipo="prensa", emisor="Gaceta del Turismo", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="ES", tema="turismo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Avoris - 'Avoris Travel Insights #5: Contexto, incertidumbre e IA en el sector turistico. Escenario de los viajes 2026' (abril 2026, PDF 58 pp); edicion anterior #4 'La brujula de los viajes de 2026' (enero 2026, PDF 60 pp), ambos listados en avoristravel.com/informes",
        primaria_url="https://d1pnk0oci680mj.cloudfront.net/uploads/AVORIS_5_2e7c0ee232.pdf",
        primaria_url_tipo="pdf_informe (texto extraible) en CDN del emisor, enlazado con boton 'Descargar' desde avoristravel.com/informes sin formulario ni registro; edicion anterior: .../Avoris_Travel_Insights_4_Brujula_2026_rev01_2a6bdf022f.pdf",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="no",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="Prevision marzo 2026: 'Seguro que si viajare en 2026' 59,2%; 'Aun no se' 37,7%; 'Seguro que no' 3,1%. Presupuesto medio 2.780 EUR (dic 2025: 3.090). Media de viajes 2,7 (dic 2025: 3,1)",
        dato_anterior="Prevision diciembre 2025 (#4, enero 2026): 'Seguro que si' 45,7%; 'Aun no se' 51,5%; 'Seguro que no' 2,8%. Presupuesto medio 3.090 EUR. Media de viajes 3,1",
        raw_value_span_actual=(
            "[Avoris #5, p.10] 'Tienes previsto realizar algun viaje o escapada de ocio durante el 2026? "
            "PREVISION MARZO 2026 51,5%45,7% 2,8% 37,7% 3,1%' | 'SEGURO QUE SI viajare en 2026 AUN NO SE si "
            "viajare en 2026 SEGURO QUE NO viajare en 2026 PREVISION DICIEMBRE 2025 59,2%' | 'Las "
            "previsiones de marzo de 2026 muestran un aumento significativo de los viajeros que declaran "
            "con certeza que realizaran algun viaje respecto a diciembre de 2025, a costa principalmente "
            "de la reduccion del segmento indeciso' | [p.12] 'pasando de 3.090EUR a 2.780EUR' | [p.11] "
            "'(de 3,1 a 2,7)' || [gacetadelturismo 2026-05-06, el claim] 'Mas del 59 % de los espanoles "
            "preve viajar en 2026 segun Avoris Travel Insights' | '59,2 % de los espanoles asegura que "
            "viajara con certeza, frente al 45,7 % registrado en diciembre de 2025'"
        ),
        raw_value_span_anterior=(
            "[Avoris #4, p.10] '51,5% 45,7% 2,8% SEGURO QUE SI viajare en 2026 AUN NO SE si viajare en "
            "2026 SEGURO QUE NO viajare en 2026' | [p.12] '3.090EUR' | [p.11] 'la media de viajes declarada "
            "se situa en 3,1 desplazamientos'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="control_negativo", excedente="si",
        notas=(
            "Relay fiel: cifra, categoria ('seguro que si'), comparacion con diciembre y presupuesto "
            "coinciden con el PDF. Control negativo; EXCEDENTE (cubeta llena). Emisor de nivel 5 que "
            "resulto nivel 4 en la practica: PDFs publicos, con texto, listados en una pagina estable. "
            "Ninguna de las dos ediciones trae ficha tecnica (muestra, campo, metodo): methodology_found=no; "
            "es un dato sin error muestral declarado. Matiz no etiquetable: 'preve viajar' = solo 'seguro "
            "que si' (59,2); con indecisos (37,7) la lectura 'no descarta viajar' seria 96,9. Otros medios "
            "titularon '60%' (pressdigital, bolsamania) redondeando 59,2. La extraccion de p.10 mezcla "
            "las etiquetas de las dos previsiones en el flujo de texto; los valores se asignaron por "
            "coherencia con el #4 (45,7/51,5/2,8 = diciembre)."
        ),
        criba_query_a="59% de los espanoles preve viajar 2026 Avoris Travel Insights",
        criba_query_b="Avoris Travel Insights 59% espanoles viajar 2026 46% diciembre verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K27", case_id="C27",
        claim_text="El 79% de los ecuatorianos califica como negativa la gestion del presidente Daniel Noboa, segun encuesta del Ciees",
        claim_date="2026-07",  # aprox.: el articulo devuelve 403; el dato (79% negativa) es de la medicion CIEES del 25-26 de julio de 2026, difundida el 28-07
        post_url="https://www.radiopichincha.com/encuesta-ciees-desplome-imagen-gestion-presidente-daniel-noboa/",
        post_url_tipo="prensa", emisor="Radio Pichincha", emisor_tipo="prensa_digital",
        emisor_nivel=5, pais="EC", tema="opinion_publica",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="NO LOCALIZADA. Emisor identificado: CIEES (Centro de Investigaciones y Estudios Especializados, ciees.com.ec), medicion 25-26 de julio de 2026. El sitio no publica los informes: el menu 'Resultados Encuestas' es un enlace de WhatsApp ('Quiero acceder a los Resultados de encuestas'); secciones boletines/publicaciones/medios sin la encuesta; difusion en X/Instagram/TikTok (excluidas)",
        primaria_url="",
        primaria_url_tipo="ninguna; revisado: ciees.com.ec (home, /boletines/, /publicaciones/, /medios/); cieeslatam.com y ciees.ec no resuelven",
        via_de_acceso="none", access_requires_login="si",
        current_edition_found="no", previous_edition_found="no",
        historical_series_found="no", methodology_found="no",
        alcanzable_por_agente="no", alcanzable_por_humano="probable",
        recuperabilidad="D", formato="none",
        dato_actual="Segun la prensa (expreso, eldiario, larepublica): julio 2026, gestion negativa 79% / positiva 21%; ficha tecnica: 820 casos, Quito y Guayaquil, mayores de 16, +-4%, 95%, 25-26 jul. NO verificable contra documento del emisor",
        dato_anterior="Segun la prensa: junio 2026 (27-28 jun, 820, +-4%) gestion positiva 26%; agosto 2026 (29-30 ago) negativa 68% / positiva 32%. Ningun documento de CIEES localizado",
        raw_value_span_actual=(
            "[radiopichincha, titular indexado; el articulo devuelve 403 'Just a moment' (Cloudflare)] 'El "
            "79% de los ecuatorianos califica como negativa la gestion del presidente Daniel Noboa, segun "
            "encuesta del Ciees' || [ciees.com.ec, menu] 'Resultados Encuestas' -> "
            "'https://wa.me/593998328973?text=Quiero acceder a los Resultados de encuestas' || [expreso "
            "2026-07-28] 'Junio 2026: 26%' | 'Julio 2026: 21%' (aprobacion positiva) | [eldiario.ec "
            "2026-09-02, agosto] 'la evaluacion negativa ... bajo de 79% a 68%'"
        ),
        raw_value_span_anterior="",
        truth="insufficient_evidence", context="undetermined",
        clase_primaria="none", clases_secundarias="", abstain_reason="PRIMARY_SOURCE_NOT_FOUND",
        abandonado_por_tiempo="", bucket_resultado="primaria_no_localizable", excedente="no",
        notas=(
            "PRIMARIA NO LOCALIZABLE por diseno del emisor: la encuestadora existe y responde 200, pero "
            "distribuye resultados por WhatsApp bajo peticion y por redes sociales; no hay documento "
            "publico. Se registra access_requires_login=si (contacto) y alcanzable_por_humano=probable "
            "(un humano puede pedirlo por WhatsApp o ver la lamina en Instagram). Ademas, el CONTENIDO del "
            "claim esta bloqueado: radiopichincha.com devolvio 403 con desafio Cloudflare a fetcher y curl "
            "(DEC-018, no se reintento); claim_date aproximada por la fecha de la medicion. El titular "
            "reproduce, segun 4 medios, la lamina de julio (79/21); la prensa coincide entre si, pero eso "
            "es concordancia entre secundarias, no verificacion. Generalizacion 'de los ecuatorianos' con "
            "muestra solo de Quito y Guayaquil: seria 4_denominator si hubiera primaria; queda anotado. "
            "Esta es la 3a de 3 en la cubeta: se cierra."
        ),
        criba_query_a="79% ecuatorianos pesimismo CIEES agosto 2026",
        criba_query_b="encuesta CIEES 79% pesimismo Ecuador Quito Guayaquil 2026 verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K28", case_id="C28",
        claim_text="Por primera vez, Ecuador tiene cifras de la poblacion LGBTIQ+",
        claim_date="2026-07-30",
        post_url="https://gk.city/2026/07/30/encuesta-condiciones-vida-cifras-poblacion-lgbtiq-ecuador-inec/",
        post_url_tipo="prensa", emisor="GK", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="EC", tema="demografia",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEC - Encuesta Nacional de Condiciones de Vida de la Poblacion LGBTI+ (ENCV-LGBTI+) 2025: Boletin tecnico N-01-2026 (abril 2026), Presentacion de principales resultados, tabulados, BDD CSV, metodologia RDS. Antecedentes del propio INEC: Censo 2022 (2,4%, difundido 2023/2024) y 'Primera Investigacion (estudio de caso)' 2013",
        primaria_url="https://www.ecuadorencifras.gob.ec/documentos/web-inec/encv-lgbt/2025/9_BOLETIN_TECNICO_ENCV-LGBTI+2025.pdf",
        primaria_url_tipo="pdf_boletin (texto extraible) + pagina ecuadorencifras.gob.ec/lgbti/ con tabulados .zip, BDD CSV/Excel, diccionario, sintaxis, metodologia; 2013: ecuadorencifras.gob.ec/wp-content/descargas/Presentaciones/Presentacion-LGBTI.pdf",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="no", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="A", formato="dataset",
        dato_actual="ENCV-LGBTI+ 2025: 6.147 entrevistas a poblacion LGBTI+ de 18+, 24 provincias, campo oct-nov 2025, muestreo no probabilistico RDS; gay 38,5%, bisexual 28,2%, lesbiana 19,5%; 53,5% sufrio discriminacion o violencia. NO estima el tamano de la poblacion LGBTI+",
        dato_anterior="Censo 2022 (INEC, difundido 2023/mayo 2024): 2,4% de las personas de 18+ se identificaron como LGBTI+ (270.970). INEC 2013: 'Primera Investigacion (estudio de caso)... poblacion LGBTI', 2.805 entrevistados, nov 2012-ene 2013. Ambas no comparables con la ENCV (RDS) segun el propio boletin",
        raw_value_span_actual=(
            "[INEC, Boletin tecnico N-01-2026, p.5] 'La muestra de la encuesta estuvo conformada por 6147 "
            "personas de 18 anos y mas que pertenecen a la poblacion LGBTI+' | 'dos en octubre y dos en "
            "noviembre de 2025' | 'Respondent Driven Sampling o por sus siglas en ingles RDS' | [p.4] 'no "
            "es estrictamente comparable con otras fuentes estadisticas, como las derivadas de registros "
            "administrativos o censos' | [Presentacion, p.3] 'la primera de alcance nacional especializada "
            "en caracterizar las condiciones de vida de la poblacion LGBTI+ en el Ecuador' || [GK "
            "2026-07-30, el claim, titular indexado; el articulo devuelve 403] 'Por primera vez, Ecuador "
            "tiene cifras de la poblacion LGBTIQ+'"
        ),
        raw_value_span_anterior=(
            "[INEC, Boletin tecnico N-01-2026, p.5] 'En 2023, el INEC difundio por primera vez resultados "
            "del Censo de Poblacion y Vivienda 2022 sobre diversidad sexo-generica, reportando que el 2,4% "
            "de las personas de 18 anos y mas se identificaron como parte de la poblacion LGBTI+' | [INEC "
            "2013, Presentacion-LGBTI.pdf, p.1 y p.12] 'Primera Investigacion (estudio de caso) sobre "
            "Condiciones de Vida, Inclusion Social y Derechos Humanos de la poblacion LGBTI en Ecuador' | "
            "'2.805 personas de la poblacion LGBTI de 18 anos en adelante. Periodo de la investigacion "
            "Noviembre 2012 - Enero 2013'"
        ),
        truth="contradicted", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="claim_falso", excedente="no",
        notas=(
            "NEEDS_REVIEW. El titular 'por primera vez Ecuador tiene cifras de la poblacion LGBTIQ+' lo "
            "contradice la propia primaria: el boletin recuerda que el Censo 2022 ya reporto el 2,4% "
            "(270.970 personas) y el INEC publico un estudio de caso en 2013. Lo que si es primera vez es "
            "'la primera encuesta nacional de condiciones de vida' (Presentacion p.3); si el cuerpo del "
            "articulo lo precisa, la etiqueta pasaria a 'mixed', pero el cuerpo no es legible (gk.city 403 "
            "Cloudflare a fetcher y curl; DEC-018, sin reintento). Ningun test de contexto dispara: no hay "
            "comparacion numerica. Cubeta claim_falso (sin objetivo), como C17. Matiz metodologico "
            "anotado para el corpus: la ENCV usa RDS (no probabilistico) y el INEC advierte que no es "
            "comparable con el censo; cualquier titular futuro que compare 2,4% (censo) con cifras de la "
            "ENCV seria 5_methodology_change. Emisor nivel 1 ejemplar: boletin, tabulados, BDD, "
            "diccionario, sintaxis, metodologia y formulario publicos."
        ),
        criba_query_a="Ecuador cifras poblacion LGBTIQ 2,4% INEC primera vez",
        criba_query_b="INEC 2,4% poblacion LGBTIQ Ecuador encuesta condiciones de vida 2026 verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K29", case_id="C29",
        claim_text="Espana, en el puesto 27 del Indice de Paz Global 2026: quien lidera y quien cae",
        claim_date="2026-06",
        post_url="https://estenerife.com/indice-paz-global-2026-espana-puesto-27-indice-paz-global/",
        post_url_tipo="prensa", emisor="EsTenerife", emisor_tipo="prensa_digital",
        emisor_nivel=4, pais="ES", tema="rankings",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="Institute for Economics & Peace (IEP) - Global Peace Index 2026 Report (PDF 125 pp) + A3 map poster (ranking); edicion anterior: Global Peace Index 2025 Report (PDF 122 pp); todos en visionofhumanity.org",
        primaria_url="https://www.visionofhumanity.org/wp-content/uploads/2026/06/Global-Peace-Index-2026-Report.pdf",
        primaria_url_tipo="pdf_informe (texto extraible; tabla de ranking p.10-12 y tabla regional p.24-26); poster: .../2026/06/Global-Peace-Index-2026-A3-map-poster.pdf; 2025: .../2025/06/Global-Peace-Index-2025-web.pdf (patron de URL por ano)",
        via_de_acceso="pdf", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="si", alcanzable_por_humano="si",
        recuperabilidad="B", formato="pdf",
        dato_actual="GPI 2026: Espana puesto 27, score 1,654, cambio de rank publicado por el IEP: UP 4 (mejora cuatro puestos respecto al rank 2025 REVISADO), cambio de score +0,002 (respecto al score 2025 revisado, 1,652). Islandia 1 (1,161); ultimo Rusia",
        dato_anterior="GPI 2025 (edicion publicada en junio 2025): Espana puesto 25, score 1,578, sin cambio (=) respecto a 2024 revisado. Diferencia entre 1,578 (publicado 2025) y 1,652 (2025 revisado en 2026): +0,074, es la revision anual de datos del IEP",
        raw_value_span_actual=(
            "[IEP, GPI 2026 Report, p.12 / poster] '26 Bulgaria 1.628 DOWN-LONG 4 27 Spain 1.654 UP-LONG 4 "
            "28 Germany 1.657 DOWN-LONG 5' (UP/DOWN = icono de cambio de puesto) | [p.26, tabla Europa: "
            "rank regional, pais, score, cambio de score, rank global] '18 Spain 1.654 0.002 27' || "
            "[estenerife 2026-06-13, el claim] 'Espana, en el puesto 27 del Indice de Paz Global 2026: "
            "quien lidera y quien cae' | 'Indice de Paz Global 2026: Espana cae al puesto 27' | 'retrocede "
            "dos posiciones' | posicion anterior (2025): puesto 25 | 'Islandia repite un ano mas en lo mas "
            "alto' | 'Rusia cierra la tabla'"
        ),
        raw_value_span_anterior=(
            "[IEP, GPI 2025 Report, p.10] '24 Estonia 1.559 DOWN-LONG 2 25 Spain 1.578 ↔ 26 Mauritius "
            "1.586 DOWN-LONG 3' | [p.21, tabla Europa] '18 Spain 1.578 0.003 25'"
        ),
        truth="mixed", context="divergence_detected",
        clase_primaria="2_baseline_selection", clases_secundarias="5_methodology_change", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="divergencia_real", excedente="si",
        notas=(
            "NEEDS_REVIEW; candidato a caso canonico. El puesto 27 es exacto (supported). 'Cae dos "
            "posiciones' se obtiene restando el rank publicado en 2025 (25) del publicado en 2026 (27). "
            "Pero el IEP revisa cada ano la serie anterior y publica el cambio de puesto contra el rank "
            "2025 REVISADO: para Espana marca UP 4, es decir, MEJORA cuatro puestos, con score practicamente "
            "plano (+0,002). Verificacion de la semantica del icono: Suiza publicada 5 (2025) -> 3 (2026) "
            "aparece como DOWN 1, e Irlanda 2 -> 5 como DOWN 1: los cambios son contra la serie revisada, "
            "no contra la edicion publicada. El mismo hecho se lee como 'cae 2' o 'sube 4' segun la base "
            "elegida: 2_baseline_selection, con 5_methodology_change (revision retroactiva de datos) como "
            "causa. El medio no menciona la revision. Divergencia; EXCEDENTE (cubeta llena). El buscador "
            "devolvio ademas 'Espana 25 en 2026' (statbase): un agregador desactualizado; se ignoro por "
            "no ser primaria. Los PDF del IEP siguen un patron de URL por ano (wp-content/uploads/<ano>/06/), "
            "lo que hizo trivial localizar la edicion anterior."
        ),
        criba_query_a="Espana puesto 27 Indice de Paz Global 2026",
        criba_query_b="Espana puesto 27 Indice Paz Global 2026 dos posiciones verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K32", case_id="C30",
        claim_text="INEI: empleo se incremento 4,7% en Lima Metropolitana en el primer trimestre de 2026",
        claim_date="2026-04-15",
        post_url="https://elcomercio.pe/economia/peru/inei-empleo-se-incremento-47-en-lima-metropolitana-en-el-primer-trimestre-de-2026-l-ultimas-noticia/",
        post_url_tipo="prensa", emisor="El Comercio (Peru)", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="PE", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEI - Informe de Empleo N 4, 'Situacion del Mercado Laboral en Lima Metropolitana', trimestre movil enero-febrero-marzo 2026 (EPEN), PDF 79 pp via gob.pe; nota de prensa gob.pe 1379039 (2026-04-15); edicion anterior: Informe de Empleo N 4, ene-feb-mar 2025",
        primaria_url="https://cdn.www.gob.pe/uploads/document/file/9807769/8016127-informe-de-empleo-n-4-trimestre-ene-feb-mar-2026.pdf",
        primaria_url_tipo="pdf_informe (texto extraible) enlazado desde gob.pe/institucion/inei/informes-publicaciones/8016127-...; coleccion completa por trimestre movil en gob.pe/institucion/inei/colecciones/6041-informe-de-empleo; 2025: cdn.www.gob.pe/uploads/document/file/7927021/6670682-...-2025.pdf",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="Ene-feb-mar 2026, Lima Metropolitana: poblacion ocupada 5.702.500, +4,7% (253.200) vs ene-feb-mar 2025; desocupados 418.900 (6,8% de la PEA), +9,6% (36.600); tasa de desempleo 6,8%, +0,2 pp (2025: 6,6%)",
        dato_anterior="Ene-feb-mar 2025: poblacion ocupada 5.449.300, +1,7% (89.600) vs 2024; desempleados 382.300; tasa de desempleo 6,6% (-1,1 pp vs 7,7% en 2024)",
        raw_value_span_actual=(
            "[INEI, Informe de Empleo N4 ene-feb-mar 2026, p.4] 'En el trimestre enero-febrero-marzo 2026, "
            "la poblacion ocupada de Lima Metropolitana se situo en 5 millones 702 mil 500 personas. "
            "Comparado con similar trimestre movil del ano anterior, aumento en 4,7% (253 mil 200)' | [p.2] "
            "'ascendio a 418 mil 900 personas (6,8% de la PEA). Comparada con similar trimestre movil del "
            "ano anterior aumento en 9,6% (36 mil 600 personas)' | [p.19] 'la tasa de desempleo de Lima "
            "Metropolitana se ubico en 6,8% ... En comparacion con similar trimestre movil del ano "
            "anterior (6,6%), la tasa de desempleo aumento en 0,2 punto porcentual' || [gob.pe nota "
            "1379039] 'En el trimestre movil enero-febrero-marzo de 2026, la tasa de desempleo de Lima "
            "Metropolitana se ubico en 6,8% con relacion a similar trimestre del ano anterior' || "
            "[elcomercio 2026-04-15, el claim] 'INEI: empleo se incremento 4,7% en Lima Metropolitana en el "
            "primer trimestre de 2026' | 'poblacion ocupada de Lima Metropolitana aumento en 4,7%' (253.200) "
            "| 5.702.500 | 'tasa de desempleo de Lima Metropolitana se ubico en 6,8%' | 418.900"
        ),
        raw_value_span_anterior=(
            "[INEI, Informe de Empleo N4 ene-feb-mar 2025, p.4] 'En el trimestre enero-febrero-marzo 2025, "
            "la poblacion ocupada de Lima Metropolitana se situo en 5 millones 449 mil 300 personas. "
            "Comparado con similar trimestre movil del ano anterior, aumento en 1,7% (89 mil 600)' | [p.19] "
            "'la tasa de desempleo de Lima Metropolitana se ubico en 6,6%, en cifras absolutas se estima "
            "que 382 mil 300 personas buscaron un empleo activamente'"
        ),
        truth="supported", context="no_divergence_detected",
        clase_primaria="none", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "DEC-021 (2026-09-25, Mateo): gob.pe devolvio 418 al fetcher; el 200 posterior de curl NO cuenta. El caso se cierra como no recuperable-por-agente y cubeta bloqueado_por_publicador. Los valores extraidos se conservan como registro (sirven para comparar con los 5 casos manuales), pero no suman en la metrica que decide. Etiquetas truth/context: las que dio la lectura, marcadas como obtenidas por via descartada. || "
            "Relay fiel del informe (cifras, periodo 'trimestre movil', comparacion interanual y tasa "
            "'se ubico en 6,8%'). Control negativo; EXCEDENTE (cubeta llena). Par con C31 (Altavoz), que "
            "convierte la misma tasa en una subida. Ruta: el buscador devolvio un PDF de INEI (boletines/"
            "4906.pdf) con el mismo titulo que resulto ser la edicion de MAYO 2003: mismo nombre de "
            "producto, 23 anos de diferencia; se descarto por fecha y se llego al informe correcto por la "
            "coleccion de gob.pe. DEC-018, zona gris a declarar: gob.pe devolvio '418 I'm a Teapot' al "
            "fetcher (respuesta anti-bot explicita) y 200 a curl con su UA por defecto; no se falsifico "
            "identidad, pero si se cambio de cliente. Se reporta para que Mateo decida si eso cuenta como "
            "evasion (P-14). La propia nota del INEI ('se ubico en 6,8% con relacion a similar trimestre "
            "del ano anterior') tiene una redaccion que invita a leer el nivel como variacion."
        ),
        criba_query_a="INEI empleo Lima Metropolitana 4,7% primer trimestre 2026",
        criba_query_b="empleo Lima Metropolitana crecio 4,7% primer trimestre 2026 INEI verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    dict(
        cid="K41", case_id="C31",
        claim_text="Desempleo en Lima Metropolitana sube en 6,8% en el primer trimestre de 2026",
        claim_date="2026-04-15",
        post_url="https://altavoz.pe/economia/desempleo-en-lima-metropolitana-sube-en-68-en-el-primer-trimestre-de-2026/",
        post_url_tipo="prensa", emisor="Altavoz", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="PE", tema="empleo",
        # --- trabajo 2026-09-25 ---
        fuente_primaria="INEI - Informe de Empleo N 4, 'Situacion del Mercado Laboral en Lima Metropolitana', ene-feb-mar 2026 (misma primaria que C30); edicion anterior: ene-feb-mar 2025",
        primaria_url="https://cdn.www.gob.pe/uploads/document/file/9807769/8016127-informe-de-empleo-n-4-trimestre-ene-feb-mar-2026.pdf",
        primaria_url_tipo="pdf_informe (texto extraible) via gob.pe (misma ruta que C30)",
        via_de_acceso="bloqueado", access_requires_login="no",
        current_edition_found="si", previous_edition_found="si",
        historical_series_found="si", methodology_found="si",
        alcanzable_por_agente="no", alcanzable_por_humano="si",
        recuperabilidad="D", formato="pdf",
        dato_actual="Tasa de desempleo ene-feb-mar 2026: 6,8% (NIVEL), +0,2 puntos porcentuales vs 6,6%; desocupados 418.900, +9,6% (36.600) interanual",
        dato_anterior="Tasa de desempleo ene-feb-mar 2025: 6,6%; desempleados 382.300",
        raw_value_span_actual=(
            "[INEI, Informe de Empleo N4 ene-feb-mar 2026, p.19] 'la tasa de desempleo de Lima "
            "Metropolitana se ubico en 6,8%, en cifras absolutas se estima que 418 mil 900 personas "
            "buscaron un empleo activamente ... En comparacion con similar trimestre movil del ano anterior "
            "(6,6%), la tasa de desempleo aumento en 0,2 punto porcentual' | [p.2] 'aumento en 9,6% (36 mil "
            "600 personas)' || [altavoz 2026-04-15, el claim] 'Desempleo en Lima Metropolitana sube en 6,8% "
            "en el primer trimestre de 2026' | 'la tasa de desempleo en Lima Metropolitana se incremento "
            "en 6,8%' | 418.900"
        ),
        raw_value_span_anterior=(
            "[INEI, Informe de Empleo N4 ene-feb-mar 2025, p.19] 'la tasa de desempleo de Lima "
            "Metropolitana se ubico en 6,6%, en cifras absolutas se estima que 382 mil 300 personas'"
        ),
        truth="contradicted", context="divergence_detected",
        clase_primaria="3_absolute_vs_relative", clases_secundarias="", abstain_reason="",
        abandonado_por_tiempo="", bucket_resultado="bloqueado_por_publicador", excedente="no",
        notas=(
            "DEC-021 (2026-09-25, Mateo): misma primaria que C30, mismo 418 de gob.pe al fetcher; el 200 de curl no cuenta. Cubeta bloqueado_por_publicador, no recuperable-por-agente; valores y etiquetas se conservan como registro obtenido por via descartada. || "
            "El 6,8% es el nivel de la tasa de desempleo, no su variacion: la tasa subio 0,2 puntos "
            "(6,6 -> 6,8) y el numero de desempleados subio 9,6%. 'Sube en 6,8%' no corresponde a ninguna "
            "magnitud del informe: contradicted. Test de contexto: nivel presentado como variacion relativa "
            "(3_absolute_vs_relative, provisional; alternativa: METRIC_AMBIGUOUS si se considera que el "
            "titular no define la magnitud). Divergencia; EXCEDENTE (cubeta llena). Par util con C30 (El "
            "Comercio relaya bien la misma tabla el mismo dia). Origen probable del error: la nota del "
            "INEI dice 'se ubico en 6,8% con relacion a similar trimestre del ano anterior'. Localizacion "
            "de coste cero (primaria ya en mano por C30): minutes_to_locate no representativo."
        ),
        criba_query_a="INEI empleo Lima Metropolitana 4,7% primer trimestre 2026",
        criba_query_b="empleo Lima Metropolitana crecio 4,7% primer trimestre 2026 INEI verificacion OR bulo",
        criba_resultado="admitido", criba_motivo="", criba_url_verificacion="",
    ),
    # ---- rechazados de la tanda 2 ------------------------------------------------
    dict(
        cid="K18",
        claim_text="Las llegadas irregulares a Canarias caen casi un 60% hasta agosto frente al 35% de descenso en la UE",
        claim_date="2026-09-11",
        post_url="https://www.moncloa.com/2026/09/11/llegadas-irregulares-canarias-caen-60-agosto-3429986/",
        post_url_tipo="prensa", emisor="Moncloa.com", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="migracion",
        criba_query_a="llegadas irregulares Canarias caen 60% 2026 agosto",
        criba_query_b="llegadas irregulares Canarias caen 59,5% 4.808 hasta agosto 2026 verificacion OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: Newtral (Saiz 2026-07-02, Sanchez 2026-09-04) y Verificat han verificado repetidamente la caida de llegadas a Canarias en 2026 contra los balances quincenales de Interior. La misma serie, con cortes anteriores",
        criba_url_verificacion="https://www.newtral.es/llegadas-irregulares-elma-saiz-factcheck/20260702/",
    ),
    dict(
        cid="K19",
        claim_text="Las llegadas irregulares a Ceuta se disparan un 191% en 2026",
        claim_date="2026-08-17",
        post_url="https://www.catalunyapress.es/articulo/sociedad/2026-08-17/5986361-llegadas-irregulares-ceuta-disparan-191-2026",
        post_url_tipo="prensa", emisor="Catalunya Press", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="migracion",
        criba_query_a="llegadas irregulares Ceuta se disparan 191% 2026",
        criba_query_b="Ceuta llegadas irregulares 191% 2026 verificacion OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: Newtral (2026-07-31, +129% desde enero) y las recopilaciones de Maldita de bulos sobre Ceuta (2026-07-31 a 2026-09-18) cubren la misma serie de entradas por tierra de Interior",
        criba_url_verificacion="https://www.newtral.es/ceuta-regularizacion-migrantes/20260731/",
    ),
    dict(
        cid="K31",
        claim_text="Indec: la pobreza subio al 32,3% en el primer semestre de 2026 y alcanza a unos 15,5 millones de argentinos",
        claim_date="2026-09-24",
        post_url="https://www.eltribuno.com/nacionales/2026-9-24-16-22-0-indec-la-pobreza-subio-al-32-3-en-el-primer-semestre-de-2026-y-alcanza-a-unos-15-5-millones-de-argentinos",
        post_url_tipo="prensa", emisor="El Tribuno", emisor_tipo="prensa_digital",
        emisor_nivel=1, pais="AR", tema="pobreza",
        criba_query_a="pobreza 32,3% primer semestre 2026 15,5 millones INDEC",
        criba_query_b="pobreza 32,3% 15,5 millones argentinos primer semestre 2026 verificacion OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="cobertura_explainer: Chequeado publico el mismo dia su explainer sobre la misma nota del INDEC, con los mismos numeros y la misma extrapolacion a poblacion total (15 millones)",
        criba_url_verificacion="https://chequeado.com/el-explicador/la-pobreza-aumento-al-323-en-el-primer-semestre-de-2026-y-alcanza-a-15-millones-de-personas-en-todo-el-pais/",
    ),
    dict(
        cid="K23",
        claim_text="Verano mas calido en 157 anos y tercero mas seco en Espana",
        claim_date="2026-09-22",
        post_url="https://agrodigital.com/2026/09/22/verano-mas-calido-aemet/",
        post_url_tipo="prensa", emisor="Agrodigital", emisor_tipo="prensa_digital",
        emisor_nivel=3, pais="ES", tema="clima",
        criba_query_a="verano 2026 mas calido 157 anos AEMET",
        criba_query_b="verano 2026 mas caluroso en 157 anos AEMET verificacion OR bulo OR fact-check",
        criba_resultado="rechazado",
        criba_motivo="duplicado: misma afirmacion, misma fecha y misma fuente primaria que K22. No es la regla dura; se excluye de la tasa de rechazo por verificacion",
        criba_url_verificacion="",
    ),
]
