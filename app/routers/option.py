from fastapi import APIRouter, HTTPException

from app.models import Option
from app.dependencies import db_dep
from app.schemas.option import *

router = APIRouter(
    prefix="/Option", 
    tags=["Option"],
)



@router.get("/options")
async def get_options(db:db_dep):
    options = db.query(Option).all()
    if not options:
        raise HTTPException(status_code=404, detail="Options not found")

    return options


@router.get("/option/{option_id}")
async def get_option(option_id: int, db: db_dep):
    option = db.query(Option).filter(Option.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    return option


@router.post("/new_option")
async def create_option(option: OptionCreate, db: db_dep):
    db.add(option)
    db.commit()
    db.refresh(option)

    return option


@router.put("/upd_option/{option_id}")
async def update_option(option_id: int, option: OptionUpdate, db: db_dep):
    db_option = db.query(Option).filter(Option.id == option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")

    for key, value in option.dict().items():
        setattr(db_option, key, value)

    db.commit()
    db.refresh(db_option)

    return db_option


@router.delete("/del_option/{option_id}")
async def delete_option(option_id: int, db: db_dep):
    db_option = db.query(Option).filter(Option.id == option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")

    db.delete(db_option)
    db.commit()

    return {"detail": "Option deleted successfully"}