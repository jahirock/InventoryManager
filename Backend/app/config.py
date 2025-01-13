from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.models.databaseTablesOrm import Base

import os

DBUSER = os.getenv('INV_DB_USER')
DBPASS = os.getenv('INV_DB_PASS')
DBHOST = os.getenv('INV_DB_HOST')
DBNAME = os.getenv('INV_DB_NAME')

if not DBUSER or not DBPASS or not DBHOST or not DBNAME:
    raise ValueError("No se encontraron las variables de entorno para la base de datos")

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=f"{DBUSER}",
    password=f"{DBPASS}",
    host=f"{DBHOST}",
    database=f"{DBNAME}",
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