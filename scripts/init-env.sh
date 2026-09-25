#!/usr/bin/env bash
# =============================================================================
# Genera el archivo .env local a partir de .env.example, con contrasenas
# aleatorias. El .env resultante esta en .gitignore y no se sube nunca.
#
#     ./scripts/init-env.sh            crea .env si no existe
#     ./scripts/init-env.sh --force    lo regenera (invalida los datos ya
#                                      guardados en el volumen de Postgres)
# =============================================================================
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLANTILLA="$RAIZ/.env.example"
DESTINO="$RAIZ/.env"
FORZAR="${1:-}"

if [[ ! -f "$PLANTILLA" ]]; then
  echo "ERROR: no se encuentra .env.example" >&2
  exit 1
fi

if [[ -f "$DESTINO" && "$FORZAR" != "--force" ]]; then
  echo "El archivo .env ya existe. No se toca."
  echo "Para regenerarlo:  ./scripts/init-env.sh --force"
  echo "AVISO: cambiar la contrasena de Postgres despues de crear el volumen"
  echo "       obliga a 'docker compose down -v', que BORRA los datos."
  exit 0
fi

# Contrasenas alfanumericas: van dentro de una URL de conexion, asi que no
# pueden contener caracteres que haya que escapar.
generar() {
  LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32
}

PASS_MIGRATOR="$(generar)"
PASS_APP="$(generar)"

python3 - "$PLANTILLA" "$DESTINO" "$PASS_MIGRATOR" "$PASS_APP" <<'PY'
import sys

plantilla, destino, pass_migrator, pass_app = sys.argv[1:5]
MARCADOR = "GENERAR_CON_init-env"

salida = []
for linea in open(plantilla, encoding="utf-8").read().splitlines():
    if linea.startswith("POSTGRES_PASSWORD="):
        linea = f"POSTGRES_PASSWORD={pass_migrator}"
    elif linea.startswith("VERITAI_APP_DB_PASSWORD="):
        linea = f"VERITAI_APP_DB_PASSWORD={pass_app}"
    elif linea.startswith("DATABASE_URL_MIGRATOR="):
        linea = linea.replace(MARCADOR, pass_migrator)
    elif linea.startswith("DATABASE_URL="):
        linea = linea.replace(MARCADOR, pass_app)
    salida.append(linea)

# Fin de linea LF de forma explicita: un \r al final de un valor entra en la
# contrasena que lee Docker Compose y la conexion falla sin decir por que.
with open(destino, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(salida) + "\n")
PY

chmod 600 "$DESTINO" 2>/dev/null || true

echo "Archivo .env creado en $DESTINO"
echo "Contrasenas generadas al azar. No las copies a ningun otro sitio."
echo
echo "Siguiente paso:  docker compose up -d"
