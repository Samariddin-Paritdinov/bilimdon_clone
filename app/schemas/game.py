from pydantic import BaseModel

class GameCreate(BaseModel):
    title: str
    description: str
    topic_id: int
    start_time: str
    end_time: str


class GameUpdate(BaseModel):
    title: str
    description: str
    topic_id: int
    start_time: str
    end_time: str


class ResponseGameGet(BaseModel):
    id: int
    title: str
    description: str
    topic_id: int
    start_time: str
    end_time: str