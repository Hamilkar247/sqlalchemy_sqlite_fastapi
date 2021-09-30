from typing import List, Optional

from sql_app.schemas_package.ogolne_schemas import CamelSchema


class SensorBaseSchema(CamelSchema):
    litery_porzadkowe: Optional[str] = None
    parametr: Optional[str] = None
    wspolczynniki_kalibracyjne: Optional[str] = "0;1"
    min: Optional[str] = None
    max: Optional[str] = None
    jednostka: Optional[str] = None
    status_sensora: Optional[str] = None


class SensorCreateSchema(SensorBaseSchema):
    pass


class SensorUpdateSchema(SensorBaseSchema):
    urzadzenie_id: Optional[int] = None


class SensorSchema(SensorBaseSchema):
    id: int
    urzadzenie_id: Optional[int] = None

    class Config:
        orm_mode = True
