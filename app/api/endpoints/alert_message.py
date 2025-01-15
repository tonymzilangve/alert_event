from fastapi import APIRouter, Depends
from fastapi_pagination import add_pagination, paginate, Page, Params
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.db.database import get_db


router = APIRouter(
    prefix='/messages',
	tags=['messages']
)


@router.get("/", response_model=Page)
async def fetch_alert_messages(
    size: int = 5, 
    page: int = 1,
    db: AsyncClient = Depends(get_db)
) -> Page:
    query = "SELECT * FROM alert_messages"
    messages = await db.query(query=query)
    
    params = Params(size=size, page=page)
    return paginate(messages.result_rows, params)

add_pagination(router)
