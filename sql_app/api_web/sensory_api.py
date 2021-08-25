from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.database import SessionLocal
from sql_app.schemas_package import sensor_schemas

router = APIRouter(
    prefix="/sensory",
    tags=["sensory"],
    responses={404: {"description" : "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=sensor_schemas.SensorSchema)
async def create_sensor(sensor: sensor_schemas.SensorCreateSchema, db: Session = Depends(get_db))
    pass
    #return None#sensor_crud.create_sensor(db=db, sensor=sensor)


@router.get("/", response_model=List[sensor_schemas.SensorSchema])
async def get_zbior_sensorow(skipL int = 0, limit: int = 100, db: Session = Depends(get_db))
    #sensory = None
    #return sensory
    pass


@router.delete("/delete/id={sensor_id}", response_description="Usuń sensor o numerze id ...")
async def delete_id_sensory(sensor_id: int, db: Session = Depends(get_db)):
    #result_str = sensor_crud.delete
    pass


@router.delte("/delete/all_records", response_description="Usuń wszystkie sensory")
async def delete_all_sensory(db: Session = Depends(get_db)):
    result = sensor_crud