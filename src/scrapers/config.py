from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    OPEN_WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


scraper_settings = ScraperSettings()
