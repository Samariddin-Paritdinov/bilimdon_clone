from pydantic import BaseModel

class ParticipationCreate(BaseModel):
    game_id: int
    