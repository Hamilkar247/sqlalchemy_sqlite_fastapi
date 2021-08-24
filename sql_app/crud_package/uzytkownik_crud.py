from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import uzytkownik_schemas


def get_uzytkownik(db: Session, uzytkownik_id: int):
    return db.query(models.Uzytkownik).filter(models.Uzytkownik.id == uzytkownik_id).first()


def get_zbior_uzytkownikow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Uzytkownik).offset(skip).limit(limit).all()


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
