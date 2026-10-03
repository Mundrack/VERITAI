/**
 * Fases de la consulta: el unico enum cerrado PROPIO de la interfaz.
 *
 * No viene de la API ni del glosario del dominio, y por eso la prueba de
 * paridad con enums.py no lo cubre: "en espera", "analizando" y "error" no son
 * veredictos, son el momento en que esta la consulta antes de que haya uno (o
 * cuando no llego a haberlo). Aprobado por Mateo el 2026-10-03 como enum
 * cerrado; anadir un valor es una decision suya, no un detalle de codigo.
 *
 *   en_espera   todavia no se ha pedido nada
 *   analizando  la consulta esta en curso
 *   error       la API no respondio, se agoto el tiempo o la respuesta no
 *               cumple el contrato. No dice nada sobre la afirmacion.
 *
 * Vive en contrato porque la fija aplicacion y la pinta presentacion, y
 * presentacion no puede importar de aplicacion (§1.2): hace falta una hoja
 * comun. Sin DOM, sin red, sin texto de interfaz.
 */
export const FaseConsulta = {
  EnEspera: "en_espera",
  Analizando: "analizando",
  Error: "error",
} as const;
export type FaseConsulta = (typeof FaseConsulta)[keyof typeof FaseConsulta];
export const VALORES_FASE_CONSULTA: readonly FaseConsulta[] = Object.values(FaseConsulta);
