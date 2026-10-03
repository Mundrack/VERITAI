/**
 * Cuentas de color para las pruebas de accesibilidad. Solo formulas de norma;
 * ninguna constante que no se pueda comprobar en la norma que la define.
 *
 *   - Luminancia relativa y razon de contraste: WCAG 2.1 (definiciones de
 *     "relative luminance" y "contrast ratio").
 *   - sRGB -> XYZ (D65) -> CIELAB: IEC 61966-2-1 y CIE 1976 L*a*b*.
 *
 * Esto es aritmetica de PRUEBA sobre colores de la interfaz. No toca ningun
 * valor del veredicto; la regla "la interfaz no calcula" (§1.3) habla de eso.
 */

type Terna = [number, number, number];

function canales(hex: string): Terna {
  const limpio = hex.trim().toLowerCase();
  if (!/^#[0-9a-f]{6}$/.test(limpio)) throw new Error(`no es un color #rrggbb: "${hex}"`);
  return [1, 3, 5].map((i) => parseInt(limpio.slice(i, i + 2), 16) / 255) as Terna;
}

/** Canal sRGB a luz lineal, con el umbral que usa WCAG (0,03928). */
function linealWcag(canal: number): number {
  return canal <= 0.03928 ? canal / 12.92 : ((canal + 0.055) / 1.055) ** 2.4;
}

/** Canal sRGB a luz lineal, con el umbral de IEC 61966-2-1 (0,04045). */
function linealSrgb(canal: number): number {
  return canal <= 0.04045 ? canal / 12.92 : ((canal + 0.055) / 1.055) ** 2.4;
}

/** Luminancia relativa WCAG: 0 es negro, 1 es blanco. */
export function luminancia(hex: string): number {
  const [r, g, b] = canales(hex).map(linealWcag) as Terna;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** Razon de contraste WCAG entre dos colores: de 1 (iguales) a 21 (negro sobre blanco). */
export function contraste(hexA: string, hexB: string): number {
  const [clara, oscura] = [luminancia(hexA), luminancia(hexB)].sort((x, y) => y - x) as [number, number];
  return (clara + 0.05) / (oscura + 0.05);
}

/** Blanco de referencia D65. */
const BLANCO_D65: Terna = [0.95047, 1.0, 1.08883];
const DELTA = 6 / 29;

function f(t: number): number {
  return t > DELTA ** 3 ? Math.cbrt(t) : t / (3 * DELTA ** 2) + 4 / 29;
}

/** CIELAB: L* claridad, a* eje rojo-verde, b* eje azul-amarillo. */
export function lab(hex: string): { L: number; a: number; b: number } {
  const [r, g, b] = canales(hex).map(linealSrgb) as Terna;
  const x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b;
  const y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b;
  const z = 0.0193339 * r + 0.119192 * g + 0.9503041 * b;
  const [fx, fy, fz] = [f(x / BLANCO_D65[0]), f(y / BLANCO_D65[1]), f(z / BLANCO_D65[2])];
  return { L: 116 * fy - 16, a: 500 * (fx - fy), b: 200 * (fy - fz) };
}

/**
 * Lo que separa a dos colores cuando NO se cuenta el eje rojo-verde (a*): la
 * diferencia de claridad (L*) y la del eje azul-amarillo (b*), cada una por su
 * lado.
 *
 * Es una aproximacion, no una simulacion de daltonismo: quien no distingue el
 * rojo del verde pierde, a grandes rasgos, la informacion de a* y conserva las
 * otras dos. No modela que el rojo se vea mas oscuro en la protanopia.
 */
export function separacionSinRojoVerde(hexA: string, hexB: string): { claridad: number; azulAmarillo: number } {
  const [p, q] = [lab(hexA), lab(hexB)];
  return { claridad: Math.abs(p.L - q.L), azulAmarillo: Math.abs(p.b - q.b) };
}

/** Tono (angulo CIELAB de 0 a 360: rojo ~30, amarillo ~90, verde ~150, azul ~280) y croma (0 = gris). */
export function tonoYCroma(hex: string): { tono: number; croma: number } {
  const { a, b } = lab(hex);
  return { tono: ((Math.atan2(b, a) * 180) / Math.PI + 360) % 360, croma: Math.hypot(a, b) };
}
