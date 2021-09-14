import os
from distutils.util import strtobool
from os.path import join, dirname

import uvicorn
from dotenv import load_dotenv


def get_boolean_value_from_string(string):
    print(f"ahoj {string}")
    if string is not None:
        if string.lower in ["true", "True"]:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    dotenv_path = join("sql_app/"+dirname(__file__), ".env")
    print(dirname(__file__))
    load_dotenv(dotenv_path)
    host = os.environ.get("HOST")
    port_uvicorn = int(os.environ.get("UVICORN_PORT"))
    reload = get_boolean_value_from_string(os.environ.get("RELOAD"))
    debug = get_boolean_value_from_string(os.environ.get("DEBUG"))
    workers = int(os.environ.get("WORKERS"))
    print(port_uvicorn)
    print(reload)
    print(debug)
    print(workers)
    uvicorn.run("sql_app.main:app", host=host, port=port_uvicorn, reload=True, debug=True) #, workers=3) #workers)

