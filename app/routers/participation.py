from fastapi import APIRouter, HTTPException

from app.models import Participation
from app.dependencies import db_dep


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