from pydantic import BaseModel

class SubmissionsGetResponse(BaseModel):
    id: int
    participation_id: int
    question_id: int
    option_id: int


class SubmissionsGetForQuestionResponse(BaseModel):
    id: int
    user_id: int
    option_id: int

class SubmissionsGetForUserResponse(BaseModel):
    id: int
    question_id: int
    option_id: int


class SubmissionCreate(BaseModel):
    participation_id: int
    question_id: int
    option_id: int


class SubmissionCreateResponse(BaseModel):
    id: int
    question_id: int
    option_id: int
    is_correct: bool



