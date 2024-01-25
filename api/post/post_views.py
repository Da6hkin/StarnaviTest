from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.auth.jwt_auth import get_current_auth_user
from api.post import post_crud
from api.post.post_schemas import Post, PostCreate, PostInput
from api.user.user_schemas import User
from core.db import db_helper

post_router = APIRouter(tags=["Posts"])


@post_router.post(
    "/post",
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
        post_in: PostInput,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    post = PostCreate(text=post_in.text, owner_id=user.id)
    result = await post_crud.create_post(session=session, post_input=post)
    user.last_activity = datetime.utcnow()
    await session.commit()
    return result
