package Steps;

import Base.BaseUtil;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class SearchStep extends BaseUtil {

    private BaseUtil base;

    public SearchStep(BaseUtil base) {
        this.base = base;
    }

    @io.cucumber.java.en.Given("^I want food in \"([^\"]*)\"$")
    public void iWantFoodIn(String postalcode) throws Throwable {

        System.out.println("Navigate to Page");


    }

    @io.cucumber.java.en.When("^I search for restaurants$")
    public void iSearchForRestaurants() {
        System.out.println("I search for restaurants");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//input[@name='postcode']")));
        driver.findElement(By.xpath("//input[@name='postcode']")).sendKeys("AR51 1AA");
        driver.findElement(By.xpath("//button[@type='submit']")).click();
    }

    @io.cucumber.java.en.Then("^I should see some restaurants in \"([^\"]*)\"$")
    public void iShouldSeeSomeRestaurantsIn(String postalcode) throws Throwable {
        // Write code here that turns the phrase above into concrete actions
        System.out.println("I should see some restaurants in " + postalcode);


    }
}
