'''
Created on 2017-04-01
@author: weipengzheng
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Optional: Chrome options
options = Options()
options.add_argument("--start-maximized")

# Create WebDriver (Selenium 4.6+ auto-manages driver)
driver = webdriver.Chrome(options=options)

# Navigate to Google
driver.get("https://www.google.com/")

# Keep browser open for a few seconds
import time

time.sleep(5)

# Close browser
driver.quit()
