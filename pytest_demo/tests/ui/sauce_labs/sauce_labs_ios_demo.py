import unittest
from time import sleep

from appium import webdriver


# Polish this one again, according to the Android one
class AndroidApplicationTests(unittest.TestCase):
    def setUp(self):
        # 00000000000000000000000000000000 -> Ticketing PROD
        # 00000000000000000000000000000000 -> Ticketing UAT
        # 00000000000000000000000000000000 -> Store PROD
        # 00000000000000000000000000000000 -> Store UAT
        desired_caps = {
            "testobject_api_key": "00000000000000000000000000000000",
            "platformName": "IOS",
            "platformVersion": "9",
            "deviceName": "iPhone 7",
            "phoneOnly": "true",
            # , 'tabletOnly': 'false'
            # , 'privateDevicesOnly': 'false'
            # Optional Capabilities:
            # , 'appiumVersion': '1.17.0'
            # , 'noReset': 'false'
            # , 'cacheId': '1719330c118'
            # , 'testobject_session_creation_timeout': '900000'
            # , 'testobject_app_id': '1'
            # , 'testobject_suite_name': 'Demo suite of Weipeng'
            # , 'testobject_test_name': 'Demo test of Weipeng'
            "name": "Automation with Sauce labs demo of IOS",
        }
        self.driver = webdriver.Remote("http://us1.appium.testobject.com/wd/hub", desired_caps)
        sleep(15)
        print(self.driver.desired_capabilities)

    def test_launch_and_login(self):
        print("Sleep here a while for now! ")
        sleep(15)

    def tearDown(self):
        self.driver.execute_script("sauce:job-result=passed")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
