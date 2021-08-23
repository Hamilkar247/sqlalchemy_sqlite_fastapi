from typing import List, Optional

from pydantic import BaseModel


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






#
#

#
#
#class WartoscPomiaruSensoraBase(BaseModel):
#    wartosc: str
#    litery_porzadkowe: str
#
#
#class WartoscPomiaruSensoraCreate(WartoscPomiaruSensoraBase):
#     pass
#
#
#class WartoscPomiaruSensora(WartoscPomiaruSensoraBase):
#    id: int
#    paczka_danych_id: int
#
#    class Config:
#        orm_mode = True
#
#
#class UrzadzenieBase(BaseModel):
#    nazwa_urzadzenia: str
#    numer_seryjny: str
#
#
#class UrzadzeniaCreate(UrzadzenieBase):
#    pass
#
#
#class Urzadzenia(UrzadzenieBase):
#    id: int
#    zbior_sesji: List[Sesja] = []
#    zbior_sensorow: List[Sensor] = []
#
#    class Config:
#        orm_mode = True
#
#
#class SensorBase(BaseModel):
#    litery_porzadkowe: str
#    parametr: str
#    kalibr_wspolczynnika: str
#    min: int
#    max: int
#    jednostka: str
#    status_sensora: str
#
#
#class SensorCreate(SensorBase):
#    pass
#
#
#class Sensor(SensorBase):
#    id: int
#    urzadzenie_id: int
#
#    class Config:
#        orm_mode = True


