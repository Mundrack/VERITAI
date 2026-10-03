/**
 * estado-servicio (docs/ARQUITECTURA-VISUAL.md §5.2, prueba de componente).
 *
 * Fija lo que main.ts pintaba el 2026-10-03: el mismo orden de elementos, los
 * mismos textos (de los catalogos, en los dos idiomas), las mismas marcas y el
 * mismo pie. Si esta prueba pasa, la reestructuracion no cambio lo que se ve.
 * Tambien comprueba que lo que llega de la API se pinta como texto y nunca
 * como HTML.
 */

import { beforeEach, describe, expect, test, vi } from "vitest";

import type { RespuestaSalud } from "../../src/contrato/salud";
import en from "../../src/i18n/en.json";
import es from "../../src/i18n/es.json";
import { fijarLocale } from "../../src/i18n";
import {
  crearEstadoServicio,
  type AccionesEstadoServicio,
} from "../../src/presentacion/componentes/estado-servicio/estado-servicio";

const SALUD_VIVA: RespuestaSalud = {
  servicio: "veritai-api",
  version: "0.1.0",
  entorno: "local",
  base_de_datos: "conectada",
};

const CONSULTADO = new Date(2026, 9, 3, 14, 3, 27);

function acciones(): AccionesEstadoServicio {
  return { alRecomprobar: vi.fn(), alCambiarIdioma: vi.fn() };
}

function textos(raiz: HTMLElement, selector: string): string[] {
  return Array.from(raiz.querySelectorAll(selector)).map((n) => n.textContent ?? "");
}

describe("estado-servicio", () => {
  beforeEach(() => fijarLocale("es"));

  test("pinta, en este orden, encabezado (simbolo y titulo), subtitulo, aviso, cabecera de seccion, tabla, acciones y pie", () => {
    const raiz = crearEstadoServicio({ salud: SALUD_VIVA, consultadoEn: CONSULTADO }, acciones());
    const orden = Array.from(raiz.children).map((hijo) => `${hijo.tagName.toLowerCase()}.${hijo.className}`);
    expect(orden).toEqual([
      "div.veritai-estado-servicio__encabezado",
      "p.veritai-estado-servicio__subtitulo",
      "div.veritai-estado-servicio__aviso",
      "h2.",
      "table.veritai-estado-servicio__tabla",
      "div.veritai-estado-servicio__acciones",
      "p.veritai-estado-servicio__pie",
    ]);
    const encabezado = Array.from(raiz.children[0]!.children).map(
      (hijo) => `${hijo.tagName.toLowerCase()}.${hijo.className}`,
    );
    expect(encabezado).toEqual(["img.veritai-estado-servicio__marca", "h1.veritai-estado-servicio__titulo"]);
  });

  test("el simbolo de la cabecera es el de orbita, entra como <img> con alt del catalogo, en los dos idiomas", () => {
    for (const [locale, catalogo] of [["es", es], ["en", en]] as const) {
      fijarLocale(locale);
      const raiz = crearEstadoServicio({ salud: SALUD_VIVA, consultadoEn: CONSULTADO }, acciones());
      const imagenes = raiz.querySelectorAll("img");
      expect(imagenes).toHaveLength(1);
      const simbolo = imagenes[0]!;
      expect(simbolo.getAttribute("alt")).toBe(catalogo["marca.alt"]);
      expect(simbolo.getAttribute("src")).toMatch(/veritai-simbolo\.svg$/);
      expect(simbolo.getAttribute("src")).not.toMatch(/-min\.svg$/);
      expect(raiz.querySelector("svg")).toBeNull(); // no se inyecta SVG en linea ni por innerHTML
    }
  });

  test("con la API y la base de datos vivas muestra OK y conectada en verde, y 2 de 2 servicios", () => {
    const raiz = crearEstadoServicio({ salud: SALUD_VIVA, consultadoEn: CONSULTADO }, acciones());

    expect(textos(raiz, "th")).toEqual([
      es["estado.api"],
      es["estado.base_de_datos"],
      es["estado.entorno"],
      es["estado.version"],
    ]);
    expect(textos(raiz, "td")).toEqual(["OK", es["estado.conectada"], "local", "0.1.0"]);
    expect(textos(raiz, ".veritai-estado-servicio__marca--ok")).toEqual(["OK", es["estado.conectada"]]);
    expect(raiz.querySelectorAll(".veritai-estado-servicio__marca--mal")).toHaveLength(0);

    const pie = raiz.querySelector(".veritai-estado-servicio__pie")?.textContent ?? "";
    expect(pie).toBe(
      `2 de 2 servicios activos · Consultado a las ${CONSULTADO.toLocaleTimeString("es")}`,
    );
  });

  test("sin respuesta de la API muestra sin respuesta y no disponible en rojo, guiones, y 0 de 2", () => {
    const raiz = crearEstadoServicio({ salud: null, consultadoEn: CONSULTADO }, acciones());

    expect(textos(raiz, "td")).toEqual([es["estado.sin_respuesta"], es["estado.no_disponible"], "-", "-"]);
    expect(textos(raiz, ".veritai-estado-servicio__marca--mal")).toEqual([
      es["estado.sin_respuesta"],
      es["estado.no_disponible"],
    ]);
    expect(raiz.querySelector(".veritai-estado-servicio__pie")?.textContent).toContain(
      "0 de 2 servicios activos",
    );
  });

  test("con la API viva pero la base de datos caida cuenta 1 de 2", () => {
    const raiz = crearEstadoServicio(
      { salud: { ...SALUD_VIVA, base_de_datos: "no disponible" }, consultadoEn: CONSULTADO },
      acciones(),
    );
    expect(textos(raiz, ".veritai-estado-servicio__marca--ok")).toEqual(["OK"]);
    expect(textos(raiz, ".veritai-estado-servicio__marca--mal")).toEqual([es["estado.no_disponible"]]);
    expect(raiz.querySelector(".veritai-estado-servicio__pie")?.textContent).toContain(
      "1 de 2 servicios activos",
    );
  });

  test("en ingles usa el catalogo en y deja seleccionado EN", () => {
    fijarLocale("en");
    const raiz = crearEstadoServicio({ salud: SALUD_VIVA, consultadoEn: CONSULTADO }, acciones());

    expect(raiz.querySelector("h1")?.textContent).toBe(en["app.titulo"]);
    expect(raiz.querySelector("h2")?.textContent).toBe(en["estado.titulo"]);
    expect(textos(raiz, "th")).toEqual([
      en["estado.api"],
      en["estado.base_de_datos"],
      en["estado.entorno"],
      en["estado.version"],
    ]);
    expect(raiz.querySelector("button")?.textContent).toBe(en["acciones.recomprobar"]);
    expect(raiz.querySelector("select")?.value).toBe("en");
    expect(textos(raiz, "option")).toEqual(["ES", "EN"]);
  });

  test("el boton y el selector llaman a las acciones recibidas, sin ids globales", () => {
    const callbacks = acciones();
    const raiz = crearEstadoServicio({ salud: SALUD_VIVA, consultadoEn: CONSULTADO }, callbacks);

    raiz.querySelector<HTMLButtonElement>("[data-veritai='recomprobar']")?.click();
    expect(callbacks.alRecomprobar).toHaveBeenCalledTimes(1);

    const selector = raiz.querySelector<HTMLSelectElement>("[data-veritai='idioma']");
    expect(selector).not.toBeNull();
    selector!.value = "en";
    selector!.dispatchEvent(new Event("change"));
    expect(callbacks.alCambiarIdioma).toHaveBeenCalledWith("en");

    expect(raiz.querySelector("#recomprobar")).toBeNull();
    expect(raiz.querySelector("#idioma")).toBeNull();
    expect(raiz.querySelector("label")?.getAttribute("for")).toBe(selector!.id);
  });

  test("lo que viene de la API se pinta como texto, nunca como HTML", () => {
    const hostil = { ...SALUD_VIVA, entorno: "<img src=x onerror=alert(1)>", version: "<b>x</b>" };
    const raiz = crearEstadoServicio({ salud: hostil, consultadoEn: CONSULTADO }, acciones());

    // La unica imagen es el simbolo de la marca; la hostil no existe como nodo.
    const imagenes = Array.from(raiz.querySelectorAll("img")).map((i) => i.getAttribute("src"));
    expect(imagenes).toHaveLength(1);
    expect(imagenes[0]).toMatch(/veritai-simbolo\.svg$/);
    expect(raiz.querySelectorAll("img[src='x'], b")).toHaveLength(0);
    expect(textos(raiz, "td").slice(2)).toEqual(["<img src=x onerror=alert(1)>", "<b>x</b>"]);
  });
});
