import '@shelex/cypress-allure-plugin';

// Prevent Cypress from failing tests due to application errors
Cypress.on("uncaught:exception", () => {
    return false;
});

afterEach(function () {
    if (this.currentTest?.state !== "passed") {
        return;
    }

    const safeTitle = this.currentTest.title.replace(/[^a-zA-Z0-9_-]+/g, " ").trim();
    cy.screenshot(`passed/${safeTitle}`);
});
