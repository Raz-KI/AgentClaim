"""Claim submission and status schemas."""
from pydantic import BaseModel


class ClaimSubmission(BaseModel):
    member_id: str
    claim_type: str
    claimed_amount: float