from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).parent.parent.joinpath(".env"),
            Path(__file__).parent.parent.joinpath(".env.dev"),
        )
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LOG_FILE = self.full_path(self.LOG_FILE)

    @staticmethod
    def full_path(*relative) -> str:
        return str(Path("src", *relative).absolute())

    MODE: Literal["PROD", "DEV", "TEST"]
    LOG_LEVEL: str
    LOG_FILE: str

    API_HOST: str
    API_PORT: int

    JWT_ACCESS_KEY: SecretStr
    JWT_REFRESH_KEY: SecretStr
    JWT_ACCESS_TTL_MIN: int
    JWT_REFRESH_TTL_MIN: int
    JWT_ALGORITHM: str

    PSQL_HOST: str
    PSQL_PORT: int
    PSQL_DB: str
    PSQL_USER: str
    PSQL_PASSWORD: str
    PSQL_URI: str

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_URI: str

    OPENAI_KEY: str
    OPENAI_MODEL: str
    OPENAI_SWEAR_CHECKER_PROMPT: str
    OPENAI_REPLY_GEN_PROMPT: str

    SENTRY_DSN: str
    SENTRY_RATE: float

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str


config = Config()
