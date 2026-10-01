import { expect, test } from '@playwright/test';

test('playwright built-in assertions demo', async ({ page }) => {
	await page.goto('https://example.com');

	// URL assertion
	await expect(page).toHaveURL('https://example.com/');

	// Visibility and text assertions
	const heading = page.locator('h1');
	await expect(heading).toBeVisible();
	await expect(heading).toHaveText('Example Domain');

	// Use a local mini form to show input and checkbox assertions
	await page.setContent(`
		<input id="username" value="john" />
		<input id="terms" type="checkbox" checked />
	`);

	await expect(page.locator('#username')).toHaveValue('john');
	await expect(page.locator('#terms')).toBeChecked();
});
