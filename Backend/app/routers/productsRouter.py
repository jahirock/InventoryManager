from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.meta import Meta
from app.models.productModel import Product
from app.config import getDBSession

from app.services import productService as service

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def getProducts(skip: int = 0, limit: int = 20, db: Session = Depends(getDBSession)) -> list[Product]:
    data:list[Product] = service.getAllProducts(db, skip=skip, limit=limit)
    return data

@router.post("/", status_code=status.HTTP_201_CREATED)
async def addProduct(product: Product, db: Session = Depends(getDBSession)) -> Product:
    if not product.name or not product.category or not product.price > 0:
        raise HTTPException(status_code=400, detail='Invalid input')
    return service.createProduct(db=db, product=product)

@router.put("/", status_code=status.HTTP_200_OK)
async def updateProduct(product: Product, db: Session = Depends(getDBSession)) -> Meta:
    if not product.name or not product.category or not product.price > 0:
        raise HTTPException(status_code=400, detail='Invalid input')
    
    prod = service.getProductById(db=db, id=product.id)

    if prod is None:
        raise HTTPException(status_code=404, detail='Product not found')

    service.updateProduct(db=db, product=product)    
    return Meta(message="Product updated")

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def deleteProduct(id: int, db: Session = Depends(getDBSession)) -> Meta:
    if not id:
        raise HTTPException(status_code=400, detail='Invalid input')
    
    product = service.getProductById(db=db, id=id)

    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    service.deleteProduct(db=db, id=id)

    return Meta(message="Product deleted")