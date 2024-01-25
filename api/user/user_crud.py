from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import User
from .user_schemas import UserCreate
from ..utils import hash_password


async def create_user(session: AsyncSession, user_input: UserCreate) -> User:
    user_input.password = hash_password(user_input.password)
    user = User(**user_input.model_dump())
    session.add(user)
    await session.commit()
    return user
