from pydantic import BaseModel

from datetime import datetime


class OptionCreate(BaseModel):
    question_id: int
    title: str
    is_correct: bool
    

class OptionUpdate(BaseModel):
    title: str
    is_correct: bool


class OptionGetResponse(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool


class OptionGetDetailResponse(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime

class OptionGetForQuestionsResponse(BaseModel):
    id: int
    title: str
    is_correct: bool

    class Config:
        orm_mode = True