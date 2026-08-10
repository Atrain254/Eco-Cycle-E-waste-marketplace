from playwright.sync_api import sync_playwright

def test_marketplace_search():
    with sync_playwright() as p:
        # 1. Launch the browser. 
        # headless=False means we can actually watch it happen on our screen!
        # slow_mo=500 adds a half-second delay so it doesn't move too fast for us to see.
        print("Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # 2. Go to the marketplace homepage
        print("Navigating to Eco-Cycle...")
        page.goto("http://127.0.0.1:8000/marketplace/")

        # 3. Verify the page loaded by checking the title
        actual_title = page.title()
        print(f"DEBUG: The actual page title found was '{actual_title}'")
        assert "Eco-Cycle" in actual_title, f"Test failed! Expected 'Eco-Cycle' but got '{actual_title}'"
        print("Page loaded successfully!")

        # 4. Find the search bar and type something into it
        # (We are targeting the input field with the name="q")
        test_search_term = "e-waste" 
        print(f"Typing '{test_search_term}' into the search bar...")
        page.fill('input[name="q"]', test_search_term)

        # 5. Click the search button
        print("Clicking the Search button...")
        page.click('button:has-text("Search")')

        # 6. Wait a moment to view the filtered results
        print("Search complete! Viewing results...")
        page.wait_for_timeout(3000) # Waits 3 seconds before closing

        # 7. Close the browser
        print("Test passed! Closing browser.")
        browser.close()

if __name__ == '__main__':
    test_marketplace_search()