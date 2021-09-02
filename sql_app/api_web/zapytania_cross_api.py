from fastapi import APIRouter
from starlette.responses import JSONResponse

from sql_app import models
from sql_app.database import SessionLocal


router = APIRouter(
    prefix="/zapytania",
    tags=["zapytania"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=paczka_danych_schemas.)