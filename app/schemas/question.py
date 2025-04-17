from pydantic import BaseModel

from typing import List





class QuestionCreate(BaseModel):
    title: str
    description: str |None = None
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
    description: str |None = None
    owner_id: int
    topic_id: int
    created_at: str
    updated_at: str


class OptionGetForQuestionsResponse(BaseModel):
    id: int
    title: str
    is_correct: bool
    ###Shuni bir so'rab ko'rish kerak
    ###Faqatgina adminga javobni to'g'ri xatoligi ko'rinishi uchun Alohida API chiqarib qo'yimi?

    class Config:
        from_attributes = True


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
        from_attributes = True
