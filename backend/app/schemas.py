from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    surname: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    IDUser: int

    class Config:
        orm_mode = True

class PlanBase(BaseModel):
    type: int

class Plan(PlanBase):
    IDPlan: int

class KeyBase(BaseModel):
    key: str

class KeyCreate(KeyBase):
    user: User
    plan: Plan
    class Config:
        orm_mode = True

class Key(KeyBase):
    IDKey: int
    user: User

    class Config:
        orm_mode = True