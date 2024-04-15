import datetime
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas


def get_key(db: Session, key_id: int):
    return db.query(models.Key).filter(models.Key.IDKey == key_id).first()

def get_keys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Key).offset(skip).limit(limit).all()

def delete_key_from_user(db: Session, user: schemas.User):
    user_db = db.query(models.User).filter(models.User.IDUser == user.IDUser).first()

    if not user_db.key:
        raise HTTPException(status_code=400, detail="You do not have an active plan")

    db.delete(user_db.key)
    db.commit()

    return True

def delete_key(db: Session, key: models.Key):
    db.delete(key)
    db.commit()

    return True

def create_key(db: Session, plan: schemas.Plan, current_user: schemas.User) -> models.Key:
    req_plan_id = plan.IDPlan

    req_plan = db.query(models.Plan).filter(models.Plan.IDPlan == req_plan_id).first()

    if req_plan is None:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    current_user_db = db.query(models.User).filter(models.User.IDUser == current_user.IDUser).first()
    
    if current_user_db.key:
        raise HTTPException(status_code=409, detail="You already have an active plan")

    new_key = models.Key(
        key=str(uuid4()), 
        user=current_user_db, 
        plan=req_plan, 
        expiration_date=datetime.datetime.now() + datetime.timedelta(days=30)
    )
    
    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return new_key

def get_key_from_value(db: Session, key: str):
    return db.query(models.Key).filter(models.Key.key == key).first()