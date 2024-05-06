from sqlalchemy.ext.asyncio import AsyncSession

from src.models.meteo_data import MeteoData
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class MeteoDataRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MeteoData, session)
