# =============================================================================
# API de VERITAI - FastAPI
#
# Decisiones:
#   - imagen slim con version fija; nunca "latest"
#   - usuario sin privilegios; el proceso no corre como root (START-HERE 25)
#   - dependencias en una capa aparte del codigo, para que un cambio de codigo
#     no invalide la cache de pip
# =============================================================================

FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN groupadd --system --gid 10001 veritai \
 && useradd --system --uid 10001 --gid veritai --no-create-home --shell /usr/sbin/nologin veritai

# ---------------------------------------------------------------------------
# runtime: lo que se publica y lo que usa el servicio de migraciones
# ---------------------------------------------------------------------------
FROM base AS runtime

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=veritai:veritai . .

USER veritai
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=6 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2).status == 200 else 1)"

CMD ["uvicorn", "veritai.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---------------------------------------------------------------------------
# dev: anade las herramientas de test. No se publica.
# ---------------------------------------------------------------------------
FROM runtime AS dev

USER root
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
USER veritai
