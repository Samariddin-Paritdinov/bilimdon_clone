from pydantic import BaseModel

from typing import List
from app.schemas.option import OptionGetForQuestionsResponse

class QuestionCreate(BaseModel):
    title: str
    description: str
    topic_id: int


class QuestionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    topic_id: int | None = None


class QuestionGetResponse(BaseModel):
    id: int
    title: str
    topic_id: int


class QuestionGetDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    topic_id: int
    created_at: str
    updated_at: str

class QuestionWithOptionsResponse(BaseModel):
    id: int
    owner_id: int
    topic_id: int

    title: str
    description: str
    options: List[OptionGetForQuestionsResponse]

    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
