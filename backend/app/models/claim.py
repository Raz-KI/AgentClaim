from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base

from app.models.base_model import (
    UUIDMixin,
    TimestampMixin
)


class ClaimModel(
    Base,
    UUIDMixin,
    TimestampMixin
):

    __tablename__ = "claims"

    member_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    claim_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    claimed_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="PENDING"
    )

    documents = relationship(
        "DocumentModel",
        back_populates="claim"
    )