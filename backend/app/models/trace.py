from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

from app.models.base_model import (
    UUIDMixin,
    TimestampMixin
)


class TraceEventModel(
    Base,
    UUIDMixin,
    TimestampMixin
):

    __tablename__ = "trace_events"

    claim_id: Mapped[UUID] = mapped_column(
        ForeignKey("claims.id")
    )

    component: Mapped[str] = mapped_column(
        String
    )

    status: Mapped[str] = mapped_column(
        String
    )

    message: Mapped[str] = mapped_column(
        String
    )

    confidence_delta: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )