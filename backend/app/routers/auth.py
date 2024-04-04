from fastapi_another_jwt_auth import AuthJWT
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import crud, schemas
from ..utils import get_db


router = APIRouter(prefix="/auth")


@router.post("/")
async def handle_key_auth(request: Request, Authorize: AuthJWT = Depends(), 
                      db: Session = Depends(get_db)):
    data = await request.json()
    
    if not (auth_key:=data.get("auth-key")) or not (key:=crud.get_key_from_value(db, auth_key)): 
        return JSONResponse(content={"msg":"Invalid key"}, status_code=401)
    
    return JSONResponse(content={"access_token":Authorize.create_access_token(subject=key,
                                                    user_claims={"plan_type": key.plan})})

@router.post("/register", response_model=schemas.UserBase)
async def handle_register(request: Request, user: schemas.UserCreate, 
                      db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError as e:
        return JSONResponse(content={"msg": "Email already in use"}, status_code=400)
    
@router.post("/login")
async def handle_login(request: Request, user: schemas.UserLogin, 
                      db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    if crud.check_login(db, user):
        access_token = Authorize.create_access_token(subject=user.email)
        json_response = JSONResponse(content={"msg": "Logged in"})
        Authorize.set_access_cookies(access_token, json_response)
        return json_response
    
    return JSONResponse(content={"msg": "Invalid credentials"}, status_code=401)