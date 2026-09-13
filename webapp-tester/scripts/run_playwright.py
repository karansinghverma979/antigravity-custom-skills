#!/usr/bin/env python3
"""
Playwright Runner Helper
Navigates to a target URL, checks status, captures a screenshot, and reports JS console logs.
"""

import sys
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def test_url(url: str, screenshot_out: str = "screenshot.png") -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] 'playwright' package not installed. Run: pip install playwright && playwright install chromium")
        return False

    print(f"[*] Navigating to: {url}")
    logs = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
            page.on("pageerror", lambda err: logs.append(f"[PAGE ERROR] {err}"))

            resp = page.goto(url, timeout=15000)
            status = resp.status if resp else "N/A"
            print(f"  [OK] Response Status: {status}")

            page.wait_for_load_state("networkidle", timeout=5000)
            page.screenshot(path=screenshot_out, full_page=True)
            print(f"  [OK] Screenshot saved to: {screenshot_out}")

            browser.close()

        if logs:
            print("\n--- Browser Console Output ---")
            for log in logs[:15]:
                print(f"  {log}")

        return True
    except Exception as e:
        print(f"[ERROR] Playwright test failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_playwright.py <url> [screenshot_output_path]")
        sys.exit(1)

    target_url = sys.argv[1]
    ss = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
    success = test_url(target_url, ss)
    sys.exit(0 if success else 1)
