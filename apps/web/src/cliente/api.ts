/**
 * Cliente de la API (docs/ARQUITECTURA-VISUAL.md §1.1): la unica capa que
 * habla con la red. Devuelve objetos del contrato ya validados y no decide
 * nada sobre lo que recibe.
 */

import { esRespuestaSalud, type RespuestaSalud } from "../contrato/salud";
import { TIEMPO_MAXIMO_API_MS, URL_BASE_API } from "./config";

/**
 * GET /health. Devuelve null si la API no responde a tiempo, responde con
 * error o devuelve algo que no tiene la forma del contrato.
 */
export async function consultarSalud(): Promise<RespuestaSalud | null> {
  const control = new AbortController();
  const limite = setTimeout(() => control.abort(), TIEMPO_MAXIMO_API_MS);
  try {
    const respuesta = await fetch(`${URL_BASE_API}/health`, { signal: control.signal });
    if (!respuesta.ok) return null;
    const cuerpo: unknown = await respuesta.json();
    return esRespuestaSalud(cuerpo) ? cuerpo : null;
  } catch {
    return null;
  } finally {
    clearTimeout(limite);
  }
}
