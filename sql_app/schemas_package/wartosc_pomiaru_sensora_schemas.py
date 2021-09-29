from typing import List, Optional
from pydantic import BaseModel


def to_camel(string):
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class WartoscPomiaruSensoraBaseSchema(CamelModel):
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




