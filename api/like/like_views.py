from datetime import datetime, date
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.auth.jwt_auth import get_current_auth_user, get_current_token_payload
from api.like import like_crud
from api.like.like_schemas import LikeCreate, LikeOutput
from api.user.user_schemas import User
from core.db import db_helper, Like, Post

like_router = APIRouter(tags=["Likes"])


async def check_post_like_by_user(
        post_id: int,
        user: User,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> LikeOutput | None:
    post_stmt = select(Post).where(Post.id == post_id)
    post_result: Result = await session.execute(post_stmt)
    post = post_result.scalars().first()
    if post is not None:
        stmt = select(Like).where(Like.post_id == post_id, Like.user_id == user.id)
        result: Result = await session.execute(stmt)
        return result.scalars().first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no post with given id",
        )


@like_router.post(
    "/like",
    response_model=LikeOutput,
    status_code=status.HTTP_201_CREATED,
)
async def like_post(
        post_id: int,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    check_like = await check_post_like_by_user(post_id, user, session)
    if not check_like:
        like = LikeCreate(like_datetime=datetime.utcnow(), user_id=user.id, post_id=post_id)
        result = await like_crud.create_like(session=session, like_input=like)
        user.last_activity = datetime.utcnow()
        await session.commit()
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post is already liked by this user",
        )


@like_router.delete(
    "/unlike/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unlike_post(
        post_id: int,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    check_like = await check_post_like_by_user(post_id, user, session)
    if check_like:
        await session.delete(check_like)
        user.last_activity = datetime.utcnow()
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post is not liked by this user",
        )


@like_router.get(
    "/analytics/",
    status_code=status.HTTP_200_OK,
)
async def like_analytics(
        date_from: datetime,
        date_to: datetime,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    result_dict = await like_crud.get_likes_analytics(session=session, start_date=date_from, end_time=date_to,
                                                      user_id=user.id)
    user.last_activity = datetime.utcnow()
    await session.commit()
    return result_dict
