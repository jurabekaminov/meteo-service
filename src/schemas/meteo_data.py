from datetime import datetime

from pydantic import BaseModel


class MeteoDataParseSchema(BaseModel):
    date_time: int
    
    temperature: float | None
    humidity: float | None
    wind_speed: float | None
    precipitation: float | None
    dew_point: float | None
    soil_temperature_0cm: float | None
    soil_temperature_6cm: float | None
    soil_temperature_18cm: float | None
    soil_moisture_0_to_1cm: float | None
    soil_moisture_1_to_3cm: float | None
    soil_moisture_3_to_9cm: float | None
    soil_moisture_9_to_27cm: float | None
    
    temperature_max: float | None
    temperature_min: float | None
    sunrise: int | None
    sunset: int | None
    precipitation_sum: float | None
    
    

class MeteoDataCreateSchema(BaseModel):
    field_id: int
    date_time: datetime
    
    temperature: float | None
    humidity: float | None
    wind_speed: float | None
    precipitation: float | None
    dew_point: float | None
    soil_temperature_0cm: float | None
    soil_temperature_6cm: float | None
    soil_temperature_18cm: float | None
    soil_moisture_0_to_1cm: float | None
    soil_moisture_1_to_3cm: float | None
    soil_moisture_3_to_9cm: float | None
    soil_moisture_9_to_27cm: float | None
    
    temperature_max: float | None
    temperature_min: float | None
    sunrise: datetime | None
    sunset: datetime | None
    precipitation_sum: float | None

class MeteoDataReadSchema(MeteoDataCreateSchema):
    id: int
