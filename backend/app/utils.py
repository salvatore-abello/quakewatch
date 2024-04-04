import logging
import bcrypt
from functools import wraps

from .constants import LOGGER_NAME
from .database import SessionLocal


class hashabledict(dict):
	""" A subclass of the built-in dict class that supports hashing. """
	def __key(self) -> tuple:
		return tuple((k,self[k]) for k in sorted(self))
	def __hash__(self) -> int:
		return hash(self.__key())
	def __eq__(self, other) -> bool:
		return self.__key() == other.__key()

def setup_logging() -> logging.Logger:
	logger = logging.getLogger(LOGGER_NAME)
	logger.setLevel(logging.WARNING)
 
	formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
 
	logger.addHandler(handler)
	return logger

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_psw(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def check_psw(password: str, hashed: str) -> bool:
	return bcrypt.checkpw(password.encode('utf-8'), hashed.encode())