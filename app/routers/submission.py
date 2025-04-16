from fastapi import APIRouter, HTTPException

from app.models import Submission, Question, User, Option, Participation

from app.dependencies import db_dep, current_user_dep
from app.schemas.submission import *
router = APIRouter(
    prefix="submissions",
    tags=["submissions"],
)

@router.get("/", response_model=SubmissionsGetResponse)
async def get_all_submissions(db: db_dep):
    return db.query(Submission).all()


@router.get("/?question_id={id}", response_model=SubmissionsGetForQuestionResponse)
async def get_submissions_question_id(
        id: int,
        db: db_dep,
):
    if not db.query(Question).filter(Question.id == id).first():
        raise HTTPException(status_code=404, detail="Question not found")

    return db.query(Submission).filter(Submission.question_id == id).all()



@router.get("/?question_id={id}", response_model=SubmissionsGetForUserResponse)
async def get_submissions_user_id(
        id: int,
        db: db_dep,
):
    if not db.query(User).filter(User.id == id).first():
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Submission).filter(Submission.user_id == id).all()


