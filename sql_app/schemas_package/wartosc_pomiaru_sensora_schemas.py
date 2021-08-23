from typing import List, Optional
from pydantic import BaseModel


class WartoscPomiaruSensoraBase(BaseModel):
    wartosc: Optional[str] = None
    litery_porzadkowe: Optional[str] = None


class WartoscPomiaruSensoraCreate(WartoscPomiaruSensoraBase):
     pass


class WartoscPomiaruSensora(WartoscPomiaruSensoraBase):
    id: int
    #paczka_danych_id: int

    class Config:
        orm_mode = True
