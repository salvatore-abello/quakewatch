import os
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from slowapi.errors import RateLimitExceeded

from .constants import DEFAULT_JWT_SECRET_KEY, LIMITS, OPENAPI_TAGS
from .utils import setup_logging
from .database import engine, SessionLocal
from .routers import query, files, users, keys
from . import models

# This create all tables in the database
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    populate_database()
    yield

app = FastAPI(
    lifespan=lifespan, 
    root_path="/api", 
    openapi_tags=OPENAPI_TAGS
)

logger = setup_logging()

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", DEFAULT_JWT_SECRET_KEY)
    authjwt_access_token_expires: int = 60 * 60
    authjwt_token_location: set = {"cookies"}
    if authjwt_secret_key == DEFAULT_JWT_SECRET_KEY:
        logger.warning("Using default JWT secret key. DO NOT RUN ON PRODUCTION!")

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    raise HTTPException(status_code=exc.status_code, detail=exc.message)

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(status_code=exc.status_code, detail="Rate limit execeeded. Try again later.")

@AuthJWT.load_config
def get_config():
    return Settings()

def populate_database():
    db = SessionLocal()
    if not db.query(models.Plan).first():
        default_plans = [{"type": x} for x in LIMITS]
        for plan in default_plans:
            plan = models.Plan(**plan)
            db.add(plan)
        db.commit()
    db.close()
    
app.include_router(query.router)
app.include_router(files.router)
app.include_router(users.router)
app.include_router(keys.router)