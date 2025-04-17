from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.models import Participation
from app.schemas.participation import *

from datetime import datetime, timezone


router = APIRouter(
    prefix="/participation",
    tags=["participation"],
)


@router.get("/")
async def get_participation(db: db_dep):    
    return db.query(Participation).all()


@router.get("/{id}/", response_model=ParticipationGetDetailResponse)
async def get_participation_by_id(id: int, db: db_dep):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    return participation


@router.get("/owner_id/{owner_id}/", response_model=list[ParticipationGetDetailResponse])
async def get_participation_by_owner_id(
        owner_id: int,
        db: db_dep,
        admin_user: admin_user_dep,
):
    return db.query(Participation).filter(Participation.user_id == owner_id).all()


@router.post("/create/")
async def create_participation(
        participation: ParticipationCreate,
        db: db_dep,
        current_user: current_user_dep,
):
    new_participation = Participation(
        user_id=current_user.id,
        registered_at=datetime.now(timezone.utc),
        **participation.model_dump()
        )

    if not new_participation:
        raise HTTPException(status_code=400, detail="Participation creation failed")

    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)
    
    return new_participation


@router.patch("/start_participation/{id}/", response_model=ParticipationGetDetailResponse)
async def start_participation(
        id: int,
        db: db_dep,
        current_user: current_user_dep,
):

    participation = db.query(Participation).filter(Participation.id == id).first()

    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    if participation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your Participation")

    if participation.start_time:
        HTTPException(status_code=403, detail="Participation already started")

    participation.start_time = datetime.now(timezone.utc)
    db.commit()
    db.refresh(participation)

    return participation


@router.patch("/end_participation/{id}/")
async def end_participation(
        id: int,
        db, db_dep,
        current_user: current_user_dep,
):
    participation = db.query(Participation).filter(Participation.id == id).first()

    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    if participation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your Participation")

    if participation.end_time:
        HTTPException(status_code=403, detail="Participation already ended")

    if not participation.start_time:
        raise HTTPException(status_code=403, detail="Participation not started")


    participation.end_time = datetime.now(timezone.utc)
    db.commit()
    db.refresh(participation)

    return participation


@router.delete("/delete/{id}/")
async def delete_participation(
        id: int,
        db: db_dep,
        current_user: current_user_dep,
):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    if participation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your Participation")

    db.delete(participation)
    db.commit()

    return {
        "participation ID": id,
        "detail": "Participation deleted successfully",
        }