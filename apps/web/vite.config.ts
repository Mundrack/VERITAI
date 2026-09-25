import { defineConfig } from "vite";

export default defineConfig({
  server: {
    // 0.0.0.0 dentro del contenedor. El puerto del host se publica en
    // 127.0.0.1 desde docker-compose.yml, no desde aqui.
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    watch: {
      // Los eventos de inotify no cruzan un bind mount de Docker Desktop en
      // Windows. Sin polling, la recarga en caliente no se dispara nunca.
      usePolling: true,
      interval: 300,
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
