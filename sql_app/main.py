from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .api_web import users_api
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

