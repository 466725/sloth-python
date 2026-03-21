# AI UI Script Generation (Playwright + MCP Context)

This module generates pytest + Playwright test scripts from a live page context.

## What it does

- Opens a page with Playwright
- Collects MCP-style context (`dom`, `element_tree`, `screenshot`, `network_events`)
- Sends context + your goal to an OpenAI-compatible model
- Writes a runnable test file

## Quick start

Set your API key first:

```powershell
$env:OPENAI_API_KEY = "<your-key>"
```

Generate a test script:

```powershell
python -m pytest_demo.ai_generation.cli --url "https://www.tangerine.ca/en" --goal "Verify homepage loads and the login entry point is visible" --test-name "test_tangerine_homepage_generated" --output "pytest_demo/tests/ui/generated_playwright/test_tangerine_homepage_generated.py"
```

Run the generated test:

```powershell
pytest -q pytest_demo/tests/ui/generated_playwright/test_tangerine_homepage_generated.py
```

## Environment variables

- `OPENAI_API_KEY` (required)
- `AI_GEN_MODEL` (default: `gpt-4.1`)
- `AI_GEN_BASE_URL` (default: value of `OPENAI_URL` from settings)
- `AI_GEN_MAX_DOM_CHARS` (default: `12000`)
- `AI_GEN_OUTPUT_DIR` (default: `pytest_demo/tests/ui/generated_playwright`)

