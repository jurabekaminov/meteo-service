from enum import Enum


class ScraperConstantsEnum(Enum):
    OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    FIELDS_SERVICE_URL = "http://fields-service:8002/api/v1/fields/meteo/all-coordinates"
    TIMEOUT = 60
    RETRY_ATTEMPTS = 3
    WAIT_BETWEEN_RETRIES_SEC = 5
