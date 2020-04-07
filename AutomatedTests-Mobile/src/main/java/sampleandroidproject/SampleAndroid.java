package sampleandroidproject;

import java.net.MalformedURLException;
import java.net.URL;

import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Test;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.ios.IOSDriver;

public class SampleAndroid {
    protected AppiumDriver driver = null;
    AndroidDriver androidDriver = (AndroidDriver) driver;
    IOSDriver iosDriver = (IOSDriver) driver;

    
    
    
	@BeforeSuite
	public void setupAppium() throws MalformedURLException {
		DesiredCapabilities caps = new DesiredCapabilities();
		caps.setCapability("testobject_api_key", "73641AF4E4F34C13A31972953A7E27F0");
		caps.setCapability("testobject_app_id", "1");
		caps.setCapability("platformName", "Android");
		caps.setCapability("platformVersion", "10");
		URL US_endpoint = new URL("http://us1.appium.testobject.com/wd/hub");
		//driver = new AppiumDriver(US_endpoint, caps);
	    // or assign correct (iOS/Android) driver with driver start
	    driver = new AndroidDriver(US_endpoint, caps);
	}

	@AfterSuite
	public void uninstallApp() throws InterruptedException {
		// driver.executeScript("sauce:job-result=passed");
		driver.quit();
	}

	@Test(enabled = true)
	public void myFirstTest() throws InterruptedException {
		driver.findElementByXPath("(//android.view.ViewGroup[@content-desc='NO THANKS'])[2]").click();
		driver.findElementByXPath("//android.view.ViewGroup[@content-desc='Account']").click();
		driver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
		driver.findElementByXPath("(//android.widget.EditText)[1]").sendKeys("cpxapitester@gmail.com");
		driver.findElementByXPath("(//android.widget.EditText)[2]").sendKeys("Cineplex123");
		driver.findElementByXPath("//android.view.ViewGroup[@content-desc='LOGIN']").click();
	}
}
