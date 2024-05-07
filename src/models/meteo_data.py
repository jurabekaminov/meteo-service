from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class MeteoData(Base):
    __tablename__ = "meteo_data"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    temp: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    wind_speed: Mapped[float] = mapped_column(Float)
    sunrise: Mapped[datetime] = mapped_column(DateTime)
    sunset: Mapped[datetime] = mapped_column(DateTime)
