from datetime import datetime
from random import randrange
import json


# przyklad
# {"sn": "AXZFS213", "wart": {"a": 3, "b": 4, "c": 3, "z": 3}, "kod": "0000000"}

def generate_json_paczka():
    numery_seryjny = "FWQ10100" #["AXZFS213", "FWQ1000", "QW320D"]
    sn = numery_seryjny #[randrange(0, 3)]
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

print(generate_json_paczka())
