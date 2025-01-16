from sqlalchemy.orm import Session

from app.models.databaseModels import User

def getUserByName(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

def createUser(db:Session, username:str, password:str) -> User | None:
    db_usuario = User(username=username, password=password, disabled=False)
    db.add(db_usuario)
    db.commit()

    return db_usuario
