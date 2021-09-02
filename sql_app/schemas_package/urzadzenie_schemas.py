from typing import Optional, List

from pydantic import BaseModel

from sql_app.schemas_package.sensor_schemas import SensorSchema
from sql_app.schemas_package.sesja_schemas import SesjaSchema


class UrzadzenieBaseSchema(BaseModel):
    nazwa_urzadzenia: Optional[str] = None
    numer_seryjny: Optional[str] = None


class UrzadzenieCreateSchema(UrzadzenieBaseSchema):
    pass


class UrzadzenieSchema(UrzadzenieBaseSchema):
    id: int
    #zbior_sensorow: List[SensorSchema] = None
    #zbior_sesji: List[SesjaSchema] = None

    class Config:
        orm_mode = True


class UrzadzenieSchemaNested(UrzadzenieBaseSchema):
    zbior_sensorow: List[SensorSchema] = None
    zbior_sesji: List[SesjaSchema] = None
