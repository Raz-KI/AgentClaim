"""Claim decision schemas."""
from pydantic import BaseModel
from typing import Literal

class ClaimDecision(BaseModel):
    decision: Literal[
        "APPROVED",
        "PARTIAL",
        "REJECTED",
        "MANUAL_REVIEW"
    ]
    approved_amount: float
    confidence_score: float

    reasons: list[str]