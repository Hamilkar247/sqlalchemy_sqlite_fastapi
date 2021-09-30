from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from sql_app import models
from sql_app.format_danych import FormatDaty
from sql_app.models import Sesja, PaczkaDanych
from sql_app.schemas_package import sesja_schemas


################ CREATE ##################
def create_sesja(db: Session,
                                            sesja: sesja_schemas.SesjaCreateSchemat,
                                            urzadzenie_id: Optional[int] = None,
                                            uzytkownik_id: Optional[int] = None
                                            ):
    db_sesja = models.Sesja(
        nazwa_sesji=sesja.nazwa_sesji,
        start_sesji=str(datetime.now().strftime("%d/%m/%y %H:%M:%S")),
        koniec_sesji="trwa",
        czy_aktywna=True,
        dlugosc_trwania_w_s="trwa",
        uzytkownik_id=uzytkownik_id,
        urzadzenie_id=urzadzenie_id
    )
    db.add(db_sesja)
    db.commit()
    db.refresh(db_sesja)
    return db_sesja


################# GET ####################
def get_sesja_o_id(db: Session, sesja_id: int):
    return db.query(models.Sesja).filter(models.Sesja.id == sesja_id).first()


def get_zbior_sesji(db: Session, skip: Optional[int] = None, limit: Optional[int] = None):
    if limit != 1:
        return db.query(models.Sesja).offset(skip).limit(limit).all()
    else:
        return db.query(models.Sesja).offset(skip).limit(limit).first()


def get_sesja_dla_urzadzen_o_numerze_seryjnym(db: Session, numer_seryjny: str):
    return db.query(models.Sesja, models.Urzadzenie).filter(models.Sesja.urzadzenie_id == models.Urzadzenie.id).filter(
        models.Urzadzenie.numer_seryjny == numer_seryjny)


def zwroc_aktywne_sesje(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True).offset(skip).limit(limit).all()


def get_aktywna_sesja_urzadzenia_id(db: Session, urzadzenie_id: int):
    return db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True).\
        filter(models.Sesja.urzadzenie_id == urzadzenie_id).first()


def get_aktywna_sesja_urzadzenia_o_numerze_seryjnym(db: Session, numer_seryjny: str):
    return db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True).\
        filter(models.Sesja.urzadzenie_id == models.Urzadzenie.id).\
        filter(models.Urzadzenie.numer_seryjny == numer_seryjny).first()

    #ahoj=db.query(models.Urzadzenie).filter(models.Urzadzenie.numer_seryjny == numer_seryjny).all()
    #ajon=db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True).all() #\
    #print()
    #xwer=db.query(models.Urzadzenie).filter(models.Sesja.urzadzenie_id == models.Urzadzenie.id).
    #    \
    #    .filter(models.Sesja.czy_aktywna == True). \
    #    filter(models.Sesja.urzadzenie_id == models.Urzadzenie.id). \
    #    filter(models.Urzadzenie.numer_seryjny == numer_seryjny).all()


################# UPDATE ##########################3
def zakoncz_sesje(db: Session, sesja_id: int):
    find_sesje = db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True, models.Sesja.id == sesja_id).first()
    # print(find_sesje.start_sesji)
    # return find_sesje
    if find_sesje is not None:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%y %H:%M:%S")
        print(f"data i czas = {dt_string}")
        dlugosc_sesji_w_s = "nie do okreslenia"
        koniec_sesji = FormatDaty().obecny_czas()
        try:
            start_timestamp = datetime.strptime(find_sesje.start_sesji, "%d/%m/%y %H:%M:%S").timestamp()
            end_timestamp = now.timestamp()
            print(end_timestamp - start_timestamp)
            dlugosc_sesji_w_s = round(end_timestamp - start_timestamp)
            print(dlugosc_sesji_w_s)
        except Exception as e:
            print("start_sesja: " + str(find_sesje))
            print("zmienna start_sesja nie przechowuje daty")
            dlugosc_sesji_w_s = "nie do okreslenia"

        find_update_sesje = db.query(models.Sesja).filter(models.Sesja.czy_aktywna == True, models.Sesja.id == sesja_id) \
            .update(
            {
            models.Sesja.czy_aktywna: False,
            models.Sesja.dlugosc_trwania_w_s: dlugosc_sesji_w_s,
            models.Sesja.koniec_sesji: koniec_sesji
            }
        )
        print("---------")
        print(find_update_sesje)
        db.commit()
        print("---------")
        return find_update_sesje
    else:
        return None


def get_zbior_paczek_danych_dla_sesji_jedna_per_n(db: Session, sesja_id: int, jedna_per_n: int):
    print("ahoj")
    liczba = 0
    lista = []
    while True:
        print(f"liczba elementów {len(lista)}")
        element = db.query(Sesja).filter(PaczkaDanych.sesja_id == sesja_id).offset(liczba).first()
        print(element)
        if element is not None:
            lista.append(element)
        else:
            break
        liczba = liczba + jedna_per_n
    return lista


##################### DELETE ###############################3
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
    db_wszystkie_rekordy = db.query(models.Sesja)
    if db_wszystkie_rekordy is not None:
        db_wszystkie_rekordy.delete()
        db.commit()
        # db.refresh(db_wszystkie_rekordy)
        return "usunieto"
    else:
        return None
