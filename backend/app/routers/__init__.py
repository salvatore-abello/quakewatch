# "here be dragons"

import functools
from slowapi import Limiter
import slowapi
from slowapi.util import get_remote_address
import slowapi.util as TEST
from fastapi_another_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi_another_jwt_auth.exceptions import AuthJWTException
import jwt
from types import FunctionType

from .. import constants as CONSTANTS
from .. import crud
from ..utils import get_db, setup_logging

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{CONSTANTS.REDIS_HOST}:{CONSTANTS.REDIS_PORT}",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window"
)

def plan_based_rate_limiter(f): # return await limiter.limit(LIMITS[plan_type])(f)(*args, **kwargs)
    """
    A decorator that applies rate limiting based on the plan type specified in the JWT claims.
    """
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        request = kwargs["request"]
        db = kwargs["db"]

        key = request.query_params.get("key")
        db_key = crud.get_key_from_value(db, key)
        if not db_key:
            raise HTTPException(status_code=400, detail="Invalid key")

        if limiter._route_limits: # Hacky way to apply the rate limit only once per function call
            limiter._route_limits.clear()

        @limiter.limit(CONSTANTS.LIMITS[db_key.plan.type], key_func=lambda: db_key.key)
        @functools.wraps(f)
        async def todecorate(*args, **kwargs):
            return await f(*args, **kwargs)
        return await todecorate(*args, **kwargs)

    return wrapper

def get_current_user(request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db = next(get_db())
    logger = setup_logging()

    Authorize.jwt_required()

    sub = Authorize.get_jwt_subject()

    current_user = crud.get_user(db, sub)
    if not current_user:
        raise ValueError("Unauthorized")
    return current_user