"""
Selenium script to open Google in a maximized Chrome window and wait for 5 seconds before closing.
Created on 2017-04-01
@author: weipengzheng
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Optional: Chrome options
options = Options()
options.add_argument("--start-maximized")

# Create WebDriver (Selenium 4.6+ auto-manages driver)
driver = webdriver.Chrome(options=options)
driver.set_window_position(5, 5)
driver.set_window_size(900, 600)
time.sleep(1)

# Navigate to Google
driver.get("https://www.google.com/")
driver.get_screenshot_as_file("./selenium_demo.png")
driver.maximize_window()
time.sleep(1)
driver.minimize_window()
time.sleep(1)
driver.maximize_window()
time.sleep(1)

# Using name='q' is more reliable for Google's search input
inputEle = driver.find_element(By.NAME, "q")
inputEle.send_keys("Selenium")
inputEle.submit()
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
time.sleep(5)

# # Handle Alert example
# alert = driver.find_element(By.ID, "AlertBtn")
# driver.switch_to.alert.accept()
#
# # Handle Comfirm example
# confirm = driver.find_element(By.ID, "confirmBtn")
# driver.switch_to.confirm.accept()
# driver.switch_to.confirm.dismiss()
#
# # Handle iFrame example
# driver.switch_to.frame(driver.find_element(By.ID, "iframeResult"))
# print(driver.page_source)
# driver.switch_to.default_content()
#
# # Handle Window example
# driver.switch_to.window(driver.window_handles[1])
# print(driver.page_source)
#
# # Forward, Back, Refresh example
# driver.forward()
# driver.back()
# driver.refresh()
#
# # Element displayed example
# inputEle = driver.find_element(By.NAME, "q")
# if inputEle.is_displayed():
#     print("Element is displayed")

# Close browser
driver.quit()
