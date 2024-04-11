from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from . import get_current_user
from .. import crud
from ..schemas import Key, KeyPurchaseRequest, KeyCreate, User
from ..utils import get_db, setup_logging
from .. import models
from ..responses import ErrorResponse, KeyResponse


router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("/purchase", response_model=KeyResponse, responses={
                 400: {"model": ErrorResponse, "description": "Invalid plan"},
                 409: {"model": ErrorResponse, "description": "You already have an active plan"}
})
async def handle_key_purchase(request: Request, key: KeyPurchaseRequest, db: Session = Depends(get_db), 
                              Authorize: AuthJWT = Depends(), current_user: User = Depends(get_current_user),
                              csrf_token: str = Header(..., alias="X-CSRF-TOKEN")):

    res = crud.create_key(db, key.plan, current_user)
    return {"msg": "Key purchased successfully", "data": res}

@router.delete("/delete", response_model=KeyResponse, responses={
    400: {"model": ErrorResponse, "description": "You do not have an active plan"}
})
async def handle_key_delete(request: Request, db: Session = Depends(get_db),
                            Authorize: AuthJWT = Depends(), current_user: User = Depends(get_current_user),
                            csrf_token: str = Header(..., alias="X-CSRF-TOKEN")):
    
    crud.delete_key(db, current_user)
    return {"msg": "Unsubscribed successfully", "data": None}
