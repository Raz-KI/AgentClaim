# Schemas to define structure of objects/data that comes in and out of our API
# Done using Pydantic models. 
# Different from models as models used to define structure of database  tables and relationship

#Here we will have one request model and one response model

import datetime

from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class ClaimCreate(BaseModel):
    member_id: str
    claim_amount: float
    treatment_type: str
    docs_type: list[str]

class ClaimResponse(BaseModel):
    claim_id: str
    status: str
    message: str
    extracted_documents: dict[str, ExtractedDocument] | None = None

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ExtractedField(BaseModel):
  # Explicitly allow primitive types, lists of primitives, or lists of dictionaries
  value: Union[
      str, int, float, bool, List[str], List[Dict[str, Any]], Dict[str, Any]
  ] = Field(
      default=None,
      description="The extracted raw value (string, float, int, array, object, or null).",
  )
  confidence: float = Field(
      description="Confidence score between 0.0 and 1.0."
  )


class ExtractedDocument(BaseModel):
  document_type: str = Field(
      description=(
          "The validated type of document (e.g., HOSPITAL_BILL, PRESCRIPTION)."
      )
  )
  summary: str = Field(
      description="One-sentence summary of the document contents."
  )
  fields: Dict[str, ExtractedField] = Field(
      description="Key-value pairs of extracted metadata."
  )
  missing_fields: List[str] = Field(
      default_factory=list,
      description="Fields expected for this document type that were missing.",
  )
  confidence: float = Field(
      description="Overall document extraction confidence score."
  )
  extraction_notes: Optional[str] = Field(
      default=None,
      description="Notes on unreadable text or image artifacts.",
  )
class OCRResult(BaseModel):
    text: str