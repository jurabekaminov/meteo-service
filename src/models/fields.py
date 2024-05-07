from sqlalchemy import Boolean, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Field(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)
    parse_meteo: Mapped[bool] = mapped_column(Boolean)
