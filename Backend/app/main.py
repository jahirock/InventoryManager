from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import products, users
from app import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.createDBTables()
    yield

app = FastAPI(
    root_path="/v1",
    lifespan=lifespan
)

app.include_router(products.router)

app.include_router(users.router)

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}


