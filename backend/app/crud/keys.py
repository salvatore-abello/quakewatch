from sqlalchemy.orm import Session
from .. import models, schemas

def get_key(db: Session, key_id: int):
    return db.query(models.Key).filter(models.Key.IDKey == key_id).first()

def get_keys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Key).offset(skip).limit(limit).all()

def create_key(db: Session, key: schemas.KeyCreate):
    db_key = models.Key(key=key.key, owner=key.user, plan=key.plan)

    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    return db_key

def get_key_from_value(db: Session, key: str):
    return db.query(models.Key).filter(models.Key.key == key).first()