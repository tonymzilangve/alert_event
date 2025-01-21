import logging
from typing import AsyncGenerator

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.exceptions import DatabaseError

from config import settings

from .models import create_table_query, drop_table_query

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncClient, None]:
    logger.info("Connecting to Clickhouse database...")
    db = await get_async_client(
        username=settings.CH_USERNAME,
        password=settings.CH_PASSWORD,
        host=settings.CH_HOST,
    )

    try:
        yield db
    finally:
        db.close()


async def create_table() -> None:
    db = await anext(get_db())

    try:
        logger.info("Creating DB table...")
        await db.query(query=drop_table_query)
        await db.query(query=create_table_query)
    except Exception:
        raise DatabaseError("Failed to create table!")
