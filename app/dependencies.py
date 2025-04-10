from fastapi import Depends

from typing import Annotated

from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]