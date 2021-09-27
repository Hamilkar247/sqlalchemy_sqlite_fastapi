import os
import shutil
from datetime import datetime
from random import randrange
import json


# przyklad
# {"sn": "AXZFS213", "wart": {"a": 3, "b": 4, "c": 3, "z": 3}, "kod": "0000000"}
from time import sleep


def generate_pojedynczy_json_paczka():
    numery_seryjny = ["AMD1000", "FWQ1000"]
    sn = numery_seryjny[randrange(0, 2)]
    a = randrange(0, 9)
    b = randrange(0, 9)
    c = randrange(0, 9)
    z = randrange(0, 9)
    kod = "0000000"

    value = {
        "sn": sn,
        "wart": {
            "a": a,
            "b": b,
            "c": c,
            "z": z,
        },
        "kod": kod
    }

    return json.dumps(value)


def main():
    list_of_sn = []
    ahoj=0
    while True:
        ahoj = ahoj + 1
        packet_string = generate_pojedynczy_json_paczka()
        print(packet_string)
        json_data = json.loads(packet_string)
        if json_data not in list_of_sn:
            list_of_sn.append(json_data["sn"])
            if os.path.isdir("paczki/"+json_data["sn"]) is False:
                os.mkdir("paczki/"+json_data["sn"])
        list_of_file = os.listdir(os.curdir+"/paczki/"+json_data["sn"])
        print(list_of_file)
        with open("paczki/"+json_data["sn"]+"/"+str(ahoj)+"_"+json_data["sn"], "a+") as text_file:
            text_file.write(packet_string)
        sleep(1)


main()
