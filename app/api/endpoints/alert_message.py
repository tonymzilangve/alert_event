from fastapi import APIRouter, Depends
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.db.database import get_db


router = APIRouter(
    prefix='/messages',
	tags=['messages']
)


@router.get("/")
async def fetch_alert_messages(db: AsyncClient = Depends(get_db)) -> list:
    query = "SELECT * FROM alert_messages"
    messages = await db.query(query=query)
    
    return messages.result_rows
