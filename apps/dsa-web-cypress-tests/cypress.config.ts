import { defineConfig } from "cypress";
import path from "node:path";
import { allureCypress } from "allure-cypress/reporter";

const baseUrl = process.env.BASE_URL || "http://localhost:8000";
// Shared test-output root used across the repo (gitignored at the project root).
const reportsRoot = path.resolve(__dirname, "../../temps/cypress_dsa_web");

export default defineConfig({

  viewportWidth: 1280,
  viewportHeight: 720,
  defaultCommandTimeout: 10000,
  pageLoadTimeout: 120000,
  chromeWebSecurity: false,
  video: false,

  screenshotsFolder: path.join(reportsRoot, "screenshots"),
  videosFolder: path.join(reportsRoot, "videos"),
  downloadsFolder: path.join(reportsRoot, "downloads"),

  retries: {
    runMode: 2,
    openMode: 0
  },

  env: {
    environment: "prod"
  },

  e2e: {
    baseUrl,
    specPattern: "cypress/tests/**/*.cy.ts",

    setupNodeEvents(on, config) {
      allureCypress(on, config, {
        resultsDir: path.join(reportsRoot, "allure-results")
      });
      return config;
    }
  },

  reporter: "spec"

});