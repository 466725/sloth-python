import unittest
from appium import webdriver
from time import sleep


def test_launch_and_login():
    print('Sleep here a while for now! ')
    sleep(2)


class AndroidApplicationTests(unittest.TestCase):
    "Class to run tests against Cineplex app"

    def setUp(self):
        "Setup for the test"
        desired_caps = {'testobject_api_key': '9C862FE0E2624DD2BAC1B293A753A63B'
            , 'platformName': 'Android'
            , 'platformVersion': '9'
            , 'automationName': 'UiAutomator2'
            , 'name': 'Mobile Ticketing App Demo Test by Weipeng'}
        self.driver = webdriver.Remote('http://us1.appium.testobject.com/wd/hub', desired_caps)
        print(self.driver.desired_capabilities)

    def tearDown(self):
        self.driver.execute_script('sauce:job-result=passed')
        self.driver.quit()


# ---START OF SCRIPT
if __name__ == '__main__':
    unittest.main()
