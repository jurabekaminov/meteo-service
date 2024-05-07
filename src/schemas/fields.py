from pydantic import BaseModel


class FieldSchema(BaseModel):
    id: int
    longitude: float
    latitude: float
    parse_meteo: bool = True
