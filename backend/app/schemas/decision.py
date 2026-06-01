"""Claim decision schemas."""
from pydantic import BaseModel


class ClaimDecision(BaseModel):
    decision: str
    approved_amount: float
    confidence_score: float