import { defineConfig, mergeConfig } from "vitest/config";

import configVite from "./vite.config";

/**
 * Pruebas de la interfaz (docs/ARQUITECTURA-VISUAL.md §5).
 *
 * Vitest reutiliza la configuracion de Vite; happy-dom da el DOM que necesitan
 * las pruebas de componente. Los umbrales de cobertura solo se aplican con
 * `npm run test:cobertura`: 80 % global, 100 % en las capas puras (§5.3).
 */
export default mergeConfig(
  configVite,
  defineConfig({
    test: {
      environment: "happy-dom",
      include: ["tests/**/*.test.ts"],
      coverage: {
        provider: "v8",
        include: ["src/**/*.ts"],
        reporter: ["text", "html"],
        thresholds: {
          lines: 80,
          branches: 80,
          "src/contrato/**": { lines: 100 },
          "src/formato/**": { lines: 100 },
          "src/i18n/index.ts": { lines: 100 },
          "src/presentacion/estados.ts": { lines: 100 },
          "src/localizacion/**": { lines: 100 },
        },
      },
    },
  }),
);
