from typing import Annotated
from pydantic import BaseModel, StringConstraints

# Esquema para la creación de un usuario
class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]
    password: str

# Esquema para devolver la información del usuario
class UserOut(BaseModel):
    id: int
    username: Annotated[str, StringConstraints(max_length=50)]
    password: str
    disabled: bool

    class Config:
        orm_mode = True