from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.repositories.uow.base import UnitOfWork
from src.repositories.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.schemas.meteo_data import MeteoDataPreviewSchema, MeteoDataReadSchema


class MeteoDataService:
    def __init__(self, uow: Annotated[UnitOfWork, Depends(SQLAlchemyUnitOfWork)]):
        self.__uow = uow

    async def get_current_meteo_data(self, field_id: int) -> MeteoDataReadSchema:
        async with self.__uow:
            res = await self.__uow.meteo_data.read_last(field_id=field_id)
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Meteo data for field with id {field_id} not found.",
                )
            return MeteoDataReadSchema.model_validate(res, from_attributes=True)

    async def get_current_meteo_data_preview(
        self, field_id: int
    ) -> MeteoDataPreviewSchema:
        async with self.__uow:
            res = await self.__uow.meteo_data.read_last(field_id=field_id)
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Meteo data for field with id {field_id} not found.",
                )
            return MeteoDataPreviewSchema.model_validate(res, from_attributes=True)
