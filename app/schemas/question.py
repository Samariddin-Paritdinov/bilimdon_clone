from pydantic import BaseModel


class QuestionCreate(BaseModel):
    title: str
    description: str
    topic_id: int


class QuestionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    topic_id: int | None = None


class ResponseQuestionGet(BaseModel):
    id: int
    title: str
    topic_id: int


class ResponseQuestionGetById(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    topic_id: int
    created_at: str
    updated_at: str

