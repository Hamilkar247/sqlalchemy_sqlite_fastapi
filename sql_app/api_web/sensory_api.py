from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from sql_app.crud_package import sensor_crud
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session

from sql_app.schemas_package import sensor_schemas

router = APIRouter(
    prefix="/sensory",
    tags=["sensory"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=sensor_schemas.SensorSchema)
async def create_sensor(sensor: sensor_schemas.SensorCreateSchema, db: Session = Depends(get_db)):
    return sensor_crud.create_sensor(db=db, sensor=sensor)


@router.post("/id_urzadzenia={id_urzadzenia}", response_model=sensor_schemas.SensorSchema)
async def create_sensor_id_urzadzenia(sensor: sensor_schemas.SensorCreateSchema, id_urzadzenia: int, db: Session = Depends(get_db)):
    return sensor_crud.create_sensor_id_urzadzenia(db=db, sensor=sensor, id_urzadzenia=id_urzadzenia)


@router.get("/", response_model=List[sensor_schemas.SensorSchema])
async def get_zbior_sensorow(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensory = sensor_crud.get_zbior_sensorow(db, skip=skip, limit=limit)
    if sensory is None:
        raise HTTPException(status_code=404, detail="Żadnego sensora nie znaleziono")
    return sensory


@router.get("/id={sensor_id}", response_model=sensor_schemas.SensorSchema)
async def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = sensor_crud.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono sensora o tym id")
    return db_sensor


@router.delete("/delete/id={sensor_id}", response_description="Usuń sensor o numerze id ...")
async def delete_id_sensory(sensor_id: int, db: Session = Depends(get_db)):
    result_str = sensor_crud.delete_sensor(db, sensor_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"udało się usunąć sensora o id {sensor_id}"})
    elif result_str is None:
       return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"nie ma sensora o id {sensor_id}"})


@router.delete("/delete/all_records", response_description="Usuń wszystkie sensory")
async def delete_all_sensory(db: Session = Depends(get_db)):
    result = sensor_crud.delete_all_sensory(db)
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"usunięto wszystkie sensory"})
