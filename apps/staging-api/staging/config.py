
from pydantic_settings import BaseSettings
from typing import List
import os


class BaseConfig(BaseSettings):
    PROJECT_NAME: str = "staging-backend"
    ENV: str = "dev"
    DEBUG: bool = False

    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    ALLOWED_ORIGINS_RAW: str = ""

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS_RAW.split(",")
            if origin.strip()
        ]


class DevConfig(BaseConfig):
    DEBUG: bool = True
    ENV: str = "dev"
    # Redis (used for rate limiting, if we decide to)
    # REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/the_project_db"
    class Config:
        env_file = ".env"


class ProdConfig(BaseConfig):
    DEBUG: bool = False
    ENV: str = "prod"


def get_settings():
    env = os.getenv("STAGING_ENV", "dev")
    if env == "prod":
        return ProdConfig()
    return DevConfig()


settings = get_settings()