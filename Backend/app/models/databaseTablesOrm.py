from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Float, Integer

class Base(DeclarativeBase):
    pass

class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(140))
    category: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)