# =============================================================================
# Web de VERITAI - Vite + TypeScript, sin framework
#
# Una extension MV3 no se ejecuta dentro de un contenedor: solo se construye.
# Por eso este contenedor sirve el panel como aplicacion web durante el
# desarrollo, y la etapa "build" produce el bundle que mas adelante se empaqueta
# como extension.
# =============================================================================

FROM node:22-alpine AS deps

RUN mkdir -p /app && chown node:node /app
WORKDIR /app
USER node

COPY --chown=node:node package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

# ---------------------------------------------------------------------------
# dev: servidor de Vite con recarga en caliente
# ---------------------------------------------------------------------------
FROM deps AS dev

COPY --chown=node:node . .
EXPOSE 5173
CMD ["npm", "run", "dev"]

# ---------------------------------------------------------------------------
# build: genera /app/dist. Todavia no se sirve desde ningun contenedor.
# ---------------------------------------------------------------------------
FROM deps AS build

COPY --chown=node:node . .
RUN npm run build
