import logging

from pydantic import ValidationError

from src.schemas.meteo_data import MeteoDataParseSchema
from src.scrapers.base import AbstractScraper
from src.scrapers.config import scraper_settings
from src.scrapers.constants import ScraperConstantsEnum

logger = logging.getLogger(__name__)


class OpenWeatherScraper(AbstractScraper):
    BASE_URL: str = ScraperConstantsEnum.OPEN_WEATHER_URL.value

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    async def get_meteo_data(
        self, lat: float, lon: float
    ) -> MeteoDataParseSchema | None:
        response_json = await self._get(
            OpenWeatherScraper.BASE_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": scraper_settings.OPEN_WEATHER_API_KEY,
                "units": "metric",
            },
        )
        try:
            meteo_data = MeteoDataParseSchema(
                temp=response_json["main"]["temp"],
                humidity=response_json["main"]["humidity"],
                wind_speed=response_json["wind"]["speed"],
                sunrise=response_json["sys"]["sunrise"],
                sunset=response_json["sys"]["sunset"],
                date_time=response_json["dt"],
            )
        except (KeyError, TypeError, ValidationError):
            logger.debug("%s - couldn't parse meteo data.", (lat, lon))
            return None
        return meteo_data
