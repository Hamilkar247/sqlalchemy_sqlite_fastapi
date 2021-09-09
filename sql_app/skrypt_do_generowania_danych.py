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
    print("------------")
    print(output)
    print("------------")
    return output


def send_curl_paczka_create(id_sesji, kod_statusu, numer_seryjny):
    print("****** send_curl_paczka_create *******")
    print(f"id_sesji: {id_sesji}")
    if id_sesji is not None:
        print("******** jest aktywną sesji ***********")
        ## uwaga gdy uzywasz format stylu ucieczka z klamrowych nawiwasów jestpoprzez podwojenie
        bashCommand = """\
        curl -X 'POST' 'http://127.0.0.1:8000/paczki_danych/id_sesji={var_id_sesji}' -H 'accept: application/json' -H 'Content-Type: application/json' \
        -d ' {{  \
        "kod_statusu": "{var_kod_statusu}", \
        "numer_seryjny": "{var_numer_seryjny}"\
        }} '
        """.format(var_id_sesji=id_sesji, var_kod_statusu=kod_statusu, var_numer_seryjny=numer_seryjny)
        output = execute_bash_command(bashCommand)
        return output
    elif id_sesji is None:
        print("******** nie ma aktywnej sesji *********")
        # get paczke do updatu
        bashCommand = """
        curl -X 'GET' \
          'http://127.0.0.1:8000/paczki_danych/bez_sesji/numer_seryjny={var_numer_seryjny}' \
          -H 'accept: application/json'
        """.format(var_numer_seryjny=numer_seryjny)
        output = execute_bash_command(bashCommand)
        ###### sprawdzam id paczki
        id_paczki = None
        try:
            paczka = json.loads(output)
            id_paczki = paczka["id"]
        except KeyError as k:
            print("nie znaleziono paczki w bazie danych!")
            print(k)
            print(traceback.print_exc())
        if id_paczki is None:
            print("nie ma paczki nie zrzeszonej dla tego urządzenia")
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
            output = execute_bash_command(bashCommand)
            return output
        else:
            print("************* ")
            # update paczki
            bashCommand = """
            curl -X 'PUT' \
              'http://127.0.0.1:8000/paczki_danych/zmien/brak_sesji/numer_seryjny_urzadzenia={var_numer_seryjny}' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -d '{{  \
              "kod_statusu": "{var_kod_statusu}" \
              }}'
            """.format(var_numer_seryjny=numer_seryjny, var_kod_statusu=kod_statusu)
            print(execute_bash_command(bashCommand))
            # usun zastane wartosci paczki
            bashCommand = """
            curl -X 'DELETE' \
              'http://127.0.0.1:8000/wartosci_pomiarowe_sensora/delete/id_paczki={var_id_paczki}' \
              -H 'accept: application/json'
            """.format(var_id_paczki=id_paczki)
            print(execute_bash_command(bashCommand))
        return output


def send_curl_wartosc_pomiaru_sensora(id_paczki, litery_porzadkowe, wartosc):
    print("****** send_curl_wartosc_pomiaru_sensora *******")
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
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------")
    print(output)
    print("------------")
    return output


def get_aktywna_sesje_urzadzenia(id_urzadzenia):
    bashCommand = """
    curl -X 'GET' \
    'http://127.0.0.1:8000/sesje/aktywna_sesja/urzadzenie_id={var_urzadzenie_id}' \
    -H 'accept: application/json'
    """.format(var_urzadzenie_id=id_urzadzenia)
    # zwroc uwage powyzej ze dalem limit=1 przez co dostane w odpowiedzi tylko jedna aktywna sesje
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------------")
    print(output)  # [1:-1]
    print("------------------")
    data = json.loads(output)  # [1:-1])
    if data is not None:
        return int(data['id'])
    else:
        return None


def get_id_urzadzenia_dla_tej_paczki(numer_seryjny):
    print(numer_seryjny)
    bashCommand = """
    curl -X 'GET' \
    'http://127.0.0.1:8000/urzadzenia/numer_seryjny={var_numer_seryjny}' \
    -H 'accept: application/json'
    """.format(var_numer_seryjny=numer_seryjny)
    print(bashCommand)
    # zwroc uwage powyzej ze dalem limit=1 przez co dostane w odpowiedzi tylko jedna aktywna sesje
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------------")
    print(output)
    # print(output[1:-1])
    print("------------------")
    print(output[1:-1])
    data = json.loads(output)  # [1:-1])
    # print(data)
    try:
        print(data['id'])
        return int(data['id'])
    except KeyError as e:
        print(f"KeyError wystąpił - {e}")
        print(traceback.print_exc())
        return None


def dane_od_arka():
    json_arek_data = generator_paczek_danych_od_arka.generate_json_paczka()
    print(json_arek_data)

    # deserializacja
    data = json.loads(json_arek_data)

    # wydrukuj typ(?)
    # print("Type:", type(data))

    numer_seryjny = data['sn']
    print(f"-----------%%%%------------ f{numer_seryjny} ----------%%%------")
    id_urzadzenia = get_id_urzadzenia_dla_tej_paczki(numer_seryjny)
    if id_urzadzenia is not None:
        print(f"id_urzadzenia: {id_urzadzenia}")
        id_sesji = get_aktywna_sesje_urzadzenia(id_urzadzenia)
        print(f"id_sesji: {id_sesji}")

        # paczka
        kod_statusu = data['kod']

        czas_paczki = str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
        wart = data["wart"]
        print(kod_statusu)
        print(numer_seryjny)
        print(czas_paczki)
        output_json_z_id_paczki = send_curl_paczka_create(id_sesji, kod_statusu, numer_seryjny)
        data_paczki = json.loads(output_json_z_id_paczki)
        id_paczki = data_paczki["id"]
        # wart
        for key, value in wart.items():
            print(key, value)
            litery_porzadkowe = key
            wartosc = value
            send_curl_wartosc_pomiaru_sensora(id_paczki, litery_porzadkowe, wartosc)
    else:
        print("Nie ma id_urzadzenia")


dane_od_arka()
