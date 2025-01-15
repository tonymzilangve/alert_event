import os
import asyncio
import nats
from dotenv import load_dotenv

load_dotenv()


async def main():
    nats_url = f"nats://{os.getenv("NATS_HOST")}:{os.getenv("NATS_PORT")}"

    async with (await nats.connect(servers=[nats_url])) as nc:
        for i in range(30):
            await nc.publish("alert.joe", b"save")
            await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
