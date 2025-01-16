from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import products, users
from app import database
from app import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.createDBTables()
    yield

app = FastAPI(
    root_path="/v1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

app.include_router(users.router)

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}


