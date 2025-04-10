from app.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]