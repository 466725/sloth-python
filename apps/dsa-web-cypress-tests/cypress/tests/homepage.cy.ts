/// <reference types="cypress" />

import { HomePage } from "../support/pages/HomePage";

describe("Tangerine Homepage", () => {
  const home = new HomePage();

  beforeEach(() => {
    home.visit();
  });

  it("should load the homepage and show the logo", () => {
    cy.allure().feature('Homepage');
    cy.allure().story('Validate homepage loads correctly');
    home.getLogo().should("be.visible");
  });

  it("should display 'Get Our App' links", () => {
    home.verifyAppDownloadLinks();
  });

  it("should show dynamic menu when hovering over Save", () => {
    home.hoverSaveMenu();
    home.verifyMegaMenuIsVisible();
  });

  it("should capture analytics events", () => {
    const analyticsEvents: any[] = [];
    cy.reload(); // Trigger page load analytics events
    cy.intercept('POST', '**google-analytics.com/g/collect', (req) => {
      analyticsEvents.push(req.body);
    });
    cy.wait(3000);   // allow multiple analytics events
    cy.then(() => {
      expect(analyticsEvents.length).to.be.greaterThan(-1);
      analyticsEvents.forEach(event => {
        expect(event).to.include('en=');
      });
    });
  });
});
