import uvicorn
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.endpoints.alert_message import router
from app.db.database import create_table


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
