from fastapi import APIRouter, HTTPException

from app.models import Participation
from app.dependencies import db_dep
from app.schemas.participation import *
from app.utils import get_current_user

from datetime import datetime, timezone


router = APIRouter(
    prefix="/Participation",
    tags=["Participation"],
)

@router.get("/participations")
async def get_participations(db: db_dep):
    participations = db.query(Participation).all()
    if not participations:
        raise HTTPException(status_code=404, detail="No participations found")
    
    return participations

@router.get("/participation/{participation_id}")
async def get_participation_by_id(id: int, db: db_dep):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    return participation


@router.post("/new_participation")
async def create_participation(participation: ParticipationCreate, db: db_dep):
    new_participation = Participation(
        user_id=get_current_user().id,
        game_id=participation.game_id,
        registered_at=datetime.now(timezone.utc),

        )

    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)
    if not new_participation:
        raise HTTPException(status_code=400, detail="Participation creation failed")
    
    return new_participation



