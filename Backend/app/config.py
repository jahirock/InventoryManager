import os

DBUSER = os.getenv('INV_DB_USER')
DBPASS = os.getenv('INV_DB_PASS')
DBHOST = os.getenv('INV_DB_HOST')
DBNAME = os.getenv('INV_DB_NAME')

if not DBUSER or not DBPASS or not DBHOST or not DBNAME:
    raise ValueError("No se encontraron las variables de entorno para la base de datos")

SECRET_KEY = "aeac1f35333f6ceb4a4eaee6f253b211599cd885d474bb7b9ac3a945466ab178"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

origins = [
    "*",
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.1.66:8000"
]