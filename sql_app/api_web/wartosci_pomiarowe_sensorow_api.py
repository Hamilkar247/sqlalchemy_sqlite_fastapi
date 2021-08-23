from typing import List

from fastapi import Depends, APIRouter, HTTPException

from sql_app.schemas_package import uzytkownik_schemas, wartosc_pomiaru_sensora_schemas
from sql_app.crud_package import uzytkownik_crud, wartosc_pomiaru_sensora_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/wartosci_pomiarowe_sensora",
    tags=["wartosci_pomiarowe_sensora"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/",
             response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensora)
async def create_wartosc_pomiaru_sensora(
        wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraCreate,
                                         db: Session = Depends(get_db)):
    return wartosc_pomiaru_sensora_crud.create_wartosc_pomiarowa_sensorow(
        db=db, wartosc_pomiaru_sensora=wartosc_pomiaru_sensora)


@router.get("/",
            response_model=List[wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensora])
async def get_zbior_wartosci_pomiaru_sensora(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zbior_wartosci_pomiaru_sensora = wartosc_pomiaru_sensora_crud.get_zbior_wartosci_pomiarowych_sensorow(db,
                                                                                      skip=skip, limit=limit)
    if zbior_wartosci_pomiaru_sensora is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono wartosci pomiaru sensora o id")
    return zbior_wartosci_pomiaru_sensora


@router.get("/id={wartosc_pomiaru_sensora_id}", response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensora)
async def get_wartosc_pomiaru_sensora(wartosc_pomiaru_sensora_id: int, db: Session = Depends(get_db)):
    db_wartosc_pomiaru_sensora = \
        wartosc_pomiaru_sensora_crud.get_wartosc_pomiaru_sensora(
            db, wartosc_pomiaru_sensora_id=wartosc_pomiaru_sensora_id)
    if db_wartosc_pomiaru_sensora is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono wartosci pomiarów sensorow")
    return db_wartosc_pomiaru_sensora
