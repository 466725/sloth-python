import allure


class ScreenshotHandler:
    def __init__(self, driver):
        if driver is None:
            raise ValueError("ScreenshotHandler requires a Selenium WebDriver instance.")
        self.driver = driver

    @allure.step("Attach screenshot")
    def attach_screenshot(self, name: str) -> None:
        """
        Attach a screenshot to the Allure report.
        Uses PNG bytes directly (no temp files, no path confusion).
        """
        png_bytes = self.driver.get_screenshot_as_png()
        allure.attach(
            png_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    def quit(self) -> None:
        self.driver.quit()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(driver={self.driver!r})"
