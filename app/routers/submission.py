from fastapi import APIRouter, HTTPException

from app.models import Submission, Question, User, Option, Participation, GameQuestion

from app.dependencies import db_dep, current_user_dep, admin_user_dep
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



@router.get("/?user_id={id}", response_model=SubmissionsGetForUserResponse)
async def get_submissions_user_id(
        id: int,
        db: db_dep,
):
    if not db.query(User).filter(User.id == id).first():
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Submission).filter(Submission.user_id == id).all()

@router.put("/create/", response_model=SubmissionCreateResponse)
async def create_submission(
        request: SubmissionCreate,
        db: db_dep,
        current_user: current_user_dep,
):
    participation = db.query(Participation).filter(Participation.id == request.participation_id).first()
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    if participation.end_time is not None:
        raise HTTPException(status_code=404, detail="Participation is ended")

    if not participation.start_time is None:
        raise HTTPException(status_code=404, detail="Participation is not started")

    if not db.query(Question).filter(Question.id == request.question_id).first():
        raise HTTPException(status_code=404, detail="Question not found")

    selected_option = db.query(Option).filter(Option.id == request.option_id).first()
    if not selected_option:
        raise HTTPException(status_code=404, detail="Option not found")

    is_correct_option = selected_option.is_correct

    new_submission = Submission(
        user_id = current_user.id,
        question_id = request.question_id,
        option_id = request.id,
        is_correct = is_correct_option
    )
    score = db.query(GameQuestion).filter(
        GameQuestion.game_id == participation.game_id,
        GameQuestion.question_id == request.question_id,
    ).first()

    participation.gained_score += score

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    db.refresh(participation)

    return new_submission


@router.delete("/delete/")
async def delete_submission(
        id: int,
        db: db_dep,
        admin_user: admin_user_dep
):
    submission = db.query(Submission).filter(Submission.id == id).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    db.delete(submission)
    db.commit()

    return {
        "Submission ID": id,
        "detail": "Submission deleted successfully",
    }




