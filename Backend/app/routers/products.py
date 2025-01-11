from fastapi import APIRouter
from app.models.product import Product
from app.models.meta import Meta 

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}}
)

products = []

products.append(Product("producto 1", 100.0))
products.append(Product("producto 2", 1000.0, 1))

@router.post("/")
async def addProduct():
    return Meta()

@router.get("/")
async def getProducts():
    return products

@router.put("/{id}")
async def updateProduct(id: int):
    return Meta("OK", f"Se actualizo el producto con id {id}")

@router.delete("/{id}")
async def deleteProduct(id: int): 
    return Meta("OK", f"Se elimino el producto con id {id}")