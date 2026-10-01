/// <reference types="cypress" />

export class LoginPage {
  private readonly clientIdInputSelector = 'input[id="login-user-id-input"]';

  login(clientId: string, pin: string) {
    return cy.get(this.clientIdInputSelector).should("be.visible");
  }
}