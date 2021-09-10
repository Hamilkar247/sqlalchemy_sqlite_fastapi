import logging
import sys
import traceback
from datetime import datetime
import subprocess
import json
import os
from generator_danych import generator_paczek_danych_od_arka


def execute_bash_command(bashCommand: str):
    print(f"bashCommand: {bashCommand}")
    stream = os.popen(bashCommand)
    output = stream.read()
    return output


def get_urzadzenie_o_numerze_seryjnym(numer_seryjny):
    bashCommand = """
    curl -X 'GET' \
    'http://127.0.0.1:8000/urzadzenia/numer_seryjny={var_numer_seryjny}' \
    -H 'accept: application/json'
    """.format(var_numer_seryjny=numer_seryjny)
    return execute_bash_command(bashCommand)


def post_paczke_danych_dla_sesji(id_sesji, kod_statusu, numer_seryjny):
    bashCommand = """\
    curl -X 'POST' 'http://127.0.0.1:8000/paczki_danych/id_sesji={var_id_sesji}' -H 'accept: application/json' -H 'Content-Type: application/json' \
    -d ' {{  \
    "kod_statusu": "{var_kod_statusu}", \
    "numer_seryjny": "{var_numer_seryjny}"\
    }} '
    """.format(var_id_sesji=id_sesji, var_kod_statusu=kod_statusu, var_numer_seryjny=numer_seryjny)
    return execute_bash_command(bashCommand)


def get_paczke_danych__bez_sesji_dla_numeru_seryjnego(numer_seryjny):
    bashCommand = """
    curl -X 'GET' \
      'http://127.0.0.1:8000/paczki_danych/bez_sesji/numer_seryjny={var_numer_seryjny}' \
      -H 'accept: application/json'
    """.format(var_numer_seryjny=numer_seryjny)
    return execute_bash_command(bashCommand)


def post_pierwsza_paczke_danych__bez_sesji_dla_numeru_seryjnego(numer_seryjny, kod_statusu):
    bashCommand = """
    curl -X 'POST' \
      'http://127.0.0.1:8000/paczki_danych/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{{ \
      "kod_statusu": "{var_kod_statusu}", \
      "numer_seryjny": "{var_numer_seryjny}"\
    }}'
    """.format(var_numer_seryjny=numer_seryjny, var_kod_statusu=kod_statusu)
    return execute_bash_command(bashCommand)


def update_paczke_danych__bez_sesji_dla_numeru_seryjnego(numer_seryjny, kod_statusu):
    bashCommand = """
     curl -X 'PUT' \
       'http://127.0.0.1:8000/paczki_danych/zmien/brak_sesji/numer_seryjny_urzadzenia={var_numer_seryjny}' \
       -H 'accept: application/json' \
       -H 'Content-Type: application/json' \
       -d '{{  \
       "kod_statusu": "{var_kod_statusu}" \
       }}'
     """.format(var_numer_seryjny=numer_seryjny, var_kod_statusu=kod_statusu)
    return execute_bash_command(bashCommand)


def delete_stare_wartosci_paczki(id_paczki):
    bashCommand = """
     curl -X 'DELETE' \
       'http://127.0.0.1:8000/wartosci_pomiarowe_sensora/delete/id_paczki={var_id_paczki}' \
       -H 'accept: application/json'
     """.format(var_id_paczki=id_paczki)
    return execute_bash_command(bashCommand)


def post_nowa_wartosc_pomiaru_sensora_dla_paczki_o_id(id_paczki, wartosc, litery_porzadkowe):
    bashCommand = """
    curl -X 'POST' \
   'http://127.0.0.1:8000/wartosci_pomiarowe_sensora/id_paczki={var_id_paczki}' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{{
    "wartosc": "{var_wartosc}",
    "litery_porzadkowe": "{var_litery_porzadkowe}"
    }}'
    """.format(var_id_paczki=id_paczki, var_wartosc=wartosc, var_litery_porzadkowe=litery_porzadkowe)
    return execute_bash_command(bashCommand)


def get_aktywna_sesja_dla_urzadzenia_o_id(id_urzadzenia):
    bashCommand = """
    curl -X 'GET' \
    'http://127.0.0.1:8000/sesje/aktywna_sesja/urzadzenie_id={var_urzadzenie_id}' \
    -H 'accept: application/json'
    """.format(var_urzadzenie_id=id_urzadzenia)
    return execute_bash_command(bashCommand)


def send_curl_paczka_create(id_sesji, kod_statusu, numer_seryjny):
    print("****** send_curl_paczka_create *******")
    print(f"id_sesji: {id_sesji}")
    if id_sesji is not None:
        print("******** jest aktywną sesji ***********")
        ## uwaga gdy uzywasz format stylu ucieczka z klamrowych nawiasów jest poprzez podwojenie
        return post_paczke_danych_dla_sesji(id_sesji=id_sesji,
                                            kod_statusu=kod_statusu,
                                            numer_seryjny=numer_seryjny)
    elif id_sesji is None:
        print("******** nie ma aktywnej sesji *********")
        # sprawdzamy czy jest istnieje już paczka dla tego urządzenia, jak tak - to ją zaktualizujemy
        output = get_paczke_danych__bez_sesji_dla_numeru_seryjnego(numer_seryjny=numer_seryjny)
        ###### sprawdzam id paczki
        id_paczki = None
        try:
            paczka = json.loads(output)
            print(paczka)
            id_paczki = None
            if type(paczka) is list:
                if len(paczka) > 0:
                    id_paczki = paczka[0]["id"]
            else:
                id_paczki = paczka["id"]
        except KeyError as k:
            print("nie znaleziono takiej paczki w bazie danych!")
            print(k)
            print(traceback.print_exc())
        if id_paczki is None:
            print("nie ma paczki  dla tego urządzenia")
            return post_pierwsza_paczke_danych__bez_sesji_dla_numeru_seryjnego(kod_statusu=kod_statusu,
                                                                               numer_seryjny=numer_seryjny)
        else:
            print("************* ")
            # update paczki
            print(update_paczke_danych__bez_sesji_dla_numeru_seryjnego(kod_statusu=kod_statusu,
                                                                       numer_seryjny=numer_seryjny))
            # usun zastane wartosci paczki
            print(delete_stare_wartosci_paczki(id_paczki))
        return output


def send_curl_wartosc_pomiaru_sensora(id_paczki, litery_porzadkowe, wartosc):
    print("****** send_curl_wartosc_pomiaru_sensora *******")
    return post_nowa_wartosc_pomiaru_sensora_dla_paczki_o_id(id_paczki=id_paczki,
                                                             litery_porzadkowe=litery_porzadkowe,
                                                             wartosc=wartosc)


def get_aktywna_sesje_urzadzenia(id_urzadzenia):
    dane = get_aktywna_sesja_dla_urzadzenia_o_id(id_urzadzenia=id_urzadzenia)
    data = json.loads(dane)  # [1:-1])
    if data is not None:
        return int(data['id'])
    else:
        return None


def get_id_urzadzenia_dla_tej_paczki(numer_seryjny):
    print(numer_seryjny)
    dane_zapytania = get_urzadzenie_o_numerze_seryjnym(numer_seryjny=numer_seryjny)
    # print(output[1:-1])
    print("------------------")
    print(dane_zapytania)
    rekord = json.loads(dane_zapytania)  # [1:-1])
    # print(data)
    try:
        print(rekord['id'])
        return int(rekord['id'])
    except KeyError as e:
        print(f"KeyError wystąpił - {e}")
        print(traceback.print_exc())
        return None


def generuje_paczki_danych():
    json_arek_daty = generator_paczek_danych_od_arka.generate_json_paczka()
    print(json_arek_daty)
    # serializacja
    dane = json.loads(json_arek_daty)
    return dane


def dane_od_arka():
    dane = generuje_paczki_danych()
    numer_seryjny = dane['sn']
    print(f"-----------%%%%------------ {numer_seryjny} ----------%%%------")
    id_urzadzenia = get_id_urzadzenia_dla_tej_paczki(numer_seryjny=numer_seryjny)
    if id_urzadzenia is not None:
        print(f"id_urzadzenia: {id_urzadzenia}")
        id_sesji = get_aktywna_sesje_urzadzenia(id_urzadzenia=id_urzadzenia)
        print(f"id_sesji: {id_sesji}")

        # paczka
        kod_statusu = dane['kod']

        czas_paczki = str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
        wart = dane["wart"]
        print(kod_statusu)
        print(numer_seryjny)
        print(czas_paczki)
        output_json_z_id_paczki = send_curl_paczka_create(id_sesji=id_sesji, kod_statusu=kod_statusu,
                                                          numer_seryjny=numer_seryjny)
        dane_paczki = json.loads(output_json_z_id_paczki)
        print(f"dane_paczki {dane_paczki}")
        if type(dane_paczki) == list:
            if len(dane_paczki)>0:
                id_paczki = dane_paczki[0]["id"]
        else:
            id_paczki = dane_paczki["id"]
        # wart
        for key, value in wart.items():
            print(key, value)
            litery_porzadkowe = key
            wartosc = value
            send_curl_wartosc_pomiaru_sensora(id_paczki=id_paczki, litery_porzadkowe=litery_porzadkowe, wartosc=wartosc)
    else:
        print("Nie ma id_urzadzenia")


dane_od_arka()
