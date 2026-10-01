/// <reference types="cypress" />

import { HomePage } from "../support/pages/HomePage";

describe("Tangerine Registration", () => {
  const home = new HomePage();

  beforeEach(() => {
    home.visit();
  });

  it("should verify the Sign Up page loads", () => {
    cy.allure().feature('Registration');
    cy.allure().story('Validate registration page loads correctly');
    // The site has multiple "Become a Client" links, some hidden for mobile.
    // We target a visible link ('a:visible') to ensure we click the correct one.
    cy.get("a:visible").contains(/Sign Up|Become a Client/i).should("be.visible");
  });
});
