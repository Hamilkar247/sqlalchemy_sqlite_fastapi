from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.schemas_package import paczka_danych_schemas, urzadzenie_schemas
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


@router.post("/id_sesji={sesja_id}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def create_paczka_danych(sesja_id: int, paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema,
                               db: Session = Depends(get_db)):
    return paczka_danych_crud.create_paczka_danych_dla_sesji(db=db, paczka_danych=paczka_danych, sesja_id=sesja_id)


@router.get("/", response_model=List[paczka_danych_schemas.PaczkaDanychSchema])
async def get_zbior_paczek_danych(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paczki_danych = paczka_danych_crud.get_zbior_paczek_danych(db, skip=skip, limit=limit)
    return paczki_danych


@router.get("/przynalezne_zbiory", response_model=paczka_danych_schemas.PaczkaDanychSchemaNested)
async def get_zbior_paczek_danych_z_zagniezdzeniami(db: Session = Depends(get_db)):
    paczki_danych = paczka_danych_crud.get_zbior_paczek_danych(db)
    return paczki_danych


@router.get("/id={paczka_danych_id}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_paczke_danych(paczka_danych_id: int, db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_paczka_danych(db, paczka_danych_id=paczka_danych_id)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Paczka danych nie znaleziony")
    return db_paczek_danych


@router.get("/numer_seryjny={numer_seryjny}", response_model=urzadzenie_schemas.UrzadzenieSchema)#paczka_danych_schemas.UrzadzeniePaczkiDanych)
async def get_paczke_danych_i_odpowiadajace_mu_urzadzenie(numer_seryjny: str, db: Session):
    dane = paczka_danych_crud.get_paczke_danych_i_odpowiadajace_mu_urzadzenie(db, numer_seryjny=numer_seryjny)
    if dane is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono urządzenia o podanym numerze seryjnym.")
    return dane


@router.get("/numer_seryjny_urzadzenia={numer_seryjny}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_ostatnia_paczke_danych(numer_seryjny: str, db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_paczka_danych_dla_urzadzenia(db=db, numer_seryjny=numer_seryjny)
    print(db_paczek_danych)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Dla tego urządzenia nie znaleziono paczek danych")
    return db_paczek_danych


@router.delete("/delete/id={paczka_danych_id}", response_description="Usuń rekord o numerze id ...")
async def delete_id_paczke_danych(paczka_danych_id: int, db: Session = Depends(get_db)):
    #usuwam rekord o numerze id
    result_str = paczka_danych_crud.delete_paczka_danych_crud(db, paczka_danych_id)
    if result_str == "usunieto rekord o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"udało się usunąć rekord o id {paczka_danych_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma rekordu o id {paczka_danych_id}"})
    return HTTPException(status_code=404, detail="Nie udało się usunąć paczki danych")


@router.delete("/delete/all_records", response_description="Usuń wszystkie paczki danych")
async def delete_all_paczki_danych(db: Session = Depends(get_db)):
    result = paczka_danych_crud.delete_all_paczki(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystkie rekordy"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie usunieto rekordów z tabeli paczki danych "})
