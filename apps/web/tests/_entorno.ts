/**
 * Preferencias del navegador de pruebas (happy-dom): tema, movimiento y
 * puntero. Son las tres media queries de las que depende la interfaz:
 * prefers-color-scheme, prefers-reduced-motion y pointer / hover.
 *
 * OJO: happy-dom calcula los estilos de un elemento con las preferencias que
 * hay cuando se le pregunta y guarda el resultado. Las preferencias se fijan
 * ANTES de crear y montar el componente, nunca despues.
 */

import type { DetachedWindowAPI } from "happy-dom";

export type Tema = "claro" | "oscuro";
export type Movimiento = "normal" | "reducido";
export type Puntero = "fino" | "grueso";

export const TEMAS: readonly Tema[] = ["claro", "oscuro"];

export interface Preferencias {
  tema?: Tema;
  movimiento?: Movimiento;
  puntero?: Puntero;
}

function api(): DetachedWindowAPI {
  return (window as unknown as { happyDOM: DetachedWindowAPI }).happyDOM;
}

/** happy-dom decide `pointer: coarse` y `hover: none` por los puntos tactiles del navegador. */
const PUNTOS_TACTILES: Record<Puntero, number> = { fino: 0, grueso: 1 };

/** Lo que no se indique vuelve a su valor por defecto: tema claro, movimiento normal, raton. */
export function fijarPreferencias(preferencias: Preferencias = {}): void {
  const dispositivo = api().settings.device;
  dispositivo.prefersColorScheme = preferencias.tema === "oscuro" ? "dark" : "light";
  dispositivo.prefersReducedMotion = preferencias.movimiento === "reducido" ? "reduce" : "no-preference";
  Object.defineProperty(window.navigator, "maxTouchPoints", {
    value: PUNTOS_TACTILES[preferencias.puntero ?? "fino"],
    configurable: true,
  });
}

/** Deja el documento de pruebas vacio y las preferencias por defecto. */
export function limpiarEntorno(): void {
  document.head.replaceChildren();
  document.body.replaceChildren();
  fijarPreferencias();
}
