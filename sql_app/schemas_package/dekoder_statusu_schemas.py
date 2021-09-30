from typing import Optional

from sql_app.schemas_package.ogolne_schemas import CamelSchema


class DekoderStatusuBaseSchema(CamelSchema):
    kod: Optional[str]
    liczba_dziesietna: Optional[int]
    opis_kodu: Optional[str]


class DekoderStatusuCreateSchema(DekoderStatusuBaseSchema):
    pass


class DekoderStatusuSchema(DekoderStatusuBaseSchema):
    id: int

    class Config:
        orm_mode = True
