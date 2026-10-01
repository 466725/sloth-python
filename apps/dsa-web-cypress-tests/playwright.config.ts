import { defineConfig } from "@playwright/test";

const baseURL = process.env.BASE_URL || "https://www.tangerine.ca/en/personal";

export default defineConfig({
  testDir: "./playwright/tests",
  testMatch: "**/*.spec.ts",
  fullyParallel: true,
  outputDir: "playwright/screenshots",
  reporter: [
    ["list"],
    ["allure-playwright", { resultsDir: "playwright/allure-results" }]
  ],
  use: {
    baseURL,
    screenshot: "only-on-failure",
    trace: "on-first-retry"
  }
});
