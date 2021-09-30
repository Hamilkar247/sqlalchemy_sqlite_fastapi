from typing import List, Optional

from pydantic import BaseModel, Field

from sql_app.schemas_package.ogolne_schemas import CamelSchema
from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchema, \
    WartoscPomiaruProstaSchema


#czas updatuj po prostu na aktualny czas
class PaczkaDanychUpdateSchema_czas_i_kod(CamelSchema):
    kod_statusu: Optional[str] = None


class PaczkaDanychBaseSchema(CamelSchema):
    kod_statusu: Optional[str] = None
    numer_seryjny: Optional[str] = None


class PaczkaDanychProsta(CamelSchema):
    pass


class PaczkaDanychCreateSchema(PaczkaDanychBaseSchema):
    pass


class PaczkaDanychUpdateSchema(PaczkaDanychBaseSchema):
    sesja_id: Optional[int] = None


class PaczkaDanychUpdateSchemaNested(PaczkaDanychUpdateSchema):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchema] = None


class PaczkaDanychSchema(PaczkaDanychBaseSchema):
    id: int
    sesja_id: Optional[int] = None
    czas_paczki: Optional[str] = None


class PaczkaDanychSchemaNested(PaczkaDanychSchema):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchema]


class PaczkaDanychProstaNested(PaczkaDanychProsta):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruProstaSchema]

    class Config(PaczkaDanychProsta.Config):
        fields = {"zbior_wartosci_pomiarow_sensorow": "ZbWart"}