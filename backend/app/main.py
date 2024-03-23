import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from slowapi.errors import RateLimitExceeded

from .utils import setup_logging
from .routers import api
from .constants import DEFAULT_JWT_SECRET_KEY
from .database import engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = setup_logging()

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", DEFAULT_JWT_SECRET_KEY)
    if authjwt_secret_key == DEFAULT_JWT_SECRET_KEY:
        logger.warning("Using default JWT secret key. DO NOT RUN ON PRODUCTION!")

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.message}
    )

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": f"Rate limit Exceeded"}
    )
    
@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(api.router)
app.state.limiter = api.limiter