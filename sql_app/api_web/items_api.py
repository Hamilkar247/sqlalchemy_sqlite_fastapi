from typing import List

from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from .. import crud_package
from ..schemas_package import schemas
from ..database import SessionLocal

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
    items = crud_package.get_items(db, skip=skip, limit=limit)
    return items

