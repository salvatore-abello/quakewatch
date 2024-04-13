from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from . import get_current_user
from .. import redis_client
from .. import crud
from ..schemas import KeyPurchaseRequest, User
from ..utils import get_db
from ..responses import * # TODO: Remove this


router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("/purchase", response_model=KeyResponse, responses={
                 400: {"model": ErrorResponse, "description": "Invalid plan"},
                 409: {"model": ErrorResponse, "description": "You already have an active plan"}
})
async def handle_key_purchase(request: Request, key: KeyPurchaseRequest, db: Session = Depends(get_db), 
                              Authorize: AuthJWT = Depends(), current_user: User = Depends(get_current_user),
                              csrf_token: str = Header(..., alias="X-CSRF-TOKEN")):
    
    """ Purchase a key """

    res = crud.create_key(db, key.plan, current_user)
    return {"msg": "Key purchased successfully", "data": res}

@router.get("/status", response_model=NReqResponse)
async def handle_get_key_status(request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    

    if hasattr(current_user, "key") and current_user.key \
        and current_user.key.expiration_date < datetime.now():
        crud.delete_key(db, current_user.key)
        raise HTTPException(status_code=400, detail="Key has expired")

    nreqs, percentage = redis_client.get_requests_number_from_key(current_user.key) \
        if hasattr(current_user, "key") and current_user.key else (0, 0)
    return {"msg": "ok", "requests": nreqs, "percentage": percentage}


@router.delete("/delete", response_model=KeyResponse, responses={
    400: {"model": ErrorResponse, "description": "You do not have an active plan"}
})
async def handle_key_delete(request: Request, db: Session = Depends(get_db),
                            Authorize: AuthJWT = Depends(), current_user: User = Depends(get_current_user),
                            csrf_token: str = Header(..., alias="X-CSRF-TOKEN")):
    
    """ Delete a key and its data """
    
    crud.delete_key_from_user(db, current_user)
    redis_client.delete_key(current_user.key)
    return {"msg": "Unsubscribed successfully", "data": None}
