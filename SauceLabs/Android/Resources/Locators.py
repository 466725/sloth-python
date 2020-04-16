# All the Locators
from selenium.webdriver.common.by import By

class Locators():
    # --- Location Services Splash Page ---
    NO_THANKS = (By.XPATH, "(//android.view.ViewGroup[@content-desc='NO THANKS'])")

    # --- Main Page ---
    ACCOUNT_ICON = (By.XPATH, "//android.view.ViewGroup[@content-desc='Account']")

    # --- Login Page ---
    LOGIN_BUTTON = (By.XPATH, "//android.view.ViewGroup[@content-desc='LOGIN']")
    LOGIN = (By.XPATH, "(//android.widget.EditText)[1]")
    PWD = (By.XPATH, "(//android.widget.EditText)[2]")