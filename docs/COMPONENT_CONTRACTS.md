# Component contracts (planned)

All agents read/write types from `backend/app/models/contracts/`.

| Contract | File | Used by |
|----------|------|---------|
| `ClaimSubmission` | `claim.py` | API, orchestrator |
| `UploadedDocument` | `document.py` | API, verifier, OCR |
| `VerificationResult` | `document.py` | Document verifier |
| `ExtractedMedicalData` | `extraction.py` | Extraction, validation |
| `PolicyConstraintResult` | `decision.py` | Rules engine |
| `ClaimDecision` | `decision.py` | Decision, API |
| `TraceEvent` | `trace.py` | All agents |

Implement Pydantic models in these files during Day 1.
