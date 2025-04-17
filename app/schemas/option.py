from pydantic import BaseModel

from datetime import datetime

from app.schemas.question import QuestionGetResponse

class OptionCreate(BaseModel):
    question_id: int
    title: str
    is_correct: bool | None = None
    

class OptionUpdate(BaseModel):
    title: str | None = None
    is_correct: bool | None = None


class OptionGetResponse(BaseModel):
    id: int
    # question_id: int
    question: QuestionGetResponse
    title: str


class OptionGetDetailResponse(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime


