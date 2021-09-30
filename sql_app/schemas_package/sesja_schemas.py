from typing import List, Optional

from sql_app.schemas_package.ogolne_schemas import CamelSchema
from sql_app.schemas_package.paczka_danych_schemas import PaczkaDanychSchemaNested


class SesjaBaseSchema(CamelSchema):
    nazwa_sesji: Optional[str] = None

    class Config:
        orm_mode = True


class SesjaCreateSchema(SesjaBaseSchema):
    pass


class SesjaSchema(SesjaBaseSchema):
    id: int
    urzadzenie_id: int = None
    uzytkownik_id: int = None
    czy_aktywna: Optional[bool] = None
    start_sesji: Optional[str] = None
    koniec_sesji: Optional[str] = None


class SesjaSchemaNested(SesjaBaseSchema):
    zbior_paczek_danych: List[PaczkaDanychSchemaNested] = None
