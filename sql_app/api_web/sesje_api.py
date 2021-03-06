from datetime import datetime
from typing import List, Optional

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


######################## CREATE #######################
@router.post("/", response_model=sesja_schemas.SesjaCreateSchemat)
async def create_sesja(sesja: sesja_schemas.SesjaCreateSchemat, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja(db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowej sesji")
    return db_sesja


@router.post("/id_uzytkownika={uzytkownik_id}", response_model=sesja_schemas.SesjaSchemat)
async def create_sesja_id_uzytkownik(uzytkownik_id: int, sesja: sesja_schemas.SesjaCreateSchemat, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja(uzytkownik_id=uzytkownik_id, db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowej sesji")
    return db_sesja


@router.post("/id_uzytkownika={uzytkownik_id}/id_urzadzenia={urzadzenie_id}", response_model=sesja_schemas.SesjaSchemat)
async def create_sesja_id_uzytkownik_id_urzadzenie(urzadzenie_id: int, uzytkownik_id: int, sesja: sesja_schemas.SesjaCreateSchemat,
                                                   db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja(urzadzenie_id=urzadzenie_id,
                                       uzytkownik_id=uzytkownik_id,
                                       db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowej sesji")
    return db_sesja


######################### GET ##############################
@router.get("/id={sesja_id}", response_model=sesja_schemas.SesjaSchemat)
async def get_sesja_o_id(sesja_id: int, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.get_sesja_o_id(db=db, sesja_id=sesja_id)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Sesji nie znaleziono")
    return db_sesja


######################### GET ##############################
@router.get("/id={sesja_id}/przynalezne_zbiory", response_model=sesja_schemas.SesjaSchematNested)
async def get_sesja_o_id_z_przynaleznymi_zbiorami(sesja_id: int, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.get_sesja_o_id(db=db, sesja_id=sesja_id)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Sesji nie znaleziono")
    return db_sesja


@router.get("/id={sesja_id}/jedna_per_n={jedna_per_n}", response_model=sesja_schemas.SesjaSchemat)
async def get_sesja_o_id__i__get_jedna_paczka_per_n_paczek_dla_tej_sesji(sesja_id: int,
                                     jedna_per_n: int,
                                     db: Session = Depends(get_db)):
    print("ahouj")
    db_paczek_danych_per_n = sesja_crud.get_zbior_paczek_danych_dla_sesji_jedna_per_n(
        db=db,
        sesja_id=sesja_id,
        jedna_per_n=jedna_per_n)
    return db_paczek_danych_per_n


#@router.get("/id_sesji={sesja_id}/jedna_per_n={jedna_per_n}/przynalezne_zbiory/uproszczone", response_model=List[paczka_danych_schemas.PaczkaDanychProstaNested])
#async def get_jedna_paczka_per_n_dla_sesji_z_wartosciami(sesja_id: int,
#                                     jedna_per_n: int,
#                                     db: Session = Depends(get_db)):
#    print("ahouj")
#    db_paczek_danych_per_n = paczka_danych_crud.get_zbior_paczek_danych_dla_sesji_jedna_per_n(
#        db=db,
#        sesja_id=sesja_id,
#        jedna_per_n=jedna_per_n)
#    return db_paczek_danych_per_n


@router.get("/", response_model=List[sesja_schemas.SesjaSchemat])
async def get_zbior_sesji(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    sesje = sesja_crud.get_zbior_sesji(db=db, skip=skip, limit=limit)
    return sesje


@router.get("/przynalezne_zbiory", response_model=List[sesja_schemas.SesjaSchematNested])
async def get_zbior_sesji_z_zagniezdzeniami(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    sesje = sesja_crud.get_zbior_sesji(db=db, skip=skip, limit=limit)
    return sesje


@router.get("/aktywne_sesje", response_model=List[sesja_schemas.SesjaSchemat])
async def zwroc_zbior_sesji_aktywne(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.zwroc_aktywne_sesje(db=db, skip=skip, limit=limit)
    return sesje


@router.get("/aktywna_sesja/urzadzenie_id={urzadzenie_id}", response_model=sesja_schemas.SesjaSchemat)
async def get_aktywna_sesja_urzadzenia_id(urzadzenie_id: int, db: Session = Depends(get_db)):
    sesja = sesja_crud.get_aktywna_sesja_urzadzenia_id(db=db, urzadzenie_id=urzadzenie_id)
    return sesja


@router.get("/aktywne_sesje/numer_seryjny_urzadzenia={numer_seryjny}", response_model=sesja_schemas.SesjaSchemat)
async def get_aktywna_sesje_urzadzenia_o_numerze_seryjnym(numer_seryjny: str, db: Session = Depends(get_db)):
    sesja = sesja_crud.get_aktywna_sesja_urzadzenia_o_numerze_seryjnym(db, numer_seryjny)
    return sesja


##################### UPDATE ##############################
@router.put("/id={sesja_id}", response_description="Zakończ działanie sesji")
async def zakoncz_sesje(sesja_id: int, db: Session = Depends(get_db)):
    #jesli znajdzie aktywna sesje pod tym id, zakonczy je, jeśli takiej nie bedzie
    zakonczona_sesja = sesja_crud.zakoncz_sesje(db, sesja_id)
    if zakonczona_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się zakończyć sesje")
    else:
        return f"Zakończono sesje o numerze id: {sesja_id}"


############### DELETE ##################3
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
