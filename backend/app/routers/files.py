import os
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi import APIRouter, Request, Response, Depends

from .. import utils
from .. import middleware


router = APIRouter(prefix="/files")

@router.get("/map.js")
async def handle_request(request: Request, response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        file = "paid-map.js"
    except AuthJWTException:
        file = "free-map.js"
    
    print(open(os.path.join("static", "files", file), "r"))
        
    with open(os.path.join("static", "files", file), "r") as f:
        return Response(content=f.read(), media_type="application/javascript")