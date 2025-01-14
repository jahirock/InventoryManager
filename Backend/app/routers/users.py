
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.security import authenticate_user, create_access_token, hash_password, verify_password, get_current_active_user
from app import database
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.crud import user 
from app.models.databaseModels import User
from app.schemas.meta import Meta
from app.auth.security import oauth2_scheme, credentials_exception, input_exception


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=Meta)
def register(usuario: UserCreate, db: Session = Depends(database.getDBSession)):
    if not usuario.username or not usuario.password:
        raise input_exception
    
    hashed_password = hash_password(usuario.password)
    user.createUser(db=db, username=usuario.username, password=hashed_password)
    return Meta(message="Usuario registrado exitosamente")

@router.post("/login", response_model=Token)
def login(usuario: UserCreate, db: Session = Depends(database.getDBSession)):
    if not usuario.username or not usuario.password:
        raise input_exception

    user = authenticate_user(db=db, username=usuario.username, password=usuario.password)
    if not user:
        raise credentials_exception
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.getDBSession)
):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
