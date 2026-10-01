/**
 * A custom command to conditionally find and click the OneTrust cookie banner.
 * This prevents tests from failing if the banner doesn't appear.
 */
Cypress.Commands.add("acceptCookies", () => {
  cy.get("body").then(($body) => {
    if ($body.find('#onetrust-accept-btn-handler').length > 0) {
      cy.get('#onetrust-accept-btn-handler').click();
    }
  });
});

Cypress.Commands.add("login", (email: string, password: string) => {
  cy.get("#email").type(email);
  cy.get("#password").type(password);
  cy.contains("Log In").click();
});