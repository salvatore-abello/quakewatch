from .schemas import *


class ErrorResponse(BaseModel): 
    detail: str

class KeyResponse(BaseModel): # TODO Use a class like this as a Base model
    msg: str
    data: Key | None

class NReqResponse(BaseModel):
    msg: str
    requests: int
    percentage: float