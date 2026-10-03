/**
 * Enums cerrados del veredicto (docs/ARQUITECTURA-VISUAL.md §1.3, §3).
 *
 * Son los mismos valores que apps/api/veritai/domain/enums.py y
 * docs/GLOSARIO.md, sin traducir ni renombrar: la interfaz no inventa estados.
 * tests/arquitectura/enums-api.test.ts lee el fichero de Python y falla si un
 * valor de aqui no esta alli o al reves.
 *
 * Solo estan los dos ejes que la interfaz pinta hoy (la bolita). Clase y
 * AbstainReason llegaran con el panel, por el mismo camino (§6.1).
 *
 * Capa contrato: sin DOM, sin red, sin texto de interfaz.
 */

/** ¿La afirmacion literal es correcta? Primer eje del veredicto (DEC-016). */
export const Truth = {
  Supported: "supported",
  Contradicted: "contradicted",
  Mixed: "mixed",
  InsufficientEvidence: "insufficient_evidence",
  NotApplicable: "not_applicable",
} as const;
export type Truth = (typeof Truth)[keyof typeof Truth];
export const VALORES_TRUTH: readonly Truth[] = Object.values(Truth);

/**
 * ¿Los datos muestran una divergencia? Segundo eje, independiente de truth
 * (DEC-016): "ningun test disparo" es no_divergence_detected, nunca supported.
 */
export const Context = {
  DivergenceDetected: "divergence_detected",
  NoDivergenceDetected: "no_divergence_detected",
  Undetermined: "undetermined",
  NotApplicable: "not_applicable",
} as const;
export type Context = (typeof Context)[keyof typeof Context];
export const VALORES_CONTEXT: readonly Context[] = Object.values(Context);
