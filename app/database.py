from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCEMY_DATABASE_URL = "sqlite:///./app.db"

# connect_args={"check_same_thred": False} needs only sqlite
engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={"check_same_thred": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
