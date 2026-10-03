/**
 * Mapa cerrado de enums a estados visuales (docs/ARQUITECTURA-VISUAL.md §1.3
 * punto 2, §6.1).
 *
 * Los estados visuales son los enums del contrato y nada mas. Un valor que no
 * esta en el enum (la API anadio uno y la interfaz aun no lo conoce) produce
 * el estado `desconocido`: se pinta como tal y no se adivina a cual se parece.
 * Anotarlo en el registro es trabajo de quien llama (aplicacion); esta capa no
 * registra nada.
 *
 * Cada estado da dos cosas, las dos derivadas del valor del enum tal cual:
 *   - el modificador de clase y de token:  <eje>-<valor>
 *       .veritai-bolita--truth-contradicted
 *       --veritai-color-truth-contradicted
 *   - la clave del texto:                  <eje>.<valor>
 *       truth.contradicted
 *
 * Funciones puras: sin DOM, sin red, sin aritmetica.
 */

import { VALORES_CONTEXT, VALORES_TRUTH, type Context, type Truth } from "../contrato/enums";
import type { FaseConsulta } from "../contrato/fase-consulta";

/** Estado visual de un valor que no esta en su enum (§1.3). */
export const DESCONOCIDO = "desconocido";

export type EstadoTruth = Truth | typeof DESCONOCIDO;
export type EstadoContext = Context | typeof DESCONOCIDO;

export interface EstadoVisual {
  /** El valor del enum, o `desconocido`. Es lo que se escribe en `data-veritai-<eje>`. */
  estado: string;
  /** Sufijo de la clase modificadora y del token de color: `<eje>-<valor>`. */
  modificador: string;
  /** Clave i18n del texto que dice el estado en palabras: `<eje>.<valor>`. */
  clave: string;
}

function pertenece<T extends string>(valores: readonly T[], valor: string): valor is T {
  return (valores as readonly string[]).includes(valor);
}

function estadoVisual(eje: string, estado: string): EstadoVisual {
  return { estado, modificador: `${eje}-${estado}`, clave: `${eje}.${estado}` };
}

/** El valor de `truth` tal como llega, o `desconocido` si no esta en el enum. */
export function estadoTruth(valor: string): EstadoTruth {
  return pertenece(VALORES_TRUTH, valor) ? valor : DESCONOCIDO;
}

/** El valor de `context` tal como llega, o `desconocido` si no esta en el enum. */
export function estadoContext(valor: string): EstadoContext {
  return pertenece(VALORES_CONTEXT, valor) ? valor : DESCONOCIDO;
}

export function visualTruth(valor: string): EstadoVisual {
  return estadoVisual("truth", estadoTruth(valor));
}

export function visualContext(valor: string): EstadoVisual {
  return estadoVisual("context", estadoContext(valor));
}

export function visualFase(fase: FaseConsulta): EstadoVisual {
  return estadoVisual("fase", fase);
}
