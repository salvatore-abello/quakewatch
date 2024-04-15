from fastapi import APIRouter, Request, Response, Depends

from . import plan_based_rate_limiter
from .. import utils
from .. import middleware
from .. import utils


router = APIRouter(prefix="/query", tags=["query"])

@router.get("/{query_type}")
@plan_based_rate_limiter
async def handle_request(query_type: str, key: str, response: Response, request: Request, 
                         db = Depends(utils.get_db)):
    """ Retrieve API data """
    return {"data": await middleware.dispatch(query_type, utils.hashabledict(request.query_params))}

@router.get("/history/{query_type}") # CHANGE THIS FUNCTION NAME
async def handle_request(query_type: str, request: Request, response: Response):
    """ Retrieve an example of an API call """
    return {"data": middleware.get_free_earthquake_data()}