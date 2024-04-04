# "here be dragons"

import functools
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi_another_jwt_auth import AuthJWT

from .. import constants as CONSTANTS

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window"
)

def query_plan_based_rate_limiter(f): # return await limiter.limit(LIMITS[plan_type])(f)(*args, **kwargs)
    """
    A decorator that applies rate limiting based on the plan type specified in the JWT claims.
    This decorator should be applied only to query endpoints (eg. /query/earthquake)
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