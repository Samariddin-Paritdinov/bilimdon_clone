from pydantic import BaseModel

from datetime import datetime


class OptionCreate(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime
    

class OptionUpdate(BaseModel):
    title: str
    is_correct: bool


class ResponseOptionGet(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool


class ResponseOptionGetById(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime

