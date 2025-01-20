import logging
from uuid import UUID

from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.exceptions import DatabaseError
from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from fastapi_filter.base.filter import BaseFilterModel
from fastapi_pagination import Page, Params, add_pagination, paginate

from app.api.schemas.alert_message import AlertMessage
from app.db.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", tags=["messages"])


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
        logger.info("Filtering query...")
        filters = []

        if self.type:
            filters.append(f"(type = '{self.type}')")
        if self.severity:
            filters.append(f"(severity = '{self.severity}')")
        if self.acknowledged:
            filters.append(f"(acknowledged ='{int(self.acknowledged)}')")

        if filters:
            sep = " AND "
            filter_query = " WHERE ".join((query, sep.join(filters)))
            return filter_query
        else:
            return query

    class Constants(BaseFilterModel.Constants):
        model = AlertMessage


@router.get("/", response_model=Page[AlertMessage])
async def fetch_alert_messages(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(5, ge=1, le=100, description="Page size"),
    db: AsyncClient = Depends(get_db),
    msg_filter: AlertMessageFilter = FilterDepends(AlertMessageFilter),
) -> Page[AlertMessage]:
    query = "SELECT * FROM alert_messages"
    filtered_query = msg_filter.filter(query)

    try:
        logger.info("Fetching data from DB...")
        db_data = await db.query(query=filtered_query)
    except Exception:
        raise DatabaseError("Failed to fetch data!")

    messages = await convert_query_data(db_data)

    params = Params(size=size, page=page)
    return paginate(messages, params)


@router.patch("/{uuid}/confirm")
async def confirm_alert_message(
    uuid: UUID,
    acknowledged: bool,
    db: AsyncClient = Depends(get_db),
) -> dict:
    query = f"ALTER TABLE alert_messages UPDATE acknowledged = {acknowledged} WHERE uuid = '{uuid}'"

    try:
        logger.info("Altering data in DB...")
        await db.query(query=query)
    except Exception:
        raise DatabaseError("Failed to alter data!")

    updated_message = {"uuid": uuid, "acknowledged": acknowledged}
    return updated_message


add_pagination(router)
