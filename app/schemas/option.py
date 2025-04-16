from pydantic import BaseModel

from datetime import datetime

from app.schemas import QuestionGetResponse

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

class OptionGetForQuestionsResponse(BaseModel):
    id: int
    title: str
    is_correct: bool
    ###Shuni bir so'rab ko'rish kerak
    ###Faqatgina adminga javobni to'g'ri xatoligi ko'rinishi uchun Alohida API chiqarib qo'yimi?

    class Config:
        from_attributes = True
