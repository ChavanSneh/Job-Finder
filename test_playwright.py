from playwright.sync_api import sync_playwright
import time

print("✅ Script started")

with sync_playwright() as p:
    print("🚀 Playwright loaded")

    browser = p.chromium.launch(headless=False)  # IMPORTANT
    print("🧭 Browser launched")

    page = browser.new_page()
    print("📄 New page created")

    page.goto("https://example.com")
    print("🌐 Page loaded")

    print("📌 Page title:", page.title())

    time.sleep(5)  # keep browser open so you SEE it
    browser.close()

print("🏁 Script finished")
