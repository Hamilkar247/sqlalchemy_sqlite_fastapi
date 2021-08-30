from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import uzytkownik_schemas


def get_uzytkownik(db: Session, uzytkownik_id: int):
    return db.query(models.Uzytkownik).filter(models.Uzytkownik.id == uzytkownik_id).first()


def get_zbior_uzytkownikow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Uzytkownik).offset(skip).limit(limit).all()


def get_uzytkownik_by_email(db: Session, email: str):
    return db.query(models.Uzytkownik).filter(models.Uzytkownik.email == email).first()


def create_uzytkownik(db: Session, uzytkownik: uzytkownik_schemas.UzytkownikCreateSchema):
    fake_hashed_password = uzytkownik.hashed_password + "notreallyhashed"
    db_uzytkownik = models.Uzytkownik(imie_nazwisko=uzytkownik.imie_nazwisko,
                                      email=uzytkownik.email,
                                      hashed_password=fake_hashed_password,
                                      stanowisko=uzytkownik.stanowisko,
                                      opis=uzytkownik.opis,
                                      uprawnienia=uzytkownik.uprawnienia)
    db.add(db_uzytkownik)
    db.commit()
    db.refresh(db_uzytkownik)
    return db_uzytkownik


def delete_uzytkownik(db: Session, uzytkownik_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(models.Uzytkownik).filter(models.Uzytkownik.id == uzytkownik_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = "usunięto użytkowniku o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystąpił błąd przy usuwaniu uzytkownika "+str(uzytkownik_id)
        return result_str


def delete_all_uzytkownicy(db: Session):
    wszystkie_rekordy = db.query(models.Uzytkownik)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        return "usunieto wszystkich użytkowników"
    else:
        return None
