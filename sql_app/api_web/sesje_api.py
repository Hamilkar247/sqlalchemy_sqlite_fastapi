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


@router.post("/", response_model=sesja_schemas.SesjaSchema)
async def create_sesja(sesja: sesja_schemas.SesjaCreateSchema, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.create_sesja(db=db, sesja=sesja)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się dodać nowerj sesji")
    return db_sesja


@router.get("/id={sesja_id}", response_model=sesja_schemas.SesjaSchema)
async def get_sesja(sesja_id: int, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.get_sesja(db, sesja_id=sesja_id)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Sesji nie znaleziono")
    return db_sesja


@router.get("/", response_model=List[sesja_schemas.SesjaSchema])
async def get_zbior_sesja(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.get_zbior_sesji(db, skip=skip, limit=limit)
    return sesje


@router.get("/aktywne_sesje", response_model=List[sesja_schemas.SesjaSchema])
async def zwroc_zbior_sesji_aktywne(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sesje = sesja_crud.zwroc_aktywne_sesje(db, skip=skip, limit=limit)
    return sesje


@router.put("/id={sesja_id}", response_description="Zakończ działanie sesji")
async def zakoncz_sesje(sesja_id: int, db: Session = Depends(get_db)):
    #jesli znajdzie aktywna sesje pod tym id, zakonczy je, jeśli takiej nie bedzie
    zakonczona_sesja = sesja_crud.zakoncz_sesje(db, sesja_id)
    if zakonczona_sesja is None:
        raise HTTPException(status_code=404, detail="Nie udało się zakończyć sesje")
    else:
        return zakoncz_sesje


@router.delete("/delete/id={sesja_id}", response_description="Usunieto sesje o numerze id ...")
async def delete_id_sesji(sesja_id: int, db: Session = Depends(get_db)):
    #usuwam rekord o numerze id
    result_str = None
    result_str = sesja_crud.delete_sesja(db, sesja_id)
    if result_str == "usunieto rekord o podanym id":
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"udało się usunąć sesji o id {sesja_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma sesji o id {sesja_id}"})
    return HTTPException(status_code=404, detail="Nie udalo się usunąć rekordu sesji")


@router.delete("/delete/all_records", response_description="Usunieto wszystkie rekordy")
async def delete_all_sesje(db: Session = Depends(get_db)):
    result = sesja_crud.delete_all_sesje(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunieto wszystie sesje"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie usunieto sesji"})
