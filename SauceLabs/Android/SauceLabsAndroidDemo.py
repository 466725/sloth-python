import unittest
from appium import webdriver
from time import sleep


class AndroidApplicationTests(unittest.TestCase):

    def setUp(self):
        # 9BF029C703084859B7A85F653A502A87 -> Ticketing PROD
        # 9C862FE0E2624DD2BAC1B293A753A63B -> Ticketing UAT
        # EB0105D50CF04B7E9E6F7A514B4A1F60 -> Store PROD
        # A37A095D95FD4A38B6FFA7258BC63BB3 -> Store UAT
        desired_caps = {'testobject_api_key': 'EB0105D50CF04B7E9E6F7A514B4A1F60'
            , 'platformName': 'Android'
            , 'platformVersion': '9'
            , 'deviceName': 'Huawei P30'
            , 'phoneOnly': 'true'
                        # , 'tabletOnly': 'false'
                        # , 'privateDevicesOnly': 'false'
                        # Optional Capabilities:
                        # , 'appiumVersion': '1.17.0'
                        # , 'noReset': 'false'
                        # , 'cacheId': '1719330c118'
                        # , 'testobject_session_creation_timeout': '900000'
             , 'testobject_app_id': '1'
             , 'testobject_suite_name': 'Demo suite'
                        # , 'testobject_test_name': 'Demo test'
            , 'name': 'Sauce labs demo with Android'}
        self.driver = webdriver.Remote('http://us1.appium.testobject.com/wd/hub', desired_caps)
        sleep(15)
        print(self.driver.desired_capabilities)

    def test_launch_and_login(self):
        print('Sleep here a while for now! ')
        sleep(15)

    def tearDown(self):
        self.driver.execute_script('sauce:job-result=passed')
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
