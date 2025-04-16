from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep
from app.models import GameQuestion, Game, Question
from app.schemas.gamequestion import *

from typing import List


router = APIRouter(
    prefix="/game_questions",
    tags=["game_questions"],
)

@router.get("/", response_model=List[GameQuestionGetResponse])
async def get_game_questions(db: db_dep):
    return db.query(GameQuestion).all()

@router.get("/{id}/", response_model=GameQuestionGetResponse)
async def get_game_question(id: int, db: db_dep):
    game_question = db.query(GameQuestion).filter(GameQuestion.id == id).first()
    if not game_question:
        raise HTTPException(status_code=404, detail="GameQuestion not found")

    return game_question


@router.post("/create/", response_model=GameQuestionGetResponse)
async def create_game_question(game_question: GameQuestionCreate, db: db_dep):
    game_question_exist = db.query(GameQuestion).filter(
        GameQuestion.game_id == game_question.game_id,
        GameQuestion.question_id == game_question.question_id,
    ).first()

    if game_question_exist:
        raise HTTPException(status_code=400, detail="GameQuestion already exists")

    if not db.query(Game).filter(Game.id == game_question.game_id).first():
        raise HTTPException(status_code=400, detail="Invalid Game ID")

    if not db.query(Question).filter(Question.id == game_question.question_id).first():
        raise HTTPException(status_code=400, detail="Invalid Question ID")

    new_game_question = GameQuestion(
        **game_question.model_dump(),
    )

    db.add(new_game_question)
    db.commit()
    db.refresh(new_game_question)

    return new_game_question


@router.put("/update/{id}/", response_model=GameQuestionGetResponse)
async def update_game_question(
        id: int,
        game_question: GameQuestionUpdate,
        db: db_dep,
):
    game_question_query = db.query(GameQuestion).filter(GameQuestion.id == id).first()

    if not game_question_query:
        raise HTTPException(status_code=404, detail="game_question not found")

    game_question_query.score = game_question.score

    db.commit()
    db.refresh(game_question_query)

    return game_question_query


@router.delete("/delete/{id}/")
async def delete_game_question(id: int, db: db_dep):
    db_game_question = db.query(GameQuestion).filter(GameQuestion.id == id).first()

    if not db_game_question:
        raise HTTPException(status_code=404, detail="GameQuestion not found")

    db.delete(db_game_question)
    db.commit()

    return {
        "game_question ID": id,
        "detail": "GameQuestion deleted",
        }
