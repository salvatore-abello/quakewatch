from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from . import get_current_user
from .. import crud
from ..schemas import KeyBase, KeyPurchaseRequest, KeyCreate, User
from ..utils import get_db, setup_logging
from .. import models


from fastapi.encoders import jsonable_encoder # TODO: DELETE THIS


router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("/purchase")
async def handle_key_purchase(request: Request, key: KeyPurchaseRequest, db: Session = Depends(get_db), 
                              Authorize: AuthJWT = Depends(), current_user: User = Depends(get_current_user),
                              csrf_token: str = Header(..., alias="X-CSRF-TOKEN")):

    new_key = crud.create_key(db, key.plan, current_user)
    if "key" in new_key:
        return JSONResponse(content={"msg": "Key purchased successfully", "key": new_key["key"].key})
    return JSONResponse(content={"msg": new_key["msg"]}, status_code=400)