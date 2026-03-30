# Playwright Built-in vs CSS vs XPath Locators

## Conclusion

All three locator styles can work for the same test scenario, but they are not equally stable over time.

### Stability and Professional Preference (Best -> Least Preferred)

1. **Playwright built-in locators** (`get_by_role`, `get_by_label`, `get_by_test_id`, etc.)
2. **CSS locators** (prefer stable attributes like `data-testid`, `id`, `aria-*`)
3. **XPath locators** (use only when needed for special cases)

### Why This Ranking

- **Built-in locators** are the most professional default because they are semantic, readable, and closer to user behavior. They are usually more resilient to DOM refactors and support accessibility-driven testing.
- **CSS locators** are a solid fallback and remain maintainable when tied to stable attributes. They become brittle when based on visual structure or dynamic classes.
- **XPath** is powerful but often harder to read and easier to break when page structure changes. It should be a targeted tool, not a default strategy.

### Recommended Team Standard

Use this priority order for new tests:

1. Built-in semantic locators first
2. CSS selectors with stable attributes second
3. XPath only for edge cases where 1 and 2 are insufficient

This approach gives the best balance of **stability, maintainability, and professionalism** for long-term Playwright UI automation.

### Quick Onboarding: Do / Avoid

| Do | Avoid |
|---|---|
| Prefer `get_by_role`, `get_by_label`, and `get_by_test_id` first | Starting with long XPath chains for routine elements |
| Use stable attributes (`data-testid`, `id`, `aria-*`) for CSS fallbacks | Selecting by dynamic classes or layout-only selectors |
| Keep locators short, readable, and tied to user intent | Overly clever selectors that are hard to debug |
| Add/maintain test IDs when semantics are not enough | Depending on fragile DOM depth (`nth-child`, deep descendant paths) |
| Treat XPath as an exception tool for edge cases | Making XPath the default team locator strategy |

### Locator Decision Tree (Fast Path)

Use this order when adding a new locator:

1. `get_by_role(...)` with accessible name
2. `get_by_label(...)` / `get_by_placeholder(...)` / `get_by_title(...)`
3. `get_by_test_id(...)` (if semantics are not enough)
4. CSS with stable attributes (`data-testid`, `id`, `aria-*`)
5. XPath only for edge cases

If a locator feels long or fragile, step back and move one level up this list.

### Uniqueness Rule (Strictness)

A locator should match exactly the intended element.

- For critical actions (click/submit), validate uniqueness.
- Prefer clear failures over silent ambiguity.

Example pattern:

```python
locator = page.get_by_role("button", name="Sign In")
expect(locator).to_have_count(1)
locator.click()
```

### Assertions Over Raw Waits

Prefer Playwright assertions (`expect`) instead of manual `count()` + `wait_for()` chains.

- `expect(...)` gives auto-retry, clearer failures, and cleaner tests.
- Keep raw waits for rare advanced timing scenarios.

### Dynamic UI and Flaky Surface Areas

Extra care is needed for:

- Loading spinners and delayed rendering
- Transient toasts/modals
- Virtualized lists/tables
- UI that appears after API completion

Guideline: assert stable end-state signals (title, heading, enabled button, URL change), not animation details.

### iFrame and Shadow DOM Notes

- For iframes, switch to `frame_locator(...)` first, then use normal locators inside it.
- For shadow DOM, prefer user-facing locators where possible; avoid deep brittle selector chains.

### Test ID Contract (Team Convention)

When test IDs are needed, keep them consistent and intentional.

- Suggested naming: `page-section-action` (example: `home-nav-login`)
- Treat test IDs as test API: avoid renaming without test impact review
- Keep test IDs stable across UI styling refactors

### Compact Good vs Bad Examples

| Scenario | Better (Good) | Fragile (Bad) |
|---|---|---|
| Main CTA button | `get_by_role("button", name="Sign In")` | `locator("div:nth-child(3) > button")` |
| Search input | `get_by_label("Search")` or `[aria-label="Search"]` | `locator(".input-7f3a")` |
| Nav link | `get_by_role("link", name="Personal")` | `locator("//header/div[2]/nav/ul/li[1]/a")` |
| Recovery fallback | `get_by_test_id("home-nav-login")` | `locator("a.link.primary.large")` |

### Pull Request Locator Checklist

Before merge, confirm:

- Locator follows team priority (semantic -> test id -> CSS -> XPath)
- Selector is readable and intention-revealing
- Critical action locators are unique (`to_have_count(1)` when needed)
- No deep DOM-coupled chains unless unavoidable
- Assertions validate user-visible behavior, not internals
- New test IDs follow naming contract and are stable
