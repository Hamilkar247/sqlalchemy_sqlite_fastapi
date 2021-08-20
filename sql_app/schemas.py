from typing import List, Optional

from pydantic import BaseModel

from sql_app.models import Sesja, Urzadzenie, PaczkaDanych, WartoscPomiaruSensora, Sensor


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class UzytkownikBase(BaseModel):
    imie_nazwisko: str
    email: str
    stanowisko: str
    opis: str


class UzytkownikCreate(UzytkownikBase):
    password: str
    uprawnienia: str


class Uzytkownik(UzytkownikBase):
    id: int
    zbior_sesji: List[Sesja] = []
    zbior_urzadzen: List[Urzadzenie] = []

    class Config:
        orm_mode = True


class SesjaBase(BaseModel):
    nazwa_sesji: str
    start_sesji: str
    koniec_sesji: str
    dlugosc_trwania_w_s: str


class SesjaCreate(SesjaBase):
    pass


class Sesja(SesjaBase):
    id: int
    czy_aktywna: bool
    start_sesji: str
    koniec_sesji: str
    dlugosc_trwania_w_s: str
    zbior_paczek_danych: List[PaczkaDanych] = []
    urzadzenia_id: int
    uzytkownika_id: int

    class Config:
        orm_mode = True


class PaczkaDanychBase(BaseModel):
    kod_statusu: str
    numer_seryjny: str
    czas_paczki: str


class PaczkaDanychCreate(PaczkaDanychBase):
    pass


class PaczkaDanych(PaczkaDanychBase):
    id: int
    zbior_wartosci_pomiarow_sensorow: List[WartoscPomiaruSensora] = []
    wartosci_pomiaru_sensorow_id: str

    class Config:
        orm_mode = True


class WartoscPomiaruSensoraBase(BaseModel):
    wartosc: str
    litery_porzadkowe: str


class WartoscPomiaruSensoraCreate(WartoscPomiaruSensoraBase):
     pass


class WartoscPomiaruSensora(WartoscPomiaruSensoraBase):
    id: int
    paczka_danych_id: int

    class Config:
        orm_mode = True


class UrzadzenieBase(BaseModel):
    nazwa_urzadzenia: str
    numer_seryjny: str


class UrzadzeniaCreate(UrzadzenieBase):
    pass


class Urzadzenia(UrzadzenieBase):
    id: int
    zbior_sesji: List[Sesja] = []
    zbior_sensorow: List[Sensor] = []

    class Config:
        orm_mode = True


class SensorBase(BaseModel):
    litery_porzadkowe: str
    parametr: str
    kalibr_wspolczynnika: str
    min: int
    max: int
    jednostka: str
    status_sensora: str


class SensorCreate(SensorBase):
    pass


class Sensor(SensorBase):
    id: int
    urzadzenie_id: int

    class Config:
        orm_mode = True


