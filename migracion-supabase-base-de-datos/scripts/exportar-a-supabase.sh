#!/usr/bin/env bash
# =============================================================================
# Volcado de la base de datos local de VERITAI.
#
# Genera tres archivos con marca de tiempo en la carpeta que se indique:
#   *_esquema.sql    solo estructura
#   *_datos.sql      solo datos, con INSERT por columna (portable)
#   *_completo.dump  formato custom de pg_dump, para restaurar rapido
#
#   ./exportar-a-supabase.sh [carpeta_destino]
#
# El destino por defecto esta FUERA del repositorio a proposito: un volcado
# puede contener datos que no deben versionarse.
# =============================================================================
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DESTINO="${1:-$RAIZ/../veritai-respaldos}"
MARCA="$(date +%Y%m%d-%H%M%S)"
SERVICIO_DB="db"

mkdir -p "$DESTINO"

# El usuario y la base salen del .env, nunca del script.
if [[ -f "$RAIZ/.env" ]]; then
  # shellcheck disable=SC1091
  set -a; source "$RAIZ/.env"; set +a
fi
USUARIO="${POSTGRES_USER:-veritai_migrator}"
BASE="${POSTGRES_DB:-veritai}"

echo "Volcando '$BASE' desde el contenedor '$SERVICIO_DB'..."
cd "$RAIZ"

docker compose exec -T "$SERVICIO_DB" pg_dump -U "$USUARIO" -d "$BASE" \
  --schema-only --schema=veritai --schema=veritai_meta \
  > "$DESTINO/${MARCA}_esquema.sql"

docker compose exec -T "$SERVICIO_DB" pg_dump -U "$USUARIO" -d "$BASE" \
  --data-only --schema=veritai --schema=veritai_meta --column-inserts \
  > "$DESTINO/${MARCA}_datos.sql"

docker compose exec -T "$SERVICIO_DB" pg_dump -U "$USUARIO" -d "$BASE" \
  --format=custom --schema=veritai --schema=veritai_meta \
  > "$DESTINO/${MARCA}_completo.dump"

echo ""
echo "Listo. Archivos en: $DESTINO"
ls -lh "$DESTINO" | grep "$MARCA" || true
echo ""
echo "AVISO: un volcado puede contener datos sensibles. Guardalo fuera del"
echo "       repositorio y no lo compartas."
