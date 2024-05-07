import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings
from src.models.fields import Field
from src.repositories.uow.base import UnitOfWork  # noqa: TCH001
from src.repositories.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.schemas.meteo_data import MeteoDataCreateSchema, MeteoDataParseSchema
from src.scrapers.fields import FieldScraper
from src.scrapers.open_meteo import OpenMeteoScraper

logger = logging.getLogger(__name__)


class ETLHandler:
    def __init__(self):
        self.__scheduler = AsyncIOScheduler(timezone=settings.TZ)
        self.__uow: UnitOfWork = SQLAlchemyUnitOfWork()

    def get_scheduler(self) -> AsyncIOScheduler:
        self.__scheduler.add_job(
            func=self.meteo_data_etl_job,
            trigger="cron",
            hour=5,
            minute=0,
        )
        self.__scheduler.add_job(
            func=self.meteo_data_etl_job,
            trigger="cron",
            hour=9,
            minute=0,
        )
        self.__scheduler.add_job(
            func=self.meteo_data_etl_job,
            trigger="cron",
            hour=13,
            minute=0,
        )
        self.__scheduler.add_job(
            func=self.meteo_data_etl_job,
            trigger="cron",
            hour=18,
            minute=0,
        )
        return self.__scheduler

    async def __fields_etl_job(self) -> None:
        logger.info("Fields etl job started.")
        async with FieldScraper() as scraper:
            fields = await scraper.get_all_fields()  # parse fields
        async with self.__uow:
            for field in fields:
                await self.__uow.fields.upsert(  # upsert fields data
                    data_on_insert=field.model_dump(),
                    data_on_update={
                        "longitude": field.longitude,
                        "latitude": field.latitude,
                        "parse_meteo": field.parse_meteo,
                    },
                    index_elements=["id"],
                )
            await self.__uow.commit()
        logger.info("Fields etl job completed.")

    @staticmethod
    def __prepare_meteo_data(
        field_id: int, meteo_data: MeteoDataParseSchema
    ) -> MeteoDataCreateSchema:
        return MeteoDataCreateSchema(
            field_id=field_id,
            date_time=datetime.fromtimestamp(meteo_data.date_time) + timedelta(hours=3),  # noqa: DTZ006
            temperature=meteo_data.temperature,
            humidity=meteo_data.humidity,
            wind_speed=meteo_data.wind_speed,
            precipitation=meteo_data.precipitation,
            dew_point=meteo_data.dew_point,
            soil_temperature_0cm=meteo_data.soil_temperature_0cm,
            soil_temperature_6cm=meteo_data.soil_temperature_6cm,
            soil_temperature_18cm=meteo_data.soil_temperature_18cm,
            soil_moisture_0_to_1cm=meteo_data.soil_moisture_0_to_1cm,
            soil_moisture_1_to_3cm=meteo_data.soil_moisture_1_to_3cm,
            soil_moisture_3_to_9cm=meteo_data.soil_moisture_3_to_9cm,
            soil_moisture_9_to_27cm=meteo_data.soil_moisture_9_to_27cm,
            temperature_max=meteo_data.temperature_max,
            temperature_min=meteo_data.temperature_min,
            sunrise=datetime.fromtimestamp(meteo_data.sunrise) + timedelta(hours=3),  # noqa: DTZ006
            sunset=datetime.fromtimestamp(meteo_data.sunset) + timedelta(hours=3),  # noqa: DTZ006
            precipitation_sum=meteo_data.precipitation_sum,
        )

    async def __parse_meteo_data(
        self, fields: list[Field]
    ) -> list[MeteoDataParseSchema]:
        async with OpenMeteoScraper() as scraper:
            tasks = [
                scraper.get_meteo_data(lat=field.latitude, lon=field.longitude)
                for field in fields
            ]
            meteo_data = await asyncio.gather(*tasks)
            return meteo_data

    async def meteo_data_etl_job(self) -> None:
        logger.info("Meteo data etl job started.")
        async with self.__uow:
            await self.__fields_etl_job()  # upsert fields data
            fields = await self.__uow.fields.read_many(parse_meteo=True)
            parsed_meteo_data = await self.__parse_meteo_data(fields)
            for field, meteo_data in zip(fields, parsed_meteo_data):
                if not meteo_data:
                    continue
                prepared_meteo_data = self.__prepare_meteo_data(field.id, meteo_data)
                await self.__uow.meteo_data.create(prepared_meteo_data.model_dump())
                await self.__uow.commit()
            logger.info("Meteo data etl job completed.")


etl_handler = ETLHandler()
