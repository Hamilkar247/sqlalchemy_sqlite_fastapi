from typing import List

from fastapi import Depends, APIRouter, HTTPException

from sql_app.schemas_package import uzytkownik_schemas
from sql_app.crud_package import uzytkownik_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/uzytkownicy",
    tags=["uzytkownicy"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=uzytkownik_schemas.Uzytkownik)
async def create_uzytkownik(uzytkownik: uzytkownik_schemas.UzytkownikCreateSchema, db: Session = Depends(get_db)):
    #db_uzytkownik = uzytkownik_crud.get_uzytkownik(db)
    return uzytkownik_crud.create_uzytkownik(db=db, uzytkownik=uzytkownik)
    #, imie_nazwisko=uzytkownik.imie_nazwisko,
    #    email=uzytkownik.email, hashed_password=uzytkownik.hashed_password,
    #    stanowisko=uzytkownik.stanowisko, opis=uzytkownik.opis, uprawnienia=uzytkownik.uprawnienia)


@router.get("/", response_model=List[uzytkownik_schemas.Uzytkownik])
async def read_zbior_uzytkownikow(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    uzytkownicy = uzytkownik_crud.get_zbior_uzytkownikow(db, skip=skip, limit=limit)
    if uzytkownicy is None:
        raise HTTPException(status_code=404, detail="Uzytkownik nie znaleziony")
    return uzytkownicy


@router.get("/id={uzytkownik_id}", response_model=uzytkownik_schemas.Uzytkownik)
async def read_uzytkownik(uzytkownik_id: int, db: Session = Depends(get_db)):
    db_uzytkownik = uzytkownik_crud.get_uzytkownik(db, uzytkownik_id=uzytkownik_id)
    if db_uzytkownik is None:
        raise HTTPException(status_code=404, detail="Uzytkownik nie znaleziony")
    return db_uzytkownik
