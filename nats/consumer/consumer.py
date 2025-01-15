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
    if msg.data.decode() == 'save':
        name = 'Larus'
        sensor_id = 'D81'
        description = 'Shut down'
        temperature = 99.9
        
        save_msg_query = f'''
        INSERT INTO alert_messages (uuid, name, sensor_id, description, temperature, timestamp)
        VALUES (generateUUIDv4(), '{name}', '{sensor_id}', '{description}', '{temperature}', now())
        '''
        
        db = await anext(get_db())

        try:
            await db.query(query=save_msg_query)
        except Exception as e:
            raise DatabaseError("Failed to save new message!")


async def main() -> None:
    nats_url = f"nats://{os.getenv("NATS_HOST")}:{os.getenv("NATS_PORT")}"
    
    async with (await nats.connect(servers=[nats_url])) as nc:

        sub = await nc.subscribe("alert.*")

        while True:
            try:
                msg = await sub.next_msg()
                print(f"{msg.data} on subject {msg.subject}")
                await save_message(msg)
            except TimeoutError:
                pass


if __name__ == '__main__':
    asyncio.run(main())
