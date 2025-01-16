from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_filter.base.filter import BaseFilterModel
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


class AlertMessageFilter(BaseFilterModel):
    type: AlertMessage.Types | None = None
    severity: AlertMessage.Severities | None = None
    acknowledged: bool | None = None
    
    def filter(self, query: str) -> str:
        filters = []
        
        if self.type:
            filters.append(f"(type = '{self.type}')")
        if self.severity:
            filters.append(f"(severity = '{self.severity}')")
        if self.acknowledged:
            filters.append(f"(acknowledged ='{int(self.acknowledged)}')")

        if filters:
            sep = ' AND '
            filter_query = " WHERE ".join((query, sep.join(filters)))
            return filter_query
        else:
            return query

    class Constants(BaseFilterModel.Constants):
        model = AlertMessage


@router.get("/", response_model=Page[AlertMessage])
async def fetch_alert_messages(
    size: int = 5, 
    page: int = 1,
    db: AsyncClient = Depends(get_db),
    msg_filter: AlertMessageFilter = FilterDepends(AlertMessageFilter)
) -> Page[AlertMessage]:
    query = "SELECT * FROM alert_messages"
    filtered_query = msg_filter.filter(query)

    db_data = await db.query(query=filtered_query)
    messages = await convert_query_data(db_data)
    
    params = Params(size=size, page=page)
    return paginate(messages, params)


add_pagination(router)
