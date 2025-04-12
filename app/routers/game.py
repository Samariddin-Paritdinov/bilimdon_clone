from fastapi import APIRouter

from app.dependencies import db_dep
from app.models import Game
from app.schemas.game import *
from app.utils import get_current_user


router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.get("/get_games")
async def get_games(db: db_dep, ):
    games_query = db.query(Game).all()

    return games_query


@router.get("/get_game/{id}")
async def get_game_by_id(id: int, db: db_dep):
    game_query = db.query(Game).filter(Game.id == id).first()

    return game_query


@router.post("/create_game")
async def create_game(game: GameCreate, db: db_dep):
    new_game = Game(
        owner_id=get_current_user().id,
        title=game.title,
        description=game.description,
        topic_id=game.topic_id,
        start_time=game.start_time,
        end_time=game.end_time,
    )

    return game_query


@router.put("/update_game/{id}")
async def update_game_by_id(id: int, game: GameUpdate, db: db_dep):
    game_query = db.query(Game).filter(Game.id == id).first()
    if not game_query:
        return {"message": "Game not found"}

    for key, value in game.dict(exclude_unset=True).items():
        setattr(game_query, key, value)

    db.commit()

    return game_query







@router.delete("/delete_game/{id}")
async def delete_game_by_id(id: int, db: db_dep):
    game_query = db.query(Game).filter(Game.id == id).first()
    if not game_query:
        return {"message": "Game not found"}
    db.delete(game_query)
    db.commit()

    return {"message": f"Game with {id} id deleted successfully"}


