from typing import Optional

from pydantic import BaseModel


class UzytkownikBase(BaseModel):
    hashed_password: Optional[str] = None
    uprawnienia: Optional[str] = None
    imie_nazwisko: Optional[str] = None
    email: Optional[str] = None
    stanowisko: Optional[str] = None
    opis: Optional[str] = None
    #id: int


class UzytkownikCreate(UzytkownikBase):
    pass


class Uzytkownik(UzytkownikBase):
    id: int
    #zbior_sesji: List[Sesja] = []
    #zbior_urzadzen: List[Urzadzenie] = []

    class Config:
        orm_mode = True