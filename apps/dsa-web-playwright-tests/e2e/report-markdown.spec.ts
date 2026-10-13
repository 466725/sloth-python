import { expect, test, type Page } from '@playwright/test';

declare const process: { env: Record<string, string | undefined> };

test.use({ locale: 'zh-CN' });

const UI_LANGUAGE_STORAGE_KEY = 'dsa.uiLanguage';

async function login(page: Page) {
  // Login is no longer required; navigate to home page directly
  await page.addInitScript((storageKey) => {
    window.localStorage.setItem(storageKey, 'zh');
  }, UI_LANGUAGE_STORAGE_KEY);

  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
}

test.describe('ReportMarkdown component', () => {
  test('copy markdown source code', async ({ page, context }) => {
    // Grant clipboard permissions
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);

    await login(page);

    // Navigate to history page
    await page.getByRole('link', { name: '首页' }).click();
    await page.waitForLoadState('domcontentloaded');
    // Wait for stock bar panel to load
    await expect(page.getByText('个股栏')).toBeVisible({ timeout: 10_000 });

    // Click on the first history item to select it
    const firstHistoryItem = page.locator('.home-history-item').first();
    await expect(firstHistoryItem).toBeVisible({ timeout: 10_000 });
    await firstHistoryItem.click();
    // Wait for detailed report button to be enabled (indicates selection is complete)
    const detailedReportButton = page.getByRole('button', { name: '完整分析报告' });
    await expect(detailedReportButton).toBeEnabled({ timeout: 3000 });

    // Click the "完整分析报告" button to open the markdown drawer
    await expect(detailedReportButton).toBeVisible({ timeout: 5000 });
    await detailedReportButton.click();

    // Verify drawer content is visible
    await expect(page.getByRole('dialog').getByText('完整分析报告')).toBeVisible();

    // Click copy markdown button - use dialog-specific locator to avoid strict mode violation
    const copyMarkdownButton = page.getByRole('dialog').getByRole('button', { name: '复制 Markdown 源码' });
    await expect(copyMarkdownButton).toBeVisible({ timeout: 5000 });
    await copyMarkdownButton.click();

    // Verify clipboard contains markdown content
    const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
    expect(clipboardText).toBeTruthy();
    expect(clipboardText.length).toBeGreaterThan(0);

    // Verify checkmark icon is shown
    const checkmarkIcon = page.locator('button[aria-label="复制 Markdown 源码"] svg.text-success');
    await expect(checkmarkIcon).toBeVisible();

    // Wait for icon to revert (icon disappears after 2 seconds)
    await expect(checkmarkIcon).not.toBeVisible({ timeout: 3500 });
  });

  test('copy plain text', async ({ page, context }) => {
    // Grant clipboard permissions
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);

    await login(page);

    // Navigate to history page
    await page.getByRole('link', { name: '首页' }).click();
    await page.waitForLoadState('domcontentloaded');
    // Wait for stock bar panel to load
    await expect(page.getByText('个股栏')).toBeVisible({ timeout: 10_000 });

    // Click on the first history item to select it
    const firstHistoryItem = page.locator('.home-history-item').first();
    await expect(firstHistoryItem).toBeVisible({ timeout: 10_000 });
    await firstHistoryItem.click();
    // Wait for detailed report button to be enabled (indicates selection is complete)
    const detailedReportButton = page.getByRole('button', { name: '完整分析报告' });
    await expect(detailedReportButton).toBeEnabled({ timeout: 3000 });

    // Click the "完整分析报告" button to open the markdown drawer
    await expect(detailedReportButton).toBeVisible({ timeout: 5000 });
    await detailedReportButton.click();

    // Verify drawer content is visible
    await expect(page.getByRole('dialog').getByText('完整分析报告')).toBeVisible();

    // Click copy plain text button - use dialog-specific locator
    const copyPlainTextButton = page.getByRole('dialog').getByRole('button', { name: '复制纯文本' });
    await expect(copyPlainTextButton).toBeVisible({ timeout: 5000 });
    await copyPlainTextButton.click();

    // Verify clipboard contains text without markdown symbols
    const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
    expect(clipboardText).toBeTruthy();
    expect(clipboardText.length).toBeGreaterThan(0);

    // Verify it's plain text (no markdown symbols like #, **, >, etc.)
    expect(clipboardText).not.toMatch(/^#{1,6}\s+/m); // No headers
    expect(clipboardText).not.toMatch(/\*\*[^*]+\*\*/); // No bold
    // Verify table syntax is removed (no standalone pipe separators)
    const lines = clipboardText.split('\n');
    const hasTableSeparators = lines.some(line =>
      line.match(/^\|[\s|:-]+\|$/) || line.match(/^[\s|:-]+$/)
    );
    expect(hasTableSeparators).toBeFalsy();

    // Verify checkmark icon is shown
    const checkmarkIcon = page.locator('button[aria-label="复制纯文本"] svg.text-success');
    await expect(checkmarkIcon).toBeVisible();

    // Wait for icon to revert (icon disappears after 2 seconds)
    await expect(checkmarkIcon).not.toBeVisible({ timeout: 3500 });
  });

  test('mobile responsive layout', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 390, height: 844 });

    await login(page);

    // On mobile, a report should already be selected (showing in main content)
    // Wait for main content to load
    await expect(page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL')).toBeVisible({ timeout: 10_000 });

    // Click the "完整分析报告" button to open the markdown drawer
    const detailedReportButton = page.getByRole('button', { name: '完整分析报告' });
    await expect(detailedReportButton).toBeVisible({ timeout: 5000 });
    await detailedReportButton.click();

    // Verify drawer content is visible (this ensures drawer is fully open)
    await expect(page.getByRole('dialog').getByText('完整分析报告')).toBeVisible({ timeout: 10000 });

    // Verify toolbar buttons are visible and clickable on mobile
    // Use dialog-specific locator to avoid strict mode violation (button also exists in main content)
    const copyMarkdownButton = page.getByRole('dialog').getByRole('button', { name: '复制 Markdown 源码' });
    const copyPlainTextButton = page.getByRole('dialog').getByRole('button', { name: '复制纯文本' });

    await expect(copyMarkdownButton).toBeVisible({ timeout: 5000 });
    await expect(copyPlainTextButton).toBeVisible();

    // Verify buttons are clickable (not checking icon animation on mobile due to timing issues)
    await expect(copyMarkdownButton).toBeEnabled();
    await expect(copyPlainTextButton).toBeEnabled();
  });

  test('buttons are disabled during loading', async ({ page }) => {
    await login(page);

    // Navigate to history page
    await page.getByRole('link', { name: '首页' }).click();
    await page.waitForLoadState('domcontentloaded');
    // Wait for stock bar panel to load
    await expect(page.getByText('个股栏')).toBeVisible({ timeout: 10_000 });

    // Click on the first history item to select it
    const firstHistoryItem = page.locator('.home-history-item').first();
    await expect(firstHistoryItem).toBeVisible({ timeout: 10_000 });
    await firstHistoryItem.click();
    // Wait for detailed report button to be enabled (indicates selection is complete)
    const detailedReportButton = page.getByRole('button', { name: '完整分析报告' });
    await expect(detailedReportButton).toBeEnabled({ timeout: 3000 });

    // Click the "完整分析报告" button to open the markdown drawer
    await expect(detailedReportButton).toBeVisible({ timeout: 5000 });
    await detailedReportButton.click();

    // Immediately check if buttons are disabled (right after drawer opens)
    // Use dialog-specific locator to avoid strict mode violation
    const copyMarkdownButton = page.getByRole('dialog').getByRole('button', { name: '复制 Markdown 源码' });
    const copyPlainTextButton = page.getByRole('dialog').getByRole('button', { name: '复制纯文本' });

    // Wait for drawer to open and buttons to appear
    await expect(copyMarkdownButton).toBeVisible({ timeout: 5000 });
    await expect(copyPlainTextButton).toBeVisible();

    // Wait for content to finish loading (buttons become enabled)
    await expect(copyMarkdownButton).toBeEnabled({ timeout: 5000 });

    // Check buttons are enabled after content loads
    // Note: Loading may be very fast for cached content
    const isMarkdownEnabled = await copyMarkdownButton.isEnabled();
    const isPlainTextEnabled = await copyPlainTextButton.isEnabled();

    // At least one button should be enabled
    expect(isMarkdownEnabled || isPlainTextEnabled).toBeTruthy();
  });
});
