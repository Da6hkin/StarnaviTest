from datetime import datetime

from pydantic import BaseModel


class LikeBase(BaseModel):
    like_datetime: datetime
    user_id: int
    post_id: int


class LikeOutput(LikeBase):
    id: int


class LikeCreate(LikeBase):
    pass
