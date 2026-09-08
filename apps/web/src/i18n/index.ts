/**
 * Internacionalizacion de la interfaz.
 *
 * Decision cerrada en 00b-DECISIONES-MATEO: la interfaz es multiidioma desde el
 * primer dia (es + en). El analisis de contenido sigue siendo solo en espanol.
 * Coste ahora: casi nulo. Coste despues: reescribir la capa de presentacion.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * REGLA CRITICA — no relajarla nunca
 *
 *   Se traduce la PLANTILLA, jamas el resultado ya renderizado.
 *
 *   correcto:    t("plantilla.caida", { puestos: 16 })
 *                  es -> "Cayo 16 puestos"
 *                  en -> "Dropped 16 places"
 *
 *   prohibido:   traducir("Cayo 16 puestos")
 *
 * Traducir la salida final vuelve a poner los numeros del veredicto en manos de
 * un traductor (o de un modelo), y eso reintroduce exactamente el riesgo que la
 * arquitectura entera existe para eliminar: ningun numero puede alterarse
 * despues de calcularse (START-HERE 3 y 5).
 * ─────────────────────────────────────────────────────────────────────────────
 */

import es from "./es.json";
import en from "./en.json";

export type Locale = "es" | "en";

const CATALOGOS: Record<Locale, Record<string, string>> = { es, en };

const LOCALES_SOPORTADOS: readonly Locale[] = ["es", "en"] as const;

function esLocaleSoportado(valor: string): valor is Locale {
  return (LOCALES_SOPORTADOS as readonly string[]).includes(valor);
}

export function localePorDefecto(): Locale {
  const configurado = import.meta.env.VITE_DEFAULT_LOCALE;
  if (typeof configurado === "string" && esLocaleSoportado(configurado)) {
    return configurado;
  }
  return "es";
}

let localeActual: Locale = localePorDefecto();

export function obtenerLocale(): Locale {
  return localeActual;
}

export function fijarLocale(locale: Locale): void {
  localeActual = locale;
  document.documentElement.lang = locale;
}

export function localesDisponibles(): readonly Locale[] {
  return LOCALES_SOPORTADOS;
}

/**
 * Devuelve el texto de `clave` en el idioma activo, sustituyendo los
 * marcadores {nombre} por los valores de `parametros`.
 *
 * Si la clave no existe se devuelve la clave misma: un texto sin traducir es
 * visible al instante, mientras que una cadena vacia pasa desapercibida.
 */
export function t(clave: string, parametros: Record<string, string | number> = {}): string {
  const plantilla = CATALOGOS[localeActual][clave] ?? CATALOGOS.es[clave] ?? clave;

  return plantilla.replace(/\{(\w+)\}/g, (coincidencia, nombre: string) => {
    const valor = parametros[nombre];
    return valor === undefined ? coincidencia : String(valor);
  });
}
