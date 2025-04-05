from pydantic import BaseModel
from datetime import date

class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    birthday: date

dummy_data = {
    "id": 1,
    "first_name":"John",
    "last_name":"Doe",
    "username":"john_doe",
    "birthday":date(year=2000, month=1, day=1)
}

user = UserSchema(**dummy_data)
user_dict = user.model_dump()
user_dict['is_user'] = True
print(user_dict)