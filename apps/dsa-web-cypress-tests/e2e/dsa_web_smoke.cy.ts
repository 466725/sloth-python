/// <reference types="cypress" />

import * as allure from "allure-js-commons";

// Backend-independent sanity check that Cypress is wired to the dsa-web app.
describe("DSA Web smoke", () => {
  it("loads the app shell and sets the expected page title", () => {
    allure.feature("Smoke");
    allure.story("Cypress is correctly configured against dsa-web");

    cy.visit("/");
    cy.title().should("eq", "dsa-web");
    cy.get("#root").should("not.be.empty");
    cy.get("nav").should("be.visible");
  });
});
