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
from src.config import config
from src.database import BaseModel, SessionLocal, engine


@pytest.fixture(
    autouse=True,
    scope="function"
)
async def prepare_database():
    assert config.MODE == "TEST"
    async with engine.begin() as db:
        await db.run_sync(BaseModel.metadata.drop_all)
        await db.run_sync(BaseModel.metadata.create_all)

    def load_mocks(model: str) -> dict:
        path = Path().resolve()/"mocks"/f"mock_{model}.json"
        with open(path, "r") as file:
            return json.load(file)

    users = load_mocks("user")
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    for user in users:
        user["registered_at"] = datetime.datetime.strptime(user["registered_at"], date_format)

    async with SessionLocal() as db:
        add_users = insert(UserModel).values(users)
        await db.execute(add_users)
        await db.commit()


# Setup new event loop for asynchronous tests
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
        response = await ac.post("/v1/auth/register", json={
            "email": "admin@test.com",
            "password": "Pass_word1"
        }
        )
        token = response.json()["access_token"]
        yield token


@pytest.fixture(scope="function")
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
