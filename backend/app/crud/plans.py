from sqlalchemy.orm import Session

from .. import models


def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.IDPlan == plan_id).first()

def get_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plan).offset(skip).limit(limit).all()