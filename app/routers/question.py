from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep
from app.models import *
from app.schemas.question import *
from app.utils import get_current_user

from datetime import datetime
from typing import List


router = APIRouter(
    prefix="/Question", 
    tags=["Question"],
)



@router.get("/questions", response_model = List[ResponseQuestionGet])
async def get_questions(db: db_dep):
    questions = db.query(Question).all()

    return questions


@router.get("/question/{question_id}", response_model = ResponseQuestionGetById)
async def get_question_by_id(question_id: int, db: db_dep):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

    
@router.post("/new_question", response_model = ResponseQuestionGetById)
async def create_question(question: QuestionCreate, db: db_dep):
    new_question = Question(
        owner_id = get_current_user().id,
        title = question.title,
        description = question.description,
        topic_id = question.topic_id,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
    )
    
    # existing_question = db.query(Question).filter(Question.title == question.title).first()
    # if existing_question:
    #     raise HTTPException(status_code=400, detail="Question already exists")

    if not question.topic_id in db.query(Topic).all():
        raise HTTPException(status_code=400, detail="Invalid topic ID")    
    
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@router.put("/update_question/{question_id}", response_model = ResponseQuestionGetById)
async def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: db_dep
):
    existing_question = db.query(Question).filter(Question.id == question_id).first()

    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.dict(exclude_unset=True).items():
        setattr(existing_question, key, value)

    existing_question.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(existing_question)

    return existing_question


@router.delete("/delete_question/{question_id}", response_model = dict)
async def delete_question(question_id: int, db: db_dep):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {"detail": "Question deleted successfully"}


