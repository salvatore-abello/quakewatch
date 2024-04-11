from .schemas import *


class ErrorResponse(BaseModel):
    detail: str

class KeyResponse(BaseModel):
    msg: str
    data: Key | None