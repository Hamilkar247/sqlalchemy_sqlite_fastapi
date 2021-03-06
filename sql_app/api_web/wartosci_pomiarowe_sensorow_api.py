from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.schemas_package import wartosc_pomiaru_sensora_schemas
from sql_app.crud_package import wartosc_pomiaru_sensora_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session
import logging
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)

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
             response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraSchemat)
async def create_wartosc_pomiaru_sensora(
        wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraCreateSchemat,
                                         db: Session = Depends(get_db)):
    return wartosc_pomiaru_sensora_crud.create_wartosc_pomiaru_sensora(
        db=db, wartosc_pomiaru_sensora=wartosc_pomiaru_sensora)


@router.post("/id_paczki={paczka_id}",
             response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraSchemat)
async def create_wartosc_pomiaru_sensora_dla_paczki_id(paczka_id: int,
        wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraCreateSchemat,
                                         db: Session = Depends(get_db)):

    return wartosc_pomiaru_sensora_crud.create_wartosc_pomiaru_sensora_dla_paczki(
        db=db, wartosc_pomiaru_sensora=wartosc_pomiaru_sensora, id_paczki=paczka_id)


@router.get("/",
            response_model=List[wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraSchemat])
async def get_zbior_wartosci_pomiaru_sensora(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zbior_wartosci_pomiaru_sensora = wartosc_pomiaru_sensora_crud.get_zbior_wartosci_pomiarowych_sensorow(db,
                                skip=skip, limit=limit)
    if zbior_wartosci_pomiaru_sensora is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono wartosci pomiaru sensora o id")
    return zbior_wartosci_pomiaru_sensora


@router.get("/id={wartosc_pomiaru_sensora_id}", response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraSchemat)
async def get_wartosc_pomiaru_sensora(wartosc_pomiaru_sensora_id: int, db: Session = Depends(get_db)):
    db_wartosc_pomiaru_sensora = \
        wartosc_pomiaru_sensora_crud.get_wartosc_pomiaru_sensora(
            db, wartosc_pomiaru_sensora_id=wartosc_pomiaru_sensora_id)
    if db_wartosc_pomiaru_sensora is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono wartosci pomiar??w sensorow")
    return db_wartosc_pomiaru_sensora


@router.get("/paczka_id={paczka_id}", response_model=wartosc_pomiaru_sensora_schemas.WartoscPomiaruSensoraSchemat)
async def get_wartosc_pomiaru_z_paczki_o_id(paczka_id: int, db: Session = Depends(get_db)):
    db_wartosc_pomiaru_sensora = \
        wartosc_pomiaru_sensora_crud.get_zbior_wartosci_pomiarowych_sensora_dla_paczki_o_id(db, paczka_id)
    if db_wartosc_pomiaru_sensora is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono warto??ci przypisanych temu id paczki")
    return db_wartosc_pomiaru_sensora


####################### DELETE ########################
@router.delete("/delete/id_paczki={paczka_id}", response_description="Usuni??to warto??ci pomiar??w sensora dla paczki o id ...")
async def delete_wartosci_pomiarow_z_paczki_o_id(paczka_id: int, db: Session = Depends(get_db)):
    result_str = wartosc_pomiaru_sensora_crud.usun_zbior_wartosci_pomiaru_sensora_z_paczki_o_id(db, paczka_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"uda??o si?? usun???? wartosci pomiarow z paczki o id {paczka_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f" nie uda??o si?? usun???? wartosci pomiarow z paczki od id {paczka_id} "})
    return result_str


@router.delete("/delete/id={wartosc_pomiaru_sensora_id}", response_description="Usunieto rekord o numerze id ...")
async def delete_id_wartosc_pomiaru_sensora(wartosc_pomiaru_sensora_id: int, db: Session = Depends(get_db)):
    #usuwam rekord o numerze id
    result_str = wartosc_pomiaru_sensora_crud.usun_wartosc_pomiaru_sensora(db, wartosc_pomiaru_sensora_id)
    if result_str == "usunieto rekord o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"uda??o si?? usun???? rekord o id {wartosc_pomiaru_sensora_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma rekordu o id {wartosc_pomiaru_sensora_id}"})
    return HTTPException(status_code=404, detail="Nie udalo si?? usun???? rekordu wartosci pomiaru sensora")


@router.delete("/delete/all_records", response_description="Usunieto wszystkie rekordy")
async def delete_all_wartosc_pomiaru_sensora(db: Session = Depends(get_db)):
    result = wartosc_pomiaru_sensora_crud.usun_caly_zbior_wartosci_pomiaru_sensora(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystie rekordy"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie usunieto rekord??w z tabeli warto??ci pomiar??w sensor??w"})
