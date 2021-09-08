from datetime import datetime
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from sql_app.format_danych import FormatDaty
from sql_app.models import PaczkaDanych
from sql_app import models
from sql_app.schemas_package import paczka_danych_schemas
from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchema


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


def get_zbior_paczek_danych_bez_przypisanej_sesji(db: Session):
    # zwraca najwiekszy indeks dla danego numeru seryjnego
    return db.query(PaczkaDanych).filter(
        PaczkaDanych.sesja_id == None
    ).all()


def get_paczka_danych_dla_urzadzenia_bez_przypisanej_sesji(db: Session, numer_seryjny: str):
    # zwraca najwiekszy indeks dla danego numeru seryjnego
    return db.query(PaczkaDanych).filter(
        PaczkaDanych.numer_seryjny == numer_seryjny).filter(
        PaczkaDanych.sesja_id == None
    ).first()


def get_paczke_danych_i_odpowiadajace_mu_urzadzenie(db: Session, numer_seryjny: str):
    # dane = db.query(models.Urzadzenie.id, models.Urzadzenie.numer_seryjny, models.Urzadzenie.nazwa_urzadzenia).filter(
    #    models.PaczkaDanych.numer_seryjny == models.Urzadzenie.numer_seryjny).all()
    dane = db.query(models.Urzadzenie).filter(models.Urzadzenie.numer_seryjny == numer_seryjny)
    return dane


def create_paczka_danych(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychSchema):
    db_paczka_danych = PaczkaDanych(
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny,
        czas_paczki=FormatDaty().obecny_czas()
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


# def paczka_danych_zamien_lub_stworz(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychSchema):
#    db_paczka_danych = db.query(models.PaczkaDanych)\
#        .filter_by(models.PaczkaDanych.numer_seryjny == paczka_danych.numer_seryjny)\
#        .update()


# jeśli nie ma żadnej przypisanej sesji - nadpisuje dane ostatniej paczki urządzenia
def create_paczka_danych_dla_sesji(db: Session,
                                   paczka_danych: paczka_danych_schemas,
                                   sesja_id: Optional[int] = None):
    db_paczka_danych = PaczkaDanych(
        czas_paczki=FormatDaty().obecny_czas(),
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny,
        sesja_id=sesja_id
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


def zmien_paczke_danych_o_id(db: Session, paczka_danych_id: int,
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchema):
    znajdz_i_zmien_paczke = db.query(models.PaczkaDanych).filter(models.PaczkaDanych.id == paczka_danych_id).update(
        {
            models.PaczkaDanych.czas_paczki: FormatDaty().obecny_czas(),
            models.PaczkaDanych.kod_statusu: paczka_danych.kod_statusu,
            models.PaczkaDanych.numer_seryjny: paczka_danych.numer_seryjny
        }
    )
    if znajdz_i_zmien_paczke is not None:
        print(znajdz_i_zmien_paczke)
        db.commit()
        return znajdz_i_zmien_paczke
    else:
        return None


def zmien_paczke_danych__bez_sesji_o_numerze_seryjnym(db: Session, numer_seryjny: str,
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchema_czas_i_kod):
    znajdz_i_zmien_paczke = db.query(models.PaczkaDanych).filter(models.PaczkaDanych.numer_seryjny == numer_seryjny)\
        .filter(models.PaczkaDanych.sesja_id == None)\
        .update(
        {
            models.PaczkaDanych.czas_paczki: FormatDaty().obecny_czas(),
            models.PaczkaDanych.kod_statusu: paczka_danych.kod_statusu
        }
    )
    if znajdz_i_zmien_paczke is not None:
        print(znajdz_i_zmien_paczke)
        db.commit()
        return znajdz_i_zmien_paczke
    else:
        return None


def zmien_paczke_danych_o_id__usun_dotychaczsowe_wartosci_pomiarow(db: Session, paczka_danych_id: int,
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchemaNested):
    znajdz_i_zmien_paczke = db.query(models.PaczkaDanych).filter(models.PaczkaDanych.id == paczka_danych_id).update(
        {
            models.PaczkaDanych.czas_paczki: FormatDaty().obecny_czas(),
            models.PaczkaDanych.kod_statusu: paczka_danych.kod_statusu,
            models.PaczkaDanych.numer_seryjny: paczka_danych.numer_seryjny,
            models.PaczkaDanych.zbior_wartosci_pomiarow_sensorow: []
        }
    )
    if znajdz_i_zmien_paczke is not None:
        print(znajdz_i_zmien_paczke)
        db.commit()
        return znajdz_i_zmien_paczke
    else:
        return None


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
        return "usunieto wszystkie paczki"
    else:
        return None
