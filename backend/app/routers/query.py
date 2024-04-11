from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Response, Depends

from . import plan_based_rate_limiter
from .. import utils
from .. import middleware


router = APIRouter(prefix="/query", tags=["query"])

@router.get("/{query_type}")
@plan_based_rate_limiter
async def handle_request(query_type: str, key: str, response: Response, request: Request):
    """ Retrieve API data """
    return {"data": await middleware.dispatch(query_type, utils.hashabledict(request.query_params))}

@router.get("/history/{query_type}") # CHANGE THIS FUNCTION NAME
async def handle_request(query_type: str, request: Request, response: Response):
    return {"data": await middleware.get_earthquake_history(utils.hashabledict(request.query_params))}