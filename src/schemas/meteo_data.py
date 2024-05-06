from datetime import datetime

from pydantic import BaseModel


class MeteoDataParseSchema(BaseModel):
    temp: float
    humidity: float
    wind_speed: float
    sunrise: int
    sunset: int
    date_time: int
    

class MeteoDataCreateSchema(BaseModel):
    field_id: int
    temp: float
    humidity: float
    wind_speed: float
    sunrise: datetime
    sunset: datetime
    date_time: datetime

class MeteoDataReadSchema(MeteoDataCreateSchema):
    id: int
