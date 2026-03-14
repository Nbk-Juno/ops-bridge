from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env", extra="ignore"
    )

    database_url: str
    rabbitmq_url: str
    secret_key: str


settings = Settings()  # type: ignore
