from typing import List, Optional

from pydantic import BaseModel


class SensorBaseSchema(BaseModel):
    litery_porzadkowe: Optional[str] = None
    parametr: Optional[str] = None
    min: Optional[str] = None
    max: Optional[str] = None
    jednostka = Optional[str]
    status_sensora = Optional[str]


class SensorCreateSchema(SensorBaseSchema):
    pass


class SensorSchema(SensorBaseSchema):
    id: int

    class Config:
        orm_mode = True
