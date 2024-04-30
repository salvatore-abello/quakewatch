import os
import re
from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi import APIRouter, Request, Response, Depends

from .. import crud
from .. import utils
from .. import constants


router = APIRouter(prefix="/files", tags=["files"])
    
@router.get("/{filename}")
async def handle_request(filename: str, request: Request, db: Session = Depends(utils.get_db),
                            Authorize: AuthJWT = Depends()):
    """ Retrieve paid/free files """

    if not re.match(r"[a-z.]{1,32}", filename): # Eg. map.html, map.js
        return Response(content="Invalid filename", status_code=400)
    
    try:
        Authorize.jwt_required()
        current_user = crud.get_user(db, Authorize.get_jwt_subject())

        if not hasattr(current_user, "key") \
            or not current_user.key or current_user.key.plan.type not in constants.LIMITS:
            raise ValueError("Invalid plan type")

        if current_user.key.plan.type == "basic":
            raise ValueError("Basic plan does not have access to the paid map")

        file = f"paid-{filename}"
    except (AuthJWTException, ValueError, KeyError) as e:
        file = f"free-{filename}"

    known_content_type = constants.KNOWN_CONTENT_TYPES.get(filename.split(".")[-1], "text/plain")

    with open(os.path.join("/app", "static", "files", file), "r") as f:
        return Response(content=f.read(), headers={"Content-Type": known_content_type})