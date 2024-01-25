from sqlalchemy import ForeignKey, Integer, Column, DateTime
from sqlalchemy.orm import mapped_column

from core.db.base import Base


class Like(Base):
    like_datetime = Column(DateTime)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
