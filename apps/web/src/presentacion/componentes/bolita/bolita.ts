/**
 * bolita: el boton circular que VERITAI pone sobre la esquina de una
 * publicacion, en la pagina de un tercero (docs/ARQUITECTURA-VISUAL.md §2.2).
 *
 * Capa de presentacion: recibe un estado del contrato y devuelve un <button>
 * suelto, construido con createElement y textContent. No hace fetch, no lee la
 * pagina y no decide nada: pinta la fase de la consulta o los dos ejes del
 * veredicto tal como llegan. Quien lo coloca en la pagina, dentro de la raiz
 * aislada de presentacion/montar.ts, es aplicacion.
 *
 * Dos canales, uno por eje (DEC-016; Mateo, 2026-10-03): el simbolo lleva el
 * color de `context` y el anillo el de `truth`. La interfaz no los resume en
 * un estado unico, porque eso seria decidir un veredicto.
 *
 * El estado se dice ademas en palabras: es el nombre accesible del boton
 * (aria-label) y la etiqueta que aparece al pasar por encima o al enfocarlo.
 * El color nunca es la unica senal.
 *
 * Es un <button> nativo a proposito: el navegador ya lo pone en el orden de
 * tabulacion y convierte Enter y Espacio en `click`. No hay manejadores de
 * teclado propios que mantener ni que puedan duplicar la pulsacion.
 *
 * Dentro lleva dos cosas: el disco, que es lo que se ve y lo que se mueve (el
 * anillo, el halo del pulso y el simbolo minimo), y la etiqueta con el estado
 * en palabras. La hoja esta en bolita.css; aqui no hay ni un color ni un tamano.
 */

import { FaseConsulta } from "../../../contrato/fase-consulta";
import { t } from "../../../i18n";
import { visualContext, visualFase, visualTruth } from "../../estados";

/**
 * Lo que la bolita muestra: una fase de la consulta, o los dos ejes de un
 * veredicto. `truth` y `context` son los valores tal como llegan de la API; un
 * valor fuera del enum se pinta como `desconocido` (estados.ts), no se corrige.
 */
export type EstadoBolita = { fase: FaseConsulta } | { truth: string; context: string };

export interface AccionesBolita {
  alPulsar: () => void;
}

const BLOQUE = "veritai-bolita";
/** Modificador comun a cualquier veredicto: anillo grueso, porque lleva `truth`. */
const MODIFICADOR_VEREDICTO = "veredicto";

/** La etiqueta visible de cada bolita, para actualizarla sin buscarla en el DOM. */
const ETIQUETAS = new WeakMap<HTMLButtonElement, HTMLSpanElement>();

/** Un <span> que solo se ve: los lectores de pantalla ya tienen el aria-label del boton. */
function decorativo(clase: string): HTMLSpanElement {
  const nodo = document.createElement("span");
  nodo.className = clase;
  nodo.setAttribute("aria-hidden", "true");
  return nodo;
}

export function crearBolita(estado: EstadoBolita, acciones: AccionesBolita): HTMLButtonElement {
  const bolita = document.createElement("button");
  bolita.type = "button";
  bolita.dataset["veritai"] = "bolita";

  // El disco es lo que se ve y lo que crece o encoge. La etiqueta va fuera de el
  // para no escalarse con el: el texto no puede cambiar de tamano al pulsar.
  const disco = decorativo(`${BLOQUE}__disco`);
  disco.append(decorativo(`${BLOQUE}__pulso`), decorativo(`${BLOQUE}__simbolo`));
  const etiqueta = decorativo(`${BLOQUE}__etiqueta`);
  ETIQUETAS.set(bolita, etiqueta);
  bolita.append(disco, etiqueta);

  bolita.addEventListener("click", () => acciones.alPulsar());
  fijarEstadoBolita(bolita, estado);
  return bolita;
}

/**
 * Cambia el estado de una bolita ya creada sin sustituir el nodo: si el
 * usuario la tiene enfocada mientras analiza, el foco no se pierde cuando
 * llega el veredicto. Tambien es lo que se llama al cambiar de idioma: el
 * texto se vuelve a componer desde las plantillas, no se traduce el ya pintado.
 */
export function fijarEstadoBolita(bolita: HTMLButtonElement, estado: EstadoBolita): void {
  const etiqueta = ETIQUETAS.get(bolita);
  if (etiqueta === undefined) {
    throw new Error("fijarEstadoBolita: este elemento no lo creo crearBolita");
  }

  let modificadores: string[];
  let texto: string;

  if ("fase" in estado) {
    const fase = visualFase(estado.fase);
    modificadores = [fase.modificador];
    texto = t("bolita.etiqueta_fase", { fase: t(fase.clave) });
    bolita.dataset["veritaiFase"] = fase.estado;
    delete bolita.dataset["veritaiTruth"];
    delete bolita.dataset["veritaiContext"];
  } else {
    const truth = visualTruth(estado.truth);
    const context = visualContext(estado.context);
    modificadores = [MODIFICADOR_VEREDICTO, context.modificador, truth.modificador];
    texto = t("bolita.etiqueta_veredicto", { context: t(context.clave), truth: t(truth.clave) });
    bolita.dataset["veritaiTruth"] = truth.estado;
    bolita.dataset["veritaiContext"] = context.estado;
    delete bolita.dataset["veritaiFase"];
  }

  bolita.className = [BLOQUE, ...modificadores.map((m) => `${BLOQUE}--${m}`)].join(" ");
  bolita.setAttribute("aria-label", texto);
  etiqueta.textContent = texto;

  if ("fase" in estado && estado.fase === FaseConsulta.Analizando) {
    bolita.setAttribute("aria-busy", "true");
  } else {
    bolita.removeAttribute("aria-busy");
  }
}
