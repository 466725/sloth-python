## Task

Generate one runnable pytest test for this goal:

{goal}

## Test contract

- Function name: `{test_name}`
- Framework: pytest with Playwright sync API
- Target URL: `{url}`
- Include every required import.
- Navigate to the target URL before interacting with the page.
- Add at least one meaningful assertion related to the goal.
- Use the supplied page context to choose realistic locators and interactions.

## Page context

Title: `{title}`
URL: `{url}`

Element tree, truncated:

{element_tree}

## Output

Return only complete Python source code. Do not include Markdown fences, explanations, or comments outside the generated code.
