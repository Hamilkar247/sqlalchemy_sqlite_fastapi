from sql_app import models
from sqlalchemy.orm import Session
from sql_app.schemas_package import wartosc_pomiaru_sensora_schemas


def get_wartosc_pomiaru_sensora(db: Session, wartosc_pomiaru_sensora_id: int):
    return db.query(models.WartoscPomiaruSensora).filter(models.WartoscPomiaruSensora.id == wartosc_pomiaru_sensora_id).first()


def get_zbior_wartosci_pomiarowych_sensorow(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WartoscPomiaruSensora).offset(skip).limit(limit).all()


def create_wartosc_pomiaru_sensora(db: Session, wartosc_pomiaru_sensora: wartosc_pomiaru_sensora_schemas):
    db_wartosc_pomiaru_sensora = models.WartoscPomiaruSensora(
        wartosc=wartosc_pomiaru_sensora.wartosc,
        litery_porzadkowe=wartosc_pomiaru_sensora.litery_porzadkowe
    )
    db.add(db_wartosc_pomiaru_sensora)
    db.commit()
    db.refresh(db_wartosc_pomiaru_sensora)
    return db_wartosc_pomiaru_sensora
