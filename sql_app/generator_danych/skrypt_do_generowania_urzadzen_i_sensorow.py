import json
import os

from dotenv import load_dotenv

str_path_to_env = "../../.env"
load_dotenv(str_path_to_env)
UVICORN_HOST = os.environ.get("UVICORN_HOST")
UVICORN_PORT = os.environ.get("UVICORN_PORT")
HTTPS_HTTP = os.environ.get("HTTPS_HTTP")
basic_url = HTTPS_HTTP+"://"+UVICORN_HOST+":"+UVICORN_PORT


def execute_bash_command(bashCommand: str):
    print(f"bashCommand: {bashCommand}")
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------")
    print(output)
    print("------------")
    return output


# {"sn": "FWQ1000", "wart": {"a": 2, "b": 7, "c": 5, "z": 5}, "kod": "0000000"}
def post_curl_urzadzenia(nazwa_urzadzenia, numer_seryjny):
    bashCommand = """\
    curl -X 'POST' \
      '{basic_url}/urzadzenia/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{{\
      "nazwa_urzadzenia": "{var_nazwa_urzadzenia}",\
      "numer_seryjny": "{var_numer_seryjny}"\
    }}'
    """.format(basic_url=basic_url, var_nazwa_urzadzenia=nazwa_urzadzenia, var_numer_seryjny=numer_seryjny)
    output = execute_bash_command(bashCommand)
    return output


def post_curl_sensor(id_urzadzenia, litery_porzadkowe, parametr, wspolczynnik_kalibracyjny, min, max, jednostka, status_sensora):
    print(f"id_urzadzenia: {id_urzadzenia}")
    bashCommand = """
    curl -X 'POST'\\
    '{basic_url}/sensory/id_urzadzenia={{id_urzadzenia}}?urzadzenie_id={var_id_urzadzenia}' \\
    -H 'accept: application/json' \\
    -H 'Content-Type: application/json' \\
    -d '{{
    "litery_porzadkowe": "{var_litery_porzadkowe}",
    "parametr": "{var_parametr}",
    "wspolczynniki_kalibracyjne": "{var_wsp_kalibr}",
    "min": "{var_min}",
    "max": "{var_max}",
    "jednostka": "{var_jednostka}",
    "status_sensora": "{var_status_sensora}"
    }}'
    """.format(basic_url=basic_url,
               var_id_urzadzenia=id_urzadzenia,
               var_litery_porzadkowe=litery_porzadkowe,
               var_parametr=parametr, var_wsp_kalibr=wspolczynnik_kalibracyjny,
               var_min=min, var_max=max,
               var_jednostka=jednostka,
               var_status_sensora=status_sensora)
    output = execute_bash_command(bashCommand)


def get_urzadzenie_id_by_numer_seryjny(numer_seryjny):
    bashCommand = """
    curl -X 'GET' \
    '{basic_url}/urzadzenia/numer_seryjny={var_numer_seryjny}' \
    -H 'accept: application/json' 
    """.format(basic_url=basic_url,
               var_numer_seryjny=numer_seryjny)
    print(bashCommand)
    stream = os.popen(bashCommand)
    output = stream.read()
    print("------------")
    print(output)
    print("------------")
    try:
        data = json.loads(output)
        print(data)
        print(data['id'])
        return int(data['id'])
    except KeyError as e:
        return None


# {"sn": "FWQ1000", "wart": {"a": 2, "b": 7, "c": 5, "z": 5}, "kod": "0000000"}
def tworzenie_pierwszego_urzadzenia_i_sensorow():
    numer_seryjny = "FWQ1000"
    nazwa_urzadzenia = "bomilwkar"
    czy_istnieje_urzadzenie_o_tym_numerze_seryjnym = get_urzadzenie_id_by_numer_seryjny(numer_seryjny)
    print(f"czy istnieje ju?? takie urzadzenie? {czy_istnieje_urzadzenie_o_tym_numerze_seryjnym}")
    if czy_istnieje_urzadzenie_o_tym_numerze_seryjnym is None:
        post_curl_urzadzenia(numer_seryjny=numer_seryjny, nazwa_urzadzenia=nazwa_urzadzenia)
        id_urzadzenia = get_urzadzenie_id_by_numer_seryjny(numer_seryjny)
        litery_porzadkowe = ["a", "b", "c", "z"]
        parametr = ["temperatura", "pm2.5", "pm5", "napiecie"]
        wspolczynnik_kalibracyjny = ["1;4", "0;1", "0:3", "1:2"]
        min = ["-15", "-15", "-20", "-5"]
        max = ["5", "30", "30", "5"]
        jednostka = ["stopnie Celsjusza", "smogowe", "smogowe", "volty"]
        status_sensora = ["aktywny", "aktywny", "aktywny", "aktywny"]
        iteracja = [0, 1, 2, 3]
        for numer in iteracja:
            post_curl_sensor(id_urzadzenia=id_urzadzenia,
                             litery_porzadkowe=litery_porzadkowe[numer],
                             parametr=parametr[numer],
                             wspolczynnik_kalibracyjny=wspolczynnik_kalibracyjny[numer],
                             min=min[numer],
                             max=max[numer],
                             jednostka=jednostka[numer],
                             status_sensora=status_sensora[numer])
    else:
        print("urzadzenie o podanym numerze seryjnym ju?? istnieje")


def tworzenie_drugiego_urzadzenia_i_sensorow():
    numer_seryjny = "AMD1000"
    nazwa_urzadzenia = "tabnit"
    czy_istnieje_urzadzenie_o_tym_numerze_seryjnym = get_urzadzenie_id_by_numer_seryjny(numer_seryjny)
    print(f"czy istnieje ju?? takie urzadzenie? {czy_istnieje_urzadzenie_o_tym_numerze_seryjnym}")
    if czy_istnieje_urzadzenie_o_tym_numerze_seryjnym is None:
        post_curl_urzadzenia(numer_seryjny=numer_seryjny, nazwa_urzadzenia=nazwa_urzadzenia)
        id_urzadzenia = get_urzadzenie_id_by_numer_seryjny(numer_seryjny)
        litery_porzadkowe = ["a", "b", "c", "z"]
        parametr = ["stezenie wodoru", "hydrowod??r", "alkohol etylowy", "napiecie"]
        wspolczynnik_kalibracyjny = ["1;4", "0;1", "0:3", "1:2"]
        min = ["-15", "-15", "-20", "-5"]
        max = ["5", "30", "30", "5"]
        jednostka = ["procent", "obj??to????", "procent", "volty"]
        status_sensora = ["aktywny", "aktywny", "aktywny", "aktywny"]
        iteracja = [0, 1, 2, 3]
        for numer in iteracja:
            post_curl_sensor(id_urzadzenia=id_urzadzenia,
                             litery_porzadkowe=litery_porzadkowe[numer],
                             parametr=parametr[numer],
                             wspolczynnik_kalibracyjny=wspolczynnik_kalibracyjny[numer],
                             min=min[numer],
                             max=max[numer],
                             jednostka=jednostka[numer],
                             status_sensora=status_sensora[numer])


tworzenie_pierwszego_urzadzenia_i_sensorow()
tworzenie_drugiego_urzadzenia_i_sensorow()
