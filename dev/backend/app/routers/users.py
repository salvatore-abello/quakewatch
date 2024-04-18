from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import get_current_user, captcha
from .. import crud, schemas
from .. import utils


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/current", response_model=schemas.User)
async def get_current_user(request: Request, db: Session = Depends(utils.get_db), Authorize: AuthJWT = Depends(), 
                           current_user: schemas.User=Depends(get_current_user)):
    """ Get current user data """
    return current_user

@router.get("/logout")
async def handle_logout(request: Request, Authorize: AuthJWT = Depends()):
    response = JSONResponse(content={"msg": "Successfully logged out"})
    Authorize.unset_access_cookies(response)

    return response

@router.post("/register", response_model=schemas.UserBase)
@captcha
async def handle_register(request: Request, user: schemas.UserCreate, 
                      db: Session = Depends(utils.get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError as e:
        return JSONResponse(content={"detail": "Email already in use"}, status_code=400)

@router.post("/login", responses={200: {"description": "Successfully logged in"}, 
                                  401: {"detail": "Invalid credentials"}})
async def handle_login(request: Request, user: schemas.UserLogin, 
                      db: Session = Depends(utils.get_db), Authorize: AuthJWT = Depends()):
    if (user:=crud.check_login(db, user)):
        access_token = Authorize.create_access_token(subject=user.IDUser)
        json_response = JSONResponse(content={"msg": "Successfully logged in"})
        
        Authorize.set_access_cookies(access_token, json_response)
        
        return json_response
    
    return JSONResponse(content={"detail": "Invalid credentials"}, status_code=401)