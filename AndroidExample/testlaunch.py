import os
import unittest
from appium import webdriver
from time import sleep

from Resources.Locators import Locators
from Resources.TestData import TestData

class LaunchCineplexTests(unittest.TestCase):
    "Class to run tests against Cineplex app"
    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'emulator'
        desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'apps/com.fivemobile.cineplex.uat-anycpu.apk'))
        desired_caps['appPackage'] = 'com.fivemobile.cineplex.uat'
        desired_caps['appActivity'] = 'com.fivemobile.cineplex.MainActivity'
        desired_caps['noReset'] = 'true'
        desired_caps['gpsEnabled'] = 'true'
        desired_caps['newCommandTimeout'] = 120
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        "Tear down test and uninstall the application from the device"
        self.driver.remove_app('com.fivemobile.cineplex.uat')

    def test_launch_and_login_then_logout(self):
        "Test that the app launched and user can log in and then logout"
        self.driver.find_element_by_xpath("(//android.view.ViewGroup[@content-desc='NO THANKS'])").click()
        self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='Account']").click()
        self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='LOGIN']").click()
        self.driver.find_element_by_xpath("(//android.widget.EditText)[1]").send_keys(TestData.USERNAME)
        self.driver.find_element_by_xpath("(//android.widget.EditText)[2]").send_keys(TestData.PASSWORD)
        self.driver.find_element_by_xpath("//android.view.ViewGroup[@content-desc='LOGIN']").click()
        "User is logged in"
        sleep(30)

#---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LaunchCineplexTests)
    unittest.TextTestRunner(verbosity=2).run(suite)