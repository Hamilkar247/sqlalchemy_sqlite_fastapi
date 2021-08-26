from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sensor_schemas, urzadzenie_schemas


def get_urzadzenie(db: Session, urzadzenie_id: int):
    return db.query(models.Urzadzenie).filter(models.Urzadzenie.id == urzadzenie_id).first()


def get_zbior_urzadzen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Urzadzenie).offset(skip).limit(limit).all()


def create_urzadzenie(db: Session, urzadzenie: urzadzenie_schemas.UrzadzenieCreateSchema):
    db_urzadzenie = models.Urzadzenie(
        nazwa_urzadzenia=urzadzenie.nazwa_urzadzenia,
        numer_seryjny=urzadzenie.numer_seryjny
    )
    db.add(db_urzadzenie)
    db.commit()
    db.refresh(db_urzadzenie)
    return db_urzadzenie


def delete_urzadzenie(db: Session, urzadzenie_id: int):
    try:
        obj_to_delete = db.query(models.Urzadzenie).filter(models.Urzadzenie.id == urzadzenie_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunięto urządzenie o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystąpił błąd przy usuwaniu urządzeniu o "+str(urzadzenie_id)
        print(result_str)
        return None


def delete_all_urzadzenia(db: Session):
    wszystkie_rekordy = db.query(models.Urzadzenie)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunięto wszystkie sensory"
    else:
        return None
