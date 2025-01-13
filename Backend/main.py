from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import productsRouter
from app.config import createDBTables

@asynccontextmanager
async def lifespan(app: FastAPI):
    createDBTables()
    yield

app = FastAPI(
    root_path="/v1",
    lifespan=lifespan
)

app.include_router(productsRouter.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


