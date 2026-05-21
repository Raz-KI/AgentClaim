# API (planned)

Base URL: `http://localhost:8000/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/claims/submit` | Submit claim + documents |
| `GET` | `/claims/{claim_id}` | Claim status and decision |
| `GET` | `/claims/{claim_id}/trace` | Full execution trace |
| `GET` | `/claims/{claim_id}/extraction` | Extracted medical fields |
| `POST` | `/eval/run` | Run evaluation suite |
| `GET` | `/eval/results` | Eval pass/fail summary |
| `GET` | `/health` | Health check |

## Response contracts

All responses use shared Pydantic models from `backend/app/models/contracts/`.
