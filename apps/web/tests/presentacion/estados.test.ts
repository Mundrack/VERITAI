/**
 * estados.ts: el mapa cerrado de enums a estados visuales
 * (docs/ARQUITECTURA-VISUAL.md §1.3 punto 2, §5.2 prueba unitaria pura).
 *
 * La interfaz no inventa estados: cada valor del enum da su propio estado, con
 * el valor tal cual en el modificador y en la clave de texto; cualquier otra
 * cosa da `desconocido`. Y todo estado tiene su texto en los dos idiomas.
 */

import { describe, expect, test } from "vitest";

import { Context, Truth, VALORES_CONTEXT, VALORES_TRUTH } from "../../src/contrato/enums";
import { FaseConsulta, VALORES_FASE_CONSULTA } from "../../src/contrato/fase-consulta";
import en from "../../src/i18n/en.json";
import es from "../../src/i18n/es.json";
import {
  DESCONOCIDO,
  estadoContext,
  estadoTruth,
  visualContext,
  visualFase,
  visualTruth,
} from "../../src/presentacion/estados";

const CATALOGOS: Record<string, Record<string, string>> = { es, en };

/** docs/GLOSARIO.md §Terminos que NO se usan. */
const TERMINOS_VETADOS = [/\bfals[oa]s?\b/i, /\bverdader[oa]s?\b/i, /\bfake\b/i, /enga[nñ]os/i, /\btrue\b/i, /\bfalse\b/i, /misleading/i, /\bcree\b/i, /\bbelieves?\b/i];

describe("estados visuales", () => {
  test("cada valor de truth es su propio estado, con el valor del enum en el modificador y en la clave", () => {
    expect(VALORES_TRUTH).toEqual([
      "supported",
      "contradicted",
      "mixed",
      "insufficient_evidence",
      "not_applicable",
    ]);
    for (const valor of VALORES_TRUTH) {
      expect(estadoTruth(valor)).toBe(valor);
      expect(visualTruth(valor)).toEqual({
        estado: valor,
        modificador: `truth-${valor}`,
        clave: `truth.${valor}`,
      });
    }
  });

  test("cada valor de context es su propio estado, con el valor del enum en el modificador y en la clave", () => {
    expect(VALORES_CONTEXT).toEqual([
      "divergence_detected",
      "no_divergence_detected",
      "undetermined",
      "not_applicable",
    ]);
    for (const valor of VALORES_CONTEXT) {
      expect(estadoContext(valor)).toBe(valor);
      expect(visualContext(valor)).toEqual({
        estado: valor,
        modificador: `context-${valor}`,
        clave: `context.${valor}`,
      });
    }
  });

  test("las fases de la consulta son tres y cada una es su propio estado", () => {
    expect(VALORES_FASE_CONSULTA).toEqual(["en_espera", "analizando", "error"]);
    for (const fase of VALORES_FASE_CONSULTA) {
      expect(visualFase(fase)).toEqual({ estado: fase, modificador: `fase-${fase}`, clave: `fase.${fase}` });
    }
    expect(FaseConsulta.Analizando).toBe("analizando");
  });

  test("un valor que no esta en el enum da desconocido: no se adivina a cual se parece", () => {
    const ajenos = ["", "SUPPORTED", "supported ", "apoyado", "verdadero", "<b>supported</b>", "constructor", "toString"];
    for (const valor of ajenos) {
      expect(estadoTruth(valor), `truth "${valor}"`).toBe(DESCONOCIDO);
      expect(estadoContext(valor), `context "${valor}"`).toBe(DESCONOCIDO);
    }
    expect(visualTruth("no_existe")).toEqual({
      estado: "desconocido",
      modificador: "truth-desconocido",
      clave: "truth.desconocido",
    });
    expect(visualContext("no_existe")).toEqual({
      estado: "desconocido",
      modificador: "context-desconocido",
      clave: "context.desconocido",
    });
  });

  test("un valor de un eje no vale en el otro: los dos ejes son independientes", () => {
    expect(estadoTruth(Context.DivergenceDetected)).toBe(DESCONOCIDO);
    expect(estadoTruth(Context.Undetermined)).toBe(DESCONOCIDO);
    expect(estadoContext(Truth.Supported)).toBe(DESCONOCIDO);
    expect(estadoContext(Truth.Contradicted)).toBe(DESCONOCIDO);
    // not_applicable existe en los dos enums, y en cada uno es un valor propio.
    expect(estadoTruth(Truth.NotApplicable)).toBe("not_applicable");
    expect(estadoContext(Context.NotApplicable)).toBe("not_applicable");
  });

  test("todo estado, incluido desconocido, tiene su texto en espanol y en ingles", () => {
    const claves = [
      ...[...VALORES_TRUTH, DESCONOCIDO].map((v) => visualTruth(v).clave),
      ...[...VALORES_CONTEXT, DESCONOCIDO].map((v) => visualContext(v).clave),
      ...VALORES_FASE_CONSULTA.map((v) => visualFase(v).clave),
    ];
    expect(claves).toHaveLength(6 + 5 + 3);
    for (const [idioma, catalogo] of Object.entries(CATALOGOS)) {
      for (const clave of claves) {
        expect(catalogo[clave], `falta "${clave}" en ${idioma}.json`).toBeTypeOf("string");
        expect(catalogo[clave]?.trim(), `"${clave}" esta vacia en ${idioma}.json`).not.toBe("");
      }
    }
  });

  test("los textos de estado no usan los terminos que el glosario veta", () => {
    for (const [idioma, catalogo] of Object.entries(CATALOGOS)) {
      for (const [clave, texto] of Object.entries(catalogo)) {
        if (!/^(truth|context|fase|bolita)\./.test(clave)) continue;
        for (const vetado of TERMINOS_VETADOS) {
          expect(texto, `${idioma}.json "${clave}" usa un termino vetado (${vetado})`).not.toMatch(vetado);
        }
      }
    }
  });
});
