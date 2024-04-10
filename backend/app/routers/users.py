from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from fastapi import Query


from . import get_current_user
from .. import crud, schemas
from ..utils import get_db


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/current", response_model=schemas.User)
async def get_current_user(request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), 
                           current_user=Depends(get_current_user)):
    """ Get current user data """
    return current_user
    
@router.post("/register", response_model=schemas.UserBase)
async def handle_register(request: Request, user: schemas.UserCreate, 
                      db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError as e:
        return JSONResponse(content={"msg": "Email already in use"}, status_code=400)
    
@router.post("/login", responses={200: {"description": "Successfully logged in"}, 
                                  401: {"description": "Invalid credentials"}})
async def handle_login(request: Request, user: schemas.UserLogin, 
                      db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    if (user:=crud.check_login(db, user)):
        access_token = Authorize.create_access_token(subject=user.IDUser)
        json_response = JSONResponse(content={"msg": "Successfully logged in"})
        
        Authorize.set_access_cookies(access_token, json_response)
        
        return json_response
    
    return JSONResponse(content={"msg": "Invalid credentials"}, status_code=401)