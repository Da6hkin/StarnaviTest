from sqlalchemy.ext.asyncio import AsyncSession

from .post_schemas import PostCreate
from core.db import Post


async def create_post(session: AsyncSession, post_input: PostCreate) -> Post:
    post = Post(**post_input.model_dump())
    session.add(post)
    await session.commit()
    return post
