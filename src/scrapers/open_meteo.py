import logging

from pydantic import ValidationError

from src.schemas.meteo_data import MeteoDataParseSchema
from src.scrapers.base import AbstractScraper
from src.scrapers.constants import ScraperConstantsEnum

logger = logging.getLogger(__name__)


class OpenMeteoScraper(AbstractScraper):
    BASE_URL: str = ScraperConstantsEnum.OPEN_METEO_URL.value

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    async def get_meteo_data(
        self, lat: float, lon: float
    ) -> MeteoDataParseSchema | None:
        response_json = await self._get(
            OpenMeteoScraper.BASE_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",  # noqa: E501
                "hourly": "dew_point_2m,soil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm",  # noqa: E501
                "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum",  # noqa: E501
                "wind_speed_unit": "ms",
                "timezone": "Europe%2FMoscow",
                "forecast_days": 1,
                "forecast_hours": 1,
                "timeformat": "unixtime",
            },
        )
        try:
            meteo_data = MeteoDataParseSchema(
                date_time=response_json["current"]["time"],
                temperature=response_json["current"]["temperature_2m"],
                humidity=response_json["current"]["relative_humidity_2m"],
                wind_speed=response_json["current"]["wind_speed_10m"],
                precipitation=response_json["current"]["precipitation"],
                dew_point=response_json["hourly"]["dew_point_2m"][0],
                soil_temperature_0cm=response_json["hourly"]["soil_temperature_0cm"][0],
                soil_temperature_6cm=response_json["hourly"]["soil_temperature_6cm"][0],
                soil_temperature_18cm=response_json["hourly"]["soil_temperature_18cm"][0],
                soil_moisture_0_to_1cm=response_json["hourly"]["soil_moisture_0_to_1cm"][0],
                soil_moisture_1_to_3cm=response_json["hourly"]["soil_moisture_1_to_3cm"][0],
                soil_moisture_3_to_9cm=response_json["hourly"]["soil_moisture_3_to_9cm"][0],
                soil_moisture_9_to_27cm=response_json["hourly"]["soil_moisture_9_to_27cm"][0],
                temperature_max=response_json["daily"]["temperature_2m_max"][0],
                temperature_min=response_json["daily"]["temperature_2m_min"][0],
                sunrise=response_json["daily"]["sunrise"][0],
                sunset=response_json["daily"]["sunset"][0],
                precipitation_sum=response_json["daily"]["precipitation_sum"][0],
            )
        except (KeyError, TypeError, ValidationError):
            logger.debug("%s - couldn't parse meteo data.", (lat, lon))
            return None
        return meteo_data
