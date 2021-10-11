from typing import Optional, List

from pydantic import BaseModel

from sql_app.schemas_package.sensor_schemas import SensorSchemat
from sql_app.schemas_package.sesja_schemas import SesjaSchemat


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class UrzadzenieBaseSchemat(PodstawowySchemat):
    nazwa_urzadzenia: Optional[str] = None
    numer_seryjny: Optional[str] = None

    class Config:
        orm_mode = True


class UrzadzenieSchemat(UrzadzenieBaseSchemat):
    id: int


class UrzadzenieUpdateSchemat(UrzadzenieBaseSchemat):
    pass


class UrzadzenieSchemat_ZagniezdzoneZbiory(UrzadzenieSchemat):
    zbior_sensorow: List[SensorSchemat] = None
    zbior_sesji: List[SesjaSchemat] = None


class UrzadzenieSchemat_ZagniezdzoneSensory(UrzadzenieSchemat):
    zbior_sensorow: List[SensorSchemat] = None


class UrzadzenieSchemat_ZagniezdzoneSesje(UrzadzenieSchemat):
    zbior_sesji: List[SesjaSchemat] = None
