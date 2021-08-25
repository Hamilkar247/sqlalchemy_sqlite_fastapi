from typing import Optional, List

from pydantic import BaseModel

from sql_app.schemas_package.sesja_schemas import SesjaSchema


class UzytkownikBaseSchema(BaseModel):
    hashed_password: Optional[str] = None
    uprawnienia: Optional[str] = None
    imie_nazwisko: Optional[str] = None
    email: Optional[str] = None
    stanowisko: Optional[str] = None
    opis: Optional[str] = None
    #id: int


class UzytkownikCreateSchema(UzytkownikBaseSchema):
    pass


class UzytkownikSchema(UzytkownikBaseSchema):
    id: int
    zbior_sesji: List[SesjaSchema]
    #zbior_urzadzen: List[Urzadzenie] = []

    class Config:
        orm_mode = True