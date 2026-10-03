/**
 * montar: la raiz aislada (docs/ARQUITECTURA-VISUAL.md §2).
 *
 * Lo que Mateo pidio el 2026-10-03: que nada de lo que haga la bolita pueda
 * afectar al CSS de la pagina que la aloja, ni al reves, y que no se filtren
 * estilos fuera del shadow root.
 *
 * Que mide esta prueba y que no. happy-dom modela bien la frontera de los
 * SELECTORES (los de la pagina no entran, los nuestros no salen), las hojas
 * adoptadas y las custom properties; eso se comprueba aqui con estilos
 * calculados. No aplica `all: initial` ni las reglas `:host`, asi que el corte
 * de la HERENCIA se comprueba por estructura (la regla esta y dice lo que debe)
 * y, con un navegador de verdad, en la autocomprobacion de la vitrina.
 */

import { afterEach, describe, expect, test } from "vitest";

import { FaseConsulta } from "../../src/contrato/fase-consulta";
import cssBolita from "../../src/presentacion/componentes/bolita/bolita.css?inline";
import { crearBolita } from "../../src/presentacion/componentes/bolita/bolita";
import cssRaiz from "../../src/presentacion/estilos/raiz.css?inline";
import { crearRaizAislada } from "../../src/presentacion/montar";
import { fijarPreferencias, limpiarEntorno, TEMAS } from "../_entorno";
import { token } from "./_tokens";

/** Propiedades que la hoja de la bolita fija y que, si se filtrara, cambiarian en la pagina. */
const PROPIEDADES_VIGILADAS = [
  "width",
  "height",
  "color",
  "backgroundColor",
  "borderTopColor",
  "borderTopWidth",
  "borderTopStyle",
  "borderRadius",
  "display",
  "position",
  "boxShadow",
  "cursor",
  "transitionProperty",
  "animationName",
  "fontFamily",
] as const;

function foto(elemento: Element): Record<string, string> {
  const estilo = getComputedStyle(elemento);
  return Object.fromEntries(PROPIEDADES_VIGILADAS.map((propiedad) => [propiedad, estilo[propiedad]]));
}

/** Un boton DE LA PAGINA con las mismas clases que el nuestro: lo peor que puede pasar por casualidad. */
function gemeloDeLaPagina(): { boton: HTMLButtonElement; pulso: HTMLSpanElement } {
  const boton = document.createElement("button");
  boton.className = "veritai-bolita veritai-bolita--fase-analizando";
  boton.dataset["veritai"] = "bolita";
  const pulso = document.createElement("span");
  pulso.className = "veritai-bolita__pulso";
  const envoltorio = document.createElement("div");
  envoltorio.className = "veritai-raiz";
  boton.append(pulso);
  envoltorio.append(boton);
  document.body.append(envoltorio);
  return { boton, pulso };
}

function montarBolita() {
  const raiz = crearRaizAislada();
  const bolita = crearBolita({ fase: FaseConsulta.Analizando }, { alPulsar: () => undefined });
  raiz.punto.append(bolita);
  document.body.append(raiz.anfitrion);
  return { ...raiz, bolita, sombra: raiz.punto.getRootNode() as ShadowRoot };
}

function estiloDePagina(css: string): void {
  const estilo = document.createElement("style");
  estilo.textContent = css;
  document.head.append(estilo);
}

function sinComentarios(css: string): string {
  return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

/** Selectores de las reglas de estilo de una hoja, incluidas las de dentro de @media; uno por elemento. */
function selectoresDe(hoja: CSSStyleSheet): string[] {
  const selectores: string[] = [];
  const recorrer = (lista: CSSRuleList) => {
    for (const regla of Array.from(lista)) {
      if (regla instanceof CSSStyleRule) {
        selectores.push(...regla.selectorText.split(",").map((s) => s.replace(/\s+/g, " ").trim()));
      } else if (regla instanceof CSSMediaRule) {
        recorrer(regla.cssRules);
      }
    }
  };
  recorrer(hoja.cssRules);
  return selectores;
}

describe("raiz aislada", () => {
  afterEach(limpiarEntorno);

  describe("como se monta", () => {
    test("el anfitrion es un elemento con nombre propio, sin atributos, y su shadow root esta cerrado", () => {
      const { anfitrion, punto } = crearRaizAislada();
      const sombra = punto.getRootNode() as ShadowRoot;

      expect(anfitrion.tagName.toLowerCase()).toBe("veritai-raiz");
      expect(anfitrion.attributes).toHaveLength(0); // ni class, ni id, ni style: nada a lo que la pagina pueda agarrarse
      expect(anfitrion.childNodes).toHaveLength(0); // nada nuestro queda en el DOM de la pagina
      expect(anfitrion.shadowRoot).toBeNull(); // cerrado: el JavaScript de la pagina no entra
      expect(sombra).toBeInstanceOf(ShadowRoot);
      expect(sombra.mode).toBe("closed");
      expect(sombra.host).toBe(anfitrion);
      expect(`${punto.tagName.toLowerCase()}.${punto.className}`).toBe("div.veritai-raiz");
      expect(Array.from(sombra.children)).toEqual([punto]);
    });

    test("crear la raiz no inserta nada en la pagina: la coloca quien llama", () => {
      const { anfitrion } = crearRaizAislada();
      expect(anfitrion.isConnected).toBe(false);
      expect(document.body.childNodes).toHaveLength(0);
      expect(document.head.childNodes).toHaveLength(0);
    });

    test("los estilos entran como hojas adoptadas y compartidas: ni un <style> ni un <link>, ni dentro ni fuera", () => {
      const primera = montarBolita();
      const segunda = montarBolita();

      expect(primera.sombra.adoptedStyleSheets).toHaveLength(3);
      primera.sombra.adoptedStyleSheets.forEach((hoja, i) => {
        expect(segunda.sombra.adoptedStyleSheets[i]).toBe(hoja); // las mismas hojas, no copias
        expect(hoja.cssRules.length).toBeGreaterThan(0); // y no vacias
      });
      expect(primera.sombra.querySelectorAll("style, link")).toHaveLength(0);
      expect(document.querySelectorAll("style, link")).toHaveLength(0);
      expect(document.adoptedStyleSheets).toHaveLength(0);
      expect(document.styleSheets).toHaveLength(0);
    });
  });

  describe("hacia fuera: lo nuestro no toca la pagina", () => {
    test("un boton de la pagina con nuestras mismas clases se queda exactamente como estaba", () => {
      const antes = gemeloDeLaPagina();
      const fotoAntes = { boton: foto(antes.boton), pulso: foto(antes.pulso) };

      const { bolita } = montarBolita();

      const despues = gemeloDeLaPagina(); // otro, creado ya con lo nuestro montado
      expect(foto(despues.boton)).toEqual(fotoAntes.boton);
      expect(foto(despues.pulso)).toEqual(fotoAntes.pulso);

      // La comparacion mide algo: el nuestro, con las mismas clases, si esta estilado.
      expect(foto(bolita)).not.toEqual(fotoAntes.boton);
      expect(getComputedStyle(bolita).width).toBe("54px");
      expect(getComputedStyle(despues.boton).width).not.toBe("54px");
      expect(getComputedStyle(despues.pulso).animationName).not.toBe("veritai-bolita-pulso");
    });

    test("los tokens no salen: ni el documento ni sus elementos ven ninguna variable --veritai-", () => {
      const gemelo = gemeloDeLaPagina();
      montarBolita();
      for (const nodo of [document.documentElement, document.body, gemelo.boton]) {
        const estilo = getComputedStyle(nodo);
        expect(estilo.getPropertyValue("--veritai-bolita-tamano")).toBe("");
        expect(estilo.getPropertyValue("--veritai-color-fase-analizando")).toBe("");
      }
    });

    test("desde el documento no se alcanza nada de dentro", () => {
      const { anfitrion } = montarBolita();
      expect(document.querySelector("[data-veritai]")).toBeNull();
      expect(document.querySelector(".veritai-bolita, .veritai-raiz")).toBeNull();
      expect(document.querySelectorAll("button")).toHaveLength(0);
      expect(anfitrion.innerHTML).toBe("");
      expect(document.body.textContent).toBe("");
    });
  });

  describe("hacia dentro: la pagina no toca lo nuestro", () => {
    const PAGINA_HOSTIL = `
      * { color: #00ff00; font-family: fantasy; box-sizing: content-box; }
      button { width: 300px; height: 300px; border-radius: 0; border: 9px dotted #00ff00; background-color: #00ff00; }
      span { display: block; width: 200px; height: 200px; background-color: #00ff00; }
      div { display: none; }
      .veritai-bolita { width: 1px; height: 1px; display: none; color: #00ff00; border-color: #00ff00; }
      .veritai-bolita__etiqueta { display: block; }
      .veritai-raiz { display: none; }
      [data-veritai] { display: none; }
      :root, *, veritai-raiz, .veritai-raiz {
        --veritai-bolita-tamano: 999px;
        --veritai-color-fase-analizando: #00ff00;
        --veritai-bolita-fondo: #00ff00;
      }
    `;

    for (const tema of TEMAS) {
      test(`tema ${tema}: con una hoja hostil en la pagina, la bolita mide, se ve y se colorea igual`, () => {
        fijarPreferencias({ tema });
        estiloDePagina(PAGINA_HOSTIL);
        const { bolita, punto } = montarBolita();
        const estilo = getComputedStyle(bolita);
        const disco = getComputedStyle(bolita.querySelector(".veritai-bolita__disco")!);
        const color = token("--veritai-color-fase-analizando", { tema });

        expect([estilo.width, estilo.height]).toEqual(["54px", "54px"]);
        expect(estilo.display).toBe("block");
        expect(estilo.color).toBe(color);
        expect(estilo.backgroundColor).toBe("transparent");
        expect(estilo.boxSizing).toBe("border-box");
        expect(disco.display).toBe("flex");
        expect(disco.borderTopColor).toBe(color);
        expect(disco.borderTopStyle).toBe("solid");
        expect(disco.borderTopWidth).toBe(token("--veritai-bolita-anillo-ancho-fase", { tema }));
        expect(disco.backgroundColor).toBe(token("--veritai-bolita-fondo", { tema }));

        expect(getComputedStyle(punto).display).toBe("block");
        expect(getComputedStyle(punto).fontFamily).toBe(token("--veritai-tipografia-familia", { tema }));
        expect(getComputedStyle(punto).color).toBe(token("--veritai-color-texto", { tema }));

        const etiqueta = bolita.querySelector(".veritai-bolita__etiqueta")!;
        expect(getComputedStyle(etiqueta).display).toBe("none");
        expect(getComputedStyle(etiqueta).color).toBe(token("--veritai-color-texto", { tema }));
      });
    }

    test("la hoja hostil si hace efecto en la pagina: la prueba anterior no pasa por casualidad", () => {
      estiloDePagina(PAGINA_HOSTIL);
      const gemelo = gemeloDeLaPagina();
      expect(getComputedStyle(gemelo.boton).display).toBe("none");
      expect(getComputedStyle(gemelo.boton).color).toBe("#00ff00");
      expect(getComputedStyle(gemelo.boton).getPropertyValue("--veritai-bolita-tamano")).toBe("999px");
    });
  });

  describe("la herencia y las unidades", () => {
    test("la herencia se corta dos veces: all: initial en :host y en .veritai-raiz", () => {
      const { sombra } = montarBolita();
      const reglas = sombra.adoptedStyleSheets.flatMap((hoja) =>
        Array.from(hoja.cssRules).filter((regla): regla is CSSStyleRule => regla instanceof CSSStyleRule),
      );
      for (const selector of [":host", ".veritai-raiz"]) {
        const reinicio = reglas.find((regla) => regla.selectorText === selector && regla.style.getPropertyValue("all") !== "");
        expect(reinicio, `no hay reinicio en ${selector}`).toBeDefined();
        expect(reinicio!.style.getPropertyValue("all")).toBe("initial");
        // `all` no reinicia `direction` (la especificacion la excluye) y se hereda: va a mano.
        expect(reinicio!.style.getPropertyValue("direction"), `${selector} no fija direction`).toBe("ltr");
      }
    });

    test("una pagina de derecha a izquierda no cambia la direccion de lo nuestro", () => {
      estiloDePagina("* { direction: rtl; } veritai-raiz { direction: rtl; }");
      const { punto, bolita } = montarBolita();
      expect(getComputedStyle(document.body).direction).toBe("rtl"); // la regla de la pagina actua
      expect(getComputedStyle(punto).direction).toBe("ltr");
      expect(getComputedStyle(bolita.querySelector(".veritai-bolita__etiqueta")!).direction).toBe("ltr");
    });

    test("los tokens se declaran dentro, en .veritai-raiz, donde la pagina no llega", () => {
      const { sombra } = montarBolita();
      const [tokens] = sombra.adoptedStyleSheets;
      expect(selectoresDe(tokens!).sort()).toEqual([".veritai-raiz", ".veritai-raiz", ".veritai-raiz", ":root", ":root", ":root"]);
    });

    test("todo selector de las hojas que se inyectan empieza por .veritai- o :host, y no hay selectores de elemento", () => {
      const { sombra } = montarBolita();
      const [, raiz, bolita] = sombra.adoptedStyleSheets;
      const selectores = [...selectoresDe(raiz!), ...selectoresDe(bolita!)];

      expect(selectores.length).toBeGreaterThan(20);
      for (const selector of selectores) {
        expect(selector, selector).toMatch(/^(\.veritai-|:host)/);
        for (const compuesto of selector.split(/[\s>+~]+/)) {
          expect(compuesto, `"${compuesto}" en "${selector}"`).toMatch(/^[.:]/); // nunca una etiqueta suelta: button, span, div
        }
      }
    });

    test("nada de lo que se inyecta depende del <html> de la pagina: ni rem ni unidades de ventana", () => {
      const inyectado = sinComentarios(cssRaiz) + sinComentarios(cssBolita);
      const dependeDeLaPagina = /\d(rem|vw|vh|vmin|vmax)\b/;
      expect(inyectado).not.toMatch(dependeDeLaPagina);

      const usados = [...new Set(inyectado.match(/--veritai-[\w-]+/g) ?? [])].filter((nombre) => !inyectado.includes(`${nombre}:`));
      expect(usados.length).toBeGreaterThan(30);
      for (const tema of TEMAS) {
        for (const puntero of ["fino", "grueso"] as const) {
          for (const nombre of usados) {
            expect(token(nombre, { tema, puntero }), `${nombre} (${tema}, puntero ${puntero})`).not.toMatch(dependeDeLaPagina);
          }
        }
      }
    });
  });
});
