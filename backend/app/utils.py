import logging
from functools import wraps

from .constants import LOGGER_NAME


class hashabledict(dict):
	"""
	A subclass of the built-in dict class that supports hashing.
	This allows instances of hashabledict to be used as keys in dictionaries and elements in sets.
	"""
 
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
