from playwright.sync_api import sync_playwright

def automate_browser(actions):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for action in actions:
            if action['type'] == 'goto':
                page.goto(action['url'])
                results.append(f"Went to {action['url']}")
            elif action['type'] == 'click':
                page.click(action['selector'])
                results.append(f"Clicked {action['selector']}")
            elif action['type'] == 'type':
                page.fill(action['selector'], action['text'])
                results.append(f"Typed in {action['selector']}")
            # Extend with more actions as needed
        browser.close()
    return results