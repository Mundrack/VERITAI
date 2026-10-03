/**
 * estado-servicio: el estado del entorno local (API y base de datos vivas o no).
 *
 * Es lo que main.ts pintaba el 2026-10-03, movido a la capa de presentacion
 * (docs/ARQUITECTURA-VISUAL.md §1.1, §2): recibe datos del contrato y
 * devuelve un elemento suelto construido con createElement y textContent.
 * No hace fetch, no lee la pagina, no calcula nada: cuenta filas.
 */

import { BASE_DE_DATOS_CONECTADA, type RespuestaSalud } from "../../../contrato/salud";
import { formatearHora } from "../../../formato/fechas";
import { localesDisponibles, obtenerLocale, t, type Locale } from "../../../i18n";

export interface DatosEstadoServicio {
  /** Respuesta de GET /health, o null si la API no respondio. */
  salud: RespuestaSalud | null;
  /** Momento en que se consulto. */
  consultadoEn: Date;
}

export interface AccionesEstadoServicio {
  alRecomprobar: () => void;
  alCambiarIdioma: (locale: Locale) => void;
}

/** Una fila de la tabla de servicios: la etiqueta y si esta vivo. */
interface Servicio {
  claveEtiqueta: string;
  activo: boolean;
  textoActivo: string;
  textoInactivo: string;
}

const BLOQUE = "veritai-estado-servicio";
const ID_SELECTOR_IDIOMA = "veritai-idioma"; // for/id del <label>; con prefijo para no chocar con la pagina

function elemento<K extends keyof HTMLElementTagNameMap>(
  etiqueta: K,
  clase?: string,
  texto?: string,
): HTMLElementTagNameMap[K] {
  const nodo = document.createElement(etiqueta);
  if (clase !== undefined) nodo.className = clase;
  if (texto !== undefined) nodo.textContent = texto;
  return nodo;
}

function marca(servicio: Servicio): HTMLSpanElement {
  const estado = servicio.activo ? "ok" : "mal";
  return elemento(
    "span",
    `${BLOQUE}__marca ${BLOQUE}__marca--${estado}`,
    servicio.activo ? servicio.textoActivo : servicio.textoInactivo,
  );
}

function fila(cabecera: string, contenido: HTMLElement | string): HTMLTableRowElement {
  const tr = elemento("tr");
  tr.append(elemento("th", `${BLOQUE}__cabecera`, cabecera));
  const td = elemento("td", `${BLOQUE}__celda`);
  if (typeof contenido === "string") td.textContent = contenido;
  else td.append(contenido);
  tr.append(td);
  return tr;
}

export function crearEstadoServicio(
  datos: DatosEstadoServicio,
  acciones: AccionesEstadoServicio,
): HTMLElement {
  const { salud } = datos;
  const locale = obtenerLocale();

  const servicios: Servicio[] = [
    {
      claveEtiqueta: "estado.api",
      activo: salud !== null,
      textoActivo: "OK",
      textoInactivo: t("estado.sin_respuesta"),
    },
    {
      claveEtiqueta: "estado.base_de_datos",
      activo: salud?.base_de_datos === BASE_DE_DATOS_CONECTADA,
      textoActivo: t("estado.conectada"),
      textoInactivo: t("estado.no_disponible"),
    },
  ];
  const activos = servicios.filter((s) => s.activo).length;

  const raiz = elemento("div", BLOQUE);

  raiz.append(
    elemento("h1", `${BLOQUE}__titulo`, t("app.titulo")),
    elemento("p", `${BLOQUE}__subtitulo`, t("app.subtitulo")),
    elemento("div", `${BLOQUE}__aviso`, t("app.aviso_puerta")),
    elemento("h2", undefined, t("estado.titulo")),
  );

  const tabla = elemento("table", `${BLOQUE}__tabla`);
  const cuerpo = elemento("tbody");
  for (const servicio of servicios) {
    cuerpo.append(fila(t(servicio.claveEtiqueta), marca(servicio)));
  }
  cuerpo.append(
    fila(t("estado.entorno"), salud?.entorno ?? "-"),
    fila(t("estado.version"), salud?.version ?? "-"),
  );
  tabla.append(cuerpo);
  raiz.append(tabla);

  const accionesNodo = elemento("div", `${BLOQUE}__acciones`);
  const boton = elemento("button", `${BLOQUE}__boton`, t("acciones.recomprobar"));
  boton.dataset["veritai"] = "recomprobar";
  boton.addEventListener("click", () => acciones.alRecomprobar());

  const etiqueta = elemento("label", undefined, t("acciones.idioma"));
  etiqueta.htmlFor = ID_SELECTOR_IDIOMA;

  const selector = elemento("select", `${BLOQUE}__selector`);
  selector.id = ID_SELECTOR_IDIOMA;
  selector.dataset["veritai"] = "idioma";
  for (const l of localesDisponibles()) {
    const opcion = elemento("option", undefined, l.toUpperCase());
    opcion.value = l;
    opcion.selected = l === locale;
    selector.append(opcion);
  }
  selector.addEventListener("change", () => {
    // Se vuelve a renderizar desde las plantillas del nuevo idioma.
    // No se traduce el DOM ya pintado (CLAUDE.md §10; src/i18n/index.ts).
    acciones.alCambiarIdioma(selector.value as Locale);
  });
  accionesNodo.append(boton, etiqueta, selector);
  raiz.append(accionesNodo);

  const pie = elemento(
    "p",
    `${BLOQUE}__pie`,
    `${t("plantilla.servicios_activos", { activos, total: servicios.length })} · ${t(
      "plantilla.consultado_en",
      { hora: formatearHora(datos.consultadoEn, locale) },
    )}`,
  );
  raiz.append(pie);

  return raiz;
}
