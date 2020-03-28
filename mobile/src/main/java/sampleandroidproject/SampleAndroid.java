package sampleandroidproject;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;
import io.appium.java_client.MobileElement;
import io.appium.java_client.TouchAction;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.remote.MobileCapabilityType;

public class SampleAndroid {
	public static URL url;
	public static DesiredCapabilities caps;
	public static AndroidDriver<MobileElement> driver;

	@BeforeSuite
	public void setupAppium() throws MalformedURLException {

		final String URL_STRING = "http://localhost:4723/wd/hub";
		url = new URL(URL_STRING);

		caps = new DesiredCapabilities();
		caps.setCapability("deviceName", "Nexus_5X");
		caps.setCapability("udid", "emulator-5554");
		caps.setCapability("app", "C:\\Users\\gleung\\Downloads\\com.fivemobile.cineplex.uat-anycpu.apk");
		caps.setCapability("noReset", false);
		caps.setCapability("skipUnlock", true);
		caps.setCapability("automationName", "UiAutomator2");
		caps.setCapability("appPackage", "com.fivemobile.cineplex");
		caps.setCapability("appActivity", "com.fivemobile.cineplex.MainActivity");

		driver = new AndroidDriver<MobileElement>(url, caps);
		driver.manage().timeouts().implicitlyWait(2, TimeUnit.SECONDS);
		driver.resetApp();
	}

	@AfterSuite
	public void uninstallApp() throws InterruptedException {
		driver.removeApp("com.fivemobile.cineplex");
	}

	@Test(enabled = true)
	public void myFirstTest() throws InterruptedException {
		driver.resetApp();
	}
}
