import json
import os
import asyncio
import nats
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


async def main():
    nats_url = f"nats://{os.getenv("NATS_HOST")}:{os.getenv("NATS_PORT")}"

    message_data = {
        "ts": datetime.now(),
        "type": "device",
        "severity": "Warning",
        "message": "Something went wrong!",
        "source": "Sensor V-55",
        "payload": json.dumps({"some": "data"}),
    }
    
    async with (await nats.connect(servers=[nats_url])) as nc:
        for i in range(30):
            await nc.publish("alert.joe", json.dumps(message_data, default=str).encode())
            await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
