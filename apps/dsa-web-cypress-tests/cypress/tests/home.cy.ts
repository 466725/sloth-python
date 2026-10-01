/// <reference types="cypress" />

import { DsaHomePage } from "../support/pages/DsaHomePage";

describe("DSA Home Page", () => {
  const home = new DsaHomePage();

  beforeEach(() => {
    home.visit();
  });

  it("should display the Analyze button in the top right corner", () => {
    home.getAnalyzeButton().should("be.visible");
  });
});
