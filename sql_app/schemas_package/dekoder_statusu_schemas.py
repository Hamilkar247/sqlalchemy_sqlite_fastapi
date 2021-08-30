from typing import List, Optional

from pydantic import BaseModel


class DekoderStatusuBaseSchema(BaseModel):
    kod: Optional[str]
    liczba_dziesietna: Optional[int]
    opis_kodu: Optional[str]


class DekoderStatusuCreateSchema(DekoderStatusuBaseSchema):
    pass


class DekoderStatusuSchema(DekoderStatusuBaseSchema):
    id: int

    class Config:
        orm_mode = True
