"""Configuracion de la aplicacion.

Toda la configuracion entra por variables de entorno. Nada de valores de
conexion, credenciales ni URLs escritos en el codigo (START-HERE 22 y 23).

PIEZA CLAVE PARA LA MIGRACION A SUPABASE
    La aplicacion conoce exactamente una forma de llegar a la base de datos:
    la cadena `DATABASE_URL`. No sabe si detras hay un contenedor local o un
    proyecto Supabase, y no debe saberlo. Migrar consiste en cambiar el valor
    de esa variable.

    Corolario, y es una regla del proyecto: queda prohibido importar el cliente
    `supabase-py` en el codigo de dominio. Hablar SQL mantiene la portabilidad;
    hablar PostgREST la destruye.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion leida del entorno del proceso."""

    model_config = SettingsConfigDict(
        env_file=None,          # el .env lo inyecta Docker Compose, no la app
        case_sensitive=False,
        extra="ignore",
    )

    # --- entorno -------------------------------------------------------------
    veritai_env: str = "local"
    log_level: str = "INFO"

    # --- base de datos -------------------------------------------------------
    # SecretStr evita que la cadena aparezca en repr(), logs o trazas de error.
    database_url: SecretStr
    db_pool_size: int = Field(default=5, ge=1, le=50)
    db_pool_max_overflow: int = Field(default=5, ge=0, le=50)
    db_use_pool: bool = True

    # --- http ----------------------------------------------------------------
    cors_allowed_origins: str = ""

    @field_validator("cors_allowed_origins")
    @classmethod
    def _rechazar_comodin(cls, valor: str) -> str:
        if "*" in valor:
            raise ValueError(
                "CORS_ALLOWED_ORIGINS no admite comodines: hay que listar los "
                "origenes de forma explicita (START-HERE 23)"
            )
        return valor

    @property
    def origenes_cors(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    @property
    def es_local(self) -> bool:
        return self.veritai_env == "local"


@lru_cache(maxsize=1)
def obtener_settings() -> Settings:
    """Instancia unica de configuracion, cacheada por proceso."""
    return Settings()  # type: ignore[call-arg]
