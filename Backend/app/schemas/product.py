from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

class Product(BaseModel):

    id: int | None = None
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str, StringConstraints(max_length=140)]
    category: Annotated[str, StringConstraints(max_length=50)]
    price: float
    stock: int

    class Config:
        orm_mode = True