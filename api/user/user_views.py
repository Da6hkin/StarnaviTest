from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.user import user_crud
from api.user.user_schemas import UserOutput, UserCreate
from core.db import db_helper

user_router = APIRouter(tags=["Users"])


@user_router.post(
    "/sign_up",
    response_model=UserOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await user_crud.create_user(session=session, user_input=user_in)

