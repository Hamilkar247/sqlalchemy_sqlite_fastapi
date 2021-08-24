from typing import List, Optional
from pydantic import BaseModel


class WartoscPomiaruSensoraBase(BaseModel):
    wartosc: Optional[str] = None
    litery_porzadkowe: Optional[str] = None
    paczka_danych_id: Optional[int]


class WartoscPomiaruSensoraCreate(WartoscPomiaruSensoraBase):
     pass


class WartoscPomiaruSensora(WartoscPomiaruSensoraBase):
    id: int
    #paczka_danych_id: Optional[int]

    class Config:
        orm_mode = True