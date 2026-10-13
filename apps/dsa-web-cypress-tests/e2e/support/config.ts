export function getBaseUrl(): string {
  return Cypress.config("baseUrl") as string;
}
