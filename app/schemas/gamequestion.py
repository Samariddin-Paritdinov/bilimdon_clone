from pydantic import BaseModel

class GameQuestionCreate(BaseModel):
    question_id: int
    game_id: int
    score: int | None = None


class GameQuestionUpdate(BaseModel):
    score: int


class GameQuestionGetResponse(BaseModel):
    id: int
    question_id: int
    game_id: int
    score: int

    