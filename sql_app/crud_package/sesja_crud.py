from sqlalchemy.orm import Session
from sql_app import models, schemas


def get_sesja(db: Session, sesja_id: int):
    return db.query(models.Sesja).filter(models.Sesja.id == sesja_id).first


def get_zbior_sesji(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sesja).offset(skip).limit(limit).all()


def create_sesja(db: Session, sesja: schemas.SesjaCreate,
                 urzadzenie_id: int, uzytkownik_id: int):
    db_sesja = models.Sesja(**sesja.dict(), urzadzenie_id=urzadzenie_id, uzytkownik_id=uzytkownik_id)
    db.add(db_sesja)
    db.commit()
    db.refresh(db_sesja)
    return db_sesja
