Goal:
{goal}

Create a runnable test function named `{test_name}` using pytest and Playwright sync API.
Requirements:
- Include imports required by the generated test.
- Navigate to `{url}`.
- Verify the page with at least one meaningful assertion.
- Prefer locator strategies (id, metadata-testid, text) that are likely stable.
- Do not include explanations, markdown, or prose. Return code only.

Page context:
Title: {title}
URL: {url}

Element tree (truncated):
{element_tree}
