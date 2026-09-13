---
name: webapp-tester
description: >-
  Headless web application tester, Playwright automation runner, and E2E visual verifier.
  Use whenever testing local frontend servers, verifying DOM selectors, capturing automated browser screenshots,
  or debugging client-side JavaScript errors via Playwright.
---

# 🌐 WebApp Tester: Headless Browser & E2E Testing Suite

Use this skill when testing local web applications, running end-to-end browser assertions, or capturing visual screenshots via Playwright.

---

## 🏛️ Core Principles & Automation Patterns

For comprehensive selector strategies and lifecycle hooks:
- [Playwright Patterns Guide](./references/playwright_patterns.md)

---

## 🔄 Webapp Verification Workflow

### Step 1: Quick URL & Screenshot Test
Run the bundled CLI helper against a local or remote URL:

```bash
python ~/.gemini/antigravity-cli/skills/webapp-tester/scripts/run_playwright.py http://localhost:3000 screenshot.png
```

### Step 2: Custom E2E Scripting
Write targeted sync/async Playwright scripts to assert user flows (login, form submission, modal dialogs) and inspect console logs for errors.
