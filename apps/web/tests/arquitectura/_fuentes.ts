/**
 * Utilidades compartidas por las pruebas de arquitectura: localizar la raiz de
 * apps/web, listar los ficheros fuente y analizarlos con el compilador de
 * TypeScript. Se usa el analizador real y no expresiones regulares porque un
 * `import` puede ocupar varias lineas, no llevar `from`, o ser dinamico.
 */

import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import ts from "typescript";

/** Raiz de apps/web (donde estan package.json y arquitectura.json). */
export const RAIZ_WEB = resolve(fileURLToPath(new URL(".", import.meta.url)), "..", "..");

export interface Fuente {
  /** Ruta relativa a apps/web con separadores "/", p. ej. "src/i18n/index.ts". */
  ruta: string;
  rutaAbsoluta: string;
  texto: string;
  arbol: ts.SourceFile;
}

function aPosix(ruta: string): string {
  return ruta.split("\\").join("/");
}

function recorrer(directorio: string, acumulado: string[]): void {
  for (const nombre of readdirSync(directorio)) {
    const ruta = join(directorio, nombre);
    if (statSync(ruta).isDirectory()) {
      recorrer(ruta, acumulado);
    } else if (nombre.endsWith(".ts") && !nombre.endsWith(".d.ts")) {
      acumulado.push(ruta);
    }
  }
}

/** Todos los .ts de src/ (sin .d.ts), analizados. */
export function listarFuentes(): Fuente[] {
  const absolutas: string[] = [];
  recorrer(resolve(RAIZ_WEB, "src"), absolutas);
  absolutas.sort();
  return absolutas.map((rutaAbsoluta) => {
    const texto = readFileSync(rutaAbsoluta, "utf-8");
    return {
      ruta: aPosix(relative(RAIZ_WEB, rutaAbsoluta)),
      rutaAbsoluta,
      texto,
      arbol: ts.createSourceFile(rutaAbsoluta, texto, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS),
    };
  });
}

/** Numero de linea (desde 1) de un nodo del arbol. */
export function lineaDe(fuente: Fuente, nodo: ts.Node): number {
  return fuente.arbol.getLineAndCharacterOfPosition(nodo.getStart(fuente.arbol)).line + 1;
}

/** Recorre todos los nodos del arbol en profundidad. */
export function paraCadaNodo(raiz: ts.Node, visitar: (nodo: ts.Node) => void): void {
  visitar(raiz);
  ts.forEachChild(raiz, (hijo) => paraCadaNodo(hijo, visitar));
}
