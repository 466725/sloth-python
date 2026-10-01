import { defineConfig } from "cypress";
import allureWriter from "@shelex/cypress-allure-plugin/writer";

const baseUrl = process.env.BASE_URL || "https://www.tangerine.ca/en/personal";

export default defineConfig({

  viewportWidth: 1280,
  viewportHeight: 720,
  defaultCommandTimeout: 10000,
  pageLoadTimeout: 120000,
  chromeWebSecurity: false,
  video: false,

  retries: {
    runMode: 2,
    openMode: 0
  },

  env: {
    environment: "prod",
    allure: true,
    allureResultsPath: "cypress/allure-results"
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