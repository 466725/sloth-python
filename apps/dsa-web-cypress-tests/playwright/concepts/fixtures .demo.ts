import { expect, test as base } from '@playwright/test';

type DemoFixtures = {
  message: string;
  decoratedMessage: string;
};

const test = base.extend<DemoFixtures>({
  message: async ({}, use) => {
    // Setup
    const value = 'Hello from fixture';

    // Provide fixture value to the test
    await use(value);

    // Teardown (nothing needed for this simple demo)
  },
  decoratedMessage: async ({ message }, use) => {
    // This fixture is composed from another fixture.
    await use(`*** ${message} ***`);
  },
});

test('uses a custom fixture value', async ({ message }) => {
  expect(message).toBe('Hello from fixture');
});

test('uses a fixture that depends on another fixture', async ({ decoratedMessage }) => {
  expect(decoratedMessage).toBe('*** Hello from fixture ***');
});