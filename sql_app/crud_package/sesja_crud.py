from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sesja_schemas


def get_sesja(db: Session, sesja_id: int):
    return db.query(models.Sesja).filter(models.Sesja.id == sesja_id).first()


def get_zbior_sesji(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sesja).offset(skip).limit(limit).all()


def create_sesja(db: Session, sesja: sesja_schemas.SesjaCreateSchema):
                 #urzadzenie_id: int, uzytkownik_id: int):
    db_sesja = models.Sesja(nazwa_sesji=sesja.nazwa_sesji,
                            start_sesji=sesja.start_sesji,
                            koniec_sesji=sesja.koniec_sesji,
                            czy_aktywna=sesja.czy_aktywna,
                            dlugosc_trwania_w_s=sesja.dlugosc_trwania_w_s)#, urzadzenie_id=urzadzenie_id, uzytkownik_id=uzytkownik_id)
    db.add(db_sesja)
    db.commit()
    db.refresh(db_sesja)
    return db_sesja


def delete_sesja(db: Session, sesje_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(models.Sesja).filter(models.Sesja.id == sesje_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunieto rekord o podanym id"
        return  result_str
    except Exception as e:
        result_str = "wystapil blad przy usuwaniu rekordu"+str(sesje_id)
        return result_str


def delete_all_sesje(db: Session):
    wszystkie_rekordy = db.query(models.Sesja)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto"
    else:
        return None