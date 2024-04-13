from sqlalchemy.orm import Session
from .. import models, schemas
from .. import utils


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.IDUser == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def check_login(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not utils.check_psw(user.password, db_user.password):
        return False
    return db_user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, 
                          name=user.name, 
                          surname=user.surname,
                          password=utils.hash_psw(user.password))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user