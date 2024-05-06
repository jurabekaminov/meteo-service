from pydantic import BaseModel


class FieldSchema(BaseModel):
    id: int
    longtitude: float
    latitude: float
    parse_meteo: bool
