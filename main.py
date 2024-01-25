from contextlib import asynccontextmanager

import uvicorn

from api.auth.jwt_auth import jwt_router
from api.like.like_views import like_router
from api.post.post_views import post_router
from api.user.user_views import user_router
from core.db import Base, db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=user_router)
app.include_router(router=jwt_router)
app.include_router(router=post_router)
app.include_router(router=like_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
