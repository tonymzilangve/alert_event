import asyncio
import json
import logging
from datetime import datetime

import nats

from config import settings

logger = logging.getLogger(__name__)


async def main():
    nats_url = f"nats://{settings.NATS_HOST}:{settings.NATS_PORT}"

    message_data = {
        "ts": datetime.now(),
        "type": "device",
        "severity": "warning",
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
