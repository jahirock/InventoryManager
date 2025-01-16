from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_active_user
from app.models.databaseModels import Product, User
from app.schemas.meta import Meta
from app.schemas.product import Product as ProductSchema
from app import database

from app.crud import product as productService

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

INVALID_INPUT = "Datos recibidos incorrectos."
NAME_EXISTS = "El nombre ya existe."
NOT_FOUND = "El producto no existe."

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_INPUT)
    
    prod:Product = productService.getProductByName(db=db, name=product.name)
    if(prod):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NAME_EXISTS)
    
    return productService.createProduct(db=db, product=product)

@router.put("/", status_code=status.HTTP_200_OK, response_model=Meta)
async def updateProduct(
    productIn: ProductSchema, 
    currentUser: User = Depends(get_current_active_user),
    db: Session = Depends(database.getDBSession)
):
    if not productIn.name or not productIn.category or not productIn.price > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_INPUT)
    
    productDB = productService.getProductById(db=db, id=productIn.id)

    if productDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    
    productSameName = productService.getProductByName(db=db, name=productIn.name)
    if(productSameName and productSameName.id != productIn.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NAME_EXISTS)

    productService.updateProduct(db=db, product=productIn)    
    return Meta(message="Producto actualizado.")

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Meta)
async def deleteProduct(
    id: int, 
    currentUser: User = Depends(get_current_active_user),
    db: Session = Depends(database.getDBSession)
):
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_INPUT)
    
    product = productService.getProductById(db=db, id=id)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    productService.deleteProduct(db=db, id=id)

    return Meta(message="Producto eliminado.")