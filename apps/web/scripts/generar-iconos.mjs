#!/usr/bin/env node
/**
 * Genera los PNG de icono de la extension a partir de los SVG de la marca.
 * (docs/ARQUITECTURA-VISUAL.md §2.1). No se dibuja nada a mano: si el simbolo
 * cambia, se vuelve a ejecutar y los PNG cambian con el.
 *
 * Regla de uso de la marca (Mateo, 2026-10-03):
 *   - 48 px o mas: el simbolo con orbita (veritai-simbolo.svg).
 *   - por debajo de 48 px: el simbolo minimo (veritai-simbolo-min.svg), que
 *     hereda el color del texto (currentColor) y no lleva color propio.
 *
 * Como el PNG de un icono no tiene "texto" del que heredar, el simbolo minimo
 * se renderiza con un color de contexto explicito. Ese color sale del token
 * --veritai-color-acento de tokens.css si existe; si no, de --color=#rrggbb;
 * si tampoco, el script se para. Un icono negro por falta de contexto es
 * justo lo que paso con el icono-16.png hecho a mano.
 *
 * Uso:
 *   node scripts/generar-iconos.mjs
 *   node scripts/generar-iconos.mjs --color=#98242c
 *   node scripts/generar-iconos.mjs --simbolo=ruta.svg --minimo=ruta.svg --salida=dir   (pruebas)
 */

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { Resvg } from "@resvg/resvg-js";

const RAIZ_WEB = resolve(dirname(fileURLToPath(import.meta.url)), "..");

/** Tamanos que pide Manifest V3 (16, 32, 48, 128) mas el de la ficha de la tienda (512). */
const TAMANOS_PX = [16, 32, 48, 128, 512];
/** A partir de este tamano se usa el simbolo con orbita. */
const UMBRAL_ORBITA_PX = 48;
/** Token que da color al simbolo minimo cuando no hay texto del que heredar. */
const TOKEN_ACENTO = "--veritai-color-acento";

const RUTAS = {
  simbolo: resolve(RAIZ_WEB, "src/presentacion/marca/veritai-simbolo.svg"),
  minimo: resolve(RAIZ_WEB, "src/presentacion/marca/veritai-simbolo-min.svg"),
  tokens: resolve(RAIZ_WEB, "src/presentacion/estilos/tokens.css"),
  salida: resolve(RAIZ_WEB, "src/extension/iconos"),
};

function argumentos() {
  const valores = {};
  for (const arg of process.argv.slice(2)) {
    const m = /^--(\w+)=(.+)$/.exec(arg);
    if (!m) {
      console.error(`argumento no reconocido: ${arg}`);
      process.exit(2);
    }
    valores[m[1]] = m[2];
  }
  return valores;
}

function parar(mensaje) {
  console.error(`generar-iconos: ${mensaje}`);
  process.exit(1);
}

/** Lee el valor de un token en el primer bloque :root de tokens.css (tema claro). */
function tokenDeTokensCss(rutaTokens, nombre) {
  if (!existsSync(rutaTokens)) return null;
  const css = readFileSync(rutaTokens, "utf-8");
  const m = new RegExp(`${nombre}\\s*:\\s*([^;]+);`).exec(css);
  return m ? m[1].trim() : null;
}

/** Pone color="..." en la etiqueta raiz <svg> si no lo tiene: resvg resuelve currentColor desde ahi. */
function conColorDeContexto(svg, color) {
  if (/<svg\b[^>]*\bcolor=/.test(svg)) return svg;
  return svg.replace(/<svg\b/, `<svg color="${color}"`);
}

function renderizar(svg, px) {
  const png = new Resvg(svg, { fitTo: { mode: "width", value: px } }).render();
  if (png.width !== px || png.height !== px) {
    parar(`el SVG no es cuadrado: ${png.width}x${png.height} al pedir ${px} px. El simbolo tiene que tener un viewBox cuadrado`);
  }
  return png.asPng();
}

function main() {
  const args = argumentos();
  const rutaSimbolo = args.simbolo ? resolve(args.simbolo) : RUTAS.simbolo;
  const rutaMinimo = args.minimo ? resolve(args.minimo) : RUTAS.minimo;
  const salida = args.salida ? resolve(args.salida) : RUTAS.salida;

  for (const [nombre, ruta] of [["simbolo con orbita", rutaSimbolo], ["simbolo minimo", rutaMinimo]]) {
    if (!existsSync(ruta)) parar(`falta el ${nombre}: ${ruta}. No se genera nada sin el SVG de la marca.`);
  }
  const color = args.color ?? tokenDeTokensCss(RUTAS.tokens, TOKEN_ACENTO);
  if (!color) {
    parar(`no hay color de contexto para el simbolo minimo: ni ${TOKEN_ACENTO} en tokens.css ni --color=#rrggbb`);
  }
  if (!/^#[0-9a-fA-F]{6}$/.test(color)) parar(`color no valido: ${color} (se espera #rrggbb)`);

  const simbolo = readFileSync(rutaSimbolo, "utf-8");
  const minimo = conColorDeContexto(readFileSync(rutaMinimo, "utf-8"), color);
  mkdirSync(salida, { recursive: true });

  const filas = [];
  for (const px of TAMANOS_PX) {
    const conOrbita = px >= UMBRAL_ORBITA_PX;
    const png = renderizar(conOrbita ? simbolo : minimo, px);
    const destino = resolve(salida, `icono-${px}.png`);
    writeFileSync(destino, png);
    filas.push({
      fichero: `icono-${px}.png`,
      origen: conOrbita ? "simbolo con orbita" : `simbolo minimo (color ${color})`,
      bytes: png.length,
      sha256: createHash("sha256").update(png).digest("hex").slice(0, 16),
    });
  }
  console.table(filas);
  console.log(`escritos en ${salida}`);
}

main();
