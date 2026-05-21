# AgentClaim

Multi-agent health insurance claim processing system with deterministic policy enforcement, hybrid OCR, and full observability.

## Architecture

```
Frontend (React) → FastAPI Gateway → LangGraph Orchestrator → Specialized Agents → Structured Output
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design rationale.

## Repository layout

| Path | Purpose |
|------|---------|
| `backend/app/models/` | Shared Pydantic contracts (claim, extraction, decision) |
| `backend/app/orchestration/` | LangGraph workflow, state, nodes |
| `backend/app/agents/` | One module per agent (verifier, OCR, extraction, policy, etc.) |
| `backend/app/services/` | OCR, vision, preprocessing, confidence engine |
| `backend/app/policy/` | `policy_terms.json` + deterministic rule engine |
| `backend/app/tracing/` | Trace events, persistence, timeline assembly |
| `backend/eval/` | Evaluation runner + test cases |
| `frontend/` | Claim submission, result + trace UI, eval dashboard |
| `data/samples/` | Sample documents and claims for dev/demo |

## Status

**Scaffold only** — structure is ready; implementation starts on request.

## Quick start (after implementation)

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev

# Database
docker compose up -d postgres
```

## Core principle

> Probabilistic extraction (AI) is separated from deterministic policy enforcement (rules) for reliability, explainability, and auditability.
