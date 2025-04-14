from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.models import Participation
from app.schemas.participation import *

from datetime import datetime, timezone
from typing import List


router = APIRouter(
    prefix="/participation",
    tags=["participation"],
)



@router.get("/")
async def get_participation(db: db_dep):    
    return db.query(Participation).all()


@router.get("/{participation_id}/", response_model=ParticipationGetDetailResponse)
async def get_participation_by_id(participation_id: int, db: db_dep):
    participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    return participation


@router.get("/?owner_id={owner_id}/", response_model=List[ParticipationGetDetailResponse])
async def get_participation_by_owner_id(
        owner_id: int,
        db: db_dep,
):

    return db.query(Participation).filter(Participation.user_id == owner_id).all()


@router.post("/create/")
async def create_participation(
        participation: ParticipationCreate,
        db: db_dep,
        current_user: current_user_dep,
):

    if db.query(Participation).filter(Participation.user_id == current_user.id, Participation.game_id == participation.game_id).first:
        raise HTTPException(status_code= 400, detail="Participation already exist")

    new_participation = Participation(
        user_id=current_user.id,
        game_id=participation.game_id,
        registered_at=datetime.now(timezone.utc),
        )

    if not new_participation:
        raise HTTPException(status_code=400, detail="Participation creation failed")

    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)
    
    return new_participation




@router.put("/update/{id}")
async def update_participation_by_id(
        id: int,

        db: db_dep,

):
    participation = db.query(Participation).filter(Participation.id == id).first()

    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")



### shuni ohiriga yetkazish uchun logikasini chunvolishim kerak





@router.delete("/delete/{id}/")
async def delete_participation(id: int, db: db_dep):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    db.delete(participation)
    db.commit()

    return {
        "participation ID": id,
        "detail": "Participation deleted successfully",
        }