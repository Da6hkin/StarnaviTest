from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship

from core.db.base import Base


class Post(Base):
    text = mapped_column(String(250), nullable=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", cascade="all, delete")
