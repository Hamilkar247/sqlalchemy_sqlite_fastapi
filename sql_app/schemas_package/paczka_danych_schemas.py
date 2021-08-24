from typing import List

from pydantic import BaseModel

from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensora


class PaczkaDanychBase(BaseModel):
    kod_statusu: str
    numer_seryjny: str
    czas_paczki: str


class PaczkaDanychCreate(PaczkaDanychBase):
    pass


class PaczkaDanych(PaczkaDanychBase):
    id: int
    #wartosci_pomiaru_sensorow_id: str
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensora]

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True
        #arbitrary_types_allowed = True