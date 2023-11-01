from psycopg2.extras import DictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base as declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:<password>@localhost/fastapi"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
