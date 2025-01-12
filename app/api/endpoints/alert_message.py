from fastapi import APIRouter

router = APIRouter(
    prefix='/messages',
	tags=['messages']
)


@router.get("/")
def fetch_alert_messages():
    return {"msg": "Hello!"}
