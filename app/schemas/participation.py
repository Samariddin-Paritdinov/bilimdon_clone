from pydantic import BaseModel



class ParticipationCreate(BaseModel):
    game_id: int





class ParticipationGetDetailResponse(BaseModel):
    id: int
    user_id: int



    