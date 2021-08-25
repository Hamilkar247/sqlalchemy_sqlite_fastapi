from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import dekoder_statusu_schemas


def get_zbior_dekoderow_statusu(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DekoderStatusu).offset(skip).limit(limit).all()


def create_dekodera_statusu(db: Session, dekoder_statusu: dekoder_statusu_schemas.DekoderStatusuCreateSchema):
    db_dekoder_statusu = models.DekoderStatusu(
        kod=dekoder_statusu.kod,
        liczba_dziesietna=dekoder_statusu.liczba_dziesietna,
        opis_kodu=dekoder_statusu.opis_kodu
    )
    db.add(db_dekoder_statusu)
    db.commit()
    #db.refresh()
    return db_dekoder_statusu


def delete_dekoder_statusu(db: Session, dekoder_statusu_id: int):
    result_str = ""
    try:
        obj_to_delete = db.query(models.DekoderStatusu).filter(models.DekoderStatusu.id == dekoder_statusu_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        db.refresh()
        result_str = "usunieto rekord o podanym id"
    except Exception as e:
        result_str = "wystąpił przy usuwaniu rekordu" + str(dekoder_statusu_id)
        return result_str


def delete_all_dekodery_statusu(db: Session):
    wszystkie_rekordy = db.query(models.DekoderStatusu)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        db.refresh()
        return "usunieto"
    else:
        return None
