import time
from playwright.sync_api import Page

def click_with_retry(page: Page, selector: str, max_retries=3, delay=2):
    """Attempts to click a button with cursor movement and retry logic."""
    for attempt in range(max_retries):
        try:
            # Locate the submit button
            submit_button = page.locator(selector)

            # Ensure button is visible & enabled
            page.wait_for_selector(selector, state="visible", timeout=5000)

            # Get bounding box (handling possible None)
            bounding_box = submit_button.bounding_box()
            if bounding_box:
                page.mouse.move(
                    bounding_box["x"] + bounding_box["width"] / 2,
                    bounding_box["y"] + bounding_box["height"] / 2
                )

            # Wait before clicking
            time.sleep(delay)

            # Click the button
            submit_button.click()
            print(f"✅ Attempt {attempt + 1}: Submit button clicked.")
            return True  # Exit loop if successful

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)  # Wait before retrying

    print("⛔ Failed to click the button after multiple attempts.")
    return False
