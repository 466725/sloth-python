/// <reference types="cypress" />

export class DsaHomePage {
  private readonly homePath = "/";
  private readonly analyzeButtonSelector = 'button:contains("Analyze")';

  visit() {
    cy.visit(this.homePath);
  }

  getAnalyzeButton() {
    return cy.get(this.analyzeButtonSelector);
  }
}
