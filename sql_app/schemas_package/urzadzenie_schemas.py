from typing import Optional, List

from pydantic import BaseModel

from sql_app.schemas_package.sensor_schemas import SensorSchema


class UrzadzenieBaseSchema(BaseModel):
    nazwa_urzadzenia: Optional[str] = None
    numer_seryjny: Optional[str] = None


class UrzadzenieCreateSchema(UrzadzenieBaseSchema):
    pass


class UrzadzenieSchema(UrzadzenieBaseSchema):
    id: int
    #zbior_sesji: List[SesjaSchema]
    zbior_sensorow: List[SensorSchema]

    class Config:
        orm_mode = True
