from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

# DIVIDE THIS INTO SEPARATE FILES INSIDE A PACKAGE

class User(Base):
    __tablename__ = "Users"

    IDUser = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    name = Column(String(30))
    surname = Column(String(30))
    password = Column(String(60))

    key = relationship("Key", uselist=False, back_populates="user")

class Plan(Base):
    __tablename__ = "Plans"

    IDPlan = Column(Integer, primary_key=True)
    type = Column(String(16))
    
    keys = relationship("Key", back_populates="plan")

class Key(Base):
    __tablename__ = "Keys"

    IDKey = Column(Integer, primary_key=True)
    key = Column(String(36), unique=True, index=True)
    expiration_date = Column(DateTime)  # Add the expiration date column

    CODPlan = Column(Integer, ForeignKey("Plans.IDPlan"))
    CODUser = Column(Integer, ForeignKey("Users.IDUser"))

    user = relationship("User", back_populates="key")
    plan = relationship("Plan", back_populates="keys")