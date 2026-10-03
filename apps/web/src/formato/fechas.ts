/**
 * Formato de fechas por idioma (docs/ARQUITECTURA-VISUAL.md §1.1, capa formato).
 * Presenta valores sin alterarlos. Funciones puras.
 */

/** Hora local en el formato del idioma, p. ej. "14:03:27" (es) o "2:03:27 PM" (en). */
export function formatearHora(fecha: Date, locale: string): string {
  return fecha.toLocaleTimeString(locale);
}
