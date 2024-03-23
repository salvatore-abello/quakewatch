from sqlalchemy.orm import Session
from .. import models, schemas

from bcrypt import hashpw, gensalt

def hash_password(password: str) -> str:
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    return hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.IDUser == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, 
                          name=user.name, 
                          surname=user.surname, 
                          password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user