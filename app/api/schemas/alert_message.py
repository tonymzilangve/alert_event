from datetime import datetime
from pydantic import BaseModel


class AlertMessage(BaseModel):
    sensor_id: str
    description: str
    temperature: float
    timestamp: datetime
