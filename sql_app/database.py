import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from dotenv import load_dotenv

#dla sqlite
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


#dla mysql
#czynnik ?charset=utf8mb4 jest dla polskich znaków ( i inne literki nie angielskie)
str_path_to_env = "../.env"
load_dotenv(str_path_to_env)
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://db:db@localhost/db"
print(os.environ.get("DB_NAME"))
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{user}:{password}@{host}/{name_database}?charset=utf8mb4".format(
    host="localhost:"+os.environ.get("MYSQL_PORT"),
    name_database=os.environ.get("DB_DATABASE"),#"db",#os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
    )

##MYSQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    convert_unicode=True
    #echo=False
)
args, kwargs = engine.dialect.create_connect_args(engine.url)
print(args, kwargs)

##SQLITE
##check_same_thread - tylko dla sqlite
#engine = create_engine(
#    SQLALCHEMY_DATABASE_URL # SQLITE:, connect_args={"check_same_thread": False}
#)

#dla sqlite3 wymagane by dzialal cascade_delete
#event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

