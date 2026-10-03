/**
 * montar: la raiz aislada donde VERITAI pinta dentro de una pagina de terceros
 * (docs/ARQUITECTURA-VISUAL.md §2).
 *
 * Todo lo que se inyecta va dentro de un shadow root. Es la unica manera de
 * que el CSS de la pagina no deforme lo nuestro y de que el nuestro no toque
 * la pagina. Cuatro decisiones, cada una cierra una via de fuga:
 *
 *   1. El anfitrion es un elemento con nombre propio (<veritai-raiz>), no un
 *      <div>: los selectores de elemento de la pagina (`div`, `span`,
 *      `button`) no lo alcanzan. No se registra como custom element: solo se
 *      usa el nombre.
 *   2. El shadow root es cerrado: el JavaScript de la pagina no puede entrar
 *      por `anfitrion.shadowRoot`.
 *   3. Los estilos entran como hojas adoptadas (adoptedStyleSheets), no como
 *      <style>: no se anade ningun nodo de estilo al documento ni al arbol, y
 *      todas las raices comparten las mismas hojas.
 *   4. Dentro hay un unico elemento raiz, .veritai-raiz, que es donde se
 *      declaran los tokens y donde se corta la herencia (estilos/raiz.css).
 *
 * Esta funcion no inserta nada en la pagina: devuelve el anfitrion y el punto
 * de montaje. Donde se coloca el anfitrion lo decide aplicacion.
 *
 * El panel suelto de desarrollo (index.html) no pasa por aqui: es una pagina
 * nuestra y enlaza sus hojas directamente.
 */

import cssBolita from "./componentes/bolita/bolita.css?inline";
import cssRaiz from "./estilos/raiz.css?inline";
import cssTokens from "./estilos/tokens.css?inline";

/** Nombre del elemento anfitrion. Lleva guion: es un nombre de elemento propio valido. */
const ETIQUETA_ANFITRION = "veritai-raiz";
/** Clase del elemento raiz de dentro; es el selector donde tokens.css declara los tokens. */
const CLASE_RAIZ = "veritai-raiz";

/**
 * Las hojas que entran al shadow root, en orden: tokens, reinicio de la raiz y
 * la de cada componente que se inyecta. Un componente nuevo se registra aqui
 * (§6.2, paso 4).
 */
const HOJAS_CSS: readonly string[] = [cssTokens, cssRaiz, cssBolita];

let hojas: CSSStyleSheet[] | null = null;

/** Las hojas se construyen una vez y las comparten todas las raices. */
function hojasCompartidas(): CSSStyleSheet[] {
  if (hojas === null) {
    hojas = HOJAS_CSS.map((css) => {
      const hoja = new CSSStyleSheet();
      hoja.replaceSync(css);
      return hoja;
    });
  }
  return hojas;
}

export interface RaizAislada {
  /** El elemento que se inserta en la pagina. Lo coloca quien llama. */
  anfitrion: HTMLElement;
  /** Donde se montan los componentes: el elemento raiz de dentro del shadow root. */
  punto: HTMLElement;
}

export function crearRaizAislada(): RaizAislada {
  const anfitrion = document.createElement(ETIQUETA_ANFITRION);
  const sombra = anfitrion.attachShadow({ mode: "closed" });
  sombra.adoptedStyleSheets = hojasCompartidas();

  const punto = document.createElement("div");
  punto.className = CLASE_RAIZ;
  sombra.append(punto);

  return { anfitrion, punto };
}
