from pydantic import BaseModel

from datetime import datetime



class ParticipationUser(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None


class ParticipationResponse(BaseModel):
    id: int
    user: ParticipationUser
    game_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None
    gained_score: int
    registered_at: datetime


class ParticipationCreate(BaseModel):
    game_id: int







    