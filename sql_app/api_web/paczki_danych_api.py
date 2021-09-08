from typing import List, Optional

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


########################## POST ################################
@router.post("/", response_description="stworz paczkę bez sesji", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def create_paczka_danych(paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema,
                               db: Session = Depends(get_db)):
    return paczka_danych_crud.create_paczka_danych_dla_sesji(db=db, paczka_danych=paczka_danych)


@router.post("/id_sesji={sesja_id}", response_description="stworz paczkę z sesją", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def create_paczka_danych(
        sesja_id: int,
        paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema,
        db: Session = Depends(get_db)):
    return paczka_danych_crud.create_paczka_danych_dla_sesji(db=db, paczka_danych=paczka_danych, sesja_id=sesja_id)


########################## GET ######################################
@router.get("/", response_model=List[paczka_danych_schemas.PaczkaDanychSchema])
async def get_zbior_paczek_danych(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paczki_danych = paczka_danych_crud.get_zbior_paczek_danych(db, skip=skip, limit=limit)
    return paczki_danych


@router.get("/przynalezne_zbiory", response_model=List[paczka_danych_schemas.PaczkaDanychSchemaNested])
async def get_zbior_paczek_danych_z_zagniezdzeniami(db: Session = Depends(get_db)):
    paczki_danych = paczka_danych_crud.get_zbior_paczek_danych(db)
    return paczki_danych


@router.get("/id={paczka_danych_id}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_paczke_danych(paczka_danych_id: int, db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_paczka_danych(db, paczka_danych_id=paczka_danych_id)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Paczka danych nie znaleziony")
    return db_paczek_danych


@router.get("/bez_sesji", response_model=List[paczka_danych_schemas.PaczkaDanychSchema])
async def get_paczke_danych_bez_przypisanej_sesji(db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_zbior_paczek_danych_bez_przypisanej_sesji(db)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Paczka danych nie znaleziony")
    return db_paczek_danych


@router.get("/bez_sesji/numer_seryjny={numer_seryjny}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_paczke_danych_urzadzenia_bez_przypisanej_sesji(numer_seryjny: str, db: Session = Depends(get_db)):
    id_sesji = None
    db_paczek_danych = paczka_danych_crud.get_paczka_danych_dla_urzadzenia_bez_przypisanej_sesji(db, numer_seryjny)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Paczka danych nie znaleziony")
    return db_paczek_danych


# @router.get("/numer_seryjny={numer_seryjny}", response_model=urzadzenie_schemas.UrzadzenieSchema)#paczka_danych_schemas.UrzadzeniePaczkiDanych)
# async def get_paczke_danych_i_odpowiadajace_mu_urzadzenie(numer_seryjny: str, db: Session):
#    dane = paczka_danych_crud.get_paczke_danych_i_odpowiadajace_mu_urzadzenie(db, numer_seryjny=numer_seryjny)
#    if dane is None:
#        raise HTTPException(status_code=404, detail="Nie znaleziono urządzenia o podanym numerze seryjnym.")
#    return dane


@router.get("/numer_seryjny_urzadzenia={numer_seryjny}", response_model=paczka_danych_schemas.PaczkaDanychSchema)
async def get_ostatnia_paczke_danych(numer_seryjny: str, db: Session = Depends(get_db)):
    db_paczek_danych = paczka_danych_crud.get_paczka_danych_dla_urzadzenia(db=db, numer_seryjny=numer_seryjny)
    print(db_paczek_danych)
    if db_paczek_danych is None:
        raise HTTPException(status_code=404, detail="Dla tego urządzenia nie znaleziono paczek danych")
    return db_paczek_danych


############################### PUT ################################33

@router.put("/zmien/paczka_danych_id={paczka_danych_id}", response_model=paczka_danych_schemas.PaczkaDanychUpdateSchema
    , response_description="zmień paczkę danych")
async def zmien_paczka_danych_o_id(paczka_danych_id: int, paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchema
                                   , db: Session = Depends(get_db)):
    update_paczka_danych = paczka_danych_crud.zmien_paczke_danych_o_id(db, paczka_danych_id, paczka_danych)
    print(update_paczka_danych)
    if update_paczka_danych is None:
        raise HTTPException(status_code=404, detail="Nie ma paczki o tym id")
    else:
        return update_paczka_danych


@router.put("/zmien/paczka_danych_id={paczka_danych_id}/usun_zastane_wartosci",
            response_model=paczka_danych_schemas.PaczkaDanychUpdateSchemaNested
    , response_description="zmień paczkę danych")
async def zmien_paczka_danych_o_id_usun_zastane_wartosci(paczka_danych_id: int,
                                                         paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchemaNested
                                                         , db: Session = Depends(get_db)):
    update_paczka_danych = paczka_danych_crud.zmien_paczke_danych_o_id__usun_dotychaczsowe_wartosci_pomiarow(db,
                                                                                                             paczka_danych_id,
                                                                                                             paczka_danych)
    print(update_paczka_danych)
    if update_paczka_danych is None:
        raise HTTPException(status_code=404, detail="Nie ma paczki o tym id")
    else:
        return update_paczka_danych


@router.put("/zmien/brak_sesji/numer_seryjny_urzadzenia={numer_seryjny}",
            response_model=paczka_danych_schemas.PaczkaDanychUpdateSchema_czas_i_kod)
async def zmien_paczka_danych_bez_przypisanej_sesji_o_numerze_seryjny(numer_seryjny: str
                                                                      ,
                                                                      paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchema_czas_i_kod
                                                                      , db: Session = Depends(get_db)):
    update_paczka_danych = paczka_danych_crud.zmien_paczke_danych__bez_sesji_o_numerze_seryjnym(db,
                                                                                                numer_seryjny,
                                                                                                paczka_danych)
    print(update_paczka_danych)
    if update_paczka_danych is None:
        raise HTTPException(status_code=404, detail="Nie ma paczki (bez przypisanej sesji) z tym numerem id")
    else:
        return update_paczka_danych


################################## DELETE #####################################
@router.delete("/delete/id={paczka_danych_id}", response_description="Usuń rekord o numerze id ...")
async def delete_id_paczke_danych(paczka_danych_id: int, db: Session = Depends(get_db)):
    # usuwam rekord o numerze id
    result_str = paczka_danych_crud.delete_paczka_danych(db, paczka_danych_id)
    if result_str == "usunieto rekord o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"udało się usunąć rekord o id {paczka_danych_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": f"nie ma rekordu o id {paczka_danych_id}"})
    return HTTPException(status_code=404, detail="Nie udało się usunąć paczki danych")


@router.delete("/delete/all_records", response_description="Usuń wszystkie paczki danych")
async def delete_all_paczki_danych(db: Session = Depends(get_db)):
    result = paczka_danych_crud.delete_all_paczki(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystkie rekordy"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "nie usunieto rekordów z tabeli paczki danych "})
