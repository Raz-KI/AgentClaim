# Schemas to define structure of objects/data that comes in and out of our API
# Done using Pydantic models. 
# Different from models as models used to define structure of database  tables and relationship

#Here we will have one request model and one response model

import datetime

from pydantic import BaseModel


class ClaimCreate(BaseModel):
    member_id: str
    claim_amount: float
    treatment_type: str
    docs_type: list[str]

class ClaimResponse(BaseModel):
    claim_id: str
    status: str
    message: str
