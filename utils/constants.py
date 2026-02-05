import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLURE_IMG_DIR = os.path.join(BASE_DIR, "temps\\allure-report\\images")
SELENIUM_IMPLICITLY_WAIT = 10
SELENIUM_EXPLICITLY_WAIT = 10
AMAZON_URL = "https://www.amazon.com"

if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"ALLURE_IMG_DIR: {ALLURE_IMG_DIR}")
