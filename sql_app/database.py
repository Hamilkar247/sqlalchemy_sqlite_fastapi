from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://db:db@localhost/db"


##check_same_thread - tylko dla sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL # SQLITE:, connect_args={"check_same_thread": False}
)

#dla sqlite3 wymagane by dzialal cascade_delete
#event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

