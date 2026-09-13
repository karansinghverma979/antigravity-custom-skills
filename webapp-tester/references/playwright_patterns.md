# Playwright Headless Automation & E2E Testing Patterns

This guide outlines reliable browser automation patterns for verifying web apps and catching UI bugs using Playwright.

---

## 1. Core Lifecycle & Network Synchronization

Always wait for `networkidle` or specific locator visibility before asserting state:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:3000")
    
    # Crucial for React/Vite/Next SPAs:
    page.wait_for_load_state("networkidle")
    
    # Assert and screenshot
    assert page.is_visible("text=Dashboard")
    page.screenshot(path="dashboard_verification.png", full_page=True)
    browser.close()
```

---

## 2. Best Practices for Element Selection

1. **User-Visible Roles**: Prefer `page.get_by_role("button", name="Submit")` or `page.get_by_text("Confirm")`.
2. **Test IDs**: Use `data-testid` attributes when present to avoid brittle CSS selector chains.
3. **Console Log Auditing**: Listen to browser error events to catch silent JavaScript exceptions:
   ```python
   page.on("console", lambda msg: print(f"[BROWSER {msg.type}] {msg.text}"))
   ```
