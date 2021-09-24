import os
from distutils.util import strtobool
from os.path import join, dirname

import uvicorn
from dotenv import load_dotenv


def get_boolean_value_from_string(string):
    print(f"ahoj {string}")
    if string is not None:
        if string.lower() in ["true"]:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    str_path_to_env = ".env"
    print(str_path_to_env)
    load_dotenv(str_path_to_env)
    host = os.environ.get("HOST")
    port_uvicorn = int(os.environ.get("UVICORN_PORT"))
    reload = get_boolean_value_from_string(os.environ.get("RELOAD"))
    debug = get_boolean_value_from_string(os.environ.get("DEBUG"))
    workers = int(os.environ.get("WORKERS"))
    print(port_uvicorn)
    print(reload)
    print(debug)
    print(workers)
    uvicorn.run("sql_app.main:app", host=host, port=port_uvicorn, reload=reload, debug=debug) #, workers=3) #workers)
    print("ahoj!")
