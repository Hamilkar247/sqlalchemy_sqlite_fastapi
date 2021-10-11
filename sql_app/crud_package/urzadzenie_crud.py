from operator import or_

from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sensor_schemas, urzadzenie_schemas


################ CREATE ##################
def create_urzadzenie(db: Session, urzadzenie: urzadzenie_schemas.UrzadzenieBaseSchemat):
    db_urzadzenie = models.Urzadzenie(
        nazwa_urzadzenia=urzadzenie.nazwa_urzadzenia,
        numer_seryjny=urzadzenie.numer_seryjny
    )
    db.add(db_urzadzenie)
    db.commit()
    db.refresh(db_urzadzenie)
    return db_urzadzenie


################### GET ################3
#zwraca pierwszy napotkane urzadzenie
def get_urzadzenie_id(db: Session, urzadzenie_id: int):
    return db.query(models.Urzadzenie).filter(models.Urzadzenie.id == urzadzenie_id).first()


def get_urzadzenie_id_zagniezdzone_sesje(db: Session, urzadzenie_id: int):
    return db.query(models.Urzadzenie).filter(models.Urzadzenie.id == urzadzenie_id).first()


#zwraca pierwsze napotkane urządzenie
def get_urzadzenie_by_numer_seryjny(db: Session, numer_seryjny: str):
    return db.query(models.Urzadzenie).filter(models.Urzadzenie.numer_seryjny == numer_seryjny).first()


def get_urzadzenie_by_numer_seryjny__zbior_sesji(db: Session, numer_seryjny: str):
    return db.query(models.Urzadzenie).filter(
        models.Urzadzenie.numer_seryjny == numer_seryjny).filter(
        models.Urzadzenie.id == models.Sesja.urzadzenie_id)


#zwraca pierwsze napotkane urządzenie
def get_urzadzenie_id_and_numer_seryjny(db: Session, nazwa_urzadzenia: str, numer_seryjny: str):
    return db.query(models.Urzadzenie).filter(or_(models.Urzadzenie.nazwa_urzadzenia == nazwa_urzadzenia,
                                        models.Urzadzenie.numer_seryjny == numer_seryjny)).first()


#zwraca pierwsze napotkane urządzenie
def get_urzadzenia_id(db: Session, numer_seryjny: str):
    return db.query(models.Urzadzenie).filter(models.Urzadzenie.numer_seryjny == numer_seryjny).first()


def get_zbior_urzadzen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Urzadzenie).offset(skip).limit(limit).all()


################### UPDATE ######################
def update_urzadzenie_o_id(db: Session, urzadzenie_id: int, urzadzenie: urzadzenie_schemas.UrzadzenieUpdateSchemat):
    print("update_urzadzenie_o_id")
    znajdz_i_zamien = db.query(models.Urzadzenie).filter(models.Urzadzenie.id == urzadzenie_id) \
                  .update(
                      {
                         models.Urzadzenie.numer_seryjny: urzadzenie.numer_seryjny,
                         models.Urzadzenie.nazwa_urzadzenia: urzadzenie.nazwa_urzadzenia
                      }
                  )
    print(znajdz_i_zamien)
    if znajdz_i_zamien is not None:
        print(znajdz_i_zamien)
        db.commit()
        return znajdz_i_zamien
    else:
        return None


#################### DELETE ################
def delete_urzadzenie_o_id(db: Session, urzadzenie_id: int):
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


def delete_caly_zbior_urzadzenia(db: Session):
    wszystkie_urzadzenia = db.query(models.Urzadzenie)
    if wszystkie_urzadzenia is not None:
        wszystkie_urzadzenia.delete()
        db.commit()
        return "usunięto wszystkie urządzenia"
    else:
        return None
