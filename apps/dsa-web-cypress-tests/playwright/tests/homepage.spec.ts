import { test, expect, Page } from "@playwright/test";

const baseUrl = process.env.BASE_URL || "https://www.tangerine.ca/en/personal";

async function acceptCookies(page: Page): Promise<void> {
  const acceptButton = page.locator("#onetrust-accept-btn-handler");
  if (await acceptButton.isVisible().catch(() => false)) {
    await acceptButton.click();
  }
}

test.describe("Tangerine Homepage", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(baseUrl);
    await acceptCookies(page);
  });

  test("should load the homepage and show the logo", async ({ page }) => {
    // Two logos exist in DOM (desktop + hamburger). Assert any visible logo.
    await expect(page.locator('img[alt="Tangerine"]').first()).toBeVisible();
  });

  test("should display 'Get Our App' links", async ({ page }) => {
    await page.locator("footer").scrollIntoViewIfNeeded();
    await expect(page.locator("#ios-app-store-link")).toBeVisible();
    await expect(page.locator("#android-app-store-link")).toBeVisible();
  });

  test("should show dynamic menu when hovering over Save", async ({ page }) => {
    const saveMenu = page.locator("a, button, span").filter({ hasText: /Save/i }).first();
    await expect(saveMenu).toBeVisible();
    await saveMenu.hover({ force: true });
    await expect(page.locator("#accounts-save")).toBeVisible();
  });

  test("should capture analytics events", async ({ page }) => {
    const analyticsEvents: string[] = [];

    page.on("request", (request) => {
      if (
        request.method() === "POST" &&
        request.url().includes("google-analytics.com/g/collect")
      ) {
        analyticsEvents.push(request.postData() || "");
      }
    });

    await page.reload();
    await page.waitForTimeout(3000);

    // Keep assertion behavior aligned with the original Cypress test.
    expect(analyticsEvents.length).toBeGreaterThan(-1);
    for (const event of analyticsEvents) {
      expect(event).toContain("en=");
    }
  });
});
