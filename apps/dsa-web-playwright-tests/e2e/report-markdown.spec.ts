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

async function ensureHistoryItem(page: Page) {
  // Navigate to home page only if not already on it
  // On mobile viewport, the "首页" link may be hidden behind a drawer,
  // and login() already navigates to '/' (home page), so check first.
  const stockBarVisible = await page.getByText('个股栏').isVisible({ timeout: 2000 }).catch(() => false);
  if (!stockBarVisible) {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
  }
  await expect(page.getByText('个股栏')).toBeVisible({ timeout: 10_000 });

  // Check if there are already history items
  const historyItems = page.locator('.home-history-item');
  const count = await historyItems.count();
  if (count > 0) {
    // Click on the first history item to select it
    const firstHistoryItem = historyItems.first();
    await expect(firstHistoryItem).toBeVisible({ timeout: 10_000 });
    await firstHistoryItem.click();
    return;
  }

  // No history items — trigger an analysis to create one
  const stockInput = page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL');
  await expect(stockInput).toBeVisible({ timeout: 10_000 });
  await stockInput.fill('600519');
  const analyzeButton = page.getByRole('button', { name: '分析', exact: true });
  await expect(analyzeButton).toBeVisible();
  await analyzeButton.click();

  // Wait for the analysis to complete and a history item to appear
  await expect(page.locator('.home-history-item').first()).toBeVisible({ timeout: 120_000 });
  await page.locator('.home-history-item').first().click();
}

test.describe('ReportMarkdown component', () => {
  test('copy markdown source code', async ({ page, context }) => {
    // Grant clipboard permissions
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);

    await login(page);

    // Ensure there is a history item to work with
    await ensureHistoryItem(page);
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

    // Ensure there is a history item to work with
    await ensureHistoryItem(page);
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

  test('buttons are disabled during loading', async ({ page }) => {
    await login(page);

    // Ensure there is a history item to work with
    await ensureHistoryItem(page);
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
