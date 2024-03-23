import json
import functools
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .. import utils
from .. import middleware
from .. import constants as CONSTANTS
from ..utils import get_db

router = APIRouter()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window"
)

def plan_based_rate_limiter(f): # return await limiter.limit(LIMITS[plan_type])(f)(*args, **kwargs)
    """
    A decorator that applies rate limiting based on the plan type specified in the JWT claims.
    """
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        Authorize = kwargs["Authorize"]
        Authorize.jwt_required()
        
        plan_type = Authorize.get_raw_jwt()["plan_type"]
        
        @limiter.limit(CONSTANTS.LIMITS[plan_type], key_func=Authorize.get_jwt_subject)
        @functools.wraps(f)
        async def todecorate(*args, **kwargs):
            return await f(*args, **kwargs)
        return await todecorate(*args, **kwargs)

    return wrapper

@router.get("/query/{query_type}")
@plan_based_rate_limiter
async def handle_request(query_type: str, request: Request, response: Response, Authorize: AuthJWT = Depends()):
    return {"data": await middleware.dispatch(query_type, utils.hashabledict(request.query_params))}
    
@router.post("/auth")
async def handle_auth(request: Request, Authorize: AuthJWT = Depends(), 
                      db: Session = Depends(get_db)):
    data = await request.json()

    if not (auth_key:=data.get("auth-key")) or not (key:=crud.get_key_from_value(db, auth_key)): 
        return {"msg": "Unauthorized."}
    
    return {"access_token": Authorize.create_access_token(subject=auth_key,
                                                      user_claims={"plan_type": key.plan})}