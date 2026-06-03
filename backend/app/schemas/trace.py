"""Trace event and timeline schemas."""
from pydantic import BaseModel
from datetime import datetime


class TraceEvent(BaseModel):

    timestamp: datetime

    component: str

    status: str

    message: str

    confidence_delta: float = 0.0