import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BasePage:
    def __init__(self, driver):
        if driver is None:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--incognito")
            options.add_argument("--lang=en-US")
            driver = webdriver.Chrome(options=options)
        else:
            self.driver = driver

    def quit(self):
        self.driver.quit()

    # save a screenshot to an allure report
    @allure.step("Save screenshot")
    def save_allure_screenshot(self, test_name):
        with open(self.driver.save_screenshot(f"{test_name}.png"), "rb") as image_file:
            allure.attach(image_file.read(), name=test_name, attachment_type=allure.attachment_type.PNG)

    def __repr__(self):
        return f"BasePage(driver={self.driver})"
