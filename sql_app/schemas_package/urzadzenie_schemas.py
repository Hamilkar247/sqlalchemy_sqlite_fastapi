from typing import Optional, List
from sql_app.schemas_package.sensor_schemas import SensorSchema
from sql_app.schemas_package.sesja_schemas import SesjaSchema
from sql_app.schemas_package.ogolne_schemas import CamelSchema


class UrzadzenieBaseSchema(CamelSchema):
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
