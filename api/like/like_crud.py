from datetime import datetime

from sqlalchemy import select, Result, delete, asc, between
from sqlalchemy.ext.asyncio import AsyncSession

from .like_schemas import LikeCreate
from core.db import Like


async def create_like(session: AsyncSession, like_input: LikeCreate) -> Like:
    like = Like(**like_input.model_dump())
    session.add(like)
    await session.commit()
    return like


async def delete_like(session: AsyncSession, like: Like) -> None:
    await session.delete(like)
    await session.commit()


async def get_likes_analytics(session: AsyncSession, start_date: datetime, end_time: datetime, user_id: int) -> dict:
    qry = select(Like).where(Like.user_id == user_id, between(Like.like_datetime, start_date, end_time)).order_by(
        Like.like_datetime)
    result: Result = await session.execute(qry)
    likes = result.scalars().all()
    output = {}
    for like in likes:
        date = like.like_datetime.date()
        if date not in output:
            output[date] = [like]
        else:
            output[date].append(like)

    return output
