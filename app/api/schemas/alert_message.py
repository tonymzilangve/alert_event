from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Literal


class AlertMessage(BaseModel):
    uuid: UUID
    ts: datetime
    type: Literal["user", "device", "system"]
    severity: Literal["Critical", "Warning", "Info"]
    message: str
    source: str
    payload: str
    acknowledged: bool = False
