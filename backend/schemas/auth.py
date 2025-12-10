from pydantic import BaseModel
from .user import UserOut


class RegisterIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str


class LoginOut(BaseModel):
    token : str
    user : UserOut


