import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from slowapi.errors import RateLimitExceeded

from .constants import DEFAULT_JWT_SECRET_KEY, LIMITS
from .utils import setup_logging
from .database import engine, SessionLocal
from .routers import query, auth, files, limiter
from . import models

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    populate_database()
    yield

app = FastAPI(lifespan=lifespan, root_path="/api")
logger = setup_logging()

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", DEFAULT_JWT_SECRET_KEY)
    authjwt_token_location: set = {"cookies", "headers"}
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

def populate_database():
    # db = SessionLocal()
    # if not db.query(models.Plan).first():
    #     default_plans = [{"type": x} for x in LIMITS]
    #     for plan in default_plans:
    #         plan = models.Plan(**plan)
    #         db.add(plan)
    #     db.commit()
    # db.close()
    pass

app.include_router(query.router)
app.include_router(auth.router)
app.include_router(files.router)
app.state.limiter = limiter