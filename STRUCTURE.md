# Project structure reference

```
AgentClaim/
├── README.md
├── STRUCTURE.md
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── EVALUATION.md
│
├── scripts/
│   ├── seed_db.py
│   └── run_eval.sh
│
├── data/samples/
│   ├── documents/
│   └── claims/
│
├── backend/
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py                 # FastAPI entry
│   │   ├── config/settings.py
│   │   ├── core/                   # logging, exceptions
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   ├── routes/             # claims, health, eval
│   │   │   └── dependencies/
│   │   ├── models/
│   │   │   ├── contracts/          # shared agent contracts
│   │   │   └── schemas/            # HTTP schemas
│   │   ├── db/
│   │   │   ├── models/             # claims, documents, traces, ...
│   │   │   ├── repositories/
│   │   │   └── migrations/
│   │   ├── orchestration/          # LangGraph
│   │   │   ├── state.py
│   │   │   ├── graph.py
│   │   │   └── nodes/              # one file per workflow step
│   │   ├── agents/
│   │   │   ├── document_verifier/
│   │   │   ├── ocr/
│   │   │   ├── extraction/
│   │   │   ├── validation/
│   │   │   ├── policy/
│   │   │   ├── decision/
│   │   │   ├── explainability/
│   │   │   └── fraud/              # bonus
│   │   ├── services/
│   │   │   ├── preprocessing/
│   │   │   ├── ocr/
│   │   │   ├── vision/
│   │   │   ├── classification/
│   │   │   └── confidence/
│   │   ├── policy/
│   │   │   ├── policy_terms.json
│   │   │   ├── loader.py
│   │   │   └── rules_engine.py
│   │   └── tracing/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── failure/
│   └── eval/
│       ├── runner.py
│       ├── metrics.py
│       ├── test_cases/
│       └── fixtures/
│
└── frontend/
    ├── package.json
    ├── src/
    │   ├── pages/                  # Submission, Result, Eval
    │   ├── components/             # trace, claim, common
    │   ├── api/
    │   ├── types/
    │   └── hooks/
    └── README.md
```

## Implementation order (when ready)

| Phase | Focus |
|-------|--------|
| Day 1 | Contracts, FastAPI, LangGraph skeleton, OCR/extraction |
| Day 2 | Policy engine, decision, traces, confidence, tests |
| Day 3 | UI, eval runner, polish |
