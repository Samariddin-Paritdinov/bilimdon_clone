# from fastapi import APIRouter

# from app.dependencies import db_dep
# from app.models import Game

# router = APIRouter(
#     prefix="/game",
#     tags=["game"],
# )


# @router.get("/get_games")
# async def get_games(db: db_dep, ):
#     games_query = db.query(Game).all()

#     return games_query


# @router.get("/get_game/{id}")
# async def get_game_by_id(id: int, db: db_dep):
#     game_query = db.query(Game).filter(Game.id == id).first()

#     return game_query


# @router.delete("/delete_game/{id}")
# async def delete_game_by_id(id: int, db: db_dep):
#     game_query = db.query(Game).filter(Game.id == id).first()
#     if not game_query:
#         return {"message": "Game not found"}
#     db.delete(game_query)
#     db.commit()

#     return {"message": f"Game with {id} id deleted successfully"}


