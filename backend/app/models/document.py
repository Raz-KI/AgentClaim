from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

from app.models.base_model import (
    UUIDMixin,
    TimestampMixin
)


class DocumentModel(
    Base,
    UUIDMixin,
    TimestampMixin
):

    __tablename__ = "documents"

    claim_id: Mapped[UUID] = mapped_column(
        ForeignKey("claims.id")
    )

    filename: Mapped[str] = mapped_column(
        String
    )

    document_type: Mapped[str] = mapped_column(
        String
    )

    storage_path: Mapped[str] = mapped_column(
        String
    )

    claim = relationship(
        "ClaimModel",
        back_populates="documents"
    )