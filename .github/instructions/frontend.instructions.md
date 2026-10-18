---
applyTo: "apps/dsa-web/**"
---

# DSA Web Client Instructions

These instructions apply only to files under `apps/dsa-web/`, as specified by
the `applyTo` pattern above. They guide changes to the React web client.

## Implementation

- Preserve the existing Vite + React structure.
- Reuse current API and state patterns instead of adding parallel client abstractions.

## Compatibility

When changes affect API fields, route behavior, Markdown or chart rendering,
local backend startup, or report payloads, assess their impact on the Web client.

## Validation

When feasible, validate Web changes from `apps/dsa-web/` with:

```bash
npm ci
npm run lint
npm run build
```
