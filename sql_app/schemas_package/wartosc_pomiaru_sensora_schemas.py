from typing import List, Optional
from pydantic import BaseModel


class WartoscPomiaruSensoraBaseSchema(BaseModel):
    wartosc: Optional[str] = None
    litery_porzadkowe: Optional[str] = None
    paczka_danych_id: Optional[int] = None


class WartoscPomiaruSensoraCreateSchema(WartoscPomiaruSensoraBaseSchema):
     pass


class WartoscPomiaruSensoraSchema(WartoscPomiaruSensoraBaseSchema):
    id: int

    class Config:
        orm_mode = True
