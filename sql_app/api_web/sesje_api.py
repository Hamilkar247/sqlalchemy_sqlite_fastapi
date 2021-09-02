from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from sql_app import models
from sql_app.crud_package import sesja_crud
from sql_app.database import SessionLocal
from sql_app.schemas_package import sesja_schemas

router = APIRouter(
    prefix="/sesje",
    tags=["sesje"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=sesja_schemas.SesjaCreateSchema)
async def create_sesja(sesja: sesja_schemas.SesjaCreateSchema, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja(db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowerj sesji")
    return db_sesja


@router.post("/id_uzytkownika={uzytkownik_id}", response_model=sesja_schemas.SesjaSchema)
async def create_sesja_id_uzytkownik(uzytkownik_id: int, sesja: sesja_schemas.SesjaCreateSchema, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja_dla_uzytkownika(uzytkownik_id=uzytkownik_id, db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowej sesji")
    return db_sesja


@router.post("/id_uzytkownika={uzytkownik_id}/id_urzadzenia={urzadzenie_id}", response_model=sesja_schemas.SesjaSchema)
async def create_sesja_id_uzytkownik_id_urzadzenie(urzadzenie_id: int, uzytkownik_id: int, sesja: sesja_schemas.SesjaCreateSchema,
                                                   db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja_urzadzenia_dla_uzytkownika(urzadzenie_id=urzadzenie_id,
                                                                  uzytkownik_id=uzytkownik_id,
                                                                  db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowej sesji")
    return db_sesja


@router.get("/id={sesja_id}", response_model=sesja_schemas.SesjaSchema)
async def get_sesja(sesja_id: int, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.get_sesja(db, sesja_id=sesja_id)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Sesji nie znaleziono")
    return db_sesja


@router.get("/", response_model=List[sesja_schemas.SesjaSchema])
async def get_zbior_sesji(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.get_zbior_sesji(db, skip=skip, limit=limit)
    return sesje


@router.get("/przynalezne_zbiory", response_model=List[sesja_schemas.SesjaSchemaNested])
async def get_zbior_sesji_z_zagniezdzeniami(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.get_zbior_sesji(db, skip=skip, limit=limit)
    return sesje


@router.get("/aktywne_sesje", response_model=List[sesja_schemas.SesjaSchema])
async def zwroc_zbior_sesji_aktywne(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.zwroc_aktywne_sesje(db, skip=skip, limit=limit)
    return sesje


@router.get("/aktywna_sesja/urzadzenie_id={urzadzenie_id}", response_model=sesja_schemas.SesjaSchema)
async def get_aktywna_sesja_urzadzenia_id(urzadzenie_id: int, db: Session = Depends(get_db)):
    sesja = sesja_crud.get_aktywna_sesja_urzadzenia_id(db, urzadzenie_id)
    return sesja


@router.get("/aktywne_sesje/numer_seryjny_urzadzenia={numer_seryjny}", response_model=sesja_schemas.SesjaSchema)
async def get_aktywna_sesje_urzadzenia_numer_seryjny(numer_seryjny: str, db: Session = Depends(get_db)):
    sesja = sesja_crud.get_aktywna_sesje_urzadzenia__num_ser(db, numer_seryjny)
    return sesja


@router.put("/id={sesja_id}", response_description="Zakończ działanie sesji")
async def zakoncz_sesje(sesja_id: int, db: Session = Depends(get_db)):
    #jesli znajdzie aktywna sesje pod tym id, zakonczy je, jeśli takiej nie bedzie
    zakonczona_sesja = sesja_crud.zakoncz_sesje(db, sesja_id)
    if zakonczona_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się zakończyć sesje")
    else:
        return zakonczona_sesja


@router.delete("/delete/id={sesja_id}", response_description="Usunieto sesje o numerze id ...")
async def delete_id_sesji(sesja_id: int, db: Session = Depends(get_db)):
    #usuwam rekord o numerze id
    result_str = None
    result_str = sesja_crud.delete_sesja(db, sesja_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"udało się usunąć sesji o id {sesja_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma sesji o id {sesja_id}"})


@router.delete("/delete/all_records", response_description="Usunieto wszystkie rekordy")
async def delete_all_sesje(db: Session = Depends(get_db)):
    result = sesja_crud.delete_all_sesje(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystie sesje"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie usunieto sesji"})
