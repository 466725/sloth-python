import { test, expect, Page } from "@playwright/test";

const baseUrl = process.env.BASE_URL || "https://www.tangerine.ca/en/personal";

async function acceptCookies(page: Page): Promise<void> {
  const acceptButton = page.locator("#onetrust-accept-btn-handler");
  if (await acceptButton.isVisible().catch(() => false)) {
    await acceptButton.click();
  }
}

test.describe("Tangerine Registration", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(baseUrl);
    await acceptCookies(page);
  });

  test("should verify the Sign Up page loads", async ({ page }) => {
    // Match the Cypress behavior: verify a visible Sign Up / Become a Client link exists.
    const signUpLink = page.locator("a:visible").filter({ hasText: /Sign Up|Become a Client/i }).first();
    await expect(signUpLink).toBeVisible();
  });
});
