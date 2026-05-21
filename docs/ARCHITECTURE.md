# Architecture

## System overview

```
                ┌────────────────────┐
                │   Frontend (React) │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ FastAPI Gateway    │
                └─────────┬──────────┘
                          │
                ▼ ORCHESTRATION LAYER ▼

        ┌──────────────────────────────────┐
        │ Claim Orchestrator (LangGraph)   │
        └──────────────────────────────────┘

     ┌────────────┬─────────────┬─────────────┐
     ▼            ▼             ▼             ▼

Document      OCR / Vision   Extraction     Policy
Verifier      Pipeline       Agent          Rules Engine

     ▼            ▼             ▼             ▼

 Fraud       Validation      Decision      Explainability
 Checks      Agent           Agent         / Traces
```

## Separation of concerns

| Concern | Implementation |
|---------|----------------|
| Deterministic rules | `backend/app/policy/` |
| Fuzzy extraction | `backend/app/agents/extraction/` |
| Policy validation | Rule engine (not LLM) |
| Orchestration | `backend/app/orchestration/` |
| Explainability | `backend/app/tracing/` |

## LangGraph workflow

```
START → Validate Input → Document Verification → OCR/Vision
     → Structured Extraction → Validation → Policy Rules
     → Decision → Explainability → END
```

## Why multi-agent?

Each agent owns one contract and one trace surface. Failures degrade confidence instead of crashing the graph.

## Why hybrid OCR?

Vision LLM (primary) + Tesseract/PaddleOCR (fallback) improves reliability on handwritten, skewed, and low-quality scans.

## Confidence propagation

```
overall = extraction_confidence × ocr_quality × field_completeness × policy_match
```

Low composite confidence routes to `MANUAL_REVIEW`.

## Implementation phases

1. **Day 1** — FastAPI, models, workflow skeleton, OCR, extraction
2. **Day 2** — Policy engine, decisioning, traces, confidence, tests
3. **Day 3** — UI, eval runner, deployment, demo
