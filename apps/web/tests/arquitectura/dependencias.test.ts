// @vitest-environment node
// Lee ficheros con node:fs; no necesita DOM (con happy-dom, import.meta.url no es file:).
/**
 * La matriz de dependencias permitidas (docs/ARQUITECTURA-VISUAL.md §1.2 y
 * §1.4), comprobada contra el codigo.
 *
 * Lee apps/web/arquitectura.json, asigna cada fichero de src/ a su capa por la
 * ruta, y recorre sus imports. Falla, con fichero y linea, por cada import que
 * cruce una casilla no permitida, por cada fichero que no pertenezca a ninguna
 * capa declarada y por cada import dinamico cuyo destino no sea una cadena
 * literal (no se puede saber a que capa va).
 *
 * Se espera que falle contra el codigo del 2026-10-03: main.ts importa i18n
 * directamente. Esa prueba en rojo es la prueba de que la matriz mide algo.
 */

import { readFileSync } from "node:fs";
import { posix, resolve } from "node:path";

import ts from "typescript";
import { describe, expect, test } from "vitest";

import { lineaDe, listarFuentes, paraCadaNodo, RAIZ_WEB, type Fuente } from "./_fuentes";

interface Capa {
  raiz: string;
  puede_importar: string[];
}

interface Arquitectura {
  capas: Record<string, Capa>;
}

const ARQUITECTURA: Arquitectura = JSON.parse(
  readFileSync(resolve(RAIZ_WEB, "arquitectura.json"), "utf-8"),
) as Arquitectura;

/** Capa a la que pertenece una ruta relativa a apps/web, o null si no esta en ninguna. */
function capaDe(ruta: string): string | null {
  for (const [nombre, capa] of Object.entries(ARQUITECTURA.capas)) {
    if (ruta === capa.raiz || ruta.startsWith(`${capa.raiz}/`)) return nombre;
  }
  return null;
}

/** Resuelve un especificador relativo a una ruta relativa a apps/web con "/" (sin extension si no la lleva). */
function resolverRelativo(fuente: Fuente, especificador: string): string {
  const directorio = posix.dirname(fuente.ruta);
  const resuelto = posix.normalize(posix.join(directorio, especificador));
  // Un import que sale de src/ (por ejemplo "../arquitectura.json") se deja tal cual.
  return resuelto;
}

interface Import {
  especificador: string | null; // null = dinamico con expresion, no analizable
  linea: number;
}

/** Todos los imports y re-exports del fichero, estaticos y dinamicos. */
function importsDe(fuente: Fuente): Import[] {
  const resultado: Import[] = [];
  paraCadaNodo(fuente.arbol, (nodo) => {
    if (ts.isImportDeclaration(nodo) && ts.isStringLiteral(nodo.moduleSpecifier)) {
      resultado.push({ especificador: nodo.moduleSpecifier.text, linea: lineaDe(fuente, nodo) });
    } else if (ts.isExportDeclaration(nodo) && nodo.moduleSpecifier && ts.isStringLiteral(nodo.moduleSpecifier)) {
      resultado.push({ especificador: nodo.moduleSpecifier.text, linea: lineaDe(fuente, nodo) });
    } else if (ts.isCallExpression(nodo) && nodo.expression.kind === ts.SyntaxKind.ImportKeyword) {
      const argumento = nodo.arguments[0];
      const literal =
        argumento !== undefined &&
        (ts.isStringLiteral(argumento) || ts.isNoSubstitutionTemplateLiteral(argumento))
          ? argumento.text
          : null;
      resultado.push({ especificador: literal, linea: lineaDe(fuente, nodo) });
    }
  });
  return resultado;
}

function esRelativo(especificador: string): boolean {
  return especificador.startsWith(".") || especificador.startsWith("/");
}

describe("matriz de dependencias (arquitectura.json)", () => {
  const fuentes = listarFuentes();

  test("la matriz declara al menos una capa y cada capa solo permite capas que existen", () => {
    const nombres = Object.keys(ARQUITECTURA.capas);
    expect(nombres.length).toBeGreaterThan(0);
    for (const [nombre, capa] of Object.entries(ARQUITECTURA.capas)) {
      for (const permitida of capa.puede_importar) {
        expect(nombres, `${nombre} permite importar de "${permitida}", que no es una capa declarada`).toContain(
          permitida,
        );
      }
    }
  });

  test("todo fichero de src/ pertenece a una capa declarada", () => {
    const fuera = fuentes.filter((f) => capaDe(f.ruta) === null).map((f) => f.ruta);
    expect(fuera, `ficheros fuera de las capas declaradas:\n  ${fuera.join("\n  ")}`).toEqual([]);
  });

  test("ningun import cruza una casilla no permitida de la matriz", () => {
    const violaciones: string[] = [];

    for (const fuente of fuentes) {
      const capaOrigen = capaDe(fuente.ruta);
      if (capaOrigen === null) continue; // ya lo recoge la prueba anterior
      const permitidas = ARQUITECTURA.capas[capaOrigen]?.puede_importar ?? [];

      for (const imp of importsDe(fuente)) {
        if (imp.especificador === null) {
          violaciones.push(
            `${fuente.ruta}:${imp.linea}  import() dinamico con una expresion: no se puede saber a que capa va`,
          );
          continue;
        }
        if (!esRelativo(imp.especificador)) continue; // paquete externo: no lo gobierna la matriz

        const destino = resolverRelativo(fuente, imp.especificador);
        const capaDestino = capaDe(destino);
        if (capaDestino === null) {
          violaciones.push(
            `${fuente.ruta}:${imp.linea}  importa "${imp.especificador}" (${destino}), que no esta en ninguna capa declarada`,
          );
          continue;
        }
        if (capaDestino === capaOrigen || permitidas.includes(capaDestino)) continue;

        violaciones.push(
          `${fuente.ruta}:${imp.linea}  [${capaOrigen}] importa "${imp.especificador}" (capa ${capaDestino}); ` +
            `${capaOrigen} solo puede importar de: ${permitidas.length ? permitidas.join(", ") : "ninguna capa"}`,
        );
      }
    }

    expect(
      violaciones,
      `imports que cruzan la matriz de dependencias:\n  ${violaciones.join("\n  ")}`,
    ).toEqual([]);
  });
});
