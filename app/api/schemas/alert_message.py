from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class AlertMessage(BaseModel):
    class Types(str, Enum):
        USER = "user"
        DEVICE = "device"
        SYSTEM = "system"

    class Severities(str, Enum):
        CRITICAL = "Critical"
        WARNING = "Warning"
        INFO = "Info"
    
    uuid: UUID
    ts: datetime
    type: Types
    severity: Severities
    message: str
    source: str
    payload: str
    acknowledged: bool = False
