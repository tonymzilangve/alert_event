import os
from typing import AsyncGenerator

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.exceptions import DatabaseError

from .models import create_table_query, drop_table_query


async def get_db() -> AsyncGenerator[AsyncClient, None]:
    db = await get_async_client(
        username=os.getenv("CH_USERNAME"),
        password=os.getenv("CH_PASSWORD"),
        host=os.getenv("CH_HOST"),
    )

    try:
        yield db
    finally:
        db.close()


async def create_table() -> None:
    db = await anext(get_db())

    try:
        await db.query(query=drop_table_query)
        await db.query(query=create_table_query)
    except Exception:
        raise DatabaseError("Failed to create table!")
