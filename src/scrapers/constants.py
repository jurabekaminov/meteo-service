from enum import Enum


class ScraperConstantsEnum(Enum):
    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
    FIELDS_SERVICE_URL = "http://fields-service:8002/api/v1/fields/meteo/all-coordinates"
    TIMEOUT = 60
    RETRY_ATTEMPTS = 3
    WAIT_BETWEEN_RETRIES_SEC = 5
