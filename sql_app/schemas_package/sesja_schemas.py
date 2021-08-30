from typing import List, Optional

from pydantic import BaseModel

from sql_app.schemas_package.paczka_danych_schemas import PaczkaDanychSchema


class SesjaBaseSchema(BaseModel):
    nazwa_sesji: Optional[str] = None


class SesjaCreateSchema(SesjaBaseSchema):
    pass


class SesjaSchema(SesjaBaseSchema):
    id: int
    czy_aktywna: Optional[bool] = None
    start_sesji: Optional[str] = None
    koniec_sesji: Optional[str] = None
    dlugosc_trwania_w_s: Optional[str] = None
    zbior_paczek_danych: List[PaczkaDanychSchema] = None
    urzadzenia_id: int = None
    uzytkownik_id: int = None

    class Config:
        orm_mode = True
