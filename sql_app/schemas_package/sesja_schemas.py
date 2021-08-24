from typing import List, Optional

from pydantic import BaseModel

from sql_app.schemas_package.paczka_danych_schemas import PaczkaDanychSchema


class SesjaBaseSchema(BaseModel):
    czy_aktywna: Optional[bool] = None
    nazwa_sesji: Optional[str] = None
    start_sesji: Optional[str] = None
    koniec_sesji: Optional[str] = None
    dlugosc_trwania_w_s: Optional[str] = None


class SesjaCreateSchema(SesjaBaseSchema):
    pass


class SesjaSchema(SesjaBaseSchema):
    id: int
    zbior_paczek_danych: List[PaczkaDanychSchema]
    #urzadzenia_id: int
    #uzytkownika_id: int

    class Config:
        orm_mode = True
