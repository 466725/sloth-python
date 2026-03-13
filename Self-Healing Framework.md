## Self-Healing UI Test Framework in Python

To make a Self-Healing UI Test Framework in Python, you basically combine Selenium + intelligent locator recovery + DOM similarity analysis. I’ll break it into practical implementation steps so you can actually build a working demo project (which is great for interviews and GitHub).

1. Project Structure

Start with a clean structure.

self_healing_ui/
│
├── tests/
│   └── test_login.py
│
├── framework/
│   ├── driver_manager.py
│   ├── element_finder.py
│   ├── locator_store.py
│   ├── dom_similarity.py
│   └── self_healing.py
│
├── locators/
│   └── locators.json
│
├── requirements.txt
└── README.md

Dependencies:

selenium
beautifulsoup4
lxml
scikit-learn
pytest

2. Step 1 — Build a Basic Selenium Framework

First create a simple Selenium wrapper.

driver_manager.py
from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver

3. Step 2 — Store Locators in a Central Repository

Store all locators so the framework can update them automatically.

locators.json
{
  "login_button": {
    "primary": {"by": "id", "value": "loginBtn"},
    "fallbacks": [
      {"by": "xpath", "value": "//button[text()='Login']"},
      {"by": "css", "value": "button.login"}
    ]
  }
}
locator_store.py
import json

def load_locators():
    with open("locators/locators.json") as f:
        return json.load(f)

4. Step 3 — Implement Locator Fallback Strategy

If the primary locator fails, try alternatives.

element_finder.py
from selenium.webdriver.common.by import By

def find_element_with_fallback(driver, locator):

    strategies = [locator["primary"]] + locator.get("fallbacks", [])

    for strategy in strategies:
        try:
            by = getattr(By, strategy["by"].upper())
            return driver.find_element(by, strategy["value"])
        except:
            continue

    raise Exception("Element not found using any locator strategy")

This alone already improves test resilience.

5. Step 4 — Capture DOM Metadata for Self-Healing

When an element is found, save metadata:

tag

class

text

attributes

location in DOM

Example metadata
{
 "tag": "button",
 "text": "Login",
 "class": "btn primary",
 "xpath": "/html/body/div/button"
}

This will later help identify a similar element if locator changes.

6. Step 5 — DOM Similarity Heuristic

When locators fail, scan the DOM and find the most similar element.

Use BeautifulSoup.

dom_similarity.py
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_similar_element(page_source, expected_text):

    soup = BeautifulSoup(page_source, "lxml")
    candidates = soup.find_all(True)

    best = None
    best_score = 0

    for c in candidates:
        text = c.get_text(strip=True)

        score = similarity(text, expected_text)

        if score > best_score:
            best = c
            best_score = score

    return best

This identifies elements even if ID or XPath changed.

7. Step 6 — Self-Healing Logic

Now combine everything.

self_healing.py
from element_finder import find_element_with_fallback
from dom_similarity import find_similar_element

def find_element(driver, locator):

    try:
        return find_element_with_fallback(driver, locator)

    except:

        page = driver.page_source
        expected_text = locator["primary"]["value"]

        candidate = find_similar_element(page, expected_text)

        if candidate:
            print("Self-healing activated")

            new_xpath = generate_xpath(candidate)

            return driver.find_element("xpath", new_xpath)

        raise

8. Step 7 — Update Locator Automatically (Optional but impressive)

When healing succeeds:

Generate a new XPath

Save it to locators.json

Example:

Old locator: id=loginBtn
New locator: //button[@data-testid='login']

This makes the framework learn over time.

9. Step 8 — Write a Test Using the Framework

test_login.py
from framework.driver_manager import get_driver
from framework.self_healing import find_element
from framework.locator_store import load_locators

def test_login():

    driver = get_driver()
    driver.get("https://example.com")

    locators = load_locators()

    login_btn = find_element(driver, locators["login_button"])

    login_btn.click()

    driver.quit()

10. Step 9 — Add Logging for Demonstration

Very useful for interviews.

Example log:

[INFO] Trying primary locator: id=loginBtn
[WARNING] Primary locator failed
[INFO] Trying fallback locator: xpath=//button[text()='Login']
[WARNING] Fallback failed
[INFO] Running DOM similarity scan
[SUCCESS] Self-healed element located
11. Step 10 — Optional AI Improvement (Very Impressive)

Use ML similarity instead of string matching.

Example:

scikit-learn
sentence-transformers

Compare:

text

attributes

DOM path

to rank elements.

Final Result (What you can claim on resume)

The project demonstrates:

✔ Intelligent locator fallback strategies
✔ DOM similarity heuristics
✔ Automatic locator healing
✔ Reduced test maintenance
✔ Experimental AI-driven automation framework