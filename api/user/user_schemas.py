from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class UserCreate(UserSchema):
    password: str


class UserOutput(UserSchema):
    id: int


class User(UserSchema):
    id: int
    last_activity: datetime
