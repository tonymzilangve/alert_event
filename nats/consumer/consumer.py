import json
import os
import asyncio
import nats

from typing import AsyncGenerator
from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.exceptions import DatabaseError
from nats.errors import TimeoutError


from dotenv import load_dotenv

load_dotenv()


async def get_db() -> AsyncGenerator[AsyncClient, None]:
    db = await get_async_client(
        username=os.getenv("CH_USERNAME"),
        password=os.getenv("CH_PASSWORD"),
        host=os.getenv("CH_HOST")
    )

    try:
        yield db
    finally:
        db.close()  


async def save_message(msg: str) -> None:
    data = json.loads(msg.data)
    
    save_msg_query = f'''
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
    '''
    
    db = await anext(get_db())

    try:
        await db.query(query=save_msg_query)
    except Exception as e:
        raise DatabaseError("Failed to save new message!")


async def main() -> None:
    nats_url = f"nats://{os.getenv('NATS_HOST')}:{os.getenv('NATS_PORT')}"
    
    async with (await nats.connect(servers=[nats_url])) as nc:
        sub = await nc.subscribe("alert.*")

        while True:
            try:
                msg = await sub.next_msg()
                await save_message(msg)
                await asyncio.sleep(0.1)
            except TimeoutError:
                pass


if __name__ == '__main__':
    asyncio.run(main())
