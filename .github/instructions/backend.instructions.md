---
applyTo: "main.py,server.py,ai_stock/**/*.py,api/**/*.py,tests/**/*.py"
---

# DSA Backend Instructions

These instructions apply to the backend entry points, `ai_stock/`, `api/`, and
Python tests selected by the `applyTo` pattern above.

## Architecture and resilience

- Preserve existing pipeline boundaries. Reuse services, repositories, schemas,
  and fallback logic instead of creating parallel paths.
- A failure in one provider, notification channel, or optional integration
  should not break the main analysis flow unless fail-fast behavior is required.

## Configuration and compatibility

When changes affect configuration, CLI flags, schedule behavior, API behavior,
or report payloads, update `.env.example` as needed and assess Web/Desktop
compatibility.

## Data providers

Changes to providers under `ai_stock/stock_data/` or `ai_stock/stock_news/`
should preserve provider priority, normalization, timeout and retry behavior,
and graceful degradation.

## Validation

Run `python -m py_compile` on changed Python files and the closest deterministic
tests when feasible.
