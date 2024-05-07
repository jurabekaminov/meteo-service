from src.schemas.fields import FieldSchema
from src.scrapers.base import AbstractScraper
from src.scrapers.constants import ScraperConstantsEnum


class FieldScraper(AbstractScraper):
    BASE_URL = ScraperConstantsEnum.FIELDS_SERVICE_URL.value

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}
    
    async def get_all_fields(self) -> list[FieldSchema]:
        response_json = await self._get(FieldScraper.BASE_URL)
        return [FieldSchema.model_validate(field) for field in response_json]
