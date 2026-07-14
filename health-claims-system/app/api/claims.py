# These are endpoints 
from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.services.claim_service import ClaimService

claim_service = ClaimService()

router = APIRouter()

@router.post("/claims/submit", response_model=ClaimResponse)
async def submit_claim(
    member_id: str = Form(...),
    claim_amount: float = Form(...),
    treatment_type: str = Form(...),
    docs: list[UploadFile] = File(...)
):
    claim_data = ClaimCreate(
        member_id=member_id,
        claim_amount=claim_amount,
        treatment_type=treatment_type
    )
    result = claim_service.submit_claim(claim_data, docs)
    return result