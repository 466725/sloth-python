import '@shelex/cypress-allure-plugin';

// Load custom Cypress commands
import "./commands";

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

// Custom command type definitions
declare global {
    namespace Cypress {
        interface Chainable {
            /**
             * Conditionally accepts the OneTrust cookie banner if it's visible.
             */
            acceptCookies(): Chainable<void>;

            /**
             * Login via the UI (used in tests that require authentication).
             */
            login(email: string, password: string): Chainable<void>;

        }
    }
}