from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.models import Game, Topic, Question, GameQuestion
from app.schemas import GameCreate, GameUpdate,  GameGetResponse, QuestionGetResponse, GameSelectQuestion

from datetime import datetime, timezone, timedelta


router = APIRouter(
    prefix="/games",
    tags=["games"],
)



@router.get("/", response_model=list[GameGetResponse])
async def get_active_games(db:db_dep):
    return db.query(Game).filter(Game.end_time > datetime.now(timezone.utc)).all()


@router.get("/all/", response_model=list[GameGetResponse])
async def get_games(db: db_dep, ):
    return db.query(Game).all()


@router.get("/{id}/", response_model=GameGetResponse)
async def get_game_by_id(id: int, db: db_dep):
    game_query = db.query(Game).filter(Game.id == id).first()
    if not game_query:
        raise HTTPException(status_code=400, detail="Game not found")

    return game_query


@router.post("/create/", response_model=GameGetResponse)
async def create_game(
        game: GameCreate,
        db: db_dep,
        current_user: current_user_dep,
):
    topic_id_exist = db.query(Topic).filter(Topic.id == game.topic_id).first()
    if not topic_id_exist:
        raise HTTPException(
            status_code=400,
            detail="Topic with this id does not exist",
        )


    if game.start_time > game.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be less than end time",
        )
    if game.start_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Start time must be greater than current time",
        )

    if game.end_time - game.start_time < timedelta(hours=1):
        raise HTTPException(
            status_code=400,
            detail="Game must last at least 1 hour."
        )

    new_game = Game(
        owner_id=current_user.id,
        **game.model_dump()
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


@router.put("/update/{id}/")
async def update_game_by_id(id: int, game: GameUpdate, db: db_dep):
    game_query = db.query(Game).filter(Game.id == id).first()
    if not game_query:
        return {"message": "Game not found"}

    for key, value in game.model_dump(exclude_unset=True).items():
        setattr(game_query, key, value)

    db.commit()

    return game_query


@router.delete("/delete/{id}/")
async def delete_game_by_id(
    id: int, 
    db: db_dep,
    admin_user: admin_user_dep,
    ):
    game_query = db.query(Game).filter(Game.id == id).first()
    if not game_query:
        return {"message": "Game not found"}

    db.delete(game_query)
    db.commit()

    return {
        "Game ID": id,
        "message": "Game deleted successfully",
    }


@router.get("/{id}/questions", response_model=list[QuestionGetResponse])
async def game_questions(
        db: db_dep,
        current_user: current_user_dep,
        id: int
):
    db_game = db.query(Game).filter(Game.id == id).first()

    if not db_game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    db_questions = db.query(GameQuestion).filter(GameQuestion.game_id == id).all()

    if db_questions:
        return [db.query(Question).filter(Question.id == question.question_id).first() for question in db_questions]

    return []


@router.post("/{id}/select-question/", response_model=QuestionGetResponse)
async def select_question(
        db: db_dep,
        current_user: current_user_dep,
        request: GameSelectQuestion
):
    db_question = db.query(Question).filter(Question.id == request.question_id).first()

    if not db_question:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    db_game = db.query(Game).filter(Game.id == request.game_id).first()

    if not db_game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    db_game_question = GameQuestion(
        game_id=db_game.id,
        question_id=db_question.id
    )

    db.add(db_game_question)
    db.commit()
    db.refresh(db_game_question)

    return db_question


