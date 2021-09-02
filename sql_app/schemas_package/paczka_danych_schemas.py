from typing import List, Optional

from pydantic import BaseModel

from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchema


class PaczkaDanychBaseSchema(BaseModel):
    kod_statusu: Optional[str] = None
    numer_seryjny: Optional[str] = None
    czas_paczki: Optional[str] = None


class PaczkaDanychCreateSchema(PaczkaDanychBaseSchema):
    pass


class PaczkaDanychSchema(PaczkaDanychBaseSchema):
    id: int
    #wartosci_pomiaru_sensorow_id: str
    sesja_id: Optional[str] = None
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchema]

    class Config:
        orm_mode = True


class PaczkaDanychSchemaNested(PaczkaDanychSchema):
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensoraSchema]


class UrzadzeniePaczkiDanych(BaseModel):
    id: int
    numer_seryjny: str
    nazwa_urzadzenia: str

    class Config:
        orm_mode = True

