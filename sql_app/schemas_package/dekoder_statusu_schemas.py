from typing import Optional

from pydantic import BaseModel


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class DekoderStatusuBaseSchemat(PodstawowySchemat):
    kod: Optional[str]
    liczba_dziesietna: Optional[int]
    opis_kodu: Optional[str]


class DekoderStatusuCreateSchemat(DekoderStatusuBaseSchemat):
    pass


class DekoderStatusuSchemat(DekoderStatusuBaseSchemat):
    id: int

    class Config:
        orm_mode = True
