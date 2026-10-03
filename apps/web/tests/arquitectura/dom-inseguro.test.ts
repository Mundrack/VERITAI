// @vitest-environment node
// Lee ficheros con node:fs; no necesita DOM (con happy-dom, import.meta.url no es file:).
/**
 * DOM inseguro (docs/ARQUITECTURA-VISUAL.md §4).
 *
 * Prohibido en src/:
 *   - asignar `innerHTML` u `outerHTML` (tambien con `+=`) salvo con una cadena
 *     literal constante, sin interpolacion;
 *   - `insertAdjacentHTML(...)`, `document.write(...)`, `document.writeln(...)`;
 *   - `eval(...)`, `new Function(...)`, y `setTimeout` / `setInterval` con una
 *     cadena como primer argumento (son eval con otro nombre);
 *   - `import()` cuyo destino no sea una cadena literal.
 *
 * Los componentes construyen el DOM con createElement y textContent. Leer
 * innerHTML no se prohibe aqui (lo hace escapar() en main.ts hoy); escribirlo
 * con datos, si. Se espera que falle contra el codigo del 2026-10-03: main.ts
 * pinta el panel con `raiz.innerHTML = \`...${...}\``.
 */

import ts from "typescript";
import { describe, expect, test } from "vitest";

import { lineaDe, listarFuentes, paraCadaNodo, type Fuente } from "./_fuentes";

const PROPIEDADES_HTML = new Set(["innerHTML", "outerHTML"]);
const METODOS_HTML = new Set(["insertAdjacentHTML"]);
const METODOS_DOCUMENT = new Set(["write", "writeln"]);
const TEMPORIZADORES = new Set(["setTimeout", "setInterval"]);

function esLiteralConstante(nodo: ts.Expression): boolean {
  return ts.isStringLiteral(nodo) || ts.isNoSubstitutionTemplateLiteral(nodo);
}

function nombreDePropiedad(nodo: ts.Expression): string | null {
  if (ts.isPropertyAccessExpression(nodo)) return nodo.name.text;
  if (ts.isElementAccessExpression(nodo) && ts.isStringLiteral(nodo.argumentExpression)) {
    return nodo.argumentExpression.text;
  }
  return null;
}

function objetoDe(nodo: ts.Expression): string | null {
  if (ts.isPropertyAccessExpression(nodo) && ts.isIdentifier(nodo.expression)) return nodo.expression.text;
  return null;
}

function hallazgosDe(fuente: Fuente): string[] {
  const hallazgos: string[] = [];
  const anotar = (nodo: ts.Node, motivo: string) =>
    hallazgos.push(`${fuente.ruta}:${lineaDe(fuente, nodo)}  ${motivo}`);

  paraCadaNodo(fuente.arbol, (nodo) => {
    // x.innerHTML = ...   /   x.innerHTML += ...
    if (ts.isBinaryExpression(nodo)) {
      const operador = nodo.operatorToken.kind;
      const esAsignacion = operador === ts.SyntaxKind.EqualsToken || operador === ts.SyntaxKind.PlusEqualsToken;
      const propiedad = nombreDePropiedad(nodo.left);
      if (esAsignacion && propiedad !== null && PROPIEDADES_HTML.has(propiedad)) {
        if (operador === ts.SyntaxKind.PlusEqualsToken || !esLiteralConstante(nodo.right)) {
          anotar(nodo, `asigna ${propiedad} con datos (solo se admite una cadena literal constante)`);
        }
      }
    }

    if (ts.isCallExpression(nodo)) {
      const llamada = nodo.expression;
      const metodo = nombreDePropiedad(llamada);
      const primerArgumento = nodo.arguments[0];

      if (metodo !== null && METODOS_HTML.has(metodo)) {
        anotar(nodo, `llama a ${metodo}()`);
      }
      if (metodo !== null && METODOS_DOCUMENT.has(metodo) && objetoDe(llamada) === "document") {
        anotar(nodo, `llama a document.${metodo}()`);
      }
      if (ts.isIdentifier(llamada) && llamada.text === "eval") {
        anotar(nodo, "llama a eval()");
      }
      if (
        ts.isIdentifier(llamada) &&
        TEMPORIZADORES.has(llamada.text) &&
        primerArgumento !== undefined &&
        (esLiteralConstante(primerArgumento) || ts.isTemplateExpression(primerArgumento))
      ) {
        anotar(nodo, `${llamada.text}() con una cadena como primer argumento (es eval)`);
      }
      if (llamada.kind === ts.SyntaxKind.ImportKeyword) {
        if (primerArgumento === undefined || !esLiteralConstante(primerArgumento)) {
          anotar(nodo, "import() dinamico con una expresion construida");
        }
      }
    }

    if (ts.isNewExpression(nodo) && ts.isIdentifier(nodo.expression) && nodo.expression.text === "Function") {
      anotar(nodo, "new Function()");
    }
  });

  return hallazgos;
}

describe("DOM inseguro en src/", () => {
  const fuentes = listarFuentes();

  test("hay ficheros fuente que analizar", () => {
    expect(fuentes.length).toBeGreaterThan(0);
  });

  test("ningun fichero escribe HTML con datos ni ejecuta codigo a partir de cadenas", () => {
    const hallazgos = fuentes.flatMap(hallazgosDe);
    expect(hallazgos, `usos prohibidos:\n  ${hallazgos.join("\n  ")}`).toEqual([]);
  });
});
