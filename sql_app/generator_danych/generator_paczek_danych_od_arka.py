import os
from datetime import datetime
from random import randrange
import json


# przyklad
# {"sn": "AXZFS213", "wart": {"a": 3, "b": 4, "c": 3, "z": 3}, "kod": "0000000"}
from time import sleep


def generate_json_paczka():
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


def srednia_z_dotychaczasowych_pomiarow(path):
    curr_dir=os.curdir
    os.chdir(path)
    list_of_packet = os.listdir(path)
    json_dict=[]
    for file_with_packet in list_of_packet:
        with open(file_with_packet) as f:
            json_dict=f


def main():
    print(generate_json_paczka())
    list_of_sn = []
    ahoj=0
    while True:
        ahoj = ahoj + 1
        packet_string = generate_json_paczka()
        print(packet_string)
        json_data=json.loads(packet_string)
        if json_data["sn"] in list_of_sn:
            print("jeden")
            list_of_file = os.listdir(os.curdir+"/"+json_data["sn"])
            print(list_of_file)
            if len(list_of_file) < 5:
                with open(json_data["sn"]+"/"+str(ahoj)+"_"+json_data["sn"], "a+") as text_file:
                    text_file.write("Ahoj !" + "_")
            else:
                srednia_z_dotychaczasowych_pomiarow(path=os.curdir+"/"+json_data["sn"])
        else:
            print("dwa")
            list_of_sn.append(json_data["sn"])
            if os.path.isdir(json_data["sn"]) is False:
               os.mkdir(json_data["sn"])
        sleep(1)




main()