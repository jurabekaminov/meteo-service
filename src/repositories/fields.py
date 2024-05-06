from sqlalchemy.ext.asyncio import AsyncSession

from src.models.fields import Field
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class FieldsRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Field, session)
