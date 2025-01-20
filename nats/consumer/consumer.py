import asyncio
import json
import logging
import os
from typing import AsyncGenerator

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.exceptions import DatabaseError
from dotenv import load_dotenv

import nats
from nats.errors import TimeoutError

load_dotenv()
logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncClient, None]:
    logger.info("Connecting to Clickhouse database...")
    db = await get_async_client(
        username=os.getenv("CH_USERNAME"),
        password=os.getenv("CH_PASSWORD"),
        host=os.getenv("CH_HOST"),
    )

    try:
        yield db
    finally:
        db.close()


async def save_message(msg: str) -> None:
    data = json.loads(msg.data)

    save_msg_query = f"""
    INSERT INTO alert_messages (uuid, ts, type, severity, message, source, payload, acknowledged)
    VALUES (
        generateUUIDv4(),
        '{data["ts"]}',
        '{data["type"]}',
        '{data["severity"]}',
        '{data["message"]}',
        '{data["source"]}',
        '{data["payload"]}',
        false
    )
    """

    db = await anext(get_db())

    try:
        logger.info("Saving message to Clickhouse database...")
        await db.query(query=save_msg_query)
    except Exception:
        raise DatabaseError("Failed to save new message!")


async def main() -> None:
    nats_url = f"nats://{os.getenv('NATS_HOST')}:{os.getenv('NATS_PORT')}"

    async with await nats.connect(servers=[nats_url]) as nc:
        logger.info("Subscribing to [alert] topic...")
        sub = await nc.subscribe("alert.*")

        while True:
            try:
                msg = await sub.next_msg()
                logger.info("Received a new message!")
                await save_message(msg)
                await asyncio.sleep(0.1)
            except TimeoutError:
                pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="#%(levelname)s [%(asctime)s] - %(filename)s:%(lineno)d - %(message)s",
    )
    asyncio.run(main())
