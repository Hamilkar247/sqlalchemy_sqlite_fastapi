from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import paczka_danych_schemas


def get_paczka_danych(db: Session, paczka_danych_id: int):
    return db.query(models.PaczkaDanych).filter(models.PaczkaDanych.id == paczka_danych_id).first()


def get_zbior_paczek_danych(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PaczkaDanych).offset(skip).limit(limit).all()


def create_paczka_danych(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema):
    db_paczka_danych = models.PaczkaDanych(
        czas_paczki=paczka_danych.czas_paczki,
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


def create_paczka_danych_dla_sesji(db: Session,
                        paczka_danych: paczka_danych_schemas,
                                   sesja_id: int):
    db_paczka_danych = models.PaczkaDanych(
        czas_paczki=paczka_danych.czas_paczki,
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny,
        sesja_id=sesja_id
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


def delete_paczka_danych(db: Session, paczka_danych_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(models.PaczkaDanych).filter(models.PaczkaDanych.id == paczka_danych_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunieto paczke o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystapił błąd przy usuwaniu rekordu"+str(paczka_danych_id)
        return result_str


def delete_all_paczki(db: Session):
    wszystkie_rekordy = db.query(models.PaczkaDanych)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto"
    else:
        return None


