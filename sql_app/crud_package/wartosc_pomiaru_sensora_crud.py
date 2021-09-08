import logging

from sql_app.models import WartoscPomiaruSensora
from sqlalchemy.orm import Session
from sql_app.schemas_package import wartosc_pomiaru_sensora_schemas


########################### GET ####################
def get_wartosc_pomiaru_sensora(db: Session, wartosc_pomiaru_sensora_id: int):
    return db.query(WartoscPomiaruSensora).filter(WartoscPomiaruSensora.id == wartosc_pomiaru_sensora_id).first()


def get_zbior_wartosci_pomiarowych_sensora_dla_paczki_o_id(db: Session, paczka_id: int):
    return db.query(WartoscPomiaruSensora).filter(WartoscPomiaruSensora.paczka_danych_id == paczka_id).all()


def get_zbior_wartosci_pomiarowych_sensorow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(WartoscPomiaruSensora).offset(skip).limit(limit).all()


######################### CREATE #####################
def create_wartosc_pomiaru_sensora(db: Session, wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas):
    db_wartosc_pomiaru_sensora = WartoscPomiaruSensora(
        wartosc=wartosc_pomiaru_sensora.wartosc,
        litery_porzadkowe=wartosc_pomiaru_sensora.litery_porzadkowe
    )
    db.add(db_wartosc_pomiaru_sensora)
    db.commit()
    db.refresh(db_wartosc_pomiaru_sensora)
    return db_wartosc_pomiaru_sensora


def create_wartosc_pomiaru_sensora_dla_paczki(db: Session,
                wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas,
                                              id_paczki: int):
    db_wartosc_pomiaru_sensora = WartoscPomiaruSensora(
        wartosc=wartosc_pomiaru_sensora.wartosc,
        litery_porzadkowe=wartosc_pomiaru_sensora.litery_porzadkowe,
        paczka_danych_id=id_paczki
    )
    db.add(db_wartosc_pomiaru_sensora)
    db.commit()
    db.refresh(db_wartosc_pomiaru_sensora)
    return db_wartosc_pomiaru_sensora


####################### DELETE ###################
def usun_wartosc_pomiaru_sensora(db: Session, wartosc_pomiaru_sensora_id: int):
    try:
        obj_to_delete = db.query(WartoscPomiaruSensora).filter(WartoscPomiaruSensora.id == wartosc_pomiaru_sensora_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunieto rekord o podanym id"
        return result_str
    except Exception as e:
        result_str="wystapil blad przy usuwaniu rekordu"+str(wartosc_pomiaru_sensora_id)
        return result_str


def usun_zbior_wartosci_pomiaru_sensora_z_paczki_o_id(db: Session, paczka_id: int):
    usun_zbior_wartosci_pomiaru_sensora \
                 = db.query(WartoscPomiaruSensora).filter(WartoscPomiaruSensora.paczka_danych_id==paczka_id)
    if usun_zbior_wartosci_pomiaru_sensora is not None:
        usun_zbior_wartosci_pomiaru_sensora.delete()
        db.commit()
        return "usunieto"
    else:
        return None


def usun_caly_zbior_wartosci_pomiaru_sensora(db: Session):
    wszystkie_rekordy = db.query(WartoscPomiaruSensora)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto"
    else:
        return None