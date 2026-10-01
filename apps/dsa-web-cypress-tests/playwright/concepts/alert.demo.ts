import { expect, test } from '@playwright/test';

test('handle alert popup demo', async ({ page }) => {
	await page.setContent(`
		<button id="open-alert">Open Alert</button>

		<script>
			document.getElementById('open-alert').addEventListener('click', () => {
				alert('This is a demo alert');
			});
		</script>
	`);

	let dialogMessage = '';
	page.once('dialog', async (dialog) => {
		dialogMessage = dialog.message();
		await dialog.accept();
	});

	await page.locator('#open-alert').click();
	await expect.poll(() => dialogMessage).toBe('This is a demo alert');
});
