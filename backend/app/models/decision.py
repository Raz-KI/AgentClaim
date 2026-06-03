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


class DecisionModel(
    Base,
    UUIDMixin,
    TimestampMixin
):

    __tablename__ = "decisions"

    claim_id: Mapped[UUID] = mapped_column(
        ForeignKey("claims.id"),
        unique=True
    )

    decision: Mapped[str] = mapped_column(
        String
    )

    approved_amount: Mapped[float] = mapped_column(
        Float
    )

    confidence_score: Mapped[float] = mapped_column(
        Float
    )

    reason: Mapped[str] = mapped_column(
        String
    )