import java.net.MalformedURLException;
import java.net.URL;

import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Test;

import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.ios.IOSDriver;

public class SauceLabsDemo {
	AndroidDriver<?> androidDriver;
	IOSDriver<?> iosDriver;

	@BeforeSuite
	public void beforeSuite() throws MalformedURLException {
		DesiredCapabilities androidCaps = new DesiredCapabilities();
		androidCaps.setCapability("testobject_api_key", "7B0F153A1C564E13934E7C5908228326");
		androidCaps.setCapability("testobject_app_id", "1");
		androidCaps.setCapability("platformName", "Android");
		androidCaps.setCapability("platformVersion", "10");
		DesiredCapabilities iosCaps = new DesiredCapabilities();
		iosCaps.setCapability("testobject_api_key", "7B0F153A1C564E13934E7C5908228326");
		iosCaps.setCapability("testobject_app_id", "1");
		iosCaps.setCapability("platformName", "iOS");
		iosCaps.setCapability("platformVersion", "11.0");
		URL US_endpoint = new URL("http://us1.appium.testobject.com/wd/hub");
		androidDriver = new AndroidDriver<WebElement>(US_endpoint, androidCaps);
		iosDriver = new IOSDriver<WebElement>(US_endpoint, iosCaps);
	}

	@AfterSuite
	public void afterSuite() throws InterruptedException {
		androidDriver.quit();
		iosDriver.quit();
	}

	@Test(enabled = true)
	public void androidLogin() throws InterruptedException {
		androidDriver.findElementByXPath("(//android.view.ViewGroup[@content-desc='NO THANKS'])[2]").click();
		androidDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='Account']").click();
		androidDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
		androidDriver.findElementByXPath("(//android.widget.EditText)[1]").sendKeys("cpxapitester@gmail.com");
		androidDriver.findElementByXPath("(//android.widget.EditText)[2]").sendKeys("Cineplex123");
		androidDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
	}
	
	@Test(enabled = true)
	public void iosLogin() throws InterruptedException {
		iosDriver.findElementByXPath("(//android.view.ViewGroup[@content-desc='NO THANKS'])[2]").click();
		iosDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='Account']").click();
		iosDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
		iosDriver.findElementByXPath("(//android.widget.EditText)[1]").sendKeys("cpxapitester@gmail.com");
		iosDriver.findElementByXPath("(//android.widget.EditText)[2]").sendKeys("Cineplex123");
		iosDriver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
	}
}
