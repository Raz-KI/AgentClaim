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


class ExtractionResultModel(
    Base,
    UUIDMixin,
    TimestampMixin
):

    __tablename__ = "extraction_results"

    claim_id: Mapped[UUID] = mapped_column(
        ForeignKey("claims.id")
    )

    patient_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    doctor_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    diagnosis: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    total_amount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )