from typing import Optional, List

from pydantic import BaseModel

from sql_app.schemas_package.sensor_schemas import SensorSchema
from sql_app.schemas_package.sesja_schemas import SesjaSchema


class UrzadzenieBaseSchema(BaseModel):
    nazwa_urzadzenia: Optional[str] = None
    numer_seryjny: Optional[str] = None

    class Config:
        orm_mode = True


class UrzadzenieSchema(UrzadzenieBaseSchema):
    id: int


class UrzadzenieUpdateSchema(UrzadzenieBaseSchema):
    pass


class UrzadzenieSchema_ZagniezdzoneZbiory(UrzadzenieSchema):
    zbior_sensorow: List[SensorSchema] = None
    zbior_sesji: List[SesjaSchema] = None


class UrzadzenieSchema_ZagniezdzoneSensory(UrzadzenieSchema):
    zbior_sensorow: List[SensorSchema] = None


class UrzadzenieSchema_ZagniezdzoneSesje(UrzadzenieSchema):
    zbior_sesji: List[SesjaSchema] = None
