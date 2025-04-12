from pydantic import BaseModel

class QuestionCreate(BaseModel):
    title: str
    description: str
    topic_id: int


class QuestionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    topic_id: int | None = None

