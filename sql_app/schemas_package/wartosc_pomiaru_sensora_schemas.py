from typing import Optional
from pydantic import BaseModel


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class WartoscPomiaruSensoraBaseSchemat(PodstawowySchemat):
    wartosc: Optional[str] = None
    litery_porzadkowe: Optional[str] = None


class WartoscPomiaruSensoraCreateSchemat(WartoscPomiaruSensoraBaseSchemat):
     pass


class WartoscPomiaruProstaSchemat(WartoscPomiaruSensoraBaseSchemat):
    class Config(WartoscPomiaruSensoraBaseSchemat.Config):
        fields = {
            "wartosc": "w",
            "litery_porzadkowe": "l"
        }


class WartoscPomiaruSensoraSchemat(WartoscPomiaruSensoraBaseSchemat):
    id: int
    paczka_danych_id: Optional[int] = None




