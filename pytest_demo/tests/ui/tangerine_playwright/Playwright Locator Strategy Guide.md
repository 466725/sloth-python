# Playwright Locator Strategy Guide

A comprehensive guide for choosing stable, maintainable element selectors in Playwright tests.

---

## Quick Reference: Locator Types

| Type | Example | Stability | Best For |
|---|---|---:|---|
| **Built-in role** | `page.get_by_role("button", name="Click")` | ⭐⭐⭐⭐⭐ | Primary choice |
| **Built-in label** | `page.get_by_label("Username")` | ⭐⭐⭐⭐⭐ | Forms & inputs |
| **Built-in test ID** | `page.get_by_test_id("submit-btn")` | ⭐⭐⭐⭐⭐ | When semantics fail |
| **Built-in text** | `page.get_by_text("Submit")` | ⭐⭐⭐⭐ | Visible text (if unique) |
| **Built-in placeholder** | `page.get_by_placeholder("Enter email...")` | ⭐⭐⭐⭐ | Input prompts |
| **Built-in alt text** | `page.get_by_alt_text("Icon")` | ⭐⭐⭐⭐ | Images & media |
| **Built-in title** | `page.get_by_title("Help")` | ⭐⭐⭐⭐ | Tooltips |
| **CSS by stable attr** | `page.locator("[data-testid='submit']")` or `page.locator("#login")` | ⭐⭐⭐⭐ | Fallback |
| **CSS by class/structure** | `page.locator(".btn.primary")` or `page.locator("div > button:first")` | ⭐⭐⭐ | Fragile; avoid if possible |
| **XPath by ID** | `page.locator('//button[@id="submit"]')` | ⭐⭐⭐⭐ | Acceptable fallback |
| **XPath by structure** | `page.locator('//div[@class="header"]//button')` | ⭐⭐ | Last resort; very brittle |

---

## Professional Preference (Best → Least Preferred)

### 1. **Playwright Built-in Locators** — Semantic & Accessibility-Driven

```python
page.get_by_role("button", name="Submit")       # Most professional
page.get_by_label("Email Address")
page.get_by_test_id("login-form")
page.get_by_text("Welcome")
```

**Why preferred:**
- Aligned with user behavior and accessibility standards
- Self-documenting: reads like "user intent"
- Most resilient to DOM refactors
- Supports semantic HTML best practices
- Easier for non-technical stakeholders to understand

### 2. **CSS Selectors with Stable Attributes** — Practical Fallback

```python
page.locator("#login")                          # Stable: IDs rarely change
page.locator("[data-testid='submit-btn']")      # Stable: test IDs are intentional
page.locator("[aria-label='Close']")            # Stable: accessibility attributes
```

**When to use:**
- Builtin semantic locators are insufficient
- Element lacks accessible name or role clarity
- Need to combine multiple criteria

**Avoid:**
- Dynamic classes: `.btn-abc123` (changes on every build)
- Visual structure: `div:nth-child(3) > button` (breaks on layout change)

### 3. **XPath Selectors** — Exception Tool Only

```python
page.locator('//button[@id="submit"]')          # Acceptable if stable
page.locator('//button[contains(text(), "Click")]')  # Last resort
```

**When to use:**
- Edge cases where options 1–2 are genuinely insufficient
- Complex conditional logic that CSS cannot express

**Avoid:**
- As a default strategy
- Deep DOM coupling (`//header/div[2]/nav/ul/li[1]/a`)
- Without careful documentation

---

## Decision Tree: Choose Your Locator

Follow this priority when adding a new locator to a test:

```
1. Is there a semantic role (button, link, input, dialog)?
   └─ YES → Use get_by_role() with accessible name
            (Example: page.get_by_role("button", name="Log In"))
   └─ NO  → Continue

2. Is it a form input or labeled element?
   └─ YES → Use get_by_label(), get_by_placeholder(), get_by_alt_text(), or get_by_title()
            (Example: page.get_by_label("Password"))
   └─ NO  → Continue

3. Is there a unique, stable ID or data-testid?
   └─ YES → Use get_by_test_id() or CSS selector
            (Example: page.get_by_test_id("submit-btn") or page.locator("#login"))
   └─ NO  → Continue

4. Is the element uniquely identifiable by stable CSS attributes?
   └─ YES → Use CSS selector
            (Example: page.locator("[aria-label='Close']"))
   └─ NO  → Continue

5. Is a simple XPath sufficient to uniquely identify by stable attributes?
   └─ YES → Use XPath only if CSS cannot express it
            (Example: page.locator('//button[@id="submit"]'))
   └─ NO  → STOP: Refactor your test or add a test ID to the element
```

**Rule of thumb:** If a locator feels long or brittle, step back one level in this list.

---

## Locator Uniqueness & Strictness

Playwright runs in **strict mode by default**. A locator must match exactly one element for actions.

### Validate Uniqueness

```python
locator = page.get_by_role("button", name="Sign In")
expect(locator).to_have_count(1)  # Ensure exactly one match
locator.click()
```

### Handling Multiple Matches

If `get_by_text("Click")` matches 2 elements (desktop + mobile versions):

```python
# Option A: Use more specific semantic locator
page.get_by_role("button", name="Click")

# Option B: Filter by visibility
page.get_by_text("Click").filter(has=page.locator(".desktop-nav"))

# Option C: Use test ID (best long-term)
page.get_by_test_id("primary-cta-button")
```

...existing code...

### Practical Example: Cookie Banner

Below, three approaches to the same element:

```html
<button id="onetrust-accept-btn-handler">Accept All</button>
```

```python
# ✅ Best: Semantic + text (user-centric)
button = page.get_by_role("button", name="Accept All")

# ⭐ Good: Stable ID
button = page.locator("#onetrust-accept-btn-handler")

# ⚠️ Acceptable: XPath by stable ID
button = page.locator('//button[@id="onetrust-accept-btn-handler"]')

# ❌ Avoid: CSS by dynamic class
button = page.locator(".btn.primary.large")  # Likely to change

# ❌ Avoid: DOM structure
button = page.locator("div:nth-child(3) > button")  # Breaks on layout change
```

---

## Best Practices for Stability & Maintainability

### Assertions Over Raw Waits

```python
# ✅ Preferred: Explicit assertion with auto-retry
expect(page.locator("#login")).to_be_visible()

# ⚠️ Manual waits: Use sparingly for advanced timing
page.locator("#login").wait_for(state="visible", timeout=5000)
```

Playwright assertions provide:
- Automatic retry logic
- Clearer failure messages
- Better test readability

### Dynamic UI & Flaky Elements

Extra care for elements that appear after conditions:

- Loading spinners and delayed rendering
- Transient toasts/modals
- Virtualized lists/tables
- UI that appears after API completion

**Guideline:** Assert stable end-state signals (title, heading, enabled button, URL change), not animation details.

```python
# ✅ Stable: Assert final state
expect(page).to_have_title("Dashboard")

# ❌ Fragile: Assert mid-transition
page.locator(".spinner").wait_for(state="hidden")  # May not exist yet
```

### Advanced Selectors: iFrame and Shadow DOM

**iFrames:**
```python
# Switch to frame first, then use normal locators
frame_locator = page.frame_locator("#iframe-id")
frame_locator.get_by_role("button", name="Submit").click()
```

**Shadow DOM:**
- Prefer user-facing locators where possible
- Avoid deep brittle selector chains
- Consider adding stable test IDs in shadow roots if testing is critical

### Test ID Naming Convention

When test IDs are necessary, follow a consistent pattern:

```python
# Suggested format: {page-section}-{action}
page.get_by_test_id("home-nav-login")
page.get_by_test_id("cart-checkout-complete")
page.get_by_test_id("dialog-close-button")

# Treat as test API: changes require test impact review
# Keep stable across UI styling refactors
```

---

## Quick Onboarding: Do / Avoid

| ✅ Do | ❌ Avoid |
|---|---|
| Prefer `get_by_role()`, `get_by_label()`, `get_by_test_id()` first | Starting with long XPath chains for routine elements |
| Use stable attributes (`data-testid`, `id`, `aria-*`) for CSS fallbacks | Selecting by dynamic classes (`.btn-abc123`) or layout-only paths |
| Keep locators short, readable, and tied to user intent | Overly clever selectors that are hard to debug or maintain |
| Add/maintain test IDs when semantics are not sufficient | Depending on fragile DOM depth (`nth-child`, deep nesting) |
| Treat XPath as an exception tool for edge cases | Making XPath the default team locator strategy |
| Validate uniqueness for critical actions (`to_have_count(1)`) | Assuming a locator matches only one element without verification |

---

## Compact Good vs Bad Examples

| Scenario | ✅ Better (Good) | ❌ Fragile (Bad) |
|---|---|---|
| **Main CTA button** | `page.get_by_role("button", name="Sign In")` | `page.locator("div:nth-child(3) > button")` |
| **Search input** | `page.get_by_label("Search")` | `page.locator(".input-7f3a")` (dynamic class) |
| **Nav link** | `page.get_by_role("link", name="Personal")` | `page.locator("//header/div[2]/nav/ul/li[1]/a")` |
| **Form submit** | `page.get_by_test_id("form-submit")` | `page.locator("form button:last-of-type")` |
| **Close icon** | `page.get_by_role("button", name="Close")` | `page.locator("button.close.icon")` |
| **Recovery fallback** | `page.locator("#login-btn")` | `page.locator("a.link.primary.large")` |

---

## Pull Request Locator Checklist

Before merging a test PR with new locators, confirm:

- [ ] Locator follows team priority: **semantic → test ID → CSS → XPath**
- [ ] Selector is readable and intention-revealing
- [ ] Critical action locators are verified unique (`expect().to_have_count(1)`)
- [ ] No deep DOM-coupled chains (`nth-child`, 5+ levels of nesting)
- [ ] Assertions validate user-visible behavior, not internals
- [ ] New test IDs follow naming convention and will remain stable
- [ ] XPath is justified with a comment if used

---

## Summary

✅ **Built-in semantic locators first** — they're the most professional and maintainable  
✅ **CSS with stable attributes second** — solid fallback when semantics fail  
✅ **XPath only for edge cases** — powerful but should be rare  
✅ **Prioritize readability & intent** — tests are living documentation  
✅ **Treat test IDs as test API** — changes are not trivial  

This approach ensures **stability, maintainability, and long-term professionalism** for your Playwright automation strategy.
