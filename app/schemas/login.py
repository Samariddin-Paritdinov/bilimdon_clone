from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class SignupSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    birthdate: str
    # joined_at:
    # is_active: bool
    # is_staff
    # is_superuser
