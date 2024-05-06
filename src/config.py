import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    TITLE: str
    VERSION: str
    TZ: datetime.timezone = datetime.timezone(
        datetime.timedelta(hours=3), "Europe/Moscow"
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )


settings = Settings()
