# Python + Playwright + MCP + AI Test Generation

This document describes the implemented feature for AI-generated UI tests in this repository.

## Implemented modules

- `pytest_demo/ai_generation/mcp_context.py`
  - Collects browser context from Playwright
  - Exposes MCP-style payload (`dom`, `element_tree`, `screenshot`, `network_events`)
- `pytest_demo/ai_generation/prompt_builder.py`
  - Builds strict prompts for test generation
- `pytest_demo/ai_generation/ai_client.py`
  - OpenAI-compatible chat client wrapper
- `pytest_demo/ai_generation/generator.py`
  - Generates and writes pytest + Playwright scripts
- `pytest_demo/ai_generation/cli.py`
  - CLI entry point to generate tests from URL + goal

## End-to-end workflow

1. Playwright opens the target page.
2. MCP-style context is collected from the live browser.
3. AI receives your goal and the context payload.
4. AI returns a Python pytest + Playwright test script.
5. The script is written to `pytest_demo/tests/ui/generated_playwright/`.

## Prerequisites

- `OPENAI_API_KEY` must be set.
- Dependencies from `requirements.txt` installed.

## Quick start

Set API key:

```powershell
$env:OPENAI_API_KEY = "<your-key>"
```

Generate a homepage test:

```powershell
python -m pytest_demo.ai_generation.cli --url "https://www.tangerine.ca/en" --goal "Verify homepage loads and Sign In entry point is visible" --test-name "test_tangerine_homepage_generated" --output "pytest_demo/tests/ui/generated_playwright/test_tangerine_homepage_generated.py"
```

Generate a sign-in page test:

```powershell
python -m pytest_demo.ai_generation.cli --url "https://www.tangerine.ca/app/#/login" --goal "Verify sign-in page loads and username/password fields are present" --test-name "test_tangerine_signin_generated" --output "pytest_demo/tests/ui/generated_playwright/test_tangerine_signin_generated.py"
```

Generate a sign-up page test:

```powershell
python -m pytest_demo.ai_generation.cli --url "https://www.tangerine.ca/app/#/signup" --goal "Verify sign-up page loads and registration form is visible" --test-name "test_tangerine_signup_generated" --output "pytest_demo/tests/ui/generated_playwright/test_tangerine_signup_generated.py"
```

Run generated tests:

```powershell
pytest -q pytest_demo/tests/ui/generated_playwright
```

## Configuration

The generator reads these settings from `utils/config.py`:

- `AI_GEN_MODEL` (default: `gpt-4.1`)
- `AI_GEN_BASE_URL` (default: `OPENAI_URL`)
- `AI_GEN_MAX_DOM_CHARS` (default: `12000`)
- `AI_GEN_OUTPUT_DIR` (default: `pytest_demo/tests/ui/generated_playwright`)

## Notes

- Generated scripts are normalized into runnable Python code.
- If model output is malformed, generator falls back to a safe pytest template.
- Existing Playwright self-healing locators remain available for your main Tangerine test suite.
