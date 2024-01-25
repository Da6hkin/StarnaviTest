from datetime import datetime

from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.user_schemas import UserSchema
from core.db import User, db_helper

from api import utils

http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


jwt_router = APIRouter(prefix="", tags=["Users"])


async def validate_auth_user(
        username: str,
        password: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    if not result:
        raise unauthed_exc
    user = result.scalars().first()
    if not utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    return user


async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    token = credentials.credentials
    try:
        payload = utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> User:
    username: str | None = payload.get("sub")
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )

    return result.scalars().first()


@jwt_router.post("/login", response_model=TokenInfo)
async def login(
        user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    token = utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@jwt_router.get("/activity")
async def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "logged_in_at": datetime.utcfromtimestamp(iat),
        "last_activity": user.last_activity
    }
