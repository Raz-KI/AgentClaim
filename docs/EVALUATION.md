# Evaluation framework (planned)

## Metrics

- Decision accuracy
- Extraction field completeness
- Confidence calibration
- False approvals / false rejections

## Layout

- `backend/eval/runner.py` — batch runner over test cases
- `backend/eval/test_cases/` — JSON fixtures with `expected` vs `actual` comparison
- Admin UI: `frontend/src/pages/EvalDashboard.tsx`

## Usage (after implementation)

```bash
cd backend && python -m eval.runner --suite default
```
