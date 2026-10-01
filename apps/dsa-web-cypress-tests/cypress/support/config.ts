export function getBaseUrl(): string {
  return Cypress.config("baseUrl") as string;
}

export const testCredentials = {
  user: {
    clientId: "12345678",
    pin: "123456",
  },
  invalidUser: {
    clientId: "87654321",
    pin: "654321",
  },
};
