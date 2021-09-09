from typing import List, Optional

from pydantic import BaseModel


class SensorBaseSchema(BaseModel):
    litery_porzadkowe: Optional[str] = None
    parametr: Optional[str] = None
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
    #zbior_wspolczynikow_kalibracyjnych: List[WspolczynikKalibracyjnySchema]

    class Config:
        orm_mode = True
