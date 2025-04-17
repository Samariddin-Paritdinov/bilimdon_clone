from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.models import Question, Topic, Option
from app.schemas import QuestionCreate, QuestionUpdate, QuestionGetDetailResponse, QuestionGetResponse, QuestionWithOptionsResponse

from datetime import datetime, timezone


router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)



@router.get("/", response_model = list[QuestionGetResponse])
async def get_questions(db: db_dep):
    return db.query(Question).all()


@router.get("/{id}/", response_model = QuestionGetDetailResponse)
async def get_question_by_id(id: int, db: db_dep):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

    
@router.post("/create/", response_model = QuestionGetDetailResponse)
async def create_question(
        question: QuestionCreate,
        db: db_dep,
        current_user: current_user_dep,
    ):

    existing_question = db.query(Question).filter(Question.title == question.title).first()
    if existing_question:
        raise HTTPException(status_code=400, detail="Question already exists")

    if not db.query(Topic).filter(Topic.id == question.topic_id).first():
        raise HTTPException(status_code=400, detail="Invalid topic ID")

    new_question = Question(
        owner_id = current_user.id,
        **question.model_dump(),
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@router.put("/update/{id}/", response_model = QuestionGetDetailResponse)
async def update_question(
    id: int,
    question: QuestionUpdate,
    db: db_dep
):
    existing_question = db.query(Question).filter(Question.id == id).first()
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")

    if not db.query(Topic).filter(Topic.id == question.topic_id).first():
        raise HTTPException(status_code=400, detail="Invalid topic ID")

    for key, value in question.model_dump(exclude_unset=True).items():
        setattr(existing_question, key, value)

    existing_question.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(existing_question)

    return existing_question


@router.delete("/delete/{id}/")
async def delete_question(
        id: int,
        db: db_dep,
        admin_user: admin_user_dep
):
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {
        "Question ID": id,
        "detail": "Question deleted successfully",
    }


@router.get("/{id}/options/", response_model=QuestionWithOptionsResponse)
async def get_questions_with_options(
        id: int,
        db:db_dep,
        admin_user: admin_user_dep,
):
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=400, detail="Question not found")

    return question