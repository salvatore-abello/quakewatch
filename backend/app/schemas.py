from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    IDUser: int
    key: Optional["Key"]

    class Config:
        orm_mode = True

class PlanBase(BaseModel):
    IDPlan: int

class Plan(PlanBase):
    type: str

class KeyBase(BaseModel):
    key: str

class KeyCreate(KeyBase):
    plan: PlanBase
    user: User

class KeyPurchaseRequest(BaseModel):
    plan: PlanBase

    class Config:
        orm_mode = True

class Key(KeyBase):
    IDKey: int
    plan: Plan
    expiration_date: datetime  # Add expiration_date field

    class Config:
        orm_mode = True
