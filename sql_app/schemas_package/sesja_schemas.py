from typing import List, Optional

from pydantic import BaseModel

from sql_app.schemas_package.paczka_danych_schemas import PaczkaDanychSchematNested


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class SesjaBaseSchemat(PodstawowySchemat):
    nazwa_sesji: Optional[str] = None

    class Config:
        orm_mode = True


class SesjaCreateSchemat(SesjaBaseSchemat):
    pass


class SesjaSchemat(SesjaBaseSchemat):
    id: int
    urzadzenie_id: int = None
    uzytkownik_id: int = None
    czy_aktywna: Optional[bool] = None
    start_sesji: Optional[str] = None
    koniec_sesji: Optional[str] = None


class SesjaSchematNested(SesjaBaseSchemat):
    zbior_paczek_danych: List[PaczkaDanychSchematNested] = None
