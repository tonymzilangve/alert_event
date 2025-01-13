from fastapi import APIRouter

from app.api.schemas.alert_message import AlertMessage


router = APIRouter(
    prefix='/messages',
	tags=['messages']
)


@router.get("/")
def fetch_alert_messages() -> list[AlertMessage]:
    messages = []
    return messages
