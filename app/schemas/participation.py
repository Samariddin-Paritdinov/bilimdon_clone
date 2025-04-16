from pydantic import BaseModel

from datetime import datetime


class ParticipationCreate(BaseModel):
    game_id: int


class ParticipationGetDetailResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    registered_at: datetime
    start_time: datetime
    end_time: datetime
    gained_score: datetime





    