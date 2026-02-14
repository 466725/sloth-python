import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLURE_IMG_DIR = os.path.join(BASE_DIR, "temps\\allure-report\\images")
SELENIUM_IMPLICITLY_WAIT = 10
SELENIUM_EXPLICITLY_WAIT = 10
SLEEP_TIME = 1
AMAZON_URL = "https://www.amazon.com"
TANGERINE_URL = "https://www.tangerine.ca/en/personal"
DEEP_SEEK_URL = "https://api.deepseek.com"
OPENAI_URL = "https://api.openai.com"
CINEPLEX_URL = "https://connect.cineplex.com"

if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"ALLURE_IMG_DIR: {ALLURE_IMG_DIR}")
    print(f"SELENIUM_IMPLICITLY_WAIT: {SELENIUM_IMPLICITLY_WAIT}")
    print(f"SELENIUM_EXPLICITLY_WAIT: {SELENIUM_EXPLICITLY_WAIT}")
    print(f"SLEEP_TIME: {SLEEP_TIME}")
    print(f"AMAZON_URL: {AMAZON_URL}")
    print(f"TANGERINE_URL: {TANGERINE_URL}")
    print(f"DEEP_SEEK_URL: {DEEP_SEEK_URL}")
    print(f"OPENAI_URL: {OPENAI_URL}")
    print(f"CINEPLEX_URL: {CINEPLEX_URL}")
