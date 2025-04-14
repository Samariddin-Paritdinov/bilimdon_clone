from pydantic import BaseModel

from datetime import datetime

class GameCreate(BaseModel):
    title: str
    description: str | None = None
    topic_id: int
    start_time: datetime
    end_time: datetime


class GameUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    topic_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class GameGetResponse(BaseModel):
    id: int
    title: str
    description: str
    topic_id: int
    start_time: datetime
    end_time: datetime