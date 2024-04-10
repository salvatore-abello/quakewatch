from sqlalchemy.orm import Session
from .. import models, schemas
from ..schemas import User, Plan
from uuid import uuid4

from datetime import datetime, timedelta

from ..utils import setup_logging

def get_key(db: Session, key_id: int):
    return db.query(models.Key).filter(models.Key.IDKey == key_id).first()

def get_keys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Key).offset(skip).limit(limit).all()

def create_key(db: Session, plan: Plan, current_user: User) -> models.Key:
    req_plan_id = plan.IDPlan

    req_plan = db.query(models.Plan).filter(models.Plan.IDPlan == req_plan_id).first()

    if req_plan is None:
        return {"msg": "Invalid plan"}

    current_user_db = db.query(models.User).filter(models.User.IDUser == current_user.IDUser).first()
    
    if current_user_db.key:
        return {"msg": "You already have an active plan"}

    new_key = models.Key(key=str(uuid4()), user=current_user_db, plan=req_plan, expiration_date=datetime.now() + timedelta(days=30))
    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return {"key": new_key}

def get_key_from_value(db: Session, key: str):
    return db.query(models.Key).filter(models.Key.key == key).first()