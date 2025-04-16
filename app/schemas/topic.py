from pydantic import BaseModel

class TopicGetResponse(BaseModel):
    id: int
    name: str

class TopicCreate(BaseModel):
    name: str