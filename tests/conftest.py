from typing import AsyncGenerator, AsyncIterator
from unittest.mock import AsyncMock

import httpx
import pytest_asyncio

from app.db.database import get_db
from main import app

mock_db = AsyncMock()


async def override_get_db() -> AsyncGenerator[AsyncMock, None]:
    try:
        yield mock_db
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture()
async def mock_db_session():
    return mock_db


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
