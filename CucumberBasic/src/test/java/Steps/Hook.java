package Steps;

import Base.BaseUtil;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.concurrent.TimeUnit;

public class Hook extends BaseUtil {

    private BaseUtil base;

    public Hook(BaseUtil base) {
        this.base = base;
    }

    @Before
    public void InitializeTest() {
        System.out.println("Opening the browser : Firefox");
        System.setProperty("webdriver.chrome.driver", "C:\\WebDrivers\\geckodriver.exe");
        base.driver = new FirefoxDriver();
        base.driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        base.driver.get("https://www.just-eat.co.uk/");
    }

    @After
    public void TearDownTest(Scenario scenario) {

        if (scenario.isFailed()) {
            //Take Screenshot
            System.out.println(scenario.getName());
        }

        System.out.println("Closing the browser : Firefox");
        base.driver.quit();
    }

}
