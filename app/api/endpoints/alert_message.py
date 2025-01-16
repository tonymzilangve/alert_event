from fastapi import APIRouter, Depends
from fastapi_pagination import add_pagination, paginate, Page, Params
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.api.schemas.alert_message import AlertMessage
from app.db.database import get_db


router = APIRouter(
    prefix='/messages',
	tags=['messages']
)

async def convert_query_data(data: list[tuple]) -> list[dict]:
    converted_data = []
    for row in data.result_rows:
        converted_data.append(dict(zip(data.column_names, row)))

    return converted_data


@router.get("/", response_model=Page[AlertMessage])
async def fetch_alert_messages(
    size: int = 5, 
    page: int = 1,
    db: AsyncClient = Depends(get_db)
) -> Page[AlertMessage]:
    query = "SELECT * FROM alert_messages"
    params = Params(size=size, page=page)
    
    db_data = await db.query(query=query)
    messages = await convert_query_data(db_data)
    
    return paginate(messages, params)


add_pagination(router)
