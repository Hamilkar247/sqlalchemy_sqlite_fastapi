from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
async def create_sesja(sesja: sesja_schemas.SesjaSchema, db: Session = Depends(get_db)):
    return sesja_crud.create_sesja(db=db, sesja=sesja)


@router.get("/", response_model=List[sesja_schemas.SesjaSchema])
async def read_zbior_sesja(skip: int = 0, limit: int = 100, db: Session = Depends()):
    sesje = sesja_crud.get_zbior_sesji(db, skip=skip, limit=limit)
    return sesje


@router.get("/id={sesja_id}", response_model=sesja_schemas.SesjaSchema)
async def read_sesja(sesja_id: int, db: Session = Depends(get_db)):
    db_sesja = sesja_crud.get_sesja(db, sesja_id=sesja_id)
    if db_sesja is None:
        raise HTTPException(status_code=404, detail="Sesji nie znaleziono")
    return db_sesja


