from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Response, Depends

from . import query_plan_based_rate_limiter
from .. import utils
from .. import middleware


router = APIRouter(prefix="/query")

@router.get("/{query_type}")
@query_plan_based_rate_limiter
async def handle_request(query_type: str, request: Request, response: Response, Authorize: AuthJWT = Depends()):
    return {"data": await middleware.dispatch(query_type, utils.hashabledict(request.query_params))}

@router.get("/history/{query_type}")
async def handle_request(query_type: str, request: Request, response: Response):
    return {"data": await middleware.get_earthquake_history(utils.hashabledict(request.query_params))}