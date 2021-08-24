from typing import List

from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from .. import crud_package
from ..crud_package import item_crud
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
    items = item_crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return item_crud.create_user_item(db=db, item=item, user_id=user_id)
