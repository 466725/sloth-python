/// <reference types="cypress" />

export class DsaHomePage {
    private readonly homePath = "/";

    visit() {
        cy.visit(this.homePath, {
            onBeforeLoad(window) {
                window.localStorage.setItem("dsa.uiLanguage", "en");
            },
        });
    }

    getAnalyzeButton() {
        return cy.contains("button", /^Analyze$/);
    }
}
