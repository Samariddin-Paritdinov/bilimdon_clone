from fastapi import APIRouter, HTTPException


from app.dependencies import db_dep,current_user_dep
from app.models import Participation
from app.dependencies import db_dep
from app.schemas.participation import *

from datetime import datetime, timezone


router = APIRouter(
    prefix="/participation",
    tags=["participation"],
)

@router.get("/")
async def get_participation(db: db_dep):
    participation = db.query(Participation).all()
    if not participation:
        raise HTTPException(status_code=404, detail="No participations found")
    
    return participation

@router.get("/{id}/")
async def get_participation_by_id(id: int, db: db_dep):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    return participation


@router.post("/create/")
async def create_participation(participation: ParticipationCreate, db: db_dep):
    new_participation = Participation(
        user_id=current_user_dep.id,
        game_id=participation.game_id,
        registered_at=datetime.now(timezone.utc),

        )

    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)
    if not new_participation:
        raise HTTPException(status_code=400, detail="Participation creation failed")
    
    return new_participation



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