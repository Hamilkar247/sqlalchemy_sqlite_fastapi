from typing import List, Optional

from pydantic import BaseModel

from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchema


#czas updatuj po prostu na aktualny czas
class PaczkaDanychUpdateSchema_czas_i_kod(BaseModel):
    kod_statusu: Optional[str] = None

    class Config:
        orm_mode = True


class PaczkaDanychBaseSchema(BaseModel):
    kod_statusu: Optional[str] = None
    numer_seryjny: Optional[str] = None

    class Config:
        orm_mode = True


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


class UrzadzeniePaczkiDanych(BaseModel):
    id: int
    numer_seryjny: str
    nazwa_urzadzenia: str
