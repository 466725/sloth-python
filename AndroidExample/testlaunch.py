import os
import unittest
from appium import webdriver
from time import sleep

class LaunchCineplexTests(unittest.TestCase):
    "Class to run tests against Cineplex app"
    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = 'android'
        desired_caps['deviceName'] = 'Nexus_5X'
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'apps/com.fivemobile.cineplex.uat-anycpu.apk'))
        desired_caps['appPackage'] = 'com.fivemobile.cineplex'
        desired_caps['appActivity'] = '.MainActivity'
        desired_caps['appWaitPackage'] = 'com.fivemobile.cineplex'
        desired_caps['appWaitActivity'] = '.MainActivity'
        desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['noReset'] = 'true'
        desired_caps['autoAcceptAlerts'] = 'true'
        desired_caps['gpsEnabled'] = 'true'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        "Tear down"
        self.driver.quit()

    def test_launch(self):
        "Test that the app launched"
        self.driver.find_element_by_id('btnAccounts').click()
        self.driver.find_element_by_id('btnLogin').click()
        sleep(50)

#---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LaunchCineplexTests)
    unittest.TextTestRunner(verbosity=2).run(suite)