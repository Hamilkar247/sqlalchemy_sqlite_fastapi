from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base   # może z kropką przed database?


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Uzytkownik(Base):
    __tablename__ = "zbior_uzytkownikow"

    id = Column(Integer, primary_key=True, index=True)
    imie_nazwisko = Column(String)
    email = Column(String)
    stanowisko = Column(String)
    opis = Column(String)
    uprawnienia = Column(String)


class Sesja(Base):
    __tablename__ = "zbior_sesji"

    id = Column(Integer, primary_key=True, index=True)
    nazwa_sesji = Column(String)
    start_sesji = Column(String)
    koniec_sesji = Column(String)
    czy_aktywna = Column(Boolean)
    dlugosc_trwania_w_s = Column(String)
    urzadzenie_id = Column(Integer, ForeignKey("zbior_urzadzen"))
    uzytkownik_id = Column(Integer, ForeignKey("zbior_uzytkownikow"))

    urzadzenie = relationship("Urzadzenie", backpopulates="zbior_sesji")
    uzytkownik = relationship("Uzytkownik", backpopulates="zbior_sesji")


class PaczkaDanych(Base):
    __tablename__ = "zbior_paczek_danych"

    id = Column(Integer, primary_key=True, index=True)
    czas_paczki = Column(String) # do dodania pola z datą
    kod_statusu = Column(String)
    numer_seryjny = Column(String)
    sesja_id = Column(Integer, ForeignKey("zbior_sesji.id"))

    sesja = relationship("Sesja", backpopulates="zbior_paczek_danych")


class WartoscPomiaruSensora(Base):
    __tablename__ = "zbior_wartosci_pomiarow_sensora"

    id = Column(Integer, primary_key=True, index=True)
    wartosc = Column(String)
    litery_porzadkowe = Column(String)
    paczka_danych_id = Column(Integer, ForeignKey("zbior_paczek_danych.id"))

    paczka_danych = relationship("PaczkaDanych", backpopulates="zbior_wartosci_pomiarow_sensora")


class Urzadzenie(Base):
    __tablename__ = "zbior_urzadzen"

    id = Column(Integer, primary_key=True, index=True)
    nazwa_urzadzenia = Column(String)
    numer_seryjny = Column(String)


class Sensor(Base):
    __tablename__ = "zbior_sensorow"

    id = Column(Integer, primary_key=True, index=True)
    litery_porzadkowe = Column(String)
    parametr = Column(String)
    kalibr_wspolczynnika = Column(String) #może zewnetrzna klasa ?
    min = Column(String)
    max = Column(String)
    jednostka = Column(String)
    status_sensora = Column(String)
    urzadzenie_id = Column(Integer, ForeignKey("zbior_urzadzen.id"))

    urzadzenie = relationship("Urzadzenie", backpopulates="zbior_sensorow")

