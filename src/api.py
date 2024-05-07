from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.meteo_data import MeteoDataPreviewSchema, MeteoDataReadSchema
from src.service import MeteoDataService

router = APIRouter(prefix="/api/meteo", tags=["meteo data"])


@router.get("/{field_id}", response_model=MeteoDataReadSchema)
async def get_current_meteo_data(
    field_id: int, service: Annotated[MeteoDataService, Depends()]
):
    return await service.get_current_meteo_data(field_id)


@router.get("/preview/{field_id}", response_model=MeteoDataPreviewSchema)
async def get_current_meteo_data_preview(
    field_id: int, service: Annotated[MeteoDataService, Depends()]
):
    return await service.get_current_meteo_data_preview(field_id)
