from fastapi import FastAPI
from app.routers import products

app = FastAPI(
    root_path="/v1"
)


app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


