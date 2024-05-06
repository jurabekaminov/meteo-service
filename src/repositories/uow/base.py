from abc import ABC, abstractmethod
from typing import Type

from src.repositories.fields import FieldsRepository
from src.repositories.meteo_data import MeteoDataRepository


class UnitOfWork(ABC):
    fields: Type[FieldsRepository]
    meteo_data: Type[MeteoDataRepository]
    
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
