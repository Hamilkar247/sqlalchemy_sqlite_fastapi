from datetime import datetime
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from sql_app.format_danych import FormatDaty
from sql_app.models import PaczkaDanych, Sesja
from sql_app import models
from sql_app.schemas_package import paczka_danych_schemas
from sql_app.schemas_package.wartosc_pomiaru_sensora_schemas import WartoscPomiaruSensoraSchemat


##################### CREATE ###########################
def create_paczka_danych(db: Session, paczka_danych: paczka_danych_schemas.PaczkaDanychSchemat):
    db_paczka_danych = PaczkaDanych(
        kod_statusu=paczka_danych.kod_statusu,
        numer_seryjny=paczka_danych.numer_seryjny,
        czas_paczki=FormatDaty().obecny_czas()
    )
    db.add(db_paczka_danych)
    db.commit()
    db.refresh(db_paczka_danych)
    return db_paczka_danych


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


##################### GET #############################
def get_paczka_danych_o_id(db: Session, paczka_danych_id: Optional[int]=None):
    return db.query(PaczkaDanych).filter(PaczkaDanych.id == paczka_danych_id).first()


def get_zbior_paczek_danych(db: Session, skip: Optional[int] = None, limit: Optional[int] = None,
                            id_sesji: Optional[int] = None):
    paczki_danych = db.query(PaczkaDanych).\
        offset(skip).limit(limit).all()
    return paczki_danych


def get_zbior_paczek_danych_o_id_sesji(sesja_id: int, db: Session,
                    skip: Optional[int] = None, limit: Optional[int] = None):
    if sesja_id is not None:
        if limit != 1:
            return db.query(PaczkaDanych).filter(PaczkaDanych.sesja_id == sesja_id)\
                      .offset(skip).limit(limit).all()
        else:
            return db.query(PaczkaDanych).filter(PaczkaDanych.sesja_id == sesja_id) \
                      .offset(skip).limit(limit).first()
    return None


def get_zbior_paczek_danych_bez_przypisanej_sesji(db: Session,
                    skip: Optional[int] = None, limit: Optional[int] = None, numer_seryjny: Optional[str] = None):
    print(f'chodz {numer_seryjny}')
    #gdy nie chcemy filtrować po numerze seryjnym
    if numer_seryjny is not None:
        return db.query(PaczkaDanych).filter(PaczkaDanych.sesja_id == None) \
            .filter(PaczkaDanych.numer_seryjny == numer_seryjny) \
            .order_by(None).order_by(PaczkaDanych.czas_paczki.desc()) \
            .offset(skip).limit(limit).all()
    else:
        return db.query(PaczkaDanych).filter(PaczkaDanych.sesja_id == None)\
            .order_by(None).order_by(PaczkaDanych.czas_paczki.desc())\
            .offset(skip).limit(limit).all()


def get_zbior_paczek_danych_o_numerze_seryjnym(db: Session, numer_seryjny: str,
                                               skip: Optional[int] = None, limit: Optional[int] = None):
    return db.query(PaczkaDanych).filter(PaczkaDanych.numer_seryjny == numer_seryjny).offset(skip).limit(limit).all()


def get_zbior_paczek_danych_dla_sesji_jedna_per_n(db: Session, sesja_id: int, jedna_per_n: int):
    liczba = 0
    lista = []
    while True:
        element = db.query(PaczkaDanych).filter(PaczkaDanych.sesja_id == sesja_id).offset(liczba).first()
        if element is not None:
            lista.append(element)
        else:
            break
        liczba = liczba + jedna_per_n
    return lista


###################### UPDATE #####################################
def zmien_paczke_danych_o_id(db: Session, paczka_danych_id: int,
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchemat):
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
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchemat_czas_i_kod):
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
                               paczka_danych: paczka_danych_schemas.PaczkaDanychUpdateSchematNested):
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


############################# DELETE #################################
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


def delete_wszystkie_paczki_danych(db: Session):
    wszystkie_rekordy = db.query(PaczkaDanych)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto wszystkie paczki"
    else:
        return None
