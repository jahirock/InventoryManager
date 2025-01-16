from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.models.databaseModels import Base

from app import config

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=f"{config.DBUSER}",
    password=f"{config.DBPASS}",
    host=f"{config.DBHOST}",
    database=f"{config.DBNAME}",
    port=5432
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def getDBSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def createDBTables():
    Base.metadata.create_all(engine)