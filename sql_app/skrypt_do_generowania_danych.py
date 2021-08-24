from datetime import datetime
import subprocess
import json
import os
from generator_danych import generator_paczek_danych_od_arka


def send_curl_paczka_create(id_sesji, kod_statusu, numer_seryjny, czas_paczki):
    ## uwaga gdy uzywasz format stylu ucieczka z klamrowych nawiwasów jestpoprzez podwojenie
    bashCommand="""\
    curl -X 'POST' 'http://127.0.0.1:8000/paczki_danych/id_sesji={var_id_sesji}' -H 'accept: application/json' -H 'Content-Type: application/json' \
    -d ' {{  \
    "kod_statusu": "{var_kod_statusu}", \
    "numer_seryjny": "{var_numer_seryjny}", \
    "czas_paczki": "{var_czas_paczki}" \
    }} '
    """.format(var_id_sesji=id_sesji,var_kod_statusu=kod_statusu, var_numer_seryjny=numer_seryjny, var_czas_paczki=czas_paczki)
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------")
    print(output)
    print("------------")
    return output


def send_curl_wartosc_pomiaru_sensora(id_paczki, litery_porzadkowe, wartosc):
    bashCommand="""
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


def dane_od_arka():
    json_arek_data = generator_paczek_danych_od_arka.generate_json_paczka()
    print(json_arek_data)

    #deserializacja
    data = json.loads(json_arek_data)

    # wydrukuj typ(?)
    #print("Type:", type(data))

    id_sesji=5
    #paczka
    kod_statusu = data['kod']
    numer_seryjny = data['sn']
    czas_paczki = str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    wart = data["wart"]
    print(kod_statusu)
    print(numer_seryjny)
    print(czas_paczki)
    output_json_z_id_paczki=send_curl_paczka_create(id_sesji, kod_statusu, numer_seryjny, czas_paczki)
    data_paczki = json.loads(output_json_z_id_paczki)
    id_paczki = data_paczki["id"]
    #wart
    for key, value in wart.items():
        print(key, value)
        litery_porzadkowe = key
        wartosc = value
        send_curl_wartosc_pomiaru_sensora(id_paczki, litery_porzadkowe, wartosc)


dane_od_arka()
