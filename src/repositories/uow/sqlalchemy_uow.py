from src.database.helper import db_helper
from src.repositories.fields import FieldsRepository
from src.repositories.meteo_data import MeteoDataRepository
from src.repositories.uow.base import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        self.session_factory = db_helper.get_session_factory()

    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.fields = FieldsRepository(self.session)
        self.meteo_data = MeteoDataRepository(self.session)

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
