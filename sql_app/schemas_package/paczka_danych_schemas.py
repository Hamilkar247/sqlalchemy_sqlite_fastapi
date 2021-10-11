from typing import List, Optional
from pydantic import BaseModel

from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchemat, \
    WartoscPomiaruProstaSchemat


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class PaczkaDanychBaseSchemat(PodstawowySchemat):
    kod_statusu: Optional[str] = None
    numer_seryjny: Optional[str] = None


class PaczkaDanychProstaSchemat(PodstawowySchemat):
    pass


class PaczkaDanychCreateSchemat(PaczkaDanychBaseSchemat):
    pass


class PaczkaDanychUpdateSchemat(PaczkaDanychBaseSchemat):
    sesja_id: Optional[int] = None


#czas updatuj po prostu na aktualny czas
class PaczkaDanychUpdateSchemat_czas_i_kod(PodstawowySchemat):
    kod_statusu: Optional[str] = None


class PaczkaDanychUpdateSchematNested(PaczkaDanychUpdateSchemat):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchemat] = None


class PaczkaDanychSchemat(PaczkaDanychBaseSchemat):
    id: int
    sesja_id: Optional[int] = None
    czas_paczki: Optional[str] = None


class PaczkaDanychSchematNested(PaczkaDanychSchemat):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchemat]


class PaczkaDanychProstaNested(PaczkaDanychProstaSchemat):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruProstaSchemat]

    class Config(PaczkaDanychProstaSchemat.Config):
        fields = {"zbior_wartosci_pomiarow_sensorow": "ZbWart"}