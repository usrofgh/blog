import asyncio
import datetime
import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.back.app import app as fastapi_app
from src.back.models.users import UserModel
from src.back.models.posts import PostModel
from src.back.models.comments import CommentModel
from src.config import config
from src.database import BaseModel, SessionLocal, engine


# Use exactly this filename to allow pytest to detect this file
# scope=session - Call once for all tests
# scope=function - Call everytime for each test

@pytest.fixture(autouse=True, scope="function")
async def prepare_database():
    assert config.MODE == "TEST"
    async with engine.begin() as db:
        await db.run_sync(BaseModel.metadata.drop_all)
        await db.run_sync(BaseModel.metadata.create_all)

    def load_mocks(model: str) -> dict:
        path = Path().resolve()/"tests"/"mocks"/f"mock_{model}.json"
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    users = load_mocks("users")
    posts = load_mocks("posts")
    comments = load_mocks("comments")

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    for user in users:
        user["registered_at"] = datetime.datetime.strptime(user["registered_at"], date_format)

    for post in posts:
        post["created_at"] = datetime.datetime.strptime(post["created_at"], date_format)
        post["updated_at"] = datetime.datetime.strptime(post["updated_at"], date_format)

    for comment in comments:
        comment["created_at"] = datetime.datetime.strptime(comment["created_at"], date_format)
        comment["updated_at"] = datetime.datetime.strptime(comment["updated_at"], date_format)

    async with SessionLocal() as db:
        add_users = insert(UserModel).values(users)
        asd_posts = insert(PostModel).values(posts)
        add_comments = insert(CommentModel).values(comments)

        await db.execute(add_users)
        await db.execute(asd_posts)
        await db.execute(add_comments)
        await db.commit()


# Setup a new event loop for asynchronous tests
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_token():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.post("/v1/auth/login", json={
            "email": "admin@blog.com",
            "password": "string"
        }
        )
        token_data = response.json()
        yield token_data


@pytest.fixture(scope="function")
async def db_session():
    async with SessionLocal() as session:
        yield session
