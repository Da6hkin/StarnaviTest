from pydantic import BaseModel, Field


class PostBase(BaseModel):
    text: str = Field(max_length=250)


class PostCreate(PostBase):
    owner_id: int


class PostInput(PostBase):
    pass


class Post(PostBase):
    owner_id: int
    id: int
