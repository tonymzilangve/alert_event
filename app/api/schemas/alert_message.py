from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class AlertMessage(BaseModel):
    class Types(str, Enum):
        USER = "user"
        DEVICE = "device"
        SYSTEM = "system"

    class Severities(str, Enum):
        CRITICAL = "critical"
        WARNING = "warning"
        INFO = "info"

    uuid: UUID
    ts: datetime
    type: Types
    severity: Severities
    message: str
    source: str
    payload: str
    acknowledged: bool = False
