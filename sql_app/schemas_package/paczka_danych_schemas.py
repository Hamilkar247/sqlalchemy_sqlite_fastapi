from typing import List

from pydantic import BaseModel

from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchema


class PaczkaDanychBaseSchema(BaseModel):
    kod_statusu: str
    numer_seryjny: str
    czas_paczki: str


class PaczkaDanychCreateSchema(PaczkaDanychBaseSchema):
    pass


class PaczkaDanychSchema(PaczkaDanychBaseSchema):
    id: int
    #wartosci_pomiaru_sensorow_id: str
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchema]

    class Config:
        orm_mode = True
