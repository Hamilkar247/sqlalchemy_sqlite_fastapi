import os
from os.path import dirname, join
from time import sleep

from dotenv import load_dotenv

from skrypt_do_generowania_i_dodawania_paczek_danych_w_bazie import dane_od_arka

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)
Iteracja_dodania_paczki = os.environ.get("ITERACJA_DODANIA_PACZKI")
if Iteracja_dodania_paczki is not None:
    print(Iteracja_dodania_paczki)
    Iteracja_dodania_paczki = int(Iteracja_dodania_paczki)
else:
    print("nie ma wartosci w ITERACJA_DODANIA_PACZKI")


while True:
    dane_od_arka()
    sleep(Iteracja_dodania_paczki)
