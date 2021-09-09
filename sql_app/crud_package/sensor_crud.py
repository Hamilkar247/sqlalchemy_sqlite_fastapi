from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sensor_schemas


def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_zbior_sensorow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: sensor_schemas.SensorCreateSchema):
    db_sensor = models.Sensor(litery_porzadkowe=sensor.litery_porzadkowe,
                              parametr=sensor.parametr,
                              min=sensor.min,
                              max=sensor.max,
                              jednostka=sensor.jednostka,
                              status_sensora=sensor.status_sensora)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def create_sensor_id_urzadzenia(db: Session, sensor: sensor_schemas, id_urzadzenia: int):
    db_sensor = models.Sensor(litery_porzadkowe=sensor.litery_porzadkowe,
                              parametr=sensor.parametr,
                              min=sensor.min,
                              max=sensor.max,
                              jednostka=sensor.jednostka,
                              status_sensora=sensor.status_sensora,
                              urzadzenie_id=id_urzadzenia)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db: Session, sensor_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunięto  o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystąpił błąd przy usuwaniu sensora "+str(sensor_id)
        print(result_str)
        return None


def delete_caly_zbior_sensorow(db: Session):
    wszystkie_sensory = db.query(models.Sensor)
    if wszystkie_sensory is not None:
        wszystkie_sensory.delete()
        db.commit()
        return "usunieto wszystkie sensory"
    else:
        return None
