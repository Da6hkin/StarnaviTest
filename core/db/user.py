from sqlalchemy import String, Column, Text, DateTime
from sqlalchemy.orm import mapped_column
from core.db.base import Base


class User(Base):
    username = mapped_column(String(15), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    last_activity = Column(DateTime, nullable=True)
