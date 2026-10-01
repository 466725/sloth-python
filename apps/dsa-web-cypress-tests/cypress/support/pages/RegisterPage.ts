/// <reference types="cypress" />

export class RegisterPage {
  private readonly signUpPath = "/en/sign-up";
  private readonly confirmationHeaderPattern = /Become a Client|Sign Me Up/i;

  visit() {
    cy.visit(this.signUpPath);
  }

  getConfirmationHeader() {
    // Verifies we are on the "Become a Client" page
    return cy.contains(this.confirmationHeaderPattern);
  }
}