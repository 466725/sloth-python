/// <reference types="cypress" />

// Backend-independent sanity check that Cypress is wired to the dsa-web app
// (frontend dev server reachable, app shell renders) regardless of auth/API state.
describe("DSA Web smoke", () => {
  it("loads the app shell and sets the expected page title", () => {
    cy.allure().feature("Smoke");
    cy.allure().story("Cypress is correctly configured against dsa-web");

    cy.visit("/");
    cy.title().should("eq", "dsa-web");
    cy.get("#root").should("exist");
  });
});
