from pydantic import BaseModel


class VerificationResult(BaseModel):

    passed: bool

    missing_documents: list[str]

    invalid_documents: list[str]

    message: str