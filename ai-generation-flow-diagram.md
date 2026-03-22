# AI Test Script Generation Flow Diagram

## High-Level Architecture

```text
+--------------------------------------------------------------------------------------+
|                                      INTERNET                                        |
+--------------------------------------------------------------------------------------+
|                                                                                      |
|  +-----------------------------+                +----------------------------------+ |
|  |       Local Machine         |   HTTPS API    |        AI Server (OpenRouter)    | |
|  |      (Windows / Linux)      +--------------->|   OpenAI-compatible endpoint     | |
|  |                             |                |                                  | |
|  |  pytest_demo/ai_generation  |<---------------+  LLM (e.g., gpt-3.5-turbo)       | |
|  |  - cli.py                   |   Generated     +---------------------------------+ |
|  |  - generator.py             |   code text                                       | |
|  |  - prompt_builder.py        |                                                   | |
|  |  - mcp_context.py           |                                                   | |
|  |                             |                +----------------------------------+ |
|  |  +-----------------------+  |   Browser      |      Test Target (Tangerine)     | |
|  |  |      Playwright       +--+--------------->|  https://www.tangerine.ca/...    | |
|  |  | - Launch browser      |  |                +----------------------------------+ |
|  |  | - Visit page          |  |                                                   | |
|  |  | - Capture DOM         |  |                                                   | |
|  |  | - Capture screenshot  |  |                                                   | |
|  |  | - Capture network     |  |                                                   | |
|  |  +-----------+-----------+  |                                                   | |
|  |              |              |                                                   | |
|  |              v              |                                                   | |
|  |  +-----------------------+  |                                                   | |
|  |  |   MCP Context Layer   |  |                                                   | |
|  |  |   BrowserSnapshot     |  |                                                   | |
|  |  |  { url, title,        |  |                                                   | |
|  |  |    element_tree, ...} |  |                                                   | |
|  |  +-----------+-----------+  |                                                   | |
|  |              |              |                                                   | |
|  |              v              |                                                   | |
|  |  +-----------------------+  |                                                   | |
|  |  |     Prompt Builder    |  |                                                   | |
|  |  |  - Optimize context   |  |                                                   | |
|  |  |  - Build instruction  |  |                                                   | |
|  |  +-----------+-----------+  |                                                   | |
|  |              |              |                                                   | |
|  |              v              |                                                   | |
|  |  +-----------------------+  |                                                   | |
|  |  |     Test Generator    |  |                                                   | |
|  |  |  - Parse AI output    |  |                                                   | |
|  |  |  - Normalize code     |  |                                                   | |
|  |  |  - Save test file     |  |                                                   | |
|  |  +-----------+-----------+  |                                                   | |
|  |              |              |                                                   | |
|  |              v              |                                                   | |
|  |  generated_playwright/*.py  |                                                   | |
|  |  @pytest.mark.ai            |                                                   | |
|  |  Local quality check first  |                                                   | |
|  +-----------------------------+                                                   | |
|                                                                                      |
+--------------------------------------------------------------------------------------+
```

---

## Step-by-Step Flow

### 1) CLI Invocation

You run:

```bash
python -m pytest_demo.ai_generation.cli \
  --url "https://www.tangerine.ca/en/personal" \
  --goal "Verify that 'Get Our App' is visible" \
  --test-name "test_tangerine_get_our_app_links" \
  --base-url "https://openrouter.ai/api/v1" \
  --model "openai/gpt-3.5-turbo"
```

### 2) Browser Context Collection (Playwright + MCP)

Playwright opens the target page and collects runtime context:

- URL
- Page title
- DOM / element tree
- Screenshot (optional)
- Network events (optional)

This data is wrapped into a `BrowserSnapshot` (MCP-friendly structure).

### 3) Prompt Optimization (Token Control)

`prompt_builder.py` creates a structured prompt with:

- Test goal
- Constraints (pytest + Playwright sync API)
- Condensed page context

To avoid token overflow, only essential context is included.

### 4) AI Generation Request

The client sends an OpenAI-compatible request to the AI endpoint:

- `system_prompt` (QA automation behavior)
- `user_prompt` (goal + page context)

The AI returns Python test code as text.

### 5) Script Normalization and File Output

`generator.py`:

- Extracts code from the model response
- Removes markdown fences if present
- Applies fallback template if needed
- Saves to:
  - `pytest_demo/tests/AI/generated_playwright/`

### 6) Human Quality Gate (Recommended)

Developer manually validates generated tests:

- Selector stability
- Assertion quality
- Runtime pass/fail behavior

Recommended local run:

```bash
pytest -m ai -v
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

