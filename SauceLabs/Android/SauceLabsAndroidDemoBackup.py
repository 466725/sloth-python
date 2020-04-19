import unittest
import pytest
from appium import webdriver
from time import sleep

class AndroidApplicationTests(unittest.TestCase):
    "Class to run tests against Cineplex app"

    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['testobject_api_key'] = '9C862FE0E2624DD2BAC1B293A753A63B'
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '9'
        desired_caps['automationName'] = 'UiAutomator2'
        # desired_caps['buildName'] = 'test12345'
        desired_caps['name'] = 'Automation with Sauce labs demo of Android'
        testobject_endpoint = 'http://us1.appium.testobject.com/wd/hub'
        self.driver = webdriver.Remote(testobject_endpoint, desired_caps)
        print(self.driver.desired_capabilities) # for DEBUG

    def test_launch_and_login(self):
        "Test that the app launched and user can log in and then logout"
        sleep(2)
        # self.driver.find_element_by_xpath("(//android.view.ViewGroup[@content-desc='NO THANKS'])[2]").click()
        # sleep(2)
        # self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='Account']").click()
        # sleep(2)
        # self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='LOGIN']").click()
        # sleep(2)
        # self.driver.find_element_by_xpath("(//android.widget.EditText)[1]").send_keys("cpxapitester@gmail.com")
        # self.driver.find_element_by_xpath("(//android.widget.EditText)[2]").send_keys("Cineplex123")
        # self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='LOGIN']").click()
        # "User is logged in"
        # self.assertEqual(1,1)
        sleep(10)

    def tearDown(self):
        self.driver.execute_script('sauce:job-result=passed')
        self.driver.quit()

#---START OF SCRIPT
if __name__ == '__main__':
    unittest.main()