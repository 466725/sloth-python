/// <reference types="cypress" />

export class HomePage {
  private readonly homePath = "/";
  private readonly logoSelector = 'img[alt="Tangerine"]';
  private readonly loginTextPattern = /Log In|Log Me In/i;
  private readonly megaMenuMarker = 'Accounts';
  private readonly iosAppDownload = '#ios-app-store-link';
  private readonly androidAppDownload = '#android-app-store-link';
  private readonly pageBottomSelector = 'bottom';

  visit() {
    cy.visit(this.homePath); // Navigate to the base URL
    cy.acceptCookies(); // Handle the cookie banner using our custom command
  }

  getLogo() {
    // Checks for the Tangerine logo image
    return cy.get(this.logoSelector);
  }

  verifyAppDownloadLinks() {
    // Checks for the app download links for iOS and Android at the bottom of the page
    cy.scrollTo(this.pageBottomSelector);
    return cy.get(this.iosAppDownload).should('be.visible') && cy.get(this.androidAppDownload).should('be.visible');
  }

  hoverSaveMenu() {
    cy.contains('a, button, span', 'Save', { matchCase: false })
      .should('be.visible')
      .trigger('mouseenter', { force: true })
      .trigger('mouseover', { force: true });
  }

  verifyMegaMenuIsVisible() {
    cy.contains(this.megaMenuMarker).should('be.visible');
  }

  clickLogin() {
    // Updated to match "Log In" (current) or "Log Me In" (legacy)
    cy.contains(this.loginTextPattern).click();
  }
}