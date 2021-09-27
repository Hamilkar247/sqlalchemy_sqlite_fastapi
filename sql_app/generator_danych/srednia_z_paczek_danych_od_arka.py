import json
import os
import shutil
import sys
import traceback
from json import JSONDecodeError
from time import sleep

from dotenv import load_dotenv

from skrypt_do_generowania_i_dodawania_paczek_danych_w_bazie import dane_od_arka


def get_value_dotenv(name_to_value):
    if name_to_value is not None:
        wartosc=os.environ.get(name_to_value)
        if wartosc is not None:
            print("wartosc "+name_to_value+":"+wartosc)
            return wartosc
        else:
            print(" nie ma wartosci dla zmiennej "+name_to_value)


def srednia_z_elementow_pomiarow(dict_wart_srednia, dict_wart_paczki):
    if dict_wart_srednia is type(dict) and dict_wart_paczki is type(dict):
        for litera, wartosc in dict_wart_paczki.items():
            dict_wart_srednia[litera] = (int(dict_wart_srednia[litera])+int(wartosc))/2
    return dict_wart_srednia


def srednia_z_dotychaczasowych_pomiarow(path):
    curr_dir=os.curdir
    print(path)
    print(os.listdir(path))
    sn = None
    kod = None
    dict_wart_srednia = None
    dict_wart_paczki = None
    for name_json_file in os.listdir(path):
        print(name_json_file)
        json_data = None
        with open(path+"/"+name_json_file, "r") as jsonfile:
            json_data = json.load(jsonfile)
        if json_data is not None:
            try:
                print(json_data)
                if json_data is not None:
                    if sn is None:
                        sn = json_data["sn"]
                    if kod is None:
                        kod = json_data["kod"]
                    if dict_wart_srednia is None:
                        dict_wart_srednia = json_data["wart"]
                    else:
                        dict_wart_paczki = json_data["wart"]
                        dict_wart_srednia = srednia_z_elementow_pomiarow(dict_wart_srednia, dict_wart_paczki)
            except JSONDecodeError as e:
                traceback.print_exc()
                print(f"Wystapil blad typu JSONDecodeError: {e}")
    print(dict_wart_srednia)
    print("usunieto pliki z pomiarami")
    shutil.rmtree(path)
    value = {
        "sn": sn,
        "wart": dict_wart_srednia,
        "kod": kod
    }
    dane_od_arka(value)


def generate_json_paczka():
    ### usrednianie
    load_dotenv("../.."+"/.env")
    liczba_elementow_do_usredniania = int(os.environ.get("USREDNIANIE"))
    list_of_sn = []
    ahoj=0
    while True:
        print(f"folder: "+os.curdir+"/paczki/")
        urzadzenia_foldery = os.listdir(os.curdir+"/paczki/")
        for folder in urzadzenia_foldery:
            ahoj = ahoj + 1
            print(folder)
            if len(os.listdir(os.curdir+"/paczki/"+folder)) < liczba_elementow_do_usredniania:
                print("za malo danych")
            else:
                print("wystarczająco danych")
                path = os.curdir+"/paczki/"+folder
                srednia_z_dotychaczasowych_pomiarow(path=path)
        print("zzzzzz")
        sleep(3)


generate_json_paczka()