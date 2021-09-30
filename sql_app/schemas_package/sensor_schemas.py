from typing import List, Optional
from pydantic import BaseModel


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class SensorBaseSchemat(BaseModel):
    litery_porzadkowe: Optional[str] = None
    parametr: Optional[str] = None
    wspolczynniki_kalibracyjne: Optional[str] = "0;1"
    min: Optional[str] = None
    max: Optional[str] = None
    jednostka: Optional[str] = None
    status_sensora: Optional[str] = None


class SensorCreateSchemat(SensorBaseSchemat):
    pass


class SensorUpdateSchemat(SensorBaseSchemat):
    urzadzenie_id: Optional[int] = None


class SensorSchemat(SensorBaseSchemat):
    id: int
    urzadzenie_id: Optional[int] = None
