#!/usr/bin/env python3
"""Aplicador de migraciones SQL de VERITAI.

Corre como servicio de un solo uso en Docker Compose, antes de que arranque la
API. Es deliberadamente pequeno y sin dependencias fuera de psycopg.

POR QUE UN RUNNER PROPIO Y NO ALEMBIC
    Las migraciones tienen que ser archivos .sql planos y portables, capaces de
    correr tal cual con `supabase db push` el dia de la migracion. Alembic
    genera migraciones en Python acopladas a los modelos de SQLAlchemy, que
    Supabase no puede ejecutar. El runner se cambia en una tarde; un formato de
    migracion no portable se paga durante todo el proyecto.

GARANTIAS
    - idempotente: lo ya aplicado no se vuelve a aplicar
    - transaccional: cada archivo se aplica entero o no se aplica
    - detecta manipulacion: guarda el sha256 y falla si un archivo ya aplicado
      cambio en disco
    - no imprime jamas una contrasena
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
import sys
from pathlib import Path

import psycopg
from psycopg import sql

LOG = logging.getLogger("veritai.migrate")

SCHEMA_META = "veritai_meta"
TABLA_MIGRACIONES = "schema_migrations"

# Un nombre de rol valido en Postgres para nuestros fines. Se valida aunque
# despues se cite con Identifier: defensa en profundidad (START-HERE 23).
PATRON_ROL = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


def configurar_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
        stream=sys.stdout,
    )


def url_para_psycopg(url: str) -> str:
    """Quita el dialecto de SQLAlchemy para que psycopg acepte la URL.

    La aplicacion usa `postgresql+psycopg://...` porque SQLAlchemy necesita el
    driver explicito. psycopg quiere `postgresql://...`. Es la unica traduccion
    del proyecto y vive aqui, no dispersa.
    """
    return url.replace("postgresql+psycopg://", "postgresql://", 1)


def ocultar_credenciales(url: str) -> str:
    """Devuelve la URL sin contrasena, apta para logs."""
    return re.sub(r"://([^:/@]+):[^@]*@", r"://\1:***@", url)


def asegurar_tabla_de_control(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("create schema if not exists {}").format(sql.Identifier(SCHEMA_META))
        )
        cur.execute(
            sql.SQL(
                """
                create table if not exists {}.{} (
                    archivo      text        primary key,
                    sha256       text        not null,
                    aplicada_en  timestamptz not null default now()
                )
                """
            ).format(sql.Identifier(SCHEMA_META), sql.Identifier(TABLA_MIGRACIONES))
        )
    conn.commit()


def asegurar_rol_de_aplicacion(conn: psycopg.Connection) -> None:
    """Crea o actualiza el usuario con el que se conecta la API.

    La contrasena viene de una variable de entorno y se inserta como literal
    citado por psycopg. Nunca aparece en un archivo .sql versionado.
    """
    usuario = os.environ.get("VERITAI_APP_DB_USER", "").strip()
    password = os.environ.get("VERITAI_APP_DB_PASSWORD", "")

    if not usuario or not password:
        LOG.error("faltan VERITAI_APP_DB_USER o VERITAI_APP_DB_PASSWORD")
        raise SystemExit(2)

    if not PATRON_ROL.match(usuario):
        LOG.error("nombre de rol invalido: %r", usuario)
        raise SystemExit(2)

    ident = sql.Identifier(usuario)
    with conn.cursor() as cur:
        cur.execute("select 1 from pg_roles where rolname = %s", (usuario,))
        existe = cur.fetchone() is not None

        if existe:
            cur.execute(
                sql.SQL("alter role {} with login password {}").format(
                    ident, sql.Literal(password)
                )
            )
            LOG.info("rol de aplicacion '%s' actualizado", usuario)
        else:
            # Sin CREATEDB, sin CREATEROLE, sin SUPERUSER, sin BYPASSRLS.
            cur.execute(
                sql.SQL(
                    "create role {} with login nosuperuser nocreatedb "
                    "nocreaterole noinherit password {}"
                ).format(ident, sql.Literal(password))
            )
            LOG.info("rol de aplicacion '%s' creado", usuario)
    conn.commit()


def sha256_de(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def aplicadas(conn: psycopg.Connection) -> dict[str, str]:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("select archivo, sha256 from {}.{}").format(
                sql.Identifier(SCHEMA_META), sql.Identifier(TABLA_MIGRACIONES)
            )
        )
        return dict(cur.fetchall())


def aplicar(conn: psycopg.Connection, ruta: Path, digest: str) -> None:
    sentencias = ruta.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sentencias)
        cur.execute(
            sql.SQL("insert into {}.{} (archivo, sha256) values (%s, %s)").format(
                sql.Identifier(SCHEMA_META), sql.Identifier(TABLA_MIGRACIONES)
            ),
            (ruta.name, digest),
        )
    conn.commit()


def main() -> int:
    configurar_logging()

    parser = argparse.ArgumentParser(description="Aplica las migraciones SQL de VERITAI")
    parser.add_argument("--dir", required=True, help="carpeta con los archivos .sql")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="lista lo que se aplicaria sin tocar la base de datos",
    )
    args = parser.parse_args()

    url = os.environ.get("DATABASE_URL_MIGRATOR", "").strip()
    if not url:
        LOG.error("falta DATABASE_URL_MIGRATOR")
        return 2

    carpeta = Path(args.dir)
    if not carpeta.is_dir():
        LOG.error("la carpeta de migraciones no existe: %s", carpeta)
        return 2

    archivos = sorted(carpeta.glob("*.sql"))
    if not archivos:
        LOG.warning("no hay archivos .sql en %s", carpeta)
        return 0

    LOG.info("conectando a %s", ocultar_credenciales(url))

    with psycopg.connect(url_para_psycopg(url), connect_timeout=10) as conn:
        asegurar_tabla_de_control(conn)
        asegurar_rol_de_aplicacion(conn)

        ya = aplicadas(conn)
        pendientes: list[tuple[Path, str]] = []

        for ruta in archivos:
            digest = sha256_de(ruta)
            previo = ya.get(ruta.name)
            if previo is None:
                pendientes.append((ruta, digest))
            elif previo != digest:
                LOG.error(
                    "la migracion %s ya fue aplicada pero su contenido cambio. "
                    "Las migraciones son inmutables: crea una nueva en vez de "
                    "editar esta.",
                    ruta.name,
                )
                return 1

        if not pendientes:
            LOG.info("sin migraciones pendientes (%d ya aplicadas)", len(ya))
            return 0

        LOG.info("migraciones pendientes: %s", ", ".join(p.name for p, _ in pendientes))
        if args.dry_run:
            return 0

        for ruta, digest in pendientes:
            LOG.info("aplicando %s", ruta.name)
            aplicar(conn, ruta, digest)

        LOG.info("listo: %d migraciones aplicadas", len(pendientes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
