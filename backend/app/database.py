import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "db")

print(f"sqlite://{DB_USERNAME}:{DB_PASSWORD}@database/db")

SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@database/{MYSQL_DATABASE}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine( # comment connect_args if not using sqlite
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()