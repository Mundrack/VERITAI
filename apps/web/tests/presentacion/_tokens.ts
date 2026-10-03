/**
 * Lee src/presentacion/estilos/tokens.css y da el valor de cada token en cada
 * condicion (tema claro u oscuro, puntero fino o grueso), con las referencias
 * var(...) ya resueltas.
 *
 * Las pruebas comparan lo que el componente pinta con lo que dice este
 * fichero, no con valores copiados a mano: si un token cambia, la prueba sigue
 * midiendo lo mismo.
 */

import cssTokens from "../../src/presentacion/estilos/tokens.css?inline";
import type { Puntero, Tema } from "../_entorno";

export interface Condiciones {
  tema: Tema;
  puntero?: Puntero;
}

const SIN_COMENTARIOS = cssTokens.replace(/\/\*[\s\S]*?\*\//g, "");

/** Lo que hay entre las llaves de `@media (<condicion>) { ... }`, o "" si no existe. */
function bloqueMedia(condicion: RegExp): string {
  const encontrado = condicion.exec(SIN_COMENTARIOS);
  if (encontrado === null) return "";
  const inicio = SIN_COMENTARIOS.indexOf("{", encontrado.index) + 1;
  let fin = inicio;
  for (let profundidad = 1; profundidad > 0; fin++) {
    const caracter = SIN_COMENTARIOS[fin];
    if (caracter === undefined) throw new Error("tokens.css: llaves sin cerrar");
    if (caracter === "{") profundidad++;
    if (caracter === "}") profundidad--;
  }
  return SIN_COMENTARIOS.slice(inicio, fin - 1);
}

function declaraciones(texto: string): Map<string, string> {
  const mapa = new Map<string, string>();
  for (const [, nombre, valor] of texto.matchAll(/(--veritai-[\w-]+)\s*:\s*([^;]+);/g)) {
    if (nombre !== undefined && valor !== undefined) mapa.set(nombre, valor.trim());
  }
  return mapa;
}

const BASE = declaraciones(SIN_COMENTARIOS.slice(0, SIN_COMENTARIOS.indexOf("@media")));
const TEMA_OSCURO = declaraciones(bloqueMedia(/@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)/));
const PUNTERO_GRUESO = declaraciones(bloqueMedia(/@media\s*\(\s*pointer\s*:\s*coarse\s*\)/));

function sinResolver(condiciones: Condiciones): Map<string, string> {
  return new Map([
    ...BASE,
    ...(condiciones.tema === "oscuro" ? TEMA_OSCURO : []),
    ...(condiciones.puntero === "grueso" ? PUNTERO_GRUESO : []),
  ]);
}

function resolver(valor: string, mapa: Map<string, string>): string {
  return valor.replace(/var\(\s*(--veritai-[\w-]+)\s*\)/g, (_, nombre: string) => {
    const referido = mapa.get(nombre);
    if (referido === undefined) throw new Error(`tokens.css: ${nombre} no esta declarado`);
    return resolver(referido, mapa);
  });
}

/** Nombres de todos los tokens declarados en el bloque base. */
export function nombresDeTokens(): string[] {
  return [...BASE.keys()];
}

/** Valor final de un token en esas condiciones. Falla si el token no existe. */
export function token(nombre: string, condiciones: Condiciones): string {
  const mapa = sinResolver(condiciones);
  const valor = mapa.get(nombre);
  if (valor === undefined) throw new Error(`tokens.css: ${nombre} no esta declarado`);
  return resolver(valor, mapa);
}
