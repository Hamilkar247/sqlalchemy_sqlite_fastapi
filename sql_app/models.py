from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base  # może z kropką przed database?


class Uzytkownik(Base):
    __tablename__ = "zbior_uzytkownikow"

    id = Column(Integer, primary_key=True, index=True)
    imie_nazwisko = Column(String(75))
    email = Column(String(100), unique=True)
    hashed_password = Column(String(50))
    stanowisko = Column(String(75))
    opis = Column(String(100))
    uprawnienia = Column(String(50))
    zbior_sesji = relationship("Sesja", back_populates="uzytkownik", passive_deletes=True)


class Sesja(Base):
    __tablename__ = "zbior_sesji"

    id = Column(Integer, primary_key=True, index=True)
    nazwa_sesji = Column(String(80))  # może unique?
    start_sesji = Column(String(80))
    koniec_sesji = Column(String(80))
    czy_aktywna = Column(Boolean)
    dlugosc_trwania_w_s = Column(String(40))
    uzytkownik_id = Column(Integer, ForeignKey("zbior_uzytkownikow.id",
                                               ondelete="CASCADE"))  # , nullable=False)
    urzadzenie_id = Column(Integer, ForeignKey("zbior_urzadzen.id"))
    uzytkownik = relationship("Uzytkownik", back_populates="zbior_sesji")
    urzadzenie = relationship("Urzadzenie", back_populates="zbior_sesji")
    zbior_paczek_danych = relationship("PaczkaDanych", back_populates="sesja", passive_deletes=True)


class PaczkaDanych(Base):
    __tablename__ = "zbior_paczek_danych"

    id = Column(Integer, primary_key=True, index=True)
    czas_paczki = Column(String(50))  # moze do dodania pola z datą
    kod_statusu = Column(String(50))
    numer_seryjny = Column(String(50))
    sesja_id = Column(Integer, ForeignKey("zbior_sesji.id", ondelete="CASCADE"))
    # back_populates - patrz nazwa atrybutow w WartoscPomiaruSensora
    zbior_wartosci_pomiarow_sensorow = relationship("WartoscPomiaruSensora",
                                                    back_populates="paczka_danych", passive_deletes=True)
    sesja = relationship("Sesja", back_populates="zbior_paczek_danych")


class WartoscPomiaruSensora(Base):
    __tablename__ = "zbior_wartosci_pomiarow_sensorow"

    id = Column(Integer, primary_key=True, index=True)
    wartosc = Column(String(50))
    litery_porzadkowe = Column(String(50))
    paczka_danych_id = Column(Integer, ForeignKey(
        "zbior_paczek_danych.id", ondelete="CASCADE")
                             , nullable=False
                             )

    paczka_danych = relationship("PaczkaDanych", back_populates="zbior_wartosci_pomiarow_sensorow")


class Urzadzenie(Base):
    __tablename__ = "zbior_urzadzen"

    id = Column(Integer, primary_key=True, index=True)
    nazwa_urzadzenia = Column(String(50), unique=True)
    # nie jestem pewien czy powinno być unique czy nie
    numer_seryjny = Column(String(50), unique=True)
    zbior_sensorow = relationship("Sensor", back_populates="urzadzenie", passive_deletes=True)
    zbior_sesji = relationship("Sesja", back_populates="urzadzenie")


class Sensor(Base):
    __tablename__ = "zbior_sensorow"

    id = Column(Integer, primary_key=True, index=True)
    litery_porzadkowe = Column(String(10))
    parametr = Column(String(50))
    wspolczynniki_kalibracyjne = Column(String(25))
    min = Column(String(25))
    max = Column(String(25))
    jednostka = Column(String(20))
    status_sensora = Column(String(25))
    urzadzenie_id = Column(Integer, ForeignKey(
        "zbior_urzadzen.id", ondelete="CASCADE")
                           , nullable=False)
    urzadzenie = relationship("Urzadzenie", back_populates="zbior_sensorow")


class DekoderStatusu(Base):
    __tablename__ = "zbior_statusow"

    id = Column(Integer, primary_key=True, index=True)
    kod = Column(String(25), unique=True)
    liczba_dziesietna = Column(Integer, unique=True)
    opis_kodu = Column(String(200))
