# AI Test Script Generation — Flow & Reference Guide

---

## High-Level Architecture

```text
+----------------------------------------------------------------------------------------+
|                                        INTERNET                                        |
+----------------------------------------------------------------------------------------+
|                                                                                        |
|  +------------------------------+                +----------------------------------+  |
|  |        Local Machine         |   HTTPS API    |     AI Server (OpenRouter)       |  |
|  |      (Windows / Linux)       +--------------->|  OpenAI-compatible endpoint      |  |
|  |                              |                |  LLM  (e.g. gpt-4o-mini)         |  |
|  |   pytest_demo/ai_generation  |<---------------+----------------------------------+  |
|  |   - cli.py                   |  Generated                                          |
|  |   - generator.py             |  code (text)                                        |
|  |   - prompt_builder.py        |                                                     |
|  |   - mcp_context.py           |                +----------------------------------+  |
|  |   - ai_client.py             |                |   Test Target (Tangerine Bank)   |  |
|  |                              |   Browser      |  https://www.tangerine.ca/...    |  |
|  |   +-----------------------+  +--------------->+----------------------------------+  |
|  |   |      Playwright       |  |                                                     |
|  |   |  - Launch browser     |  |                                                     |
|  |   |  - Navigate to URL    |  |                                                     |
|  |   |  - Capture DOM        |  |                                                     |
|  |   |  - Capture screenshot |  |                                                     |
|  |   |  - Capture network    |  |                                                     |
|  |   +-----------+-----------+  |                                                     |
|  |               |              |                                                     |
|  |               v              |                                                     |
|  |   +-----------------------+  |                                                     |
|  |   |   MCP Context Layer   |  |                                                     |
|  |   |   BrowserSnapshot     |  |                                                     |
|  |   |  { url, title,        |  |                                                     |
|  |   |    dom, element_tree, |  |                                                     |
|  |   |    screenshot,        |  |                                                     |
|  |   |    network_events }   |  |                                                     |
|  |   +-----------+-----------+  |                                                     |
|  |               |              |                                                     |
|  |               v              |                                                     |
|  |   +-----------------------+  |                                                     |
|  |   |    Prompt Builder     |  |                                                     |
|  |   |  - Optimize context   |  |                                                     |
|  |   |  - Build instruction  |  |                                                     |
|  |   |  - Inject test goal   |  |                                                     |
|  |   +-----------+-----------+  |                                                     |
|  |               |              |                                                     |
|  |               v              |                                                     |
|  |   +-----------------------+  |                                                     |
|  |   |    Test Generator     |  |                                                     |
|  |   |  - Parse AI response  |  |                                                     |
|  |   |  - Strip MD fences    |  |                                                     |
|  |   |  - Save .py file      |  |                                                     |
|  |   +-----------+-----------+  |                                                     |
|  |               |              |                                                     |
|  |               v              |                                                     |
|  |   generated_playwright/*.py  |                                                     |
|  |   @pytest.mark.ai            |                                                     |
|  |   Manual review recommended  |                                                     |
|  +------------------------------+                                                     |
|                                                                                        |
+----------------------------------------------------------------------------------------+
```

---

## How It Works — Step by Step

### 1. CLI Invocation

Trigger generation from the project root:

```bash
python -m pytest_demo.ai_generation.cli \
  --url      "https://www.tangerine.ca/en/personal" \
  --goal     "Verify that the Get Our App links for iOS and Android are visible" \
  --test-name "test_tangerine_get_our_app_links" \
  --output   "pytest_demo/tests/AI/generated_playwright/test_tangerine_get_our_app_links.py"
```

### 2. Browser Context Collection (Playwright + MCP)

Playwright launches headless Chromium, navigates to the target URL, and collects:

| Context piece | Source |
|---|---|
| URL & page title | `page.url`, `page.title()` |
| Full DOM | `page.content()` |
| Element tree | `document.body.innerHTML` |
| Screenshot (base64) | `page.screenshot()` |
| Network events | `requestfinished` listener |

All data is packed into a `BrowserSnapshot` — an immutable, MCP-friendly structure.

### 3. Prompt Optimisation (Token Control)

`prompt_builder.py` assembles the AI prompt with:

- The natural-language test **goal**
- The desired **function name**
- Constraints: use `pytest` + Playwright **sync API**, no prose, no markdown
- Trimmed page context (DOM capped at `AI_GEN_MAX_DOM_CHARS`, default 12 000 chars)

### 4. AI Generation Request

`ai_client.py` sends an OpenAI-compatible chat request:

```
system_prompt  →  Senior QA automation engineer persona
user_prompt    →  Goal + condensed page context (JSON)
temperature    →  0.2  (low randomness = more deterministic code)
```

The AI returns raw Python code as text.

### 5. Script Normalisation and Save

`generator.py`:

1. Strips markdown code fences (` ```python … ``` `) if present
2. Injects `@pytest.mark.ai` marker if missing
3. Falls back to a minimal template when the model returns unusable output
4. Writes the final `.py` file to `pytest_demo/tests/AI/generated_playwright/`

### 6. Human Quality Gate

Always review before committing:

- [ ] Selectors are stable (`id`, `data-testid`, ARIA role, visible text)
- [ ] Assertions are meaningful (not just `assert True`)
- [ ] Test passes locally against the real site

```bash
python -m pytest pytest_demo/tests/AI/generated_playwright/<your_file>.py -v -s
```

---

## Data Flow (Concise)

```text
Goal + URL
   ->
Playwright context capture
   ->
MCP snapshot
   ->
Prompt optimization
   ->
AI API request
   ->
Generated Python test
   ->
Saved test file
   ->
Manual validation (pytest -m ai)
   ->
Optional commit/push
```

---

## Key Components and Roles

| Component | Role |
|----------|------|
| `cli.py` | Entry point (args, env, orchestration) |
| `mcp_context.py` | Collects browser context into structured snapshot |
| `prompt_builder.py` | Builds optimized AI prompt |
| `ai_client.py` | OpenAI-compatible API client |
| `generator.py` | Normalizes and writes generated test code |
| Playwright | Browser automation + page inspection |
| OpenRouter / AI server | LLM code generation |
| Tangerine website | Real test target |

---

## Practical Quality Rules

1. Treat generated tests as drafts, not final truth.
2. Prefer stable locators (`id`, `data-testid`, robust text).
3. Avoid brittle exact-title assertions unless guaranteed stable.
4. Add `@pytest.mark.ai` to generated tests so CI can exclude them by default.
5. Promote only validated tests into stable suites.

---

## Typical Timing and Cost (Approx.)

- Browser context capture: ~2-4s
- AI generation: ~2-8s
- Total generation cycle: ~6-15s
- Cost depends on model and token usage; optimization significantly reduces cost.

---

## Recommended Local Commands

```bash
# Generate
python -m pytest_demo.ai_generation.cli --help

# Validate only AI-generated tests
pytest -m ai -v

# Exclude AI-generated tests (CI-style)
pytest -m "not ai" -v
```

