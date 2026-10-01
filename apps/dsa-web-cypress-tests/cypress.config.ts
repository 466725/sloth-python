import { defineConfig } from "cypress";
import path from "node:path";
import allureWriter from "@shelex/cypress-allure-plugin/writer";

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
    environment: "prod",
    allure: true,
    // cypress-allure-plugin joins this with process.cwd() internally, so it must stay relative.
    allureResultsPath: path.relative(__dirname, path.join(reportsRoot, "allure-results"))
  },

  e2e: {
    baseUrl,
    specPattern: "cypress/tests/**/*.cy.ts",

    setupNodeEvents(on, config) {
      allureWriter(on, config);
      return config;
    }
  },

  reporter: "spec"

});