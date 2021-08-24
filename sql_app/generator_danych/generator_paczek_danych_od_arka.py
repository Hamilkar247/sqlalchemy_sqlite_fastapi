from datetime import datetime
from random import randrange
import json


def generate_json_paczka():
    numery_seryjny = ["AXZFS213", "FWQ1000", "QW320D"]
    sn = numery_seryjny[randrange(0, 3)]
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