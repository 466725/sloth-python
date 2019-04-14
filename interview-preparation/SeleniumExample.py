'''
Created on 2017-04-01
@author: weipengzheng
'''

from selenium import webdriver
driver = webdriver.Chrome('/Users/weipengzheng/Documents/workspace/ems-automation-master/src/test/resources/ChromeDrivers/osx/chromedriver-64')
driver.get('https://www.google.ca/')
text_area = driver.find_elements_by_xpath("//*[@id=\"lst-ib\"]")
text_area.send_keys("Selenium Python Example")
python_link = driver.find_elements_by_xpath("//*[@id=\"tsf\"]/div[2]/div[3]/center/input[1]")[0]
python_link.click()
assert "Selenium Python" in driver.get_page_source()
driver.quit()
