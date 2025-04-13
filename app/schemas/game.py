from pydantic import BaseModel

from datetime import datetime

class GameCreate(BaseModel):
    title: str
    description: str
    topic_id: int
    start_time: datetime
    end_time: datetime


class GameUpdate(BaseModel):
    title: str
    description: str
    topic_id: int
    start_time: datetime
    end_time: datetime


class GameGetResponse(BaseModel):
    id: int
    title: str
    description: str
    topic_id: int
    start_time: datetime
    end_time: datetime