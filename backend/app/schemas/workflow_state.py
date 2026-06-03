from pydantic import BaseModel
from typing import Optional

from app.schemas.claim import ClaimSubmission
from app.schemas.verification import VerificationResult
from app.schemas.extraction import ExtractedMedicalData
from app.schemas.decision import ClaimDecision
from app.schemas.trace import TraceEvent


class ClaimWorkflowState(BaseModel):

    claim: ClaimSubmission

    verification: Optional[VerificationResult] = None

    extraction: Optional[ExtractedMedicalData] = None

    decision: Optional[ClaimDecision] = None

    trace_events: list[TraceEvent] = []