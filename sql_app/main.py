from fastapi import FastAPI

from . import models
from .api_web import uzytkownicy_api, sesje_api, paczki_danych_api, wartosci_pomiarowe_sensorow_api, \
     dekodery_statusu_api, urzadzenia_api
from .api_web import sensory_api
from .database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(uzytkownicy_api.router)
app.include_router(sesje_api.router)
app.include_router(paczki_danych_api.router)
app.include_router(wartosci_pomiarowe_sensorow_api.router)
app.include_router(urzadzenia_api.router)
app.include_router(sensory_api.router)
app.include_router(dekodery_statusu_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

