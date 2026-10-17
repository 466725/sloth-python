import { expect, test, type Page, type TestInfo } from '@playwright/test';

async function captureSmokeScreenshot(page: Page, testInfo: TestInfo, name: string, options: { fullPage?: boolean } = {}) {
  const path = testInfo.outputPath(`${name}.png`);
  await page.screenshot({
    path,
    fullPage: options.fullPage ?? true,
  });
  await testInfo.attach(name, {
    path,
    contentType: 'image/png',
  });
}

async function openApp(page: Page) {
  await page.addInitScript(() => {
    if (window.localStorage.getItem('dsa.uiLanguage') === null) {
      window.localStorage.setItem('dsa.uiLanguage', 'zh');
    }
  });
  await page.goto('/');
  await expect(page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL')).toBeVisible({ timeout: 20_000 });
}

test.describe('web smoke', () => {
  test.use({ locale: 'zh-CN' });


  test('home page shows analysis entry and history panel', async ({ page }, testInfo) => {
    await openApp(page);

    const stockInput = page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL');
    await expect(stockInput).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole('link', { name: '首页' })).toBeVisible();
    await expect(page.getByRole('link', { name: '问股' })).toBeVisible();
    await expect(page.getByText('个股栏')).toBeVisible();

    await stockInput.fill('600519');
    const analyzeButton = page.getByRole('button', { name: '分析', exact: true });
    await expect(analyzeButton).toBeVisible();

    await captureSmokeScreenshot(page, testInfo, 'smoke-home-page-zh', { fullPage: true });
  });

  test('chat page allows entering a question and starts a request', async ({ page }) => {
    await openApp(page);

    // Navigate to chat page by clicking the link
    await page.getByRole('link', { name: '问股' }).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    await expect(page.getByTestId('chat-workspace')).toBeVisible({ timeout: 10_000 });
    await expect(page.getByTestId('chat-session-list-scroll')).toBeVisible();
    await expect(page.getByTestId('chat-message-scroll')).toBeVisible();

    const input = page.getByPlaceholder(/分析 600519/);
    await expect(input).toBeVisible({ timeout: 5000 });

    const prompt = '请简要分析 600519';
    await input.fill(prompt);
    await page.getByRole('button', { name: '发送' }).click();

    await expect(page.locator('p').filter({ hasText: prompt }).last()).toBeVisible({ timeout: 5000 });
  });

  test('chat page uses accessible labels instead of native title attributes for key actions', async ({ page }) => {
    await openApp(page);

    await page.getByRole('link', { name: '问股' }).click();
    await page.waitForLoadState('domcontentloaded');

    const sendButton = page.getByRole('button', { name: '发送' });
    const composer = page.getByPlaceholder(/分析 600519/);

    await expect(page.getByTestId('chat-workspace')).toBeVisible({ timeout: 10_000 });
    await expect(sendButton).toBeVisible({ timeout: 10_000 });
    await expect(composer).toBeVisible({ timeout: 10_000 });

    await expect(sendButton).not.toHaveAttribute('title', /.+/);
    await expect(composer).not.toHaveAttribute('title', /.+/);
  });

  test('mobile shell opens navigation drawer', async ({ page }, testInfo) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openApp(page);

    // Try to open navigation menu
    const menuButton = page.getByRole('button', { name: /打开导航|菜单/i });
    if (await menuButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await menuButton.click();
    }

    // Check if navigation is visible
    await expect(page.getByRole('link', { name: '回测' })).toBeVisible({ timeout: 5000 });

    await captureSmokeScreenshot(page, testInfo, 'smoke-mobile-shell-nav');
  });

  test('settings page renders title and save actions', async ({ page }, testInfo) => {
    await openApp(page);

    // Navigate to settings page by clicking the link
    await page.getByRole('link', { name: '设置' }).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    // Use heading role for more precise selection
    await expect(page.getByRole('heading', { name: '系统设置' })).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole('button', { name: '重置' })).toBeVisible();
    await expect(page.getByRole('button', { name: /保存配置/ })).toBeVisible();

    await captureSmokeScreenshot(page, testInfo, 'smoke-settings-page-zh');
  });

  test('language switch updates UI copy and persists after page refresh', async ({ page }, testInfo) => {
    await openApp(page);

    const languageToggle = page.getByRole('button', { name: '切换界面语言' });
    await expect(languageToggle).toBeVisible();
    await expect(page.getByRole('link', { name: '设置' })).toBeVisible();
    await expect(page.getByRole('link', { name: '首页' })).toBeVisible();

    await languageToggle.click();

    const englishLanguageToggle = page.getByRole('button', { name: 'Switch UI language' });
    await expect(englishLanguageToggle).toBeVisible();
    await expect(page.getByRole('link', { name: 'Settings' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
    await captureSmokeScreenshot(page, testInfo, 'smoke-home-page-en');

    expect(await page.evaluate(() => localStorage.getItem('dsa.uiLanguage'))).toBe('en');

    await page.reload();
    await page.waitForLoadState('domcontentloaded');

    await expect(englishLanguageToggle).toBeVisible();
    await expect(page.getByRole('link', { name: 'Settings' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();

    await page.getByRole('link', { name: 'Settings' }).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    await expect(page.getByRole('heading', { name: 'System settings' })).toBeVisible({ timeout: 10_000 });

    // Navigate to the Notifications category to find the Send test button
    const notificationsTab = page.getByRole('button', { name: /^Notifications\b/ });
    await expect(notificationsTab).toBeVisible({ timeout: 10_000 });
    await notificationsTab.click();
    await expect(page.getByRole('button', { name: 'Send test' })).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole('textbox', { name: 'Title' })).toHaveValue('DSA notification test');

    await captureSmokeScreenshot(page, testInfo, 'smoke-settings-page-en');
  });

  test('backtest page renders filter controls', async ({ page }) => {
    await openApp(page);

    // Navigate to backtest page by clicking the link
    await page.getByRole('link', { name: '回测' }).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    // Check for filter controls
    const filterInput = page.getByPlaceholder('按股票代码筛选（留空表示全部）');
    await expect(filterInput).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole('button', { name: '筛选' })).toBeVisible();
    await expect(page.getByRole('button', { name: '运行回测' })).toBeVisible();
  });
});
