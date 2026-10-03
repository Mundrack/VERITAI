/**
 * Vitrina de la bolita: una pagina local para VER el componente en todos sus
 * estados y comprobar, en un navegador de verdad, lo que happy-dom no modela.
 *
 *   npm run vitrina      ->  http://127.0.0.1:5174/vitrina/
 *
 * Es una herramienta de desarrollo, como scripts/ y tests/: vive fuera de
 * src/, no entra en el build ni en la extension, y no esta conectada a ninguna
 * pagina real ni a la API. Solo usa lo que usaria aplicacion: crearRaizAislada
 * y crearBolita.
 *
 * La pagina hace de "pagina de un tercero": no carga ninguna hoja de VERITAI.
 * La zona hostil intenta deformar la bolita con todo lo que una pagina puede
 * hacer; la tabla del final mide si lo ha conseguido.
 */

import { VALORES_CONTEXT, VALORES_TRUTH } from "../src/contrato/enums";
import { FaseConsulta, VALORES_FASE_CONSULTA } from "../src/contrato/fase-consulta";
import { fijarLocale, localesDisponibles, obtenerLocale, type Locale } from "../src/i18n";
import {
  crearBolita,
  fijarEstadoBolita,
  type EstadoBolita,
} from "../src/presentacion/componentes/bolita/bolita";
import { crearRaizAislada } from "../src/presentacion/montar";

/** Lo que tarda el analisis simulado del ciclo. No hay API detras: es un temporizador. */
const ANALISIS_SIMULADO_MS = 2500;
/** Un valor que ningun enum conoce, para ver el estado `desconocido`. */
const VALOR_AJENO = "valor_que_no_existe";
/** Lo que pidio Mateo el 2026-10-03: 54 px con raton, 44 px con dedo. */
const LADO_ESPERADO_PX = { fino: 54, grueso: 44 } as const;

interface Montada {
  anfitrion: HTMLElement;
  punto: HTMLElement;
  bolita: HTMLButtonElement;
  estado: EstadoBolita;
}

/** Todas las bolitas de la pagina, para volver a componer sus textos al cambiar de idioma. */
const MONTADAS: Montada[] = [];

function el<K extends keyof HTMLElementTagNameMap>(etiqueta: K, texto?: string, clase?: string): HTMLElementTagNameMap[K] {
  const nodo = document.createElement(etiqueta);
  if (texto !== undefined) nodo.textContent = texto;
  if (clase !== undefined) nodo.className = clase;
  return nodo;
}

function montar(estado: EstadoBolita, alPulsar: () => void = () => undefined): Montada {
  const { anfitrion, punto } = crearRaizAislada();
  const bolita = crearBolita(estado, { alPulsar });
  punto.append(bolita);
  const montada = { anfitrion, punto, bolita, estado };
  MONTADAS.push(montada);
  return montada;
}

function cambiar(montada: Montada, estado: EstadoBolita): void {
  montada.estado = estado;
  fijarEstadoBolita(montada.bolita, estado);
}

function muestra(montada: Montada, pie: string): HTMLElement {
  const figura = el("figure", undefined, "muestra");
  figura.append(montada.anfitrion, el("figcaption", pie));
  return figura;
}

function seccion(titulo: string, ...parrafos: string[]): HTMLElement {
  const nodo = el("section");
  nodo.append(el("h2", titulo), ...parrafos.map((texto) => el("p", texto)));
  return nodo;
}

// --- Secciones ---------------------------------------------------------------

function cabecera(): HTMLElement {
  const nodo = el("header");
  nodo.append(
    el("h1", "Vitrina de la bolita"),
    el(
      "p",
      "El botón circular que VERITAI pone sobre la esquina de una publicación. Cada bolita de esta página va en su " +
        "propio shadow root, como irá en la página de un tercero. Pasa el ratón por encima, pulsa, y recórrelas con " +
        "Tab: el foco muestra el estado en palabras, a la izquierda de la bolita.",
    ),
  );

  const controles = el("div", undefined, "controles");
  const etiqueta = el("label", "Idioma de las etiquetas ");
  const selector = el("select");
  for (const locale of localesDisponibles()) {
    const opcion = el("option", locale.toUpperCase());
    opcion.value = locale;
    opcion.selected = locale === obtenerLocale();
    selector.append(opcion);
  }
  selector.addEventListener("change", () => {
    fijarLocale(selector.value as Locale);
    // Se vuelve a componer desde las plantillas; no se traduce lo ya pintado.
    for (const montada of MONTADAS) fijarEstadoBolita(montada.bolita, montada.estado);
  });
  etiqueta.append(selector);
  controles.append(
    etiqueta,
    el(
      "span",
      "El tema y el movimiento siguen al sistema. Para probarlos sin cambiar el sistema: DevTools > Rendering > " +
        "\"Emulate CSS media feature\" (prefers-color-scheme, prefers-reduced-motion).",
      "nota",
    ),
  );
  nodo.append(controles);
  return nodo;
}

function fases(): HTMLElement {
  const nodo = seccion(
    "Fases de la consulta",
    "Sin veredicto todavía: símbolo y anillo del mismo color, anillo fino. El fallo lleva además el anillo discontinuo.",
  );
  const fila = el("div", undefined, "fila");
  for (const fase of VALORES_FASE_CONSULTA) fila.append(muestra(montar({ fase }), fase));
  nodo.append(fila);
  return nodo;
}

function veredictos(): HTMLElement {
  const nodo = seccion(
    "Veredicto: dos ejes, dos canales",
    "El anillo lleva truth (filas) y el símbolo lleva context (columnas). La interfaz no los resume en un estado " +
      "único. La última fila y la última columna son un valor que el enum no conoce: desconocido.",
  );
  const tabla = el("table", undefined, "matriz");
  const cabeza = el("tr");
  cabeza.append(el("th", "truth \\ context"));
  const columnas = [...VALORES_CONTEXT, VALOR_AJENO];
  for (const context of columnas) cabeza.append(el("th", context));
  tabla.append(cabeza);
  for (const truth of [...VALORES_TRUTH, VALOR_AJENO]) {
    const fila = el("tr");
    fila.append(el("th", truth));
    for (const context of columnas) {
      const celda = el("td");
      celda.append(montar({ truth, context }).anfitrion);
      fila.append(celda);
    }
    tabla.append(fila);
  }
  nodo.append(tabla);
  return nodo;
}

function ciclo(): HTMLElement {
  const nodo = seccion(
    "Ciclo: en espera, analizando, veredicto",
    "Pulsa la bolita (o enfócala y pulsa Enter o Espacio). El análisis es simulado: un temporizador, no la API. " +
      "El nodo no se sustituye, así que el foco no se pierde cuando llega el veredicto.",
  );
  const contador = el("p", "Pulsaciones: 0", "nota");
  let pulsaciones = 0;
  const montada: Montada = montar({ fase: FaseConsulta.EnEspera }, () => {
    pulsaciones += 1;
    contador.textContent = `Pulsaciones: ${pulsaciones}`;
    if ("fase" in montada.estado && montada.estado.fase === FaseConsulta.Analizando) return;
    if (!("fase" in montada.estado)) {
      cambiar(montada, { fase: FaseConsulta.EnEspera });
      return;
    }
    cambiar(montada, { fase: FaseConsulta.Analizando });
    window.setTimeout(() => cambiar(montada, { truth: "supported", context: "divergence_detected" }), ANALISIS_SIMULADO_MS);
  });
  const fila = el("div", undefined, "fila");
  fila.append(muestra(montada, "púlsame"));
  nodo.append(fila, contador);
  return nodo;
}

interface ZonaHostil {
  nodo: HTMLElement;
  dentro: Montada;
  gemelo: HTMLButtonElement;
}

function zonaHostil(): ZonaHostil {
  const nodo = seccion(
    "Página hostil",
    "Dentro del recuadro, la página aplica con !important reglas de elemento, reglas con nuestras mismas clases, " +
      "propiedades heredables y hasta nuestros propios tokens. Arriba, la bolita; debajo, un botón DE LA PÁGINA " +
      "con la clase .veritai-bolita. La página deforma el suyo y no el nuestro; lo nuestro no toca el suyo.",
  );
  const zona = el("div", undefined, "pagina-hostil");
  const dentro = montar({ fase: FaseConsulta.EnEspera });

  const gemelo = el("button", "botón de la página", "veritai-bolita veritai-bolita--fase-en_espera");
  gemelo.type = "button";
  const envoltorio = el("div", undefined, "veritai-raiz");
  envoltorio.append(gemelo);

  zona.append(dentro.anfitrion, envoltorio);
  nodo.append(zona);
  return { nodo, dentro, gemelo };
}

// --- Autocomprobacion --------------------------------------------------------

interface Comprobacion {
  que: string;
  esperado: string;
  medido: string;
  bien: boolean;
}

const PROPIEDADES_DE_LA_BOLITA = ["width", "height", "display", "boxSizing", "color", "cursor", "fontFamily", "fontSize"] as const;

const PROPIEDADES_DEL_DISCO = [
  "width",
  "height",
  "backgroundColor",
  "borderTopColor",
  "borderTopWidth",
  "borderTopStyle",
  "borderTopLeftRadius",
  "boxShadow",
] as const;

const PROPIEDADES_DE_LA_ETIQUETA = [
  "display",
  "color",
  "fontFamily",
  "fontSize",
  "lineHeight",
  "letterSpacing",
  "wordSpacing",
  "textTransform",
  "textAlign",
  "textIndent",
  "textShadow",
  "whiteSpace",
  "fontWeight",
  "fontStyle",
  "direction",
] as const;

/** Primera propiedad en la que difieren dos elementos, o null si coinciden en todas. */
function primeraDiferencia(a: Element, b: Element, propiedades: readonly (keyof CSSStyleDeclaration)[]): string | null {
  const [estiloA, estiloB] = [getComputedStyle(a), getComputedStyle(b)];
  for (const propiedad of propiedades) {
    if (estiloA[propiedad] !== estiloB[propiedad]) {
      return `${String(propiedad)}: ${String(estiloA[propiedad])} frente a ${String(estiloB[propiedad])}`;
    }
  }
  return null;
}

/** Las partes de una bolita, por su sitio: disco (con pulso y simbolo dentro) y etiqueta. */
function partesDe(montada: Montada): { disco: Element; pulso: Element; simbolo: Element; etiqueta: Element } {
  const [disco, etiqueta] = Array.from(montada.bolita.children);
  const [pulso, simbolo] = Array.from(disco?.children ?? []);
  if (disco === undefined || etiqueta === undefined || pulso === undefined || simbolo === undefined) {
    throw new Error("la bolita no tiene la estructura esperada");
  }
  return { disco, pulso, simbolo, etiqueta };
}

/** Luminancia relativa (WCAG) de un color calculado `rgb(r, g, b)`: para saber si el disco es claro u oscuro. */
function luminancia(rgb: string): number {
  const canales = (rgb.match(/[\d.]+/g) ?? []).slice(0, 3).map((texto) => {
    const canal = Number(texto) / 255;
    return canal <= 0.03928 ? canal / 12.92 : ((canal + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * (canales[0] ?? 0) + 0.7152 * (canales[1] ?? 0) + 0.0722 * (canales[2] ?? 0);
}

async function comprobar(referencia: Montada, analizando: Montada, hostil: ZonaHostil): Promise<Comprobacion[]> {
  const filas: Comprobacion[] = [];
  const anotar = (que: string, esperado: string, medido: string, bien: boolean) =>
    filas.push({ que, esperado, medido, bien });

  const tactil = window.matchMedia("(pointer: coarse)").matches;
  const reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const oscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;

  // Aislamiento
  anotar("El shadow root está cerrado", "anfitrion.shadowRoot = null", `${String(referencia.anfitrion.shadowRoot)}`, referencia.anfitrion.shadowRoot === null);

  const hojas = { adoptadas: document.adoptedStyleSheets.length, style: document.querySelectorAll("style").length, link: document.querySelectorAll("link[rel='stylesheet']").length };
  anotar(
    "No hay ninguna hoja nuestra en el documento",
    "0 adoptadas, 0 <style>, 1 <link> (la de la vitrina)",
    `${hojas.adoptadas} adoptadas, ${hojas.style} <style>, ${hojas.link} <link>`,
    hojas.adoptadas === 0 && hojas.style === 0 && hojas.link === 1,
  );

  const alcanzadas = document.querySelectorAll("[data-veritai='bolita']").length;
  anotar("Desde el documento no se alcanza ninguna bolita", `0 de ${MONTADAS.length}`, `${alcanzadas} de ${MONTADAS.length}`, alcanzadas === 0);

  const estiloGemelo = getComputedStyle(hostil.gemelo);
  const hostilActua = estiloGemelo.textTransform === "uppercase" && estiloGemelo.width === "200px" && estiloGemelo.letterSpacing === "6px";
  anotar(
    "La hoja hostil actúa de verdad sobre la página",
    "botón de la página: 200px, uppercase, 6px",
    `${estiloGemelo.width}, ${estiloGemelo.textTransform}, ${estiloGemelo.letterSpacing}`,
    hostilActua,
  );

  const [partesHostil, partesReferencia, partesAnalizando] = [partesDe(hostil.dentro), partesDe(referencia), partesDe(analizando)];
  const propiedadesComparadas = PROPIEDADES_DE_LA_BOLITA.length + PROPIEDADES_DEL_DISCO.length;
  const diferenciaBolita =
    primeraDiferencia(hostil.dentro.bolita, referencia.bolita, PROPIEDADES_DE_LA_BOLITA) ??
    primeraDiferencia(partesHostil.disco, partesReferencia.disco, PROPIEDADES_DEL_DISCO);
  anotar(
    "La bolita de la zona hostil se calcula igual que la de fuera",
    `${propiedadesComparadas} propiedades iguales`,
    diferenciaBolita ?? `${propiedadesComparadas} propiedades iguales`,
    diferenciaBolita === null,
  );

  const diferenciaEtiqueta = primeraDiferencia(partesHostil.etiqueta, partesReferencia.etiqueta, PROPIEDADES_DE_LA_ETIQUETA);
  anotar(
    "La herencia no entra: la etiqueta de la zona hostil es igual que la de fuera",
    `${PROPIEDADES_DE_LA_ETIQUETA.length} propiedades iguales`,
    diferenciaEtiqueta ?? `${PROPIEDADES_DE_LA_ETIQUETA.length} propiedades iguales`,
    diferenciaEtiqueta === null,
  );

  const radioGemelo = estiloGemelo.borderTopLeftRadius;
  anotar(
    "Lo nuestro no sale: el botón de la página con clase .veritai-bolita no recibe nuestro estilo",
    "radio 0px, sin sombra, sin transición nuestra",
    `radio ${radioGemelo}, sombra ${estiloGemelo.boxShadow}, transición ${estiloGemelo.transitionProperty}`,
    radioGemelo === "0px" && estiloGemelo.boxShadow === "none" && !estiloGemelo.transitionProperty.includes("box-shadow"),
  );

  // Tamano y unidades
  const caja = referencia.bolita.getBoundingClientRect();
  const lado = tactil ? LADO_ESPERADO_PX.grueso : LADO_ESPERADO_PX.fino;
  anotar(
    `Tamaño con puntero ${tactil ? "grueso (dedo)" : "fino (ratón)"}`,
    `${lado} x ${lado} px`,
    `${caja.width} x ${caja.height} px`,
    caja.width === lado && caja.height === lado,
  );

  const cajaAnfitrion = referencia.anfitrion.getBoundingClientRect();
  anotar(
    "El anfitrión no ocupa en la página más que la bolita",
    `${caja.width} x ${caja.height} px`,
    `${cajaAnfitrion.width} x ${cajaAnfitrion.height} px`,
    cajaAnfitrion.width === caja.width && cajaAnfitrion.height === caja.height,
  );

  const remDeLaPagina = getComputedStyle(document.documentElement).fontSize;
  const [letraRaiz, letraEtiqueta] = [getComputedStyle(referencia.punto).fontSize, getComputedStyle(partesReferencia.etiqueta).fontSize];
  anotar(
    `No depende del rem de la página (aquí el <html> está a ${remDeLaPagina})`,
    "raiz 15px, etiqueta 13px",
    `raiz ${letraRaiz}, etiqueta ${letraEtiqueta}`,
    letraRaiz === "15px" && letraEtiqueta === "13px",
  );

  // Movimiento
  const animacion = getComputedStyle(partesAnalizando.pulso).animationName;
  const transicion = getComputedStyle(partesAnalizando.disco).transitionProperty;
  anotar(
    `Movimiento ${reducido ? "reducido" : "sin preferencia"}: pulso mientras analiza`,
    reducido ? "none" : "veritai-bolita-pulso",
    animacion,
    animacion === (reducido ? "none" : "veritai-bolita-pulso"),
  );
  anotar(
    `Movimiento ${reducido ? "reducido" : "sin preferencia"}: transición al crecer y encoger`,
    reducido ? "none" : "transform, box-shadow",
    transicion,
    transicion === (reducido ? "none" : "transform, box-shadow"),
  );

  // Tema
  const disco = getComputedStyle(partesReferencia.disco).backgroundColor;
  const esOscuro = luminancia(disco) < 0.5;
  anotar(`Tema ${oscuro ? "oscuro" : "claro"}: el disco de la bolita lo sigue`, oscuro ? "disco oscuro" : "disco claro", `${disco}`, esOscuro === oscuro);

  // Simbolo
  const estiloSimbolo = getComputedStyle(partesReferencia.simbolo);
  const mascara = estiloSimbolo.maskImage || estiloSimbolo.webkitMaskImage;
  const url = /url\("?([^")]+)"?\)/.exec(mascara)?.[1];
  let respuesta = "sin url";
  if (url !== undefined) {
    try {
      const r = await fetch(url);
      respuesta = `${r.status} ${r.headers.get("content-type") ?? ""}`;
    } catch (error) {
      respuesta = String(error);
    }
  }
  anotar(
    "El símbolo mínimo carga y se pinta con el color del estado",
    "máscara veritai-simbolo-min.svg, 200 image/svg+xml, fondo = color",
    `${url?.split("/").pop() ?? "sin máscara"}, ${respuesta}, fondo ${estiloSimbolo.backgroundColor} / color ${getComputedStyle(referencia.bolita).color}`,
    (url ?? "").includes("veritai-simbolo-min") && respuesta.startsWith("200 image/svg+xml") && estiloSimbolo.backgroundColor === getComputedStyle(referencia.bolita).color,
  );

  return filas;
}

function tablaDeComprobacion(filas: Comprobacion[]): HTMLElement {
  const nodo = seccion(
    "Autocomprobación en este navegador",
    "Lo que sigue se ha medido ahora mismo, en este navegador, con getComputedStyle. Es lo que las pruebas con " +
      "happy-dom no pueden medir: que la herencia de la página no entra y que all: initial hace su trabajo.",
  );
  const tabla = el("table", undefined, "comprobacion");
  const fallos = filas.filter((fila) => !fila.bien).length;
  tabla.dataset["resultado"] = fallos === 0 ? "bien" : "mal";
  tabla.dataset["fallos"] = String(fallos);
  const cabeza = el("tr");
  cabeza.append(el("th", "Qué"), el("th", "Esperado"), el("th", "Medido"), el("th", ""));
  tabla.append(cabeza);
  for (const fila of filas) {
    const tr = el("tr");
    tr.dataset["bien"] = String(fila.bien);
    const [esperado, medido] = [el("td"), el("td")];
    esperado.append(el("code", fila.esperado));
    medido.append(el("code", fila.medido));
    tr.append(el("td", fila.que), esperado, medido, el("td", fila.bien ? "bien" : "MAL"));
    tabla.append(tr);
  }
  nodo.append(tabla, el("p", `${filas.length - fallos} de ${filas.length} comprobaciones bien.`, "nota"));
  return nodo;
}

// --- Arranque ----------------------------------------------------------------

async function iniciar(raiz: HTMLElement): Promise<void> {
  fijarLocale("es");
  const seccionFases = fases();
  const referencia = MONTADAS.find((m) => "fase" in m.estado && m.estado.fase === FaseConsulta.EnEspera);
  const analizando = MONTADAS.find((m) => "fase" in m.estado && m.estado.fase === FaseConsulta.Analizando);
  if (referencia === undefined || analizando === undefined) throw new Error("faltan las bolitas de referencia");

  const hostil = zonaHostil();
  raiz.append(cabecera(), seccionFases, veredictos(), ciclo(), hostil.nodo);
  // Las medidas se toman con todo ya en el documento.
  raiz.append(tablaDeComprobacion(await comprobar(referencia, analizando, hostil)));
}

const raiz = document.getElementById("vitrina");
if (raiz) void iniciar(raiz);
