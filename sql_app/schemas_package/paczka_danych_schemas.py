from pydantic import BaseModel


class PaczkaDanychBase(BaseModel):
    kod_statusu: str
    numer_seryjny: str
    czas_paczki: str


class PaczkaDanychCreate(PaczkaDanychBase):
    pass


class PaczkaDanych(PaczkaDanychBase):
    id: int
    #zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensora] = []
    #wartosci_pomiaru_sensorow_id: str

    class Config:
        orm_mode = True