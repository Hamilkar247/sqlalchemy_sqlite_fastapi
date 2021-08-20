from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter

from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import SessionLocal, engine

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Item], tags=["items"])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

