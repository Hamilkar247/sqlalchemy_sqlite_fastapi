from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import paczka_danych_schemas


def get_paczka_danych(db: Session, paczka_danych_id: int):
    return db.query(models.PaczkaDanych).filter(models.PaczkaDanych.id == paczka_danych_id).first()


def get_zbior_paczek_danych(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PaczkaDanych).offset(skip).limit(limit).all()


def create_paczka_danych(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychCreate):
    db_paczka_danych = models.PaczkaDanych(
        czas_paczki=paczka_danych.czas_paczki,
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych



