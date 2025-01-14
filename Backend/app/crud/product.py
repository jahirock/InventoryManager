from sqlalchemy.orm import Session
from app.models.databaseModels import Product as ProductModel
from app.schemas.product import Product as ProductSchena

def getAllProducts(db:Session, skip: int = 0, limit: int = 0) -> list[ProductModel]:
    return db.query(ProductModel).order_by(ProductModel.id).offset(skip).limit(limit).all()

def getProductById(db:Session, id:int) -> ProductModel | None:
    return db.query(ProductModel).filter(ProductModel.id == id).first()

def createProduct(db:Session, product: ProductSchena) -> ProductModel:
    prod = ProductModel(
        name=product.name, 
        description=product.description, 
        category=product.category,
        price=product.price,
        stock = product.stock
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)

    return prod

def updateProduct(db:Session, product:ProductSchena) -> None:
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