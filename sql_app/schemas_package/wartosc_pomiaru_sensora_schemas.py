from typing import Optional
from pydantic import BaseModel


class WartoscPomiaruSensoraBaseSchema(BaseModel):
    wartosc: Optional[str] = None
    litery_porzadkowe: Optional[str] = None


class WartoscPomiaruSensoraCreateSchema(WartoscPomiaruSensoraBaseSchema):
     pass


class WartoscPomiaruProstaSchema(WartoscPomiaruSensoraBaseSchema):
    class Config(WartoscPomiaruSensoraBaseSchema.Config):
        fields = {
            "wartosc": "w",
            "litery_porzadkowe": "l"
        }


class WartoscPomiaruSensoraSchema(WartoscPomiaruSensoraBaseSchema):
    id: int
    paczka_danych_id: Optional[int] = None




