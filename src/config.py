import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    TITLE: str
    VERSION: str
    TZ: datetime.timezone = datetime.UTC
    
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env"
    )


settings = Settings()
