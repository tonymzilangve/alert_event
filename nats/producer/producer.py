import asyncio
import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv

import nats

load_dotenv()
logger = logging.getLogger(__name__)


async def main():
    nats_url = f"nats://{os.getenv('NATS_HOST')}:{os.getenv('NATS_PORT')}"

    message_data = {
        "ts": datetime.now(),
        "type": "device",
        "severity": "Warning",
        "message": "Something went wrong!",
        "source": "Sensor V-55",
        "payload": json.dumps({"some": "data"}),
    }

    async with await nats.connect(servers=[nats_url]) as nc:
        for i in range(30):
            logger.info("Publishing a new message to [alert] topic...")
            await nc.publish("alert.joe", json.dumps(message_data, default=str).encode())
            await asyncio.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="#%(levelname)s [%(asctime)s] - %(filename)s:%(lineno)d - %(message)s",
    )
    asyncio.run(main())
