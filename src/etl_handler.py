import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings
from src.models.fields import Field
from src.repositories.uow.base import UnitOfWork  # noqa: TCH001
from src.repositories.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.schemas.meteo_data import MeteoDataCreateSchema, MeteoDataParseSchema
from src.scrapers.fields import FieldScraper
from src.scrapers.open_weather import OpenWeatherScraper

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
            temp=meteo_data.temp,
            humidity=meteo_data.humidity,
            wind_speed=meteo_data.wind_speed,
            sunrise=datetime.fromtimestamp(meteo_data.sunrise),  # noqa: DTZ006
            sunset=datetime.fromtimestamp(meteo_data.sunset),  # noqa: DTZ006
            date_time=datetime.fromtimestamp(meteo_data.date_time),  # noqa: DTZ006
        )

    async def __parse_meteo_data(
        self, fields: list[Field]
    ) -> list[MeteoDataParseSchema]:
        async with OpenWeatherScraper() as scraper:
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
