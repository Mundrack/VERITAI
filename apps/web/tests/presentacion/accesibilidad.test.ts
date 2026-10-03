/**
 * Accesibilidad de la bolita (docs/ARQUITECTURA-VISUAL.md §5.2, §2.2).
 *
 * Mateo, 2026-10-03: "con una etiqueta que diga el estado en palabras, no solo
 * en color. Que funcione para quien no distingue el rojo del verde."
 *
 * Las palabras se comprueban en bolita.test.ts (33 estados, 33 etiquetas). Aqui
 * se comprueba la paleta, leida de tokens.css, en tema claro y en oscuro:
 *
 *   1. cada color de estado se ve contra el disco de la bolita;
 *   2. ningun estado es verde, y dentro de un mismo eje todo par de estados
 *      se separa por claridad o por azul-amarillo, que es lo que conserva
 *      quien no distingue el rojo del verde (aproximacion: ver _color.ts);
 *   3. el anillo de foco se ve sobre cualquier fondo;
 *   4. el texto de la etiqueta se lee;
 *   5. la bolita es un objetivo tactil suficiente.
 *
 * Hoy cubre los tokens que usa la bolita. La comprobacion general de todos los
 * pares texto/fondo de tokens.css (§5.2) sigue pendiente.
 */

import { describe, expect, test } from "vitest";

import { VALORES_CONTEXT, VALORES_TRUTH } from "../../src/contrato/enums";
import { VALORES_FASE_CONSULTA } from "../../src/contrato/fase-consulta";
import { DESCONOCIDO } from "../../src/presentacion/estados";
import { TEMAS } from "../_entorno";
import { contraste, lab, separacionSinRojoVerde, tonoYCroma } from "./_color";
import { nombresDeTokens, token } from "./_tokens";

/** WCAG 2.1, 1.4.11 Non-text Contrast (AA): graficos y componentes de interfaz. */
const CONTRASTE_MINIMO_GRAFICO = 3;
/** WCAG 2.1, 1.4.3 Contrast (Minimum) (AA): texto. */
const CONTRASTE_MINIMO_TEXTO = 4.5;
/** WCAG 2.1, 2.5.5 Target Size (AAA): lado minimo de un objetivo tactil, en px CSS. */
const OBJETIVO_TACTIL_MINIMO_PX = 44;
/**
 * Los cuatro numeros que siguen NO son de ninguna norma: son los margenes que
 * fija el proyecto para una comprobacion que es aproximada (ver _color.ts).
 * Dos estados del mismo eje tienen que separarse con claridad en al menos una
 * de las dos cosas que conserva quien no distingue el rojo del verde.
 */
const DIFERENCIA_MINIMA_DE_CLARIDAD = 15; // en L*, que va de 0 a 100
const DIFERENCIA_MINIMA_AZUL_AMARILLO = 30; // en b*
/** Un color cuenta como verde si tiene croma (no es un gris) y su tono cae en esta franja. */
const CROMA_MINIMO_PARA_TENER_TONO = 15;
const FRANJA_DE_VERDES: readonly [number, number] = [110, 200];

const BLANCO = "#ffffff";
const NEGRO = "#000000";

function esVerde(hex: string): boolean {
  const { tono, croma } = tonoYCroma(hex);
  return croma >= CROMA_MINIMO_PARA_TENER_TONO && tono >= FRANJA_DE_VERDES[0] && tono <= FRANJA_DE_VERDES[1];
}

/** Los estados de cada eje, con su token de color. */
const EJES: Record<string, readonly string[]> = {
  fase: VALORES_FASE_CONSULTA,
  truth: [...VALORES_TRUTH, DESCONOCIDO],
  context: [...VALORES_CONTEXT, DESCONOCIDO],
};

function tokenDeEstado(eje: string, estado: string): string {
  return `--veritai-color-${eje}-${estado}`;
}

describe("accesibilidad de la bolita", () => {
  test("las formulas dan los valores de referencia", () => {
    expect(contraste(NEGRO, BLANCO)).toBeCloseTo(21, 5);
    expect(contraste(BLANCO, BLANCO)).toBe(1);
    // Los tres contrastes que ya estaban medidos y escritos en ARQUITECTURA-VISUAL.md §2.1:
    expect(contraste("#98242c", BLANCO)).toBeCloseTo(8.0, 1);
    expect(contraste("#d9444c", BLANCO)).toBeCloseTo(4.3, 1);
    expect(contraste("#d9444c", "#202124")).toBeCloseTo(3.7, 1);
    // CIELAB: blanco, negro y los grises no tienen ni rojo-verde ni azul-amarillo.
    expect(lab(BLANCO).L).toBeCloseTo(100, 1);
    expect(lab(NEGRO).L).toBeCloseTo(0, 5);
    for (const gris of [BLANCO, "#808080", NEGRO]) {
      expect(Math.abs(lab(gris).a)).toBeLessThan(0.01);
      expect(Math.abs(lab(gris).b)).toBeLessThan(0.01);
    }
  });

  test("los dos detectores reconocen el caso que existen para prohibir: un verde junto a un rojo", () => {
    // El verde de "servicio activo" y el rojo de "servicio caido" del panel suelto son justo ese par.
    for (const tema of TEMAS) {
      const [verde, rojo] = [token("--veritai-color-ok", { tema }), token("--veritai-color-mal", { tema })];
      expect(esVerde(verde), `${verde} deberia contar como verde`).toBe(true);
      expect(esVerde(rojo), `${rojo} no deberia contar como verde`).toBe(false);
      const { claridad, azulAmarillo } = separacionSinRojoVerde(verde, rojo);
      expect(claridad, `claridad entre ${verde} y ${rojo}`).toBeLessThan(DIFERENCIA_MINIMA_DE_CLARIDAD);
      expect(azulAmarillo, `azul-amarillo entre ${verde} y ${rojo}`).toBeLessThan(DIFERENCIA_MINIMA_AZUL_AMARILLO);
    }
    // Y no ven verde donde no lo hay: el rojo de la marca, un azul, un gris, blanco y negro.
    for (const noVerde of [token("--veritai-color-acento", { tema: "claro" }), "#1d4ed8", "#808080", BLANCO, NEGRO]) {
      expect(esVerde(noVerde), noVerde).toBe(false);
    }
  });

  test("todos los estados tienen su token de color, con un valor para el tema claro y otro para el oscuro", () => {
    const declarados = nombresDeTokens();
    for (const [eje, estados] of Object.entries(EJES)) {
      for (const estado of estados) {
        const nombre = tokenDeEstado(eje, estado);
        expect(declarados, `falta ${nombre} en tokens.css`).toContain(nombre);
        const [claro, oscuro] = TEMAS.map((tema) => token(nombre, { tema }));
        expect(claro, nombre).toMatch(/^#[0-9a-f]{6}$/);
        expect(oscuro, nombre).toMatch(/^#[0-9a-f]{6}$/);
        expect(oscuro, `${nombre} vale lo mismo en los dos temas, y el disco no es el mismo`).not.toBe(claro);
      }
    }
  });

  for (const tema of TEMAS) {
    describe(`tema ${tema}`, () => {
      const disco = token("--veritai-bolita-fondo", { tema });

      test("cada color de estado se ve contra el disco de la bolita (3:1)", () => {
        for (const [eje, estados] of Object.entries(EJES)) {
          for (const estado of estados) {
            const color = token(tokenDeEstado(eje, estado), { tema });
            expect(
              contraste(color, disco),
              `${eje}.${estado} ${color} sobre ${disco} = ${contraste(color, disco).toFixed(2)}:1`,
            ).toBeGreaterThanOrEqual(CONTRASTE_MINIMO_GRAFICO);
          }
        }
      });

      test("ningun color de estado es verde: no hay par rojo-verde que confundir", () => {
        for (const [eje, estados] of Object.entries(EJES)) {
          for (const estado of estados) {
            const color = token(tokenDeEstado(eje, estado), { tema });
            const { tono, croma } = tonoYCroma(color);
            expect(
              esVerde(color),
              `${eje}.${estado} ${color} es verde (tono ${tono.toFixed(0)}, croma ${croma.toFixed(0)})`,
            ).toBe(false);
          }
        }
      });

      test("dentro de cada eje, todo par de estados se separa por claridad o por azul-amarillo, sin contar el rojo-verde", () => {
        for (const [eje, estados] of Object.entries(EJES)) {
          for (let i = 0; i < estados.length; i++) {
            for (let j = i + 1; j < estados.length; j++) {
              const [a, b] = [estados[i]!, estados[j]!];
              const [colorA, colorB] = [token(tokenDeEstado(eje, a), { tema }), token(tokenDeEstado(eje, b), { tema })];
              const { claridad, azulAmarillo } = separacionSinRojoVerde(colorA, colorB);
              expect(
                claridad >= DIFERENCIA_MINIMA_DE_CLARIDAD || azulAmarillo >= DIFERENCIA_MINIMA_AZUL_AMARILLO,
                `${eje}: ${a} (${colorA}) y ${b} (${colorB}) solo se separan ${claridad.toFixed(1)} en claridad ` +
                  `y ${azulAmarillo.toFixed(1)} en azul-amarillo`,
              ).toBe(true);
            }
          }
        }
      });

      test("el texto de la etiqueta se lee sobre su fondo (4,5:1)", () => {
        const texto = token("--veritai-color-texto", { tema });
        const fondo = token("--veritai-color-fondo", { tema });
        expect(contraste(texto, fondo)).toBeGreaterThanOrEqual(CONTRASTE_MINIMO_TEXTO);
      });

      test("el anillo de foco se ve contra el disco", () => {
        expect(contraste(token("--veritai-color-foco", { tema }), disco)).toBeGreaterThanOrEqual(CONTRASTE_MINIMO_GRAFICO);
      });
    });
  }

  test("el anillo de foco se dibuja sobre la pagina de un tercero: se ve sobre blanco y sobre negro", () => {
    const foco = token("--veritai-color-foco", { tema: "claro" });
    expect(token("--veritai-color-foco", { tema: "oscuro" })).toBe(foco); // un solo valor: el fondo no es nuestro
    expect(contraste(foco, BLANCO)).toBeGreaterThanOrEqual(CONTRASTE_MINIMO_GRAFICO);
    expect(contraste(foco, NEGRO)).toBeGreaterThanOrEqual(CONTRASTE_MINIMO_GRAFICO);
  });

  test("la bolita es un objetivo tactil suficiente en sus dos tamanos", () => {
    for (const nombre of ["--veritai-bolita-tamano-escritorio", "--veritai-bolita-tamano-movil"]) {
      const valor = token(nombre, { tema: "claro" });
      expect(valor, nombre).toMatch(/^\d+px$/);
      expect(parseInt(valor, 10), nombre).toBeGreaterThanOrEqual(OBJETIVO_TACTIL_MINIMO_PX);
    }
    expect(token("--veritai-bolita-tamano", { tema: "claro", puntero: "fino" })).toBe("54px");
    expect(token("--veritai-bolita-tamano", { tema: "claro", puntero: "grueso" })).toBe("44px");
  });
});
