import "allure-cypress";

beforeEach(() => {
    cy.intercept("GET", "/api/v1/history?*", {
        total: 0, page: 1, limit: 20, items: [],
    });
    cy.intercept("GET", "/api/v1/history/stocks?*", {total: 0, items: []});
    cy.intercept("GET", "/api/v1/analysis/tasks?*", {
        total: 0, pending: 0, processing: 0, tasks: [],
    });
    cy.intercept("GET", "/api/v1/analysis/tasks/stream", {
        statusCode: 200,
        headers: {"content-type": "text/event-stream"},
        body: "event: connected\ndata: {}\n\n",
    });
    cy.intercept("GET", "/api/v1/agent/skills", {skills: []});
    cy.intercept("GET", "/api/v1/stocks/watchlist", {stock_codes: []});
    cy.intercept("GET", "/api/v1/system/config/setup/status", {
        is_complete: true,
        ready_for_smoke: true,
        required_missing_keys: [],
        next_step_key: null,
        checks: [],
    });
});
