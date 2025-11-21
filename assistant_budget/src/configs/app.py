from dynaconf import Dynaconf
from pydantic import BaseModel


# -----------------------------
# APP settings
# -----------------------------
class APPConfig(BaseModel):
    app_version: str
    app_name: str
    app_host: str
    app_port: int
    debug: bool = False


# -----------------------------
# DATABASE settings
# -----------------------------
class DBConfig(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    @property
    def dsl(self) -> str:
        """SQLAlchemy async DSN"""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


# -----------------------------
# GENERAL SETTINGS ENVELOPE
# -----------------------------
class Settings(BaseModel):
    app: APPConfig
    db: DBConfig


# -----------------------------
# Load from settings.toml using Dynaconf
# -----------------------------
env_settings = Dynaconf(settings_file=["settings.toml"])

settings = Settings(
    app=env_settings["app_settings"],
    db=env_settings["db_settings"]
)