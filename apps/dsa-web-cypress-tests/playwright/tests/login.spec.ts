import { test, expect, Page } from "@playwright/test";

const baseUrl = process.env.BASE_URL || "https://www.tangerine.ca/en/personal";

async function acceptCookies(page: Page): Promise<void> {
  const acceptButton = page.locator("#onetrust-accept-btn-handler");
  if (await acceptButton.isVisible().catch(() => false)) {
    await acceptButton.click();
  }
}

test.describe("Tangerine Login Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(baseUrl);
    await acceptCookies(page);
    await page.getByText(/Log In|Log Me In/i).first().click();
  });

  test("Logging in input should be displayed", async ({ page }) => {
    await expect(page.locator('input[id="login-user-id-input"]')).toBeVisible();
  });
});
