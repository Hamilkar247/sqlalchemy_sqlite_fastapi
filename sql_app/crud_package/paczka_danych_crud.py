from datetime import datetime

from sqlalchemy.orm import Session
from sql_app.models import PaczkaDanych
from sql_app import models
from sql_app.schemas_package import paczka_danych_schemas


def get_paczka_danych(db: Session, paczka_danych_id: int):
    return db.query(PaczkaDanych).filter(PaczkaDanych.id == paczka_danych_id).first()


def get_zbior_paczek_danych(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PaczkaDanych).offset(skip).limit(limit).all()


def get_paczka_danych_dla_urzadzenia(db: Session, numer_seryjny: str):
    # zwraca najwiekszy indeks dla danego numeru seryjnego
    return db.query(PaczkaDanych).filter(
        PaczkaDanych.numer_seryjny == numer_seryjny). \
        order_by(None). \
        order_by(PaczkaDanych.id.desc()).first()


def get_paczke_danych_i_odpowiadajace_mu_urzadzenie(db: Session, numer_seryjny: str):
    # dane = db.query(models.Urzadzenie.id, models.Urzadzenie.numer_seryjny, models.Urzadzenie.nazwa_urzadzenia).filter(
    #    models.PaczkaDanych.numer_seryjny == models.Urzadzenie.numer_seryjny).all()
    dane = db.query(models.Urzadzenie).filter(models.Urzadzenie.numer_seryjny == numer_seryjny)
    return dane


def create_paczka_danych(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychCreateSchema):
    db_paczka_danych = PaczkaDanych(
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
    db_paczka_danych = PaczkaDanych(
        czas_paczki=paczka_danych.czas_paczki,
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny,
        sesja_id=sesja_id
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


def zupdatuj_paczke_danych_by_item_id(db: Session, paczka_danych_id: int):
    find_paczke = db.query(PaczkaDanych).filter(
        PaczkaDanych.id == paczka_danych_id).update(
        {}
    )

    if find_paczke is not None:
        now = datetime.now()
        print(f"now")


def delete_paczka_danych(db: Session, paczka_danych_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(PaczkaDanych).filter(PaczkaDanych.id == paczka_danych_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunieto rekord o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystapił błąd przy usuwaniu rekordu"
        return result_str


def delete_all_paczki(db: Session):
    wszystkie_rekordy = db.query(PaczkaDanych)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto"
    else:
        return None
