from typing import List

from fastapi import APIRouter

from sql_app.crud_package import dekoder_statusu_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.schemas_package import dekoder_statusu_schemas

router = APIRouter(
    prefix="/dekoder_statusu",
    tags=["dekoder_statusu"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dekoder_statusu_schemas.DekoderStatusuSchemat)
async def create_dekoder_statusu(dekoder_statusu: dekoder_statusu_schemas.DekoderStatusuCreateSchemat, db: Session = Depends(get_db)):
    db_dekoder_statusu = dekoder_statusu_crud.get_dekoder_statusu(db,
                         kod=dekoder_statusu.kod, liczba_dziesietna=dekoder_statusu.liczba_dziesietna)
    if db_dekoder_statusu:
        raise HTTPException(status_code=400, detail="Pola kod statusu i liczba dziesietna są już użyte w tabeli !")
    return dekoder_statusu_crud.create_dekodera_statusu(db=db, dekoder_statusu=dekoder_statusu)


@router.get("/", response_model=List[dekoder_statusu_schemas.DekoderStatusuSchemat])
async def get_zbior_paczek_danych(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dekoder_statusu_crud.get_zbior_dekoderow_statusu(db, skip=skip, limit=limit)


@router.delete("/delete/id={kod_statusu_id}", response_description="Usunięto dekoder statusu o numerze  id ...")
async def delete_id_dekoder_statusu(dekoder_statusu_id: int, db: Session = Depends(get_db)):
    result_str = dekoder_statusu_crud.delete_dekoder_statusu(db, dekoder_statusu_id)
    if result_str == "usunięto rekord o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f" udało się usunąć dekoder statusu o id {dekoder_statusu_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma dekoder statusu o id {dekoder_statusu_id}"})
    return HTTPException(status_code=404, detail="Nie udało się usunąć dekodera statusu")


@router.delete("/delete/all_dekodery_statusu", response_description="Usunięto wszystkie rekordy")
async def delete_all_dekodery_statusu(db: Session = Depends(get_db)):
    result = dekoder_statusu_crud.delete_all_dekodery_statusu(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f" usunięto wszystkie zapisy dekoderach"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie usunięto rekordów z tabeli dekoderów statusu"})