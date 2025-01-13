from sqlalchemy.orm import Session
from app.models.databaseTablesOrm import ProductOrm
from app.models.productModel import Product

def getAllProducts(db:Session, skip: int = 0, limit: int = 0) -> list[ProductOrm]:
    return db.query(ProductOrm).order_by(ProductOrm.id).offset(skip).limit(limit).all()

def getProductById(db:Session, id:int) -> ProductOrm | None:
    return db.query(ProductOrm).filter(ProductOrm.id == id).first()

def createProduct(db:Session, product: Product) -> ProductOrm:
    prod = ProductOrm(
        name=product.name, 
        description=product.description, 
        price=product.price,
        stock = product.stock
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)

    return prod

def updateProduct(db:Session, product:Product) -> None:
    prod = getProductById(db, product.id)
    
    prod.name = product.name
    prod.description = product.description
    prod.price = product.price
    prod.stock = product.stock

    db.commit()

def deleteProduct(db:Session, id:int):
    prod = getProductById(db, id)
    db.delete(prod)
    db.commit()