from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.crud_package import uzytkownik_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session

from sql_app.schemas_package import uzytkownik_schemas

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


##################### POST ######################33
@router.post("/", response_model=uzytkownik_schemas.UzytkownikSchemat)
async def create_uzytkownik(uzytkownik: uzytkownik_schemas.UzytkownikCreateSchemat, db: Session = Depends(get_db)):
    db_uzytkownicy = uzytkownik_crud.get_uzytkownik_by_email(db, email=uzytkownik.email)
    if db_uzytkownicy:
        detail = "Na ten email jest już zarejestrowany uzytkownik!"
        print(detail)
        raise HTTPException(status_code=400, detail=detail)
    return uzytkownik_crud.create_uzytkownik(db=db, uzytkownik=uzytkownik)


################### GET ###########################3
@router.get("/", response_model=List[uzytkownik_schemas.UzytkownikSchemat])
async def get_zbior_uzytkownikow(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    uzytkownicy = uzytkownik_crud.get_zbior_uzytkownikow(db, skip=skip, limit=limit)
    if uzytkownicy is None:
        raise HTTPException(status_code=404, detail="Użytkowników nie znaleziony")
    return uzytkownicy


@router.get("/przynalezne_zbiory", response_model=List[uzytkownik_schemas.UzytkownikSchematNested])
async def get_zbior_uzytkownikow_z_zagniezdzeniami(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    uzytkownicy = uzytkownik_crud.get_zbior_uzytkownikow(db, skip=skip, limit=limit)
    if uzytkownicy is None:
        raise HTTPException(status_code=404, detail="Użytkownikóœ nie znaleziony")
    return uzytkownicy


@router.get("/id={uzytkownik_id}", response_model=uzytkownik_schemas.UzytkownikSchemat)
async def get_uzytkownik(uzytkownik_id: int, db: Session = Depends(get_db)):
    db_uzytkownik = uzytkownik_crud.get_uzytkownik(db, uzytkownik_id=uzytkownik_id)
    if db_uzytkownik is None:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    return db_uzytkownik


#################### DELETE #########################
@router.delete("/delete/id={uzytkownik_id}", response_description="Usunieto użytkownika o numerze id ...")
async def delete_id_uzytkownika(uzytkownik_id: int, db: Session = Depends(get_db)):
    #usuwam rekord o numerze id
    result_str = uzytkownik_crud.delete_uzytkownik(db, uzytkownik_id)
    if result_str == "usunieto użytkownika o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"udało się usunąć użytkownika o id {uzytkownik_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma rekordu o id {uzytkownik_id}"})


@router.delete("/delete/all_records", response_description="Usunieto wszystkich uzytkowników")
async def delete_all_uzytkownicy(db: Session = Depends(get_db)):
    result = uzytkownik_crud.delete_all_uzytkownicy(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystkie sensory"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie usunieto wszystkich sensorow"})
