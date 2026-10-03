// @vitest-environment node
// Lee ficheros con node:fs; no necesita DOM (con happy-dom, import.meta.url no es file:).
/**
 * Paridad de enums con la API (docs/ARQUITECTURA-VISUAL.md §4, §5.2, §6.1).
 *
 * Los estados visuales salen de los enums del dominio y de ningun otro sitio.
 * Esta prueba lee apps/api/veritai/domain/enums.py y comprueba que cada enum
 * de src/contrato/enums.ts tiene exactamente los mismos valores que su clase
 * de Python, en el mismo orden. Si alguien anade un valor en un lado y no en
 * el otro, falla.
 *
 * Solo LEE el fichero de Python. Si no esta al alcance (dentro del contenedor
 * web, que solo monta apps/web), la comparacion no se puede hacer y la prueba
 * se marca como omitida, a la vista: no se da por buena.
 *
 * contrato/fase-consulta.ts queda fuera a proposito: es el enum propio de la
 * interfaz y no existe en la API.
 */

import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, test } from "vitest";

import * as enumsWeb from "../../src/contrato/enums";
import { RAIZ_WEB } from "./_fuentes";

const RUTA_ENUMS_API = resolve(RAIZ_WEB, "..", "api", "veritai", "domain", "enums.py");
const HAY_API = existsSync(RUTA_ENUMS_API);

/** Los valores de cada clase `class Nombre(StrEnum):` de enums.py, en orden de declaracion. */
function enumsDePython(fuente: string): Map<string, string[]> {
  const enums = new Map<string, string[]>();
  let actual: string[] | null = null;
  for (const linea of fuente.split(/\r?\n/)) {
    const clase = /^class\s+(\w+)\(StrEnum\):/.exec(linea);
    if (clase?.[1] !== undefined) {
      actual = [];
      enums.set(clase[1], actual);
      continue;
    }
    if (/^\S/.test(linea)) actual = null; // cualquier otra linea sin sangria cierra la clase
    const miembro = /^\s+[A-Z][A-Z0-9_]*\s*=\s*"([^"]*)"/.exec(linea);
    if (actual !== null && miembro?.[1] !== undefined) actual.push(miembro[1]);
  }
  return enums;
}

/** Los enums de contrato/enums.ts: sus objetos `as const`, por nombre. */
function enumsDeLaWeb(): Map<string, string[]> {
  const enums = new Map<string, string[]>();
  for (const [nombre, valor] of Object.entries(enumsWeb)) {
    if (typeof valor === "object" && valor !== null && !Array.isArray(valor)) {
      enums.set(nombre, Object.values(valor as Record<string, string>));
    }
  }
  return enums;
}

describe("paridad de enums con la API", () => {
  test("contrato/enums.ts declara al menos los dos ejes del veredicto", () => {
    expect([...enumsDeLaWeb().keys()]).toEqual(expect.arrayContaining(["Truth", "Context"]));
  });

  test.skipIf(!HAY_API)(
    "cada enum de contrato/enums.ts tiene los mismos valores que su clase en apps/api/veritai/domain/enums.py",
    () => {
      const python = enumsDePython(readFileSync(RUTA_ENUMS_API, "utf-8"));
      expect(python.size, "no se reconocio ninguna clase StrEnum en enums.py").toBeGreaterThan(0);

      for (const [nombre, valores] of enumsDeLaWeb()) {
        expect(python.has(nombre), `${nombre} existe en contrato/enums.ts y no en enums.py`).toBe(true);
        expect(valores, `${nombre}: los valores no coinciden con los de enums.py`).toEqual(python.get(nombre));
      }
    },
  );

  test.skipIf(!HAY_API)("el analizador reconoce las cuatro clases de enums.py, no solo las que hoy se usan", () => {
    const python = enumsDePython(readFileSync(RUTA_ENUMS_API, "utf-8"));
    expect([...python.keys()].sort()).toEqual(["AbstainReason", "Clase", "Context", "Truth"]);
    for (const [nombre, valores] of python) {
      expect(valores.length, `${nombre} sin valores: el analizador no leyo sus miembros`).toBeGreaterThan(0);
    }
  });
});
