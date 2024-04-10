from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from . import login_required
from .. import crud
from ..schemas import KeyBase, KeyPurchaseRequest
from ..utils import get_db



router = APIRouter(prefix="/keys", tags=["keys"])

@router.post("/token")
@login_required
async def handle_key_auth(request: Request, key: KeyBase, Authorize: AuthJWT = Depends(), 
                      db: Session = Depends(get_db)):
    req_key = key.key
    
    if not (db_key:=crud.get_key_from_value(db, req_key)):
        return JSONResponse(content={"msg":"Invalid key"}, status_code=401)
    
    return JSONResponse(content={"access_token":Authorize.create_access_token(subject=db_key.key,
                                                    user_claims={"plan_type": db_key.plan})})

@router.post("/purchase")
@login_required
async def handle_key_purchase(request: Request, key: KeyPurchaseRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    req_plan = key.plan
    req_key = uuid4().hex

    crud.create_key(db, req_key, req_plan)
    return JSONResponse(content={"msg":"Key created successfully"})