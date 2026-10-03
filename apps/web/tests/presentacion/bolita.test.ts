/**
 * bolita (docs/ARQUITECTURA-VISUAL.md §2.2, §5.2 prueba de componente).
 *
 * Lo que Mateo pidio comprobar el 2026-10-03: que se monta, que cada estado da
 * el color y la etiqueta que debe, que el teclado funciona y que respeta la
 * preferencia de movimiento. El aislamiento del shadow root tiene su propia
 * prueba (montar.test.ts) y la paleta la suya (accesibilidad.test.ts).
 *
 * Los colores esperados no estan copiados aqui: se leen de tokens.css
 * (_tokens.ts). La prueba mide que el estado llega al token que le toca, en
 * tema claro y en oscuro, pasando por la clase y por la hoja de verdad.
 */

import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

import { VALORES_CONTEXT, VALORES_TRUTH } from "../../src/contrato/enums";
import { FaseConsulta, VALORES_FASE_CONSULTA } from "../../src/contrato/fase-consulta";
import en from "../../src/i18n/en.json";
import es from "../../src/i18n/es.json";
import { fijarLocale } from "../../src/i18n";
import cssBolita from "../../src/presentacion/componentes/bolita/bolita.css?inline";
import fuenteBolita from "../../src/presentacion/componentes/bolita/bolita.ts?raw";
import {
  crearBolita,
  fijarEstadoBolita,
  type EstadoBolita,
} from "../../src/presentacion/componentes/bolita/bolita";
import { DESCONOCIDO } from "../../src/presentacion/estados";
import { crearRaizAislada } from "../../src/presentacion/montar";
import { fijarPreferencias, limpiarEntorno, TEMAS, type Preferencias } from "../_entorno";
import { token } from "./_tokens";

const CATALOGOS = { es, en } as const;
type Idioma = keyof typeof CATALOGOS;
const IDIOMAS = Object.keys(CATALOGOS) as Idioma[];

const TRUTH_Y_DESCONOCIDO = [...VALORES_TRUTH, DESCONOCIDO];
const CONTEXT_Y_DESCONOCIDO = [...VALORES_CONTEXT, DESCONOCIDO];
/** Un valor que ningun enum conoce: la API anadio algo y la interfaz aun no lo sabe. */
const VALOR_AJENO = "valor_que_no_existe";

/** Crea la bolita, la mete en una raiz aislada y la raiz en el documento, como hara aplicacion. */
function montar(estado: EstadoBolita, preferencias: Preferencias = {}) {
  fijarPreferencias(preferencias); // antes de montar: happy-dom calcula los estilos con lo que haya entonces
  const alPulsar = vi.fn();
  const raiz = crearRaizAislada();
  const bolita = crearBolita(estado, { alPulsar });
  raiz.punto.append(bolita);
  document.body.append(raiz.anfitrion);
  return { ...raiz, bolita, alPulsar };
}

function parte(bolita: HTMLElement, nombre: string): HTMLElement {
  const nodo = bolita.querySelector<HTMLElement>(`.veritai-bolita__${nombre}`);
  if (nodo === null) throw new Error(`la bolita no tiene __${nombre}`);
  return nodo;
}

/** El valor real de un eje para pedir el estado `desconocido`: un valor que el enum no tiene. */
function valorDe(estado: string): string {
  return estado === DESCONOCIDO ? VALOR_AJENO : estado;
}

function textoFase(idioma: Idioma, fase: string): string {
  const catalogo: Record<string, string> = CATALOGOS[idioma];
  return catalogo["bolita.etiqueta_fase"]!.replace("{fase}", catalogo[`fase.${fase}`]!);
}

function textoVeredicto(idioma: Idioma, truth: string, context: string): string {
  const catalogo: Record<string, string> = CATALOGOS[idioma];
  return catalogo["bolita.etiqueta_veredicto"]!
    .replace("{context}", catalogo[`context.${context}`]!)
    .replace("{truth}", catalogo[`truth.${truth}`]!);
}

interface Regla {
  selector: string;
  estilo: CSSStyleDeclaration;
  /** Condicion del @media que la envuelve, o null si esta suelta. */
  media: string | null;
}

/** Un selector agrupado puede venir partido en lineas: se deja como "a, b". */
function selectorEnUnaLinea(selector: string): string {
  return selector
    .split(",")
    .map((trozo) => trozo.replace(/\s+/g, " ").trim())
    .join(", ");
}

/** Todas las reglas de estilo de las hojas que la raiz aislada tiene adoptadas. */
function reglasAdoptadas(nodo: Node): Regla[] {
  const reglas: Regla[] = [];
  const recorrer = (lista: CSSRuleList, media: string | null) => {
    for (const regla of Array.from(lista)) {
      if (regla instanceof CSSStyleRule) reglas.push({ selector: selectorEnUnaLinea(regla.selectorText), estilo: regla.style, media });
      else if (regla instanceof CSSMediaRule) recorrer(regla.cssRules, regla.conditionText);
    }
  };
  for (const hoja of (nodo.getRootNode() as ShadowRoot).adoptedStyleSheets) recorrer(hoja.cssRules, null);
  return reglas;
}

describe("bolita", () => {
  beforeEach(() => fijarLocale("es"));
  afterEach(limpiarEntorno);

  describe("se monta", () => {
    test("es un <button type=button> con su gancho, y dentro lleva el disco (con el pulso y el simbolo) y la etiqueta", () => {
      const { bolita, punto } = montar({ fase: FaseConsulta.EnEspera });

      expect(bolita.tagName).toBe("BUTTON");
      expect(bolita.getAttribute("type")).toBe("button");
      expect(bolita.dataset["veritai"]).toBe("bolita");
      expect(bolita.parentElement).toBe(punto);
      const hijos = (padre: Element) => Array.from(padre.children).map((hijo) => `${hijo.tagName.toLowerCase()}.${hijo.className}`);
      expect(hijos(bolita)).toEqual(["span.veritai-bolita__disco", "span.veritai-bolita__etiqueta"]);
      expect(hijos(parte(bolita, "disco"))).toEqual(["span.veritai-bolita__pulso", "span.veritai-bolita__simbolo"]);
    });

    test("el simbolo es el minimo, entra como mascara y toma el color del estado: no lleva color propio ni SVG incrustado", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });

      expect(bolita.querySelector("svg, img, use")).toBeNull();
      const regla = reglasAdoptadas(bolita).find((r) => r.selector === ".veritai-bolita__simbolo");
      expect(regla, "no hay regla para .veritai-bolita__simbolo").toBeDefined();
      expect(regla!.estilo.getPropertyValue("background-color").toLowerCase()).toBe("currentcolor");
      expect(cssBolita).toMatch(/mask-image:\s*url\([^)]*veritai-simbolo-min\.svg[^)]*\)/);
      expect(cssBolita).not.toMatch(/veritai-simbolo\.svg/); // el de orbita es para 48 px o mas
    });

    test("las partes de dentro son decorativas: el lector de pantalla solo recibe el nombre del boton", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      const dentro = Array.from(bolita.querySelectorAll("*"));
      expect(dentro).toHaveLength(4);
      for (const nodo of dentro) {
        expect(nodo.getAttribute("aria-hidden"), nodo.className).toBe("true");
      }
      expect(bolita.getAttribute("aria-label")).toBe(parte(bolita, "etiqueta").textContent);
    });
  });

  describe("cada estado da el color que debe", () => {
    for (const tema of TEMAS) {
      test(`tema ${tema}: en cada fase el simbolo y el anillo llevan el color de la fase, con anillo fino`, () => {
        for (const fase of VALORES_FASE_CONSULTA) {
          const { bolita } = montar({ fase }, { tema });
          const anillo = getComputedStyle(parte(bolita, "disco"));
          const esperado = token(`--veritai-color-fase-${fase}`, { tema });

          expect(getComputedStyle(bolita).color, `simbolo en fase ${fase}`).toBe(esperado);
          expect(anillo.borderTopColor, `anillo en fase ${fase}`).toBe(esperado);
          expect(anillo.borderTopWidth, `ancho del anillo en fase ${fase}`).toBe(
            token("--veritai-bolita-anillo-ancho-fase", { tema }),
          );
          limpiarEntorno();
        }
      });

      test(`tema ${tema}: con veredicto el simbolo lleva el color de context y el anillo el de truth, en las 30 combinaciones`, () => {
        for (const truth of TRUTH_Y_DESCONOCIDO) {
          for (const context of CONTEXT_Y_DESCONOCIDO) {
            const { bolita } = montar({ truth: valorDe(truth), context: valorDe(context) }, { tema });
            const anillo = getComputedStyle(parte(bolita, "disco"));
            const caso = `truth=${truth}, context=${context}`;

            expect(getComputedStyle(bolita).color, `simbolo con ${caso}`).toBe(token(`--veritai-color-context-${context}`, { tema }));
            expect(anillo.borderTopColor, `anillo con ${caso}`).toBe(token(`--veritai-color-truth-${truth}`, { tema }));
            expect(anillo.borderTopWidth, `ancho del anillo con ${caso}`).toBe(
              token("--veritai-bolita-anillo-ancho-veredicto", { tema }),
            );
            limpiarEntorno();
          }
        }
      });

      test(`tema ${tema}: un color por estado: dentro de cada eje no hay dos estados con el mismo color`, () => {
        const ejes: Record<string, readonly string[]> = {
          fase: VALORES_FASE_CONSULTA,
          truth: TRUTH_Y_DESCONOCIDO,
          context: CONTEXT_Y_DESCONOCIDO,
        };
        for (const [eje, estados] of Object.entries(ejes)) {
          const colores = estados.map((estado) => token(`--veritai-color-${eje}-${estado}`, { tema }));
          expect(new Set(colores).size, `${eje}: ${colores.join(", ")}`).toBe(estados.length);
        }
      });
    }

    test("el fallo de la consulta se distingue tambien por la forma: anillo discontinuo", () => {
      const estiloDelAnillo = (estado: EstadoBolita) => getComputedStyle(parte(montar(estado).bolita, "disco")).borderTopStyle;
      expect(estiloDelAnillo({ fase: FaseConsulta.Error })).toBe("dashed");
      limpiarEntorno();
      expect(estiloDelAnillo({ fase: FaseConsulta.EnEspera })).toBe("solid");
      limpiarEntorno();
      expect(estiloDelAnillo({ truth: "contradicted", context: "undetermined" })).toBe("solid");
    });

    test("la clase de estado es el valor del enum tal cual, y una bolita nunca lleva a la vez fase y veredicto", () => {
      const enFase = montar({ fase: FaseConsulta.Analizando }).bolita;
      expect(enFase.className).toBe("veritai-bolita veritai-bolita--fase-analizando");
      expect(enFase.dataset["veritaiFase"]).toBe("analizando");
      expect(enFase.dataset["veritaiTruth"]).toBeUndefined();
      expect(enFase.dataset["veritaiContext"]).toBeUndefined();

      const conVeredicto = montar({ truth: "supported", context: "divergence_detected" }).bolita;
      expect(conVeredicto.className).toBe(
        "veritai-bolita veritai-bolita--veredicto veritai-bolita--context-divergence_detected veritai-bolita--truth-supported",
      );
      expect(conVeredicto.dataset["veritaiTruth"]).toBe("supported");
      expect(conVeredicto.dataset["veritaiContext"]).toBe("divergence_detected");
      expect(conVeredicto.dataset["veritaiFase"]).toBeUndefined();
    });
  });

  describe("cada estado da la etiqueta que debe, en palabras", () => {
    for (const idioma of IDIOMAS) {
      test(`${idioma}: cada fase y cada veredicto se dicen con el texto del catalogo, en el nombre accesible y en la etiqueta visible`, () => {
        fijarLocale(idioma);

        for (const fase of VALORES_FASE_CONSULTA) {
          const { bolita } = montar({ fase });
          const esperado = textoFase(idioma, fase);
          expect(bolita.getAttribute("aria-label")).toBe(esperado);
          expect(parte(bolita, "etiqueta").textContent).toBe(esperado);
        }
        for (const truth of TRUTH_Y_DESCONOCIDO) {
          for (const context of CONTEXT_Y_DESCONOCIDO) {
            const { bolita } = montar({ truth: valorDe(truth), context: valorDe(context) });
            const esperado = textoVeredicto(idioma, truth, context);
            expect(bolita.getAttribute("aria-label")).toBe(esperado);
            expect(parte(bolita, "etiqueta").textContent).toBe(esperado);
          }
        }
      });
    }

    test("la etiqueta dice los dos ejes por separado, con las palabras que aprobo Mateo", () => {
      const { bolita } = montar({ truth: "supported", context: "divergence_detected" });
      expect(bolita.getAttribute("aria-label")).toBe(
        "VeritAI. Contexto: divergencia detectada. Dato: respaldado por la fuente.",
      );
      fijarLocale("en");
      fijarEstadoBolita(bolita, { truth: "supported", context: "divergence_detected" });
      expect(bolita.getAttribute("aria-label")).toBe(
        "VeritAI. Context: divergence detected. Figure: supported by the source.",
      );
    });

    test("no depende del color: los 33 estados posibles tienen 33 etiquetas distintas", () => {
      for (const idioma of IDIOMAS) {
        const etiquetas = [
          ...VALORES_FASE_CONSULTA.map((fase) => textoFase(idioma, fase)),
          ...TRUTH_Y_DESCONOCIDO.flatMap((truth) =>
            CONTEXT_Y_DESCONOCIDO.map((context) => textoVeredicto(idioma, truth, context)),
          ),
        ];
        expect(etiquetas).toHaveLength(33);
        expect(new Set(etiquetas).size, `etiquetas repetidas en ${idioma}`).toBe(33);
        for (const etiqueta of etiquetas) expect(etiqueta).not.toMatch(/[{}]|undefined/);
      }
    });

    test("mientras analiza, y solo entonces, el boton se declara ocupado", () => {
      const { bolita } = montar({ fase: FaseConsulta.Analizando });
      expect(bolita.getAttribute("aria-busy")).toBe("true");
      fijarEstadoBolita(bolita, { truth: "mixed", context: "undetermined" });
      expect(bolita.hasAttribute("aria-busy")).toBe(false);
      fijarEstadoBolita(bolita, { fase: FaseConsulta.Error });
      expect(bolita.hasAttribute("aria-busy")).toBe(false);
    });

    test("la etiqueta visible esta oculta en reposo y la hoja la muestra al enfocar y al pasar por encima", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      expect(getComputedStyle(parte(bolita, "etiqueta")).display).toBe("none");

      const reglas = reglasAdoptadas(bolita);
      const alEnfocar = reglas.find((r) => r.selector === ".veritai-bolita:focus-visible .veritai-bolita__etiqueta");
      const alPasar = reglas.find((r) => r.selector === ".veritai-bolita:hover .veritai-bolita__etiqueta");
      expect(alEnfocar?.estilo.getPropertyValue("display")).toBe("block");
      expect(alEnfocar?.media).toBeNull();
      expect(alPasar?.estilo.getPropertyValue("display")).toBe("block");
      expect(alPasar?.media).toBe("(hover: hover)");
    });
  });

  describe("cambia de estado sin cambiar de nodo", () => {
    test("fijarEstadoBolita actualiza clase, etiqueta y ganchos sobre el mismo boton, sin restos del estado anterior", () => {
      const { bolita, alPulsar } = montar({ fase: FaseConsulta.EnEspera });
      const etiqueta = parte(bolita, "etiqueta");

      fijarEstadoBolita(bolita, { fase: FaseConsulta.Analizando });
      fijarEstadoBolita(bolita, { truth: "contradicted", context: "no_divergence_detected" });

      expect(bolita.className).toBe(
        "veritai-bolita veritai-bolita--veredicto veritai-bolita--context-no_divergence_detected veritai-bolita--truth-contradicted",
      );
      expect(bolita.dataset["veritaiFase"]).toBeUndefined();
      expect(parte(bolita, "etiqueta")).toBe(etiqueta);
      expect(etiqueta.textContent).toBe(textoVeredicto("es", "contradicted", "no_divergence_detected"));
      expect(bolita.children).toHaveLength(2);

      fijarEstadoBolita(bolita, { fase: FaseConsulta.EnEspera });
      expect(bolita.className).toBe("veritai-bolita veritai-bolita--fase-en_espera");
      expect(bolita.dataset["veritaiTruth"]).toBeUndefined();
      expect(bolita.dataset["veritaiContext"]).toBeUndefined();

      bolita.click();
      expect(alPulsar).toHaveBeenCalledTimes(1); // el manejador no se duplica al cambiar de estado
    });

    test("no acepta un boton que no creo crearBolita", () => {
      expect(() => fijarEstadoBolita(document.createElement("button"), { fase: FaseConsulta.EnEspera })).toThrow(
        /crearBolita/,
      );
    });
  });

  describe("el teclado funciona", () => {
    test("es un boton nativo, esta en el orden de tabulacion y no esta deshabilitado", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      expect(bolita).toBeInstanceOf(HTMLButtonElement);
      expect(bolita.tabIndex).toBe(0);
      expect(bolita.hasAttribute("tabindex")).toBe(false);
      expect(bolita.disabled).toBe(false);
      expect(bolita.hasAttribute("role")).toBe(false); // el rol es el del <button>, no uno puesto a mano
    });

    test("recibe el foco dentro de la raiz aislada, y desde la pagina el foco se ve en el anfitrion", () => {
      const { bolita, anfitrion } = montar({ fase: FaseConsulta.EnEspera });
      bolita.focus();
      expect((bolita.getRootNode() as ShadowRoot).activeElement).toBe(bolita);
      expect(document.activeElement).toBe(anfitrion);
    });

    test("la activacion llama a la accion una vez: Enter y Espacio llegan como click en un <button> nativo", () => {
      // El navegador convierte Enter y Espacio en `click` sobre un <button>; happy-dom no imita ese
      // comportamiento, asi que aqui se comprueba la otra mitad: que el `click` llega a la accion.
      const { bolita, alPulsar } = montar({ fase: FaseConsulta.EnEspera });
      bolita.focus();
      bolita.click();
      expect(alPulsar).toHaveBeenCalledTimes(1);
      expect(fuenteBolita).not.toMatch(/keydown|keyup|keypress/); // nada propio que pueda duplicar la pulsacion
    });

    test("el foco se ve: anillo solido con el color y el ancho de los tokens, y nada lo apaga", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      const reglas = reglasAdoptadas(bolita);
      const foco = reglas.find((r) => r.selector === ".veritai-bolita:focus-visible");

      expect(foco, "no hay regla :focus-visible para la bolita").toBeDefined();
      expect(foco!.media).toBeNull();
      expect(foco!.estilo.getPropertyValue("outline-style")).toBe("solid");
      expect(foco!.estilo.getPropertyValue("outline-width")).toBe("var(--veritai-foco-ancho)");
      expect(foco!.estilo.getPropertyValue("outline-color")).toBe("var(--veritai-color-foco)");
      expect(foco!.estilo.getPropertyValue("outline-offset")).toBe("var(--veritai-foco-separacion)");

      for (const regla of reglas) {
        expect(regla.estilo.getPropertyValue("outline"), regla.selector).not.toMatch(/none|^0/);
        expect(regla.estilo.getPropertyValue("outline-style"), regla.selector).not.toBe("none");
      }
    });
  });

  describe("respeta la preferencia de movimiento", () => {
    test("sin preferencia: transicion al crecer y encoger, y pulso solo mientras analiza", () => {
      const analizando = montar({ fase: FaseConsulta.Analizando }, { movimiento: "normal" }).bolita;
      expect(getComputedStyle(parte(analizando, "disco")).transitionProperty).toBe("transform, box-shadow");
      expect(getComputedStyle(parte(analizando, "pulso")).animationName).toBe("veritai-bolita-pulso");
      expect(getComputedStyle(parte(analizando, "pulso")).animationIterationCount).toBe("infinite");

      for (const estado of [{ fase: FaseConsulta.EnEspera }, { fase: FaseConsulta.Error }, { truth: "supported", context: "undetermined" }]) {
        const quieta = montar(estado, { movimiento: "normal" }).bolita;
        expect(getComputedStyle(parte(quieta, "pulso")).animationName, JSON.stringify(estado)).not.toBe(
          "veritai-bolita-pulso",
        );
      }
    });

    test("con movimiento reducido no hay transicion ni pulso, en ningun estado", () => {
      const estados: EstadoBolita[] = [
        ...VALORES_FASE_CONSULTA.map((fase) => ({ fase })),
        { truth: "supported", context: "divergence_detected" },
      ];
      for (const estado of estados) {
        const { bolita } = montar(estado, { movimiento: "reducido" });
        expect(getComputedStyle(parte(bolita, "disco")).transitionProperty, JSON.stringify(estado)).toBe("none");
        expect(getComputedStyle(parte(bolita, "pulso")).animationName, JSON.stringify(estado)).not.toBe(
          "veritai-bolita-pulso",
        );
        limpiarEntorno();
      }
      const analizando = montar({ fase: FaseConsulta.Analizando }, { movimiento: "reducido" }).bolita;
      expect(getComputedStyle(parte(analizando, "pulso")).animationName).toBe("none");
    });

    test("con movimiento reducido 'analizando' sigue distinguiendose: el halo se queda fijo y visible", () => {
      const conMovimiento = montar({ fase: FaseConsulta.Analizando }, { movimiento: "normal" }).bolita;
      expect(getComputedStyle(parte(conMovimiento, "pulso")).opacity).toBe("0"); // lo mueve la animacion
      limpiarEntorno();

      const sinMovimiento = montar({ fase: FaseConsulta.Analizando }, { movimiento: "reducido" }).bolita;
      const halo = getComputedStyle(parte(sinMovimiento, "pulso"));
      expect(halo.opacity).toBe(token("--veritai-bolita-pulso-opacidad", { tema: "claro" }));
      expect(halo.transform).toBe(`scale(${token("--veritai-bolita-pulso-escala-quieta", { tema: "claro" })})`);
    });

    test("con movimiento reducido ni crece al pasar por encima ni encoge al pulsar", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      const reglas = reglasAdoptadas(bolita);

      // Sin la preferencia, si hay movimiento que apagar:
      const crece = reglas.find(
        (r) => r.selector === ".veritai-bolita:hover .veritai-bolita__disco" && r.media === "(hover: hover)",
      );
      const encoge = reglas.find((r) => r.selector === ".veritai-bolita:active .veritai-bolita__disco" && r.media === null);
      expect(crece?.estilo.getPropertyValue("transform")).toBe("scale(var(--veritai-bolita-escala-encima))");
      expect(encoge?.estilo.getPropertyValue("transform")).toBe("scale(var(--veritai-bolita-escala-pulsada))");

      // Con ella, la regla que lo apaga existe y va despues de las dos (misma especificidad: gana la ultima).
      const reducido = reglas.filter((r) => r.media === "(prefers-reduced-motion: reduce)");
      const apaga = reducido.find(
        (r) => r.selector === ".veritai-bolita:hover .veritai-bolita__disco, .veritai-bolita:active .veritai-bolita__disco",
      );
      expect(apaga?.estilo.getPropertyValue("transform")).toBe("none");
      expect(reglas.indexOf(apaga!)).toBeGreaterThan(reglas.indexOf(crece!));
      expect(reglas.indexOf(apaga!)).toBeGreaterThan(reglas.indexOf(encoge!));
    });
  });

  describe("lo que se mueve es el disco, no el texto", () => {
    test("la etiqueta cuelga del boton, fuera del disco: no crece ni encoge con el", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      expect(parte(bolita, "etiqueta").parentElement).toBe(bolita);
      expect(parte(bolita, "disco").contains(parte(bolita, "etiqueta"))).toBe(false);
    });

    test("ninguna regla transforma el boton ni la etiqueta: solo el disco y el pulso", () => {
      const { bolita } = montar({ fase: FaseConsulta.EnEspera });
      const conTransformacion = reglasAdoptadas(bolita).filter((r) => r.estilo.getPropertyValue("transform") !== "");
      expect(conTransformacion.length).toBeGreaterThan(3);
      for (const regla of conTransformacion) {
        for (const selector of regla.selector.split(", ")) {
          expect(selector, `transform en "${selector}"`).toMatch(/\.veritai-bolita__(disco|pulso)$/);
        }
      }
    });
  });

  describe("tamano", () => {
    test("54 px con raton y 44 px con dedo, los dos como tokens", () => {
      expect(token("--veritai-bolita-tamano-escritorio", { tema: "claro" })).toBe("54px");
      expect(token("--veritai-bolita-tamano-movil", { tema: "claro" })).toBe("44px");

      const conRaton = getComputedStyle(montar({ fase: FaseConsulta.EnEspera }, { puntero: "fino" }).bolita);
      expect([conRaton.width, conRaton.height]).toEqual(["54px", "54px"]);
      limpiarEntorno();

      const conDedo = getComputedStyle(montar({ fase: FaseConsulta.EnEspera }, { puntero: "grueso" }).bolita);
      expect([conDedo.width, conDedo.height]).toEqual(["44px", "44px"]);
    });
  });

  describe("no lleva valores escritos dentro", () => {
    const sinComentarios = cssBolita.replace(/\/\*[\s\S]*?\*\//g, "");

    test("la hoja de la bolita no tiene ningun color literal: todos salen de tokens", () => {
      expect(sinComentarios.match(/#[0-9a-f]{3,8}\b|\b(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch)\(/gi)).toBeNull();
      const colores = sinComentarios.match(/(?:^|[\s;{])(?:color|border-color|background-color|outline-color)\s*:\s*[^;]+;/g) ?? [];
      expect(colores.length).toBeGreaterThan(20);
      for (const declaracion of colores) {
        expect(declaracion, declaracion.trim()).toMatch(/:\s*(var\(--veritai-[\w-]+\)|currentColor|transparent);$/);
      }
    });

    test("ni tamanos, radios o duraciones literales: solo 0, 1 y 100 %", () => {
      const sinUrls = sinComentarios.replace(/url\([^)]*\)/g, "url()");
      const numeros = sinUrls.match(/(?<![\w-])-?\d*\.?\d+(?:px|rem|em|ms|s|%|vh|vw|deg)?(?![\w-])/g) ?? [];
      expect([...new Set(numeros)].sort()).toEqual(["0", "1", "100%"]);
      expect(sinComentarios).not.toMatch(/!important/);
    });

    test("el modulo no escribe estilos en linea ni colores: solo clases", () => {
      expect(fuenteBolita).not.toMatch(/\.style\b|setProperty|cssText/);
      expect(fuenteBolita).not.toMatch(/#[0-9a-f]{6}\b|rgb\(|hsl\(/i);
    });
  });

  describe("lo que llega de la API se trata como dato", () => {
    test("un valor hostil en truth o context se pinta como desconocido y no aparece en el DOM", () => {
      const hostil = '"><img src=x onerror=alert(1)>';
      const { bolita, punto } = montar({ truth: hostil, context: `divergence_detected ${hostil}` });

      expect(bolita.dataset["veritaiTruth"]).toBe("desconocido");
      expect(bolita.dataset["veritaiContext"]).toBe("desconocido");
      expect(bolita.className).toBe(
        "veritai-bolita veritai-bolita--veredicto veritai-bolita--context-desconocido veritai-bolita--truth-desconocido",
      );
      expect(bolita.getAttribute("aria-label")).toBe(textoVeredicto("es", "desconocido", "desconocido"));
      expect(punto.querySelector("img")).toBeNull();
      expect(punto.innerHTML).not.toContain("onerror");
      expect(punto.innerHTML).not.toContain("src=x");
    });
  });
});
