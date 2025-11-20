from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ScanRequest(BaseModel):
    token: str
    channel: str = "qr"
    location: Optional[str] = None


class ScanResponse(BaseModel):
    identity_id: int
    status: str
    full_name: str
    role: str | None
    verified_at: datetime

