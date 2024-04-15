from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr

    class Config:
        orm_mode = True

class User(UserBase):
    IDUser: int
    key: Optional["Key"]

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel): # We don't need name and surname to login
    email: str
    password: str

class PlanBase(BaseModel):
    IDPlan: int

class Plan(PlanBase):
    type: str

class KeyBase(BaseModel):
    key: str

class KeyCreate(KeyBase):
    plan: PlanBase
    user: User

class KeyPurchaseRequest(BaseModel): # Remove this?
    plan: PlanBase

    class Config:
        orm_mode = True

class Key(KeyBase):
    IDKey: int
    plan: Plan
    expiration_date: datetime

    class Config:
        orm_mode = True
