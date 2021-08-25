from datetime import datetime

from sqlalchemy.orm import Session
from sql_app import models
from sql_app.schemas_package import sesja_schemas


def get_sesja(db: Session, sesja_id: int):
    return db.query(models.Sesja).filter(models.Sesja.id == sesja_id).first()


def get_zbior_sesji(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sesja).offset(skip).limit(limit).all()


def zwroc_aktywne_sesje(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sesja).filter(models.Sesja.czy_aktywna==True).offset(skip).limit(limit).all()


def zakoncz_sesje(db: Session, sesja_id: int):
    find_sesje = db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True, models.Sesja.id == sesja_id).first()
    #print(find_sesje.start_sesji)
    #return find_sesje
    if find_sesje is not None:
        now = datetime.now()
        print(f"now={now}")
        dt_string = now.strftime("%d/%m/%y %H:%M:%S")
        print(f"data i czas = {dt_string}")
        dlugosc_sesji_w_s = "nie do okreslenia"
        koniec_sesji=dt_string
        try:
            start_timestamp = datetime.strptime(find_sesje.start_sesji, "%d/%m/%y %H:%M:%S").timestamp()
            end_timestamp=now.timestamp()
            print(end_timestamp-start_timestamp)
            dlugosc_sesji_w_s=round(end_timestamp-start_timestamp)
            print(dlugosc_sesji_w_s)
        except Exception as e:
            print("start_sesja: "+str(find_sesje))
            print("zmienna start_sesja nie przechowuje daty")
            dlugosc_sesji_w_s="nie do okreslenia"

        find_update_sesje = db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True, models.Sesja.id == sesja_id) \
            .update({
            models.Sesja.czy_aktywna: False,
            models.Sesja.dlugosc_trwania_w_s: dlugosc_sesji_w_s,
            models.Sesja.koniec_sesji: koniec_sesji
            })
        print("---------")
        print(find_update_sesje)
        db.commit()
        print("---------")
        return find_update_sesje
    else:
        return None


def update_status_sesji_czy_aktywna(db: Session, sesja_id: int, nowa_wartosc_boolean: bool):
    find_sesja = db.query(models.Sesja).filter(models.Sesja.id==sesja_id, models.Sesja.id==sesja_id).all()
    find_sesja.update()


def create_sesja(db: Session, sesja: sesja_schemas.SesjaCreateSchema):
    # urzadzenie_id: int, uzytkownik_id: int):
    db_sesja = models.Sesja(nazwa_sesji=sesja.nazwa_sesji,
                            start_sesji=str(datetime.now().strftime("%d/%m/%y %H:%M:%S")),
                            koniec_sesji="trwa",
                            czy_aktywna=True,
                            dlugosc_trwania_w_s="trwa")  # , urzadzenie_id=urzadzenie_id, uzytkownik_id=uzytkownik_id)
    db.add(db_sesja)
    db.commit()
    db.refresh(db_sesja)
    return db_sesja


def create_sesja_dla_uzytkownika(uzytkownik_id: int, db: Session, sesja: sesja_schemas.SesjaCreateSchema):
    # urzadzenie_id: int, uzytkownik_id: int):
    db_sesja = models.Sesja(nazwa_sesji=sesja.nazwa_sesji,
                            start_sesji=str(datetime.now().strftime("%d/%m/%y %H:%M:%S")),
                            koniec_sesji="trwa",
                            czy_aktywna=True,
                            dlugosc_trwania_w_s="trwa",
                            uzytkownik_id=uzytkownik_id)  # , urzadzenie_id=urzadzenie_id, uzytkownik_id=uzytkownik_id)
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
        db.refresh()
        result_str = "usunieto rekord o podanym id"
        return result_str
    except Exception as e:
        result_str = "wystapil blad przy usuwaniu rekordu" + str(sesje_id)
        return result_str


def delete_all_sesje(db: Session):
    wszystkie_rekordy = db.query(models.Sesja)
    if wszystkie_rekordy is not None:
        wszystkie_rekordy.delete()
        db.commit()
        db.refresh()
        return "usunieto"
    else:
        return None
