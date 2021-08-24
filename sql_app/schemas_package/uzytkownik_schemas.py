from typing import Optional

from pydantic import BaseModel


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


class Uzytkownik(UzytkownikBaseSchema):
    id: int
    #zbior_sesji: List[Sesja] = []
    #zbior_urzadzen: List[Urzadzenie] = []

    class Config:
        orm_mode = True