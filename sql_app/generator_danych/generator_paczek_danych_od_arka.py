from datetime import datetime
from random import randrange
import json


# przyklad
# {"sn": "AXZFS213", "wart": {"a": 3, "b": 4, "c": 3, "z": 3}, "kod": "0000000"}

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


def main():
    print(generate_json_paczka())
      (generate_json_paczka())
    print()


main()