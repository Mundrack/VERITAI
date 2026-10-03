/**
 * Configuracion del cliente de la API (docs/ARQUITECTURA-VISUAL.md §2, §4).
 * Aqui viven los valores con nombre; en el resto del codigo no hay numeros
 * sueltos.
 */

/** URL base de la API. En el contenedor viene de VITE_API_BASE_URL (.env). */
export const URL_BASE_API: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/**
 * Tiempo maximo de espera por una respuesta de la API, en milisegundos.
 * El panel no debe quedarse colgado si la API no responde: pasado este tiempo
 * la peticion se aborta y la API se da por no disponible.
 */
export const TIEMPO_MAXIMO_API_MS = 4000;
