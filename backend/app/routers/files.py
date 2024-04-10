import os
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi import APIRouter, Request, Response, Depends

from .. import constants


router = APIRouter(prefix="/files", tags=["files"])

# USE ONLY HARDCODED FILENAMES
# DO NOT USE USER INPUT !!!!!!

@router.get("/map.js")
async def handle_request(request: Request, response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        plan_type = Authorize.get_raw_jwt()["plan_type"]

        if plan_type not in constants.LIMITS or plan_type == "basic":
            raise ValueError("Invalid plan type / Basic plan does not have access to the custom map")

        file = "paid-map.js"
    except (AuthJWTException, ValueError, KeyError):
        file = "free-map.js"

    with open(os.path.join("/app", "static", "files", file), "r") as f:
        return Response(content=f.read(), media_type="application/javascript")
    
@router.get("/map.html")
async def handle_request(request: Request, response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        plan_type = Authorize.get_raw_jwt()["plan_type"]

        if plan_type not in constants.LIMITS:
            raise ValueError("Invalid plan type")

        file = "paid-map.html"
    except (AuthJWTException, ValueError, KeyError):
        file = "free-map.html"

    with open(os.path.join("/app", "static", "files", file), "r") as f:
        return Response(content=f.read(), media_type="text/html")