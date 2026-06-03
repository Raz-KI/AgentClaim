from pydantic import BaseModel
from typing import Optional


class ExtractedMedicalData(BaseModel):

    patient_name: Optional[str] = None

    diagnosis: list[str] = []

    doctor_name: Optional[str] = None

    registration_number: Optional[str] = None

    hospital_name: Optional[str] = None

    total_amount: Optional[float] = None

    extraction_confidence: float