from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sensor_schemas


##################### CREATE ##########################
def create_sensor(db: Session, sensor: sensor_schemas.SensorCreateSchemat):
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


######################## GET #########################3
def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_zbior_sensorow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()


######################## UPDATE ########################
def update_sensor_o_id(db: Session, sensor_id: int, sensor: sensor_schemas.SensorUpdateSchemat):
    znajdz_i_zamien = db.query(models.Sensor).filter(models.Sensor.id == sensor_id) \
                  .update(
                      {
                          models.Sensor.status_sensora: sensor.status_sensora,
                          models.Sensor.max: sensor.max,
                          models.Sensor.min: sensor.min,
                          models.Sensor.urzadzenie_id: sensor.urzadzenie_id,
                          models.Sensor.jednostka: sensor.jednostka,
                          models.Sensor.parametr: sensor.parametr,
                          models.Sensor.litery_porzadkowe: sensor.litery_porzadkowe
                      }
                  )
    if znajdz_i_zamien is not None:
        db.commit()
        return znajdz_i_zamien
    else:
        return None


####################### DELETE ###################################
def delete_sensor_o_id(db: Session, sensor_id: int):
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
