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
    hashed_password = Column(String)
    stanowisko = Column(String)
    opis = Column(String)
    uprawnienia = Column(String)

    zbior_sesji = relationship("Sesja", back_populates="uzytkownik")


class Sesja(Base):
    __tablename__ = "zbior_sesji"

    id = Column(Integer, primary_key=True, index=True)
    nazwa_sesji = Column(String)
    start_sesji = Column(String)
    koniec_sesji = Column(String)
    czy_aktywna = Column(Boolean)
    dlugosc_trwania_w_s = Column(String)
    uzytkownik_id = Column(Integer, ForeignKey("zbior_uzytkownikow.id"))

    zbior_paczek_danych = relationship("PaczkaDanych", back_populates="sesja")
    uzytkownik = relationship("Uzytkownik", back_populates="zbior_sesji")
    #urzadzenie_id = Column(Integer, ForeignKey("zbior_urzadzen"))

    #urzadzenie = relationship("Urzadzenie", back_populates="zbior_sesji")


class PaczkaDanych(Base):
    __tablename__ = "zbior_paczek_danych"

    id = Column(Integer, primary_key=True, index=True)
    czas_paczki = Column(String) # do dodania pola z datą
    kod_statusu = Column(String)
    numer_seryjny = Column(String)
    sesja_id = Column(Integer, ForeignKey("zbior_sesji.id"))
    #back_populates - patrz nazwa atrybutow w WartoscPomiaruSensora
    zbior_wartosci_pomiarow_sensorow = relationship("WartoscPomiaruSensora", back_populates="paczka_danych")
    sesja = relationship("Sesja", back_populates="zbior_paczek_danych")

#    sesja = relationship("Sesja", back_populates="zbior_paczek_danych")


class WartoscPomiaruSensora(Base):
    __tablename__ = "zbior_wartosci_pomiarow_sensorow"

    id = Column(Integer, primary_key=True, index=True)
    wartosc = Column(String)
    litery_porzadkowe = Column(String)
    paczka_danych_id = Column(Integer, ForeignKey("zbior_paczek_danych.id"))

    paczka_danych = relationship("PaczkaDanych", back_populates="zbior_wartosci_pomiarow_sensorow")


#class Urzadzenie(Base):
#    __tablename__ = "zbior_urzadzen"
#
#    id = Column(Integer, primary_key=True, index=True)
#    nazwa_urzadzenia = Column(String)
#    numer_seryjny = Column(String)


class Sensor(Base):
    __tablename__ = "zbior_sensorow"

    id = Column(Integer, primary_key=True, index=True)
    litery_porzadkowe = Column(String)
    parametr = Column(String)
    #kalibr_wspolczynnika = Column(String) #może zewnetrzna klasa ?
    min = Column(String)
    max = Column(String)
    jednostka = Column(String)
    status_sensora = Column(String)
    #urzadzenie_id = Column(Integer, ForeignKey("zbior_urzadzen.id"))

    #urzadzenie = relationship("Urzadzenie", back_populates="zbior_sensorow")


#class WspolczynnikKalibracji(Base):
#    __tablename__ = "zbior_wspolczynnikow_kalibracji"
#
#    id = Column(Integer, primary_key=True, index=True)
#    litery_porzadkowa = Column(String)
#    wartosc = Column(String) # do konca nie wiem czy tu ma być float czy int czy cos innego - wiec tymczasowo string


class DekoderStatusu(Base):
    __tablename__ = "zbior_statusow"

    id = Column(Integer, primary_key=True, index=True)
    kod = Column(String, unique=True)
    liczba_dziesietna = Column(String, unique=True)
    opis_kodu = Column(String)