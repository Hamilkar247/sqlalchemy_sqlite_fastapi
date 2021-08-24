from typing import List

from fastapi import Depends, APIRouter, HTTPException

from sql_app.schemas_package import paczka_danych_schemas
from sql_app.crud_package import paczka_danych_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/paczki_danych",
    tags=["paczki_danych"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def create_paczka_danych(paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema, db: Session = Depends(get_db)):
    return paczka_danych_crud.create_paczka_danych(db=db, paczka_danych=paczka_danych)


@router.get("/", response_model=List[paczka_danych_schemas.PaczkaDanychSchema])
async def get_zbior_paczek_danych(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paczki_danych = paczka_danych_crud.get_zbior_paczek_danych(db, skip=skip, limit=limit)
    return paczki_danych


@router.get("/id={paczka_danych_id}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_paczke_danych(paczka_danych_id: int, db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_paczka_danych(db, paczka_danych_id=paczka_danych_id)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Paczka danych nie znaleziony")
    return db_paczek_danych
