from typing import Optional, List
from pydantic import BaseModel
from sql_app.schemas_package.sesja_schemas import SesjaSchemat


class PodstawowySchemat(BaseModel):
    class Config:
        #alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class UzytkownikBaseSchemat(PodstawowySchemat):
    hashed_password: Optional[str] = None
    uprawnienia: Optional[str] = None
    imie_nazwisko: Optional[str] = None
    email: Optional[str] = None
    stanowisko: Optional[str] = None
    opis: Optional[str] = None


class UzytkownikCreateSchemat(UzytkownikBaseSchemat):
    pass


class UzytkownikSchemat(UzytkownikBaseSchemat):
    id: int


class UzytkownikSchematNested(UzytkownikSchemat):
    zbior_sesji: List[SesjaSchemat]
