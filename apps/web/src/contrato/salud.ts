/**
 * Contrato de GET /health (apps/api/veritai/api/routes/health.py, RespuestaSalud).
 *
 * Capa contrato (docs/ARQUITECTURA-VISUAL.md §1.1): tipos y validadores de lo
 * que devuelve la API. Sin DOM, sin red, sin texto de interfaz.
 */

export interface RespuestaSalud {
  servicio: string;
  version: string;
  entorno: string;
  base_de_datos: string;
}

/** Valor que devuelve la API cuando la base de datos responde al `select 1`. */
export const BASE_DE_DATOS_CONECTADA = "conectada";

const CAMPOS: ReadonlyArray<keyof RespuestaSalud> = ["servicio", "version", "entorno", "base_de_datos"];

/**
 * Comprueba que un JSON recibido tiene la forma de RespuestaSalud. No arregla
 * nada: si falta un campo o no es texto, no es una respuesta de salud.
 */
export function esRespuestaSalud(valor: unknown): valor is RespuestaSalud {
  if (typeof valor !== "object" || valor === null) return false;
  const objeto = valor as Record<string, unknown>;
  return CAMPOS.every((campo) => typeof objeto[campo] === "string");
}
