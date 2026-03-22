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
|  |   - cli.py                   |  Generated                                           |
|  |   - generator.py             |  code (text)                                         |
|  |   - prompt_builder.py        |                                                      |
|  |   - mcp_context.py           |                +----------------------------------+  |
|  |   - ai_client.py             |                |   Test Target (Tangerine Bank)   |  |
|  |                              |   Browser      |  https://www.tangerine.ca/...    |  |
|  |   +-----------------------+  +--------------->+----------------------------------+  |
|  |   |      Playwright       |  |                                                      |
|  |   |  - Launch browser     |  |                                                      |
|  |   |  - Navigate to URL    |  |                                                      |
|  |   |  - Capture DOM        |  |                                                      |
|  |   |  - Capture screenshot |  |                                                      |
|  |   |  - Capture network    |  |                                                      |
|  |   +-----------+-----------+  |                                                      |
|  |               |              |                                                      |
|  |               v              |                                                      |
|  |   +-----------------------+  |                                                      |
|  |   |   MCP Context Layer   |  |                                                      |
|  |   |   BrowserSnapshot     |  |                                                      |
|  |   |  { url, title,        |  |                                                      |
|  |   |    dom, element_tree, |  |                                                      |
|  |   |    screenshot,        |  |                                                      |
|  |   |    network_events }   |  |                                                      |
|  |   +-----------+-----------+  |                                                      |
|  |               |              |                                                      |
|  |               v              |                                                      |
|  |   +-----------------------+  |                                                      |
|  |   |    Prompt Builder     |  |                                                      |
|  |   |  - Optimize context   |  |                                                      |
|  |   |  - Build instruction  |  |                                                      |
|  |   |  - Inject test goal   |  |                                                      |
|  |   +-----------+-----------+  |                                                      |
|  |               |              |                                                      |
|  |               v              |                                                      |
|  |   +-----------------------+  |                                                      |
|  |   |    Test Generator     |  |                                                      |
|  |   |  - Parse AI response  |  |                                                      |
|  |   |  - Strip MD fences    |  |                                                      |
|  |   |  - Save .py file      |  |                                                      |
|  |   +-----------+-----------+  |                                                      |
|  |               |              |                                                      |
|  |               v              |                                                      |
|  |   generated_playwright/*.py  |                                                      |
|  |   @pytest.mark.ai            |                                                      |
|  |   Manual review recommended  |                                                      |
|  +------------------------------+                                                      |
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

## Data Flow (Summary)

```text
Goal + Target URL
        │
        ▼
Playwright browser context capture
        │
        ▼
MCP BrowserSnapshot  { url, title, dom, element_tree, screenshot, network_events }
        │
        ▼
Prompt builder  →  optimised system + user prompt
        │
        ▼
AI API request  (OpenRouter / OpenAI-compatible)
        │
        ▼
Generated Python test code (text)
        │
        ▼
Normalisation & file save  →  pytest_demo/tests/AI/generated_playwright/
        │
        ▼
Manual validation  →  pytest -m ai -v
        │
        ▼
Optional: git add / commit / promote to stable suite
```

---

## Key Components and Roles

| Component | File | Role |
|---|---|---|
| CLI entry point | `cli.py` | Parses args, wires all components, drives generation |
| Context collector | `mcp_context.py` | Captures live browser state as `BrowserSnapshot` |
| Prompt builder | `prompt_builder.py` | Builds optimised, token-efficient AI prompt |
| AI client | `ai_client.py` | OpenAI-compatible HTTP client |
| Script generator | `generator.py` | Normalises AI output and writes the `.py` test file |
| Playwright | — | Browser automation and page inspection |
| OpenRouter | — | LLM gateway (supports GPT-4o, Gemini, Mistral, etc.) |
| Tangerine website | — | Real test target used for demos |

---

## Practical Quality Rules

1. Treat generated tests as **drafts** — review before committing.
2. Prefer stable locators: `id`, `data-testid`, ARIA role, visible text.
3. Avoid exact-title assertions unless the title is guaranteed stable.
4. Keep `@pytest.mark.ai` until the test is validated and promoted.
5. Only merge tests that pass reliably against the live site.

---

## Typical Timings and Cost

| Phase | Duration |
|---|---|
| Browser context capture | ~2–4 s |
| AI generation | ~2–8 s |
| Total cycle | ~6–15 s |

Cost depends on the model and token count. Keeping DOM context trimmed
(`AI_GEN_MAX_DOM_CHARS`) significantly reduces cost per generation.

---

## Useful Commands

```bash
# Show all CLI options
python -m pytest_demo.ai_generation.cli --help

# Run only AI-generated tests
pytest -m ai -v

# Run everything except AI-generated tests (CI default)
pytest -m "not ai" -v

# Run the demo (mock client, no API key needed)
python pytest_demo/ai_generation/demo.py
```

---

## Try It Yourself — Generate a New Script

Follow these steps to generate a test for any new scenario from scratch.

### Step 1 — Set Environment Variables

If you have already added `OPENAI_API_KEY` as a **permanent Windows environment variable**
(Control Panel → System → Advanced → Environment Variables), you do **not** need to set it
again — it survives reboots and new terminal sessions.

You only need to set the two OpenRouter-specific vars per session (or add them to Windows env
vars once as well):

```powershell
# PowerShell — only required if not already set as permanent Windows env vars
$env:OPENAI_API_KEY  = "sk-or-v1-<your-openrouter-key>"   # skip if already permanent
$env:AI_GEN_BASE_URL = "https://openrouter.ai/api/v1"
$env:AI_GEN_MODEL    = "openai/gpt-4o-mini"                # any model at openrouter.ai/models
```

> **Tip:** Add `AI_GEN_BASE_URL` and `AI_GEN_MODEL` to Windows env vars too so you never
> need to set them again.
>
> **Recommended free/cheap models:** `openai/gpt-4o-mini`, `google/gemini-flash-1.5`,
> `mistralai/mistral-7b-instruct`

### Step 2 — Choose Your Scenario

| Scenario | `--url` | `--goal` |
|---|---|---|
| Tangerine homepage | `https://www.tangerine.ca/en/personal` | `verify hero section and nav links are visible` |
| Sign In page | `https://www.tangerine.ca/app#/login` | `verify sign-in form has username, password and submit button` |
| Sign Up page | `https://www.tangerine.ca/app#/signup` | `verify all required sign-up form fields are present` |
| Any other page | your URL | your natural-language goal |

### Step 3 — Run the CLI

```powershell
cd C:\path\to\sloth-python

python -m pytest_demo.ai_generation.cli `
  --url       "https://www.tangerine.ca/app#/login" `
  --goal      "verify the sign-in form has username and password fields and a submit button" `
  --test-name "test_tangerine_signin_form" `
  --output    "pytest_demo/tests/AI/generated_playwright/test_tangerine_signin_form.py"
```

Playwright opens headless Chromium, captures page context, sends it to the AI, and writes
the generated test file automatically.

### Step 4 — Review the Generated File

Open the file in your IDE and check:

- [ ] Function name matches `--test-name`
- [ ] Selectors look stable (`id`, `role`, `text` — not brittle XPath)
- [ ] Assertions are meaningful

### Step 5 — Run the Generated Test

```bash
python -m pytest pytest_demo/tests/AI/generated_playwright/test_tangerine_signin_form.py -v -s
```

### Step 6 — (Optional) Watch It in a Real Browser

```powershell
$env:PW_HEADLESS = "false"
python -m pytest pytest_demo/tests/AI/generated_playwright/test_tangerine_signin_form.py -v -s
```

### Notes

- Re-running the CLI with the same `--output` path **overwrites the file** — use a unique
  `--test-name` per scenario to keep previous scripts.
- The `@pytest.mark.ai` marker is injected automatically; CI excludes these tests by default
  until you manually promote them.
- If the first attempt fails, tweak the selector or assertion manually — AI drafts are a
  starting point, not a finished product.


