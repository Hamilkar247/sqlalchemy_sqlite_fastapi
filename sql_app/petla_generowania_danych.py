import os
from os.path import dirname, join
from time import sleep

from sql_app.generator_danych.skrypt_do_generowania_i_dodawania_paczek_danych_w_bazie import dane_od_arka
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
Iteracja_dodania_paczki = int(os.environ.get("ITERACJA_DODANIA_PACZKI"))
print(Iteracja_dodania_paczki)


while True:
    dane_od_arka()
    sleep(Iteracja_dodania_paczki)
