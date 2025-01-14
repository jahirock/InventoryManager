from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_active_user
from app.models.databaseModels import User
from app.schemas.meta import Meta
from app.schemas.product import Product as ProductSchema
from app import database

from app.crud import product as productService

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def getProducts(skip: int = 0, limit: int = 20, db: Session = Depends(database.getDBSession)):
    data:list[ProductSchema] = productService.getAllProducts(db, skip=skip, limit=limit)
    return data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def addProduct(
    product: ProductSchema, 
    currentUser: User = Depends(get_current_active_user),
    db: Session = Depends(database.getDBSession)
):
    if not product.name or not product.category or not product.price > 0:
        raise HTTPException(status_code=400, detail='Invalid input')
    return productService.createProduct(db=db, product=product)

@router.put("/", status_code=status.HTTP_200_OK, response_model=Meta)
async def updateProduct(
    product: ProductSchema, 
    currentUser: User = Depends(get_current_active_user),
    db: Session = Depends(database.getDBSession)
):
    if not product.name or not product.category or not product.price > 0:
        raise HTTPException(status_code=400, detail='Invalid input')
    
    prod = productService.getProductById(db=db, id=product.id)

    if prod is None:
        raise HTTPException(status_code=404, detail='Product not found')

    productService.updateProduct(db=db, product=product)    
    return Meta(message="Product updated")

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Meta)
async def deleteProduct(
    id: int, 
    currentUser: User = Depends(get_current_active_user),
    db: Session = Depends(database.getDBSession)
):
    if not id:
        raise HTTPException(status_code=400, detail='Invalid input')
    
    product = productService.getProductById(db=db, id=id)

    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    productService.deleteProduct(db=db, id=id)

    return Meta(message="Product deleted")