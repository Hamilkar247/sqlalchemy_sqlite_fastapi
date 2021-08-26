from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.crud_package import urzadzenie_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session

from sql_app.schemas_package import urzadzenie_schemas

router = APIRouter(
    prefix="/urzadzenia",
    tags=["urzadzenia"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=urzadzenie_schemas.UrzadzenieSchema)
async def create_urzadzenie(urzadzenie: urzadzenie_schemas.UrzadzenieCreateSchema, db: Session = Depends(get_db)):
    return urzadzenie_crud.create_urzadzenie(db=db, urzadzenie=urzadzenie)


@router.get("/", response_model=List[urzadzenie_schemas.UrzadzenieSchema])
async def get_zbior_urzadzen(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zbior_urzadzen = urzadzenie_crud.get_zbior_urzadzen(db, skip=skip, limit=limit)
    if zbior_urzadzen is None:
        raise HTTPException(status_code=404, detail="Urzadzen nie znaleziono")
    return zbior_urzadzen


@router.get("/id={urzadzenie_id}", response_model=urzadzenie_schemas.UrzadzenieSchema)
async def get_urzadzenia(urzadzenie_id: int, db: Session = Depends(get_db)):
    db_urzadzenie = urzadzenie_crud.get_urzadzenie(db, urzadzenie_id=urzadzenie_id)
    if db_urzadzenie is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono sensora o tym id")
    return db_urzadzenie


@router.delete("/delete/id={urzadzenie_id}", response_description="Usuń urządzenie o numerze id ...")
async def delete_id_urzadzenie(urzadzenie_id: int, db: Session = Depends(get_db)):
    result_str = urzadzenie_crud.delete_urzadzenie(db, urzadzenie_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Udało się usunąc urządzenie o numerze id: {urzadzenie_id}"})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Nie udało się usunąć urządzenia o numerze id"})


@router.delete("/delete/all_records", response_description="Usunięto wszystkie rekordy")
async def delete_all_urzadzenia(db: Session = Depends(get_db)):
    result = urzadzenie_crud.delete_all_urzadzenia(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunięto wszystkie sesje"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "nie udało się usunąć wszystkich urządzeń"})

